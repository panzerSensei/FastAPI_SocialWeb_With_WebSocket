from datetime import datetime
from typing import List
from typing import Optional


# класс-форма для валидации сообщения пока только по длине
class MessageCreateForm:
    def __init__(self,  message: str):
        self.errors: List = []
        self.message: str = message

    async def is_valid(self):
        if len(self.message) > 500:
            self.errors.append('Превышена длина сообщения, максимальная длина одного сообщения - 500 символов')

        if not self.errors:
            return True

        return False