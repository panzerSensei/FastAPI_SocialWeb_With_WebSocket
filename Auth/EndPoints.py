from asyncpg.pgproto.pgproto import timedelta
from fastapi import APIRouter
from sqlalchemy import select

from BD_Models import UserModel
from BD_Config import async_session
from Auth.RegistrationForm import UserCreateForm
from Auth.User_CRUD import user_create, user_login, create_token, check_token, check_refresh_token, update_tokens
from Auth.User_CRUD import exist_token, check_user_is_auth, delete_tokens, check_user, check_email, delete_user, check_user_by_id


auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@auth_router.post('/Registration/')
async def register(username: str, password: str, email: str):
    """
    API для регистрации на сайте,
    проверяет ошибки в логине, пароле и e-mail,
    не используются ли логин и email уже каким-то пользователем,
    если все в порядке, то пользователь попадает в БД, пароль шифруется
    """
    validation_errors = []
    app_error = []
    username_errors = []
    password_errors = []
    email_errors = []

    if await check_user(username):
        return {
            "status": 400,
            "validation_errors": "Имя пользователя уже используется"
        }

    if await check_email(email):
        return {
            "status": 400,
            "validation_errors": "E-mail уже используется"
        }

    form = UserCreateForm(username, password, email)

    if await form.is_valid():
        try:
            await user_create(username, password, email)
            status = 200
            validation_errors = []
            app_error = []
        except Exception as e:
            status = 500
            app_error = type(e).__name__
    else:
        status = 400
        validation_errors = form.errors
        username_errors = form.errors_with_username
        password_errors = form.errors_with_password
        email_errors = form.errors_with_email

    return {
        "status": status,
        "errors": validation_errors,
        "username_errors": username_errors,
        "password_errors": password_errors,
        "email_errors": email_errors,
        "app_error": app_error
    }


@auth_router.post('/LogIn/')
async def login_for_access_token(username: str, password: str):
    """
    API для входа на сайт, при вводе правильного логина и пароля, выдает пару JWT токенов
    """
    user = await user_login(username, password)
    userid = user[1]
    username = user[2]
    if user:
        status = 200
        if not await exist_token(userid):
            tokens = await create_token(userid, username, timedelta(minutes=20))
        else:
            tokens = await update_tokens(userid, timedelta(minutes=20))
    else:
        status = 400
        tokens = ['', '']
    return {
        "status": status,
        "access token": tokens[0],
        "refresh token": tokens[1]
    }


@auth_router.post('/LogOut/')
async def login_out(userid: int):
    """
    API для выхода из системы аутентификации (удаляет связанные токены из БД)
    """
    if await check_user_is_auth(userid):
        await delete_tokens(userid)
        status = 200
        message = "Вы вышли из системы"
    else:
        status = 400
        message = "Данный пользователь либо отсутствует, либо уже вышел"

    return {
        "status": status,
        "message": message
    }


@auth_router.post('/CheckToken/')
async def login_for_access_token(userid: int, access_token: str):
    """
    API для проверки доступа через access токен, либо дает доступ, либо сообщает, что токен устарел/недействителен
    """
    res = await check_token(userid, access_token)
    if res == 2:
        status = 200
        message = 'Access granted'
    elif res == 1:
        status = 403
        message = 'Access denied, token is outdated'
    else:
        status = 403
        message = 'Access denied, token is wrong'

    return {
        "status": status,
        "message": message
    }


@auth_router.post('/NewTokens/')
async def login_for_access_token(userid: int, refresh_token: str):
    """
    API для генерации новых токенов с помощью refresh токена,
    либо выдает новую пару токенов, либо сообщает, что токен недействиелен
    """
    new_tokens = []
    if await check_refresh_token(userid, refresh_token):
        new_tokens = await update_tokens(userid, timedelta(minutes=20))
        status = 200
        message = 'Access granted, new tokens is generated'
    else:
        status = 403
        message = 'Access denied, token is wrong'

    return {
        "status": status,
        "message": message,
        "new tokens": new_tokens
    }


@auth_router.delete("/deluser")
async def delete_user_in_table(userid: int):
    """
    Удалить пользователя по id, в последствии API будет переписана так
    чтобы это мог сделать только сам пользователь, если авторизован,
    либо модерация
    """
    if await check_user_by_id(userid):
        await delete_user(userid)
        status = 200
        message = "Пользователь успешно удален"
    else:
        status = 400
        message = "Пользователя нет в таблице"

    return {
        "status": status,
        "message": message
    }


@auth_router.get("/users")
async def get_users():
    """
    Выдать первых 20 пользователей в БДшке
    """
    async with async_session() as session:
        query = select(UserModel.username).limit(20)
        res = await session.execute(query)
        query_result = res.scalars().all()
        result = []

        for i, element in enumerate(query_result, start=1):
            # Можно добавлять элементы как словари
            result.append({f"username_{i}": element})

    return {
        "Users": result
    }