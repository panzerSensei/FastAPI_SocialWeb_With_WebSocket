from datetime import datetime

from asyncpg.pgproto.pgproto import timedelta
from fastapi import APIRouter
from sqlalchemy import select
from typing import Optional

from Chat.ChatForm import ChatCreateForm
from Chat.Сhat_CRUD import chat_create, check_chat, delete_chat


chat_router = APIRouter(
    prefix='/chat',
    tags=['chat']
)


@chat_router.post('/MakeChat/')
async def new_chat(profile_from: int, profile_to: int, chat_name: Optional[str] = None):
    """
    API для создания сообщения в чате
    """
    validation_errors = []
    app_error = []
    errors_name = []

    if await check_chat(profile_from,  profile_to):
        return {
            "status": 400,
            "validation_errors": "У между профилями уже есть чат"
        }

    form = ChatCreateForm(chat_name)

    if await form.is_valid():
        try:
            await chat_create(profile_from, profile_to, chat_name)
            status = 200
            validation_errors = []
            app_error = []
        except Exception as e:
            status = 500
            app_error = type(e).__name__
    else:
        status = 400
        validation_errors = form.errors
        errors_name = form.errors_with_chat_name

    return {
        "status": status,
        "app_errors": app_error,
        "errors": validation_errors,
        "errors_name": errors_name
    }


@chat_router.get("/ShowChat")
async def get_chat(profile_from: int, profile_to: int):
    """
    API для вывода чата между пользователями
    """
    chat_id = await check_chat(profile_from, profile_to)
    if chat_id:
        status = 200
        id = chat_id
    else:
        status = 400
        id = ["Между профилями нет чата"]

    return {
        "status": status,
        "chat": id
    }


@chat_router.delete("/DeleteChat")
async def delete_chat(profile_from: int, profile_to: int):
    """
    API для удаления чата между пользователями, в последствии API будет переписана так
    чтобы это мог сделать только сам пользователь, если авторизован,
    либо модерация
    """
    if await check_chat(profile_from, profile_to):
        await delete_chat(profile_from, profile_to)
        status = 200
        message = "Чат успешно успешно удален"
    else:
        status = 400
        message = "Чата нет в таблице"

    return {
        "status": status,
        "message": message
    }