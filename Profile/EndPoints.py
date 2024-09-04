from datetime import datetime

from fastapi import APIRouter
from typing import Optional

from Profile.ProfileForm import ProfileCreateForm
from Profile.Profile_CRUD import profile_create, check_user_has_profile, delete_profile, get_profile


profile_router = APIRouter(
    prefix='/profile',
    tags=['profile']
)


@profile_router.post('/MakeProfile/')
async def new_profile(userid: int, profile_name: str, profile_img: Optional[str] = None, profile_info: Optional[str] = None, profile_hobbies: Optional[str] = None,
                         profile_interest: Optional[str] = None, birthdate: Optional[datetime] = None):
    """
    API для создания профиля на сайте,
    проверяет нет профиля уже,
    проверяет корректность введенных данных,
    если все в порядке, то профиль попадает в БД
    """
    validation_errors = []
    app_error = []
    errors_name = []
    errors_info = []
    errors_hobbies = []
    errors_interest = []
    errors_birthdate = []

    if await check_user_has_profile(userid):
        return {
            "status": 400,
            "validation_errors": "У вас уже создан профиль"
        }

    form = ProfileCreateForm(profile_name, profile_info, profile_hobbies, profile_interest, birthdate)

    if await form.is_valid():
        try:
            await profile_create(userid, profile_name, profile_img, profile_info, profile_hobbies,
                         profile_interest, birthdate)
            status = 200
            validation_errors = []
            app_error = []
        except Exception as e:
            status = 500
            app_error = type(e).__name__
    else:
        status = 400
        validation_errors = form.errors
        errors_name = form.errors_with_profile_name
        errors_info = form.errors_with_profile_info
        errors_hobbies = form.errors_with_profile_hobbies
        errors_interest = form.errors_with_profile_interest
        errors_birthdate = form.errors_with_birthdate

    return {
        "status": status,
        "errors": validation_errors,
        "errors_name": errors_name,
        "errors_info": errors_info,
        "errors_hobbies": errors_hobbies,
        "errors_interest": errors_interest,
        "errors_birthdate": errors_birthdate
    }


@profile_router.get("/ShowProfile")
async def get_profile_data(userid: int):
    """
    Выводит данные профиля по id пользователя
    """
    if await check_user_has_profile(userid):
        status = 200
        profile_data = await get_profile(userid)
    else:
        status = 400
        profile_data = ["У данного пользователя нет профиля"]

    return {
        "status": status,
        "profile_data": profile_data
    }


@profile_router.delete("/DeleteProfile")
async def delete_profile_in_table(userid: int):
    """
    Удалить профиль по id пользователя, в последствии API будет переписана так
    чтобы это мог сделать только сам пользователь, если авторизован,
    либо модерация
    """
    if await check_user_has_profile(userid):
        await delete_profile(userid)
        status = 200
        message = "Пользователь успешно удален"
    else:
        status = 400
        message = "Пользователя нет в таблице"

    return {
        "status": status,
        "message": message
    }