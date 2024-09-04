from datetime import datetime
from typing import List
from typing import Optional


# класс-форма для валидации данных при регистрации: допустимое имя пользователя, пароль и почта.
# собирает ошибки ввода от пользователя
class ProfileCreateForm:
    def __init__(self,  profile_name, profile_info: Optional[str] = None, profile_hobbies: Optional[str] = None,
                 profile_interest: Optional[str] = None, birthdate: Optional[str] = None):
        self.errors_with_profile_name: List = []
        self.errors_with_profile_info: List = []
        self.errors_with_profile_hobbies: List = []
        self.errors_with_profile_interest: List = []
        self.errors_with_birthdate: List = []
        self.errors = []
        self.profile_name: Optional[str] = profile_name
        self.profile_info: Optional[str] = profile_info
        self.profile_hobbies: Optional[str] = profile_hobbies
        self.profile_interest: Optional[str] = profile_interest
        self.birthdate: Optional[datetime] = birthdate

    async def profile_name_is_valid(self):
        # Запрещено использовать амперсанд (&), знаки равенства (=) и сложения (+), скобки (<>), запятую (,), символ подчеркивания (_), апостроф ('), дефис (-) и несколько точек подряд.
        forbidden_symbols = ('&', '=', '-', '+', '<', '>', ',', '_', '\'', '.')

        if not self.profile_name or not len(self.profile_name) >= 4:
            self.errors_with_profile_name.append("Имя профиля должно содержать хотя бы 4 символов")

        if not len(self.profile_name) < 31:
            self.errors_with_profile_name.append("Имя профиля должно быть меньше 30 символов")

        if any(char in self.profile_name for char in forbidden_symbols):
            self.errors_with_profile_name.append("Запрещено использовать в имени профиля амперсанд (&), знаки равенства (=) и сложения (+), скобки (<>), запятую (,), символ подчеркивания (_), апостроф ('), дефис (-) и несколько точек (.).")

        if not self.errors_with_profile_name:
            return True

        return False

    async def profile_info_is_valid(self):
        if self.profile_info and not len(self.profile_info) < 1001:
            self.errors_with_profile_info.append("Максимальная длина информации о себе - 1000 символов, сократите объем описания")

        if not self.errors_with_profile_info:
            return True

        return False

    async def profile_hobbies_is_valid(self):
        if self.profile_hobbies and not len(self.profile_hobbies) < 1001:
            self.errors_with_profile_hobbies.append(
                "Максимальная длина информации о увлечениях/хобби - 1000 символов, сократите объем описания")

        if not self.errors_with_profile_hobbies:
            return True

        return False

    async def profile_interest_is_valid(self):
        if self.profile_interest and not len(self.profile_interest) < 1001:
            self.errors_with_profile_interest.append(
                "Максимальная длина информации об интересах - 1000 символов, сократите объем описания")

        if not self.errors_with_profile_interest:
            return True

        return False

    async def birthdate_is_valid(self):
        if not self.birthdate is None:
            birth_date = self.birthdate
            now_date = datetime.now()
            old = now_date - birth_date
            if old.days > 54750:
                self.errors_with_birthdate.append(
                    "Вы не верно указали дату рождения, вам вряд ли более 150 лет")

        if not self.errors_with_birthdate:
            return True

        return False

    async def is_valid(self):
        if not await self.profile_name_is_valid():
            self.errors.append('Ошибка в имени профиля')

        if not await self.profile_info_is_valid():
            self.errors.append('Ошибка в инфо')

        if not await self.profile_hobbies_is_valid():
            self.errors.append('Ошибка в увлечениях')

        if not await self.profile_interest_is_valid():
            self.errors.append('Ошибка в интересах')

        if not await self.birthdate_is_valid():
            self.errors.append('Ошибка в дате рождения')

        if not self.errors:
            return True

        return False