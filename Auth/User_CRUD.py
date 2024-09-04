import os

from dotenv import load_dotenv
from passlib.handlers.bcrypt import bcrypt
from sqlalchemy.util import deprecated
from sqlalchemy import select, update, delete
from sqlalchemy.orm import query

from BD_Config import async_session
from BD_Models import UserModel, TokenModel
from datetime import timedelta, datetime
from pydantic_settings import SettingsConfigDict, BaseSettings
from starlette import status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError


class CryptSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    REFRESH: str

    load_dotenv("_.env")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    ALGORITHM = os.environ.get("ALGORITHM")
    REFRESH = os.environ.get("REFRESH")


crypt_settings = CryptSettings()
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


## Регистрация пользователя в системе, пароли зашифрованы
async def user_create(username: str, password: str, email: str):
    async with async_session() as session:
        new_user = UserModel(
            username = username,
            password = bcrypt_context.hash(password),
            email = email
        )

        session.add(new_user)
        await session.commit()


# Проверяет наличие данного пользователя в БДшке пользователей по нику
async def check_user(username: str):
    async with async_session() as session:
        query = select(UserModel.username).filter(UserModel.username == username)
        res = await session.execute(query)
        user = res.all()
        if user:
            return True
        else:
            return False


# Проверяет наличие данного пользователя в БДшке пользователей по нику
async def check_user_by_id(userid: int):
    async with async_session() as session:
        query = select(UserModel.id).filter(UserModel.id == userid)
        res = await session.execute(query)
        user = res.all()
        if user:
            return True
        else:
            return False


# Проверяет наличие данного пользователя в БДшке пользователей по нику
async def check_email(email: str):
    async with async_session() as session:
        query = select(UserModel.email).filter(UserModel.email == email)
        res = await session.execute(query)
        email = res.all()
        if email:
            return True
        else:
            return False


# Проверяет наличие данного пользователя в БДшке токенов
async def check_user_is_auth(userid: int):
    async with async_session() as session:
        query = select(TokenModel.user).filter(TokenModel.user == userid)
        res = await session.execute(query)
        user = res.all()
        if user:
            return True
        else:
            return False


# Проверка совпадения логина и пораля в БД с введенными пользовтелем
async def user_login(username: str, password: str):
    async with async_session() as session:
        query = select(UserModel.password, UserModel.id, UserModel.username).filter(UserModel.username == username)
        res = await session.execute(query)
        user = res.one()
        if not user:
            return False
        if not bcrypt_context.verify(password, user[0]):
            return False
        return user


# проверка, что для данного пользователя токен уже есть в БД
async def exist_token(userid: int):
    async with async_session() as session:
        query = select(TokenModel.user).filter(TokenModel.user == userid)
        res = await session.execute(query)
        user = res.all()

        if user:
            return True
        else:
            return False


# Создание пары JWT токенов
async def create_token(userid: int, username: str, expires: timedelta):
    async with async_session() as session:
        encode = {'sub': username, 'id': userid}
        expires = datetime.now() + expires
        encode.update({'exp': expires})
        access_token = jwt.encode(encode, crypt_settings.SECRET_KEY, algorithm=crypt_settings.ALGORITHM)
        encode.update({'sub': crypt_settings.REFRESH})
        refresh_token = jwt.encode(encode, crypt_settings.SECRET_KEY, algorithm=crypt_settings.ALGORITHM)
        tokens = (access_token, refresh_token)

        new_token = TokenModel(
            user = userid,
            access_token = access_token,
            refresh_token = refresh_token,
            expire_time = expires,
            token_type = 'jwt'
        )

        session.add(new_token)
        await session.commit()
        return tokens


# проверка access токена
async def check_token(userid: int, access_token: str):
    async with async_session() as session:
        query = select(TokenModel.access_token, TokenModel.expire_time).filter(TokenModel.user == userid)
        res = await session.execute(query)
        access = res.one()

        if access[0] == access_token:
            if datetime.now() < access[1]:
                res = 2
                return res
            else:
                res = 1
                return res
        else:
            return False


# проверяет введенный refresh токен, если совпадает, то возвращает его
async def check_refresh_token(userid: int, refresh_token: str):
    async with async_session() as session:
        query = select(TokenModel.user, TokenModel.refresh_token).filter(TokenModel.user == userid)
        res = await session.execute(query)
        token = res.one()

        if token[1] == refresh_token:
            return token
        else:
            return False


# обновляет токены для пользователя, если он уже генерировал их когда-то
async def update_tokens(userid: int, expires: timedelta):
    async with async_session() as session:
        encode = {'sub': 'NeedNewToken', 'id': userid}
        expires = datetime.now() + expires
        encode.update({'exp': expires})
        access_token = jwt.encode(encode, crypt_settings.SECRET_KEY, algorithm=crypt_settings.ALGORITHM)
        encode.update({'sub': crypt_settings.REFRESH})
        refresh_token = jwt.encode(encode, crypt_settings.SECRET_KEY, algorithm=crypt_settings.ALGORITHM)
        tokens = (access_token, refresh_token)

        query = update(TokenModel).where(TokenModel.user == userid).values(
            {"access_token": access_token,
             "refresh_token": refresh_token,
             "expire_time": expires
             }
        )

        await session.execute(query)
        await session.commit()

        return tokens


# Удаляет токены из БД по id пользователя
async def delete_tokens(userid: int):
    async with async_session() as session:
        query = delete(TokenModel).where(TokenModel.user == userid)

        await session.execute(query)
        await session.commit()


# удаляет пользователя из таблицы пользователей
async def delete_user(userid: int):
    async with async_session() as session:
        query = delete(UserModel).where(UserModel.id == userid)

        await session.execute(query)
        await session.commit()