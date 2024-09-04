from typing import List
from typing import Optional


# класс-форма для валидации данных при регистрации: допустимое имя пользователя, пароль и почта.
# собирает ошибки ввода от пользователя
class UserCreateForm:
    def __init__(self,  username, password, email):
        self.errors_with_username: List = []
        self.errors_with_password: List = []
        self.errors_with_email: List = []
        self.errors = []
        self.username: Optional[str] = username
        self.password: Optional[str] = password
        self.email: Optional[str] = email

    async def username_is_valid(self):
        # Запрещено использовать амперсанд (&), знаки равенства (=) и сложения (+), скобки (<>), запятую (,), символ подчеркивания (_), апостроф ('), дефис (-) и несколько точек подряд.
        forbidden_symbols = ('&', '=', '-', '+', '<', '>', ',', '_', '\'', '.')

        if not self.username or not len(self.username) >= 4:
            self.errors_with_username.append("Имя пользователя должно содержать хотя бы 4 символов")

        if not len(self.username) < 31:
            self.errors_with_username.append("Имя пользователя должно быть меньше 30 символов")

        if any(char in self.username for char in forbidden_symbols):
            self.errors_with_username.append("Запрещено использовать амперсанд (&), знаки равенства (=) и сложения (+), скобки (<>), запятую (,), символ подчеркивания (_), апостроф ('), дефис (-) и несколько точек (.).")

        if not self.errors_with_username:
            return True

        return False

    async def password_is_valid(self):
        if not self.password or not len(self.password) >= 8:
            self.errors_with_password.append("Минимальная длина пароля - 8 символов")

        if not len(self.password) < 31:
            self.errors_with_password.append("Максимальная длина пароля - 30 символов")

        if not self.password or self.password.isnumeric() or self.password.islower() or self.password.isupper():
            self.errors_with_password.append("Пароль должен содержать цифры, строчные и заглавные буквы")

        if not self.errors_with_password:
            return True

        return False

    async def email_is_valid(self):
        if not self.email or not '@' in self.email:
            self.errors_with_email.append("Адрес почты введен неверно")

        if not self.email or not len(self.email) < 100:
            self.errors_with_email.append("Максимальная длина почты - 100 символов")

        if not self.errors_with_email:
            return True

        return False

    async def is_valid(self):
        if not await self.username_is_valid():
            self.errors.append('Ошибка в имени пользователя')

        if not await self.password_is_valid():
            self.errors.append('Ошибка в пароле')

        if not await self.email_is_valid():
            self.errors.append('Ошибка в почте')

        if not self.errors:
            return True

        return False