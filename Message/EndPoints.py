from datetime import datetime

from asyncpg.pgproto.pgproto import timedelta
from fastapi import APIRouter
from sqlalchemy import select
from typing import Optional

from Message.MessageForm import MessageCreateForm
from Message.Message_CRUD import message_create, get_messages_in_chat, check_messages, edit_message_in_chat, delete_message


message_router = APIRouter(
    prefix='/message',
    tags=['message']
)


@message_router.post('/MakeMessage/')
async def new_message(chat_id: int, message_from: int, message_text: Optional[str] = None,
                         message_media_img: Optional[str] = None, message_media_sound: Optional[str] = None,
                         message_media_video: Optional[str] = None):
    """
    API для создания сообщения в чате
    """
    if message_text is None and message_media_img is None and message_media_sound is None and message_media_video is None:
        return {
            "status": 400,
            "message": "В сообщении вообще ничего нет, введите хоть что-то (текст, картинку, аудио или видео)"
        }

    validation_errors = []
    app_error = []

    form = MessageCreateForm(message_text)

    if await form.is_valid():
        try:
            await message_create(chat_id, message_from, message_text, message_media_img,
                                 message_media_sound, message_media_video)
            status = 200
            validation_errors = []
            app_error = []
        except Exception as e:
            status = 500
            app_error = type(e).__name__
    else:
        status = 400
        validation_errors = form.errors

    return {
        "status": status,
        "app_errors": app_error,
        "errors": validation_errors
    }


@message_router.get("/ShowMessageInChat")
async def get_messages(chat_id: int):
    """
    API для вывода чата между пользователями
    """
    result = []
    messages = await get_messages_in_chat(chat_id)
    if messages:
        status = 200

        for i, element in enumerate(messages, start=1):
            result.append({f"message_{i}": element})
    else:
        status = 400
        result = "Либо этот чат пуст, либо для этого id нет чата"
    return {
        "status": status,
        "messages": result
    }


@message_router.patch("/EditMessage")
async def alter_messages(message_id: int, message_text: Optional[str] = None,
                         message_media_img: Optional[str] = None, message_media_sound: Optional[str] = None,
                         message_media_video: Optional[str] = None):
    """
    API для редактирования контента сообщения по id
    """
    if message_text is None and message_media_img is None and message_media_sound is None and message_media_video is None:
        return {
            "status": 400,
            "message": "В сообщении вообще ничего нет, введите хоть что-то (текст, картинку, аудио или видео)"
        }

    if await check_messages(message_id):
        await edit_message_in_chat(message_id, message_text, message_media_img,
                                   message_media_sound, message_media_video)

        status = 200
        message = "Done"
    else:
        status = 400
        message = "Такого сообщения нет"

    return {
        "status": status,
        "message": message
    }


@message_router.delete("/DeleteMessage")
async def del_message(message_id: int):
    """
    API для удаления сообщения, в последствии API будет переписана так
    чтобы это мог сделать только сам пользователь, если авторизован,
    либо модерация
    """
    if await check_messages(message_id):
        await delete_message(message_id)
        status = 200
        message = "Сообщение успешно удалено"
    else:
        status = 400
        message = "Сообщения нет в таблице"

    return {
        "status": status,
        "message": message
    }