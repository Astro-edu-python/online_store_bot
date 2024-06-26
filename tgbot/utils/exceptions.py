
class BotException(Exception):
    def __init__(self, message: str, *args):
        super().__init__(*args)
        self.message = message

    def __str__(self):
        return self.message
