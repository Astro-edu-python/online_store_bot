from __future__ import annotations

import json
from dataclasses import dataclass, asdict

from redis.asyncio import Redis


@dataclass
class BaseRedisDbType:

    def db_key_prefix(self):
        raise NotImplementedError

    async def load(self, redis: Redis, key: str):
        raise NotImplementedError

    async def insert_to_db(self, redis: Redis):
        raise NotImplementedError


@dataclass
class UserBasket:
    products_ids: list[int]

    def add_product(self, product_id: int):
        if product_id not in self.products_ids:
            self.products_ids.append(product_id)

    def remove_product(self, product_id: int):
        if product_id in self.products_ids:
            self.products_ids.remove(product_id)


@dataclass
class UserProfile(BaseRedisDbType):
    user_id: int
    basket: UserBasket | dict | None = None

    def __post_init__(self):
        if not self.basket:
            self.basket = UserBasket([])
        elif isinstance(self.basket, dict):
            self.basket = UserBasket(**self.basket)

    @classmethod
    def db_key_prefix(cls) -> str:
        return f'user_'

    @property
    def db_key(self) -> str:
        return f'{self.db_key_prefix()}{self.user_id}'

    def dump(self) -> str:
        return json.dumps(asdict(self))

    @classmethod
    async def load(cls, redis: Redis, key: str) -> UserProfile | None:
        result: bytes | None = await redis.get(f'{cls.db_key_prefix()}{key}')
        if result is not None:
            result: dict = json.loads(result)
            return cls(**result)

    async def insert_to_db(self, redis: Redis) -> "UserProfile":
        await redis.set(self.db_key, self.dump())
        return self
