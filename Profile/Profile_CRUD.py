from typing import Optional

from sqlalchemy import select, delete

from BD_Config import async_session
from BD_Models import ProfileModel
from datetime import datetime


## Создание профиля пользователя в системе
async def profile_create(userid: int, profile_name: str, profile_img: Optional[str] = None,
                         profile_info: Optional[str] = None, profile_hobbies: Optional[str] = None,
                         profile_interest: Optional[str] = None, birthdate: Optional[datetime] = datetime.now()):
    async with async_session() as session:
        new_profile = ProfileModel(
            user = userid,
            profile_name = profile_name,
            profile_img = profile_img,
            profile_info = profile_info,
            profile_hobbies = profile_hobbies,
            profile_interest = profile_interest,
            birthdate = birthdate,
            registration_date = datetime.now()
        )

        session.add(new_profile)
        await session.commit()


# Проверяет есть у данного пользователя профиль в БД профилей
async def check_user_has_profile(userid: int):
    async with async_session() as session:
        query = select(ProfileModel.user).filter(ProfileModel.user == userid)
        res = await session.execute(query)
        profile = res.all()
        if profile:
            return True
        else:
            return False


# Проверяет наличие данного пользователя в БДшке пользователей по нику
async def get_profile(userid: int):
    async with async_session() as session:
        query = select(ProfileModel).filter(ProfileModel.user == userid)
        res = await session.execute(query)
        profile = res.scalars().all()
        if profile:
            return profile
        else:
            return False


# удаляет профиль из таблицы пользователей
async def delete_profile(userid: int):
    async with async_session() as session:
        query = delete(ProfileModel).where(ProfileModel.user == userid)

        await session.execute(query)
        await session.commit()