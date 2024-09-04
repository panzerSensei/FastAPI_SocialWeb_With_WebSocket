from datetime import datetime
from typing import List
from typing import Optional


# класс-форма для валидации данных при регистрации: допустимое имя пользователя, пароль и почта.
# собирает ошибки ввода от пользователя
class ChatCreateForm:
    def __init__(self,  chat_name: Optional[str] = None):
        self.errors_with_chat_name: List = []
        self.errors: List = []
        self.chat_name: Optional[str] = chat_name

    async def chat_name_is_valid(self):
        # Запрещено использовать амперсанд (&), знаки равенства (=) и сложения (+), скобки (<>), запятую (,), символ подчеркивания (_), апостроф ('), дефис (-) и несколько точек подряд.
        forbidden_symbols = ('&', '=', '-', '+', '<', '>', ',', '_', '\'', '.')

        if not self.chat_name is None and not len(self.chat_name) >= 4:
            self.errors_with_chat_name.append("Название чата должно быть хотя бы из 4 символа")

        if not self.chat_name is None and not len(self.chat_name) < 31:
            self.errors_with_chat_name.append("Название чата должно быть не более 30 символов")

        if not self.chat_name is None and any(char in self.chat_name for char in forbidden_symbols):
            self.errors_with_chat_name.append("Запрещено использовать в названии чата амперсанд (&), знаки равенства (=) и сложения (+), скобки (<>), запятую (,), символ подчеркивания (_), апостроф ('), дефис (-) и несколько точек (.).")

        if not self.errors_with_chat_name:
            return True

        return False

    async def is_valid(self):
        if not await self.chat_name_is_valid():
            self.errors.append('Ошибки в названии чата')

        if not self.errors:
            return True

        return False