from typing import Optional
from datetime import datetime

from sqlalchemy import select, delete, update, values

from BD_Config import async_session
from BD_Models import CommentModel


## Создать комментарий на профиле profile_to от profile_from
async def comment_create(profile_from: int, profile_to: int, comment_text: Optional[str] = None,
                         comment_media_img: Optional[str] = None, comment_media_sound: Optional[str] = None,
                         comment_media_video: Optional[str] = None):
    async with async_session() as session:
        new_comment = CommentModel(
            profile_from = profile_from,
            profile_to = profile_to,
            comment_text = comment_text,
            comment_media_img = comment_media_img,
            comment_media_sound = comment_media_sound,
            comment_media_video = comment_media_video,
            comment_date = datetime.now()
        )

        session.add(new_comment)
        await session.commit()


# Возвращает комментарии в профиле по id
async def get_comment_on_profile(profile_id: int):
    async with (async_session() as session):
        query = select(
            CommentModel.profile_from, CommentModel.comment_date, CommentModel.comment_text
                       ).filter(CommentModel.profile_to == profile_id).order_by(CommentModel.comment_date.desc())
        res = await session.execute(query)
        comments = res.mappings().all()
        if comments:
            return comments
        else:
            return False


# Проверяет наличие комментария по id в БД
async def check_comment(comment_id: int):
    async with (async_session() as session):
        query = select(CommentModel.id).filter(CommentModel.id == comment_id)
        res = await session.execute(query)
        message = res.all()
        if message:
            return True
        else:
            return False


# Проверяет наличие комментария по id в БД
async def check_comment_from_to(comment_id: int):
    async with (async_session() as session):
        query = select(CommentModel.id).filter(CommentModel.id == comment_id)
        res = await session.execute(query)
        message = res.all()
        if message:
            return True
        else:
            return False


# Редактирует комментарий под id
async def edit_comment(comment_id: int, comment_text: Optional[str] = None,
                         comment_media_img: Optional[str] = None, comment_media_sound: Optional[str] = None,
                         comment_media_video: Optional[str] = None):
    async with async_session() as session:
        updated_comment = update(CommentModel).filter(CommentModel.id == comment_id).values(
            comment_text = comment_text,
            comment_media_img = comment_media_img,
            comment_media_sound = comment_media_sound,
            comment_media_video = comment_media_video,
        )

        await session.execute(updated_comment)
        await session.commit()


# удаляет комментарий из БД
async def delete_comment(comment_id: int):
    async with async_session() as session:
        query = delete(CommentModel).where(CommentModel.id == comment_id)

        await session.execute(query)
        await session.commit()