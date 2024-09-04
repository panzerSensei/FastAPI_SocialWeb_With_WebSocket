from typing import Optional

from sqlalchemy import select, delete

from BD_Config import async_session
from BD_Models import ChatModel
from datetime import datetime


## Создание чата между 2 профилями в системе
async def chat_create(profile_from: int, profile_to: int, chat_name: Optional[str] = None):
    async with async_session() as session:
        new_profile = ChatModel(
            chat_name = chat_name,
            profile_from = profile_from,
            profile_to = profile_to,
        )

        session.add(new_profile)
        await session.commit()


# Проверяет есть чат между 2 пользователями и возвращает его id
async def check_chat(profile_from: int, profile_to: int):
    async with async_session() as session:
        query = select(ChatModel.id).filter(
            ChatModel.profile_from == profile_from and ChatModel.profile_to == profile_to
        )
        res = await session.execute(query)
        chat = res.scalars().all()
        if chat:
            return chat
        else:
            return False


# удаляет чат между пользователями из таблицы чатов
async def delete_chat(profile_from: int, profile_to: int):
    async with async_session() as session:
        query = delete(ChatModel).where(
            ChatModel.profile_from == profile_from and ChatModel.profile_to == profile_to
            or
            ChatModel.profile_from == profile_to and ChatModel.profile_to == profile_from
        )

        await session.execute(query)
        await session.commit()