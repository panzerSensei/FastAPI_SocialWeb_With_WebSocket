from typing import Optional
from datetime import datetime

from sqlalchemy import select, delete, update, values

from BD_Config import async_session
from BD_Models import MessageModel


## Создать сообщение в чате по id чата
async def message_create(chat_id: int, message_from: int, message_text: Optional[str] = None,
                         message_media_img: Optional[str] = None, message_media_sound: Optional[str] = None,
                         message_media_video: Optional[str] = None):
    async with async_session() as session:
        new_message = MessageModel(
            chat_id = chat_id,
            message_from = message_from,
            message_text = message_text,
            message_media_img = message_media_img,
            message_media_sound = message_media_sound,
            message_media_video = message_media_video,
            message_date = datetime.now()
        )

        session.add(new_message)
        await session.commit()


# Возвращает сообщения из чата по id
async def get_messages_in_chat(chat_id: int):
    async with (async_session() as session):
        query = select(
            MessageModel.message_from, MessageModel.message_date, MessageModel.message_text
                       ).filter(MessageModel.chat_id == chat_id).order_by(MessageModel.message_date.desc())
        res = await session.execute(query)
        messages = res.mappings().all()
        if messages:
            return messages
        else:
            return False


# Проверяет наличие сообщения по id в БД сообщений
async def check_messages(messages_id: int):
    async with (async_session() as session):
        query = select(MessageModel.id).filter(MessageModel.id == messages_id)
        res = await session.execute(query)
        message = res.all()
        if message:
            return True
        else:
            return False


# Редактирует сообщение под id
async def edit_message_in_chat(message_id: int, message_text: Optional[str] = None,
                         message_media_img: Optional[str] = None, message_media_sound: Optional[str] = None,
                         message_media_video: Optional[str] = None):
    async with async_session() as session:
        query = update(MessageModel).filter(MessageModel.id == message_id).values(
            message_text=message_text,
            message_media_img=message_media_img,
            message_media_sound=message_media_sound,
            message_media_video=message_media_video
        )

        await session.execute(query)
        await session.commit()


# удаляет сообщение из БД
async def delete_message(message_id: int):
    async with async_session() as session:
        query = delete(MessageModel).where(MessageModel.id == message_id)

        await session.execute(query)
        await session.commit()