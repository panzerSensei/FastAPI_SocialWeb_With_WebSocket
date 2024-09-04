import os

from dotenv import load_dotenv
from pydantic_settings import SettingsConfigDict, BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy.ext.asyncio import AsyncSession


## Две функции, которые возращает строки адресса БД для синхронной и асинхронной работы,
# адрес задан в неявном виде через файл .env, таким будем отправлять в репозиторий без угроз для моей БД от "шутников"

class Settings(BaseSettings):
    DB_HOST: str
    DB_NAME: str
    DB_SUPER_USER: str
    DB_SUPER_USER_PASSWORD: str
    DB_PORT: int


    # достаем из .env данные для подключения к нашей БД
    load_dotenv()
    DB_HOST = os.environ.get("DB_HOST")
    DB_NAME = os.environ.get("DB_NAME")
    DB_SUPER_USER = os.environ.get("DB_SUPER_USER")
    DB_SUPER_USER_PASSWORD = os.environ.get("DB_SUPER_USER_PASSWORD")
    DB_PORT = os.environ.get("DB_PORT")

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_SUPER_USER}:{self.DB_SUPER_USER_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_pg8000(self):
        return f"postgresql+pg8000://{self.DB_SUPER_USER}:{self.DB_SUPER_USER_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file ='.env') ### ВАЖНО!!!! БЛЯТЬ В ЭТОМ ФАЙЛЕ НЕ ДОЛЖНО
                                                                # НИ ОДНОЙ ЛИШНЕЙ ПЕРЕМЕННОЙ, ИНАЧЕ ПИЗДА!!!

settings = Settings()

async_engine = create_async_engine(
    url = settings.DATABASE_URL_asyncpg,
    echo = True
)

sync_engine = create_engine(
    url = settings.DATABASE_URL_pg8000,
    echo = True
)

# async_session = AsyncSession(async_engine,  expire_on_commit=False)

async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

sync_session = sessionmaker(sync_engine)


# async_session_factory = sessionmaker(async_engine, class_=AsyncSession)
# AsyncScopedSession = async_scoped_session(async_session_factory, scopefunc=current_task)
#
# async_session = AsyncScopedSession()