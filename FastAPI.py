from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import redis
import uvicorn

from Auth.EndPoints import auth_router
from Profile.EndPoints import profile_router
from Chat.EndPoints import chat_router
from Message.EndPoints import message_router
from Comment.EndPoints import comment_router

## объявляем редис и некоторые параметры его работы
r = redis.Redis(host='localhost', port=6379, decode_responses=True)


## при запуске приложения произойдет подключение к редис для Кэширования некоторых результатов запросов, например,
# которые будут часто запрашивать пользователи
@asynccontextmanager
async def lifespan(app: FastAPI):
    # redis = aioredis.from_url("redis://[::1]:6379/0", encoding="utf8", decode_respones=True)
    FastAPICache.init(RedisBackend(r), prefix="fastapi-cache")
    yield


app = FastAPI(
    title='JOGU\'s SocialWeb - мини соц сеть с месседжером',
    lifespan=lifespan
)

# объявляем путь хранения МЕДИА файлов
app.mount("/media", StaticFiles(directory='media'), name='media')

# Включаем роутеры наших приложений, чтобы приложение было очень легко масштабировать и не потеряться
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(chat_router)
app.include_router(message_router)
app.include_router(comment_router)


##--------------САМО ПРИЛОЖЕНИЕ BACKEND-------------------------------------------------------------------------------##


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7777)