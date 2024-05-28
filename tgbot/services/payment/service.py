from abc import abstractmethod
from dataclasses import dataclass
from typing import Iterable


@dataclass
class Currency:
    name: str
    code: str
    min_price: float
    max_price: float


@dataclass
class UzSumCurrency(Currency):
    min_price: int
    max_price: int


@dataclass
class PaymentService:
    amount: int | float
    user_id: int

    @property
    def payload(self) -> str:
        return f'{self.user_id}__{self.amount}'

    @classmethod
    def parse_payload(cls, payload: str) -> Iterable[int]:
        split = payload.split('__')
        if len(split) != 2:
            raise ValueError('Payload is invalid')
        return map(int, split)

    @abstractmethod
    def parse_amount(self) -> int:
        pass

    @abstractmethod
    def resolve_amount(self) -> int:
        pass


@dataclass
class UzPaymentService(PaymentService):
    amount: int

    def parse_amount(self) -> int:
        return int(str(self.amount) + '00')

    def resolve_amount(self) -> int:
        return self.amount // 100
