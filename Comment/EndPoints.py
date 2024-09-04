from datetime import datetime

from asyncpg.pgproto.pgproto import timedelta
from fastapi import APIRouter
from sqlalchemy import select
from typing import Optional

from Comment.CommentForm import CommentCreateForm
from Comment.Comment_CRUD import comment_create, edit_comment, get_comment_on_profile, delete_comment, check_comment


comment_router = APIRouter(
    prefix='/comment',
    tags=['comment']
)


@comment_router.post('/MakeComment/')
async def new_comment(profile_from: int, profile_to: int, comment_text: Optional[str] = None,
                         comment_media_img: Optional[str] = None, comment_media_sound: Optional[str] = None,
                         comment_media_video: Optional[str] = None):
    """
    API для создания комментария на странице профиля
    """
    if comment_text is None and comment_media_img is None and comment_media_sound is None and comment_media_video is None:
        return {
            "status": 400,
            "message": "В комментарии вообще ничего нет, введите хоть что-то (текст, картинку, аудио или видео)"
        }

    validation_errors = []
    app_error = []

    form = CommentCreateForm(comment_text)

    if await form.is_valid():
        try:
            await comment_create(profile_from, profile_to, comment_text, comment_media_img,
                                 comment_media_sound, comment_media_video)
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


@comment_router.get("/ShowCommentOnProfile")
async def get_comments(profile_id: int):
    """
    API для вывода комментариев на профиле пользователя по id профиля
    """
    result = []
    comments = await get_comment_on_profile(profile_id)
    if comments:
        status = 200

        for i, element in enumerate(comments, start=1):
            result.append({f"message_{i}": element})
    else:
        status = 400
        result = "Либо на профиле нет комментариев, либо вы ввели неверный id"
    return {
        "status": status,
        "messages": result
    }


@comment_router.patch("/EditComment")
async def alter_comment(comment_id: int, comment_text: Optional[str] = None,
                         comment_media_img: Optional[str] = None, comment_media_sound: Optional[str] = None,
                         comment_media_video: Optional[str] = None):
    """
    API для редактирования контента комментария по id
    """
    if comment_text is None and comment_media_img is None and comment_media_sound is None and comment_media_video is None:
        return {
            "status": 400,
            "message": "В сообщении вообще ничего нет, введите хоть что-то (текст, картинку, аудио или видео)"
        }

    if await check_comment(comment_id):
        await edit_comment(comment_id, comment_text, comment_media_img,
                                   comment_media_sound, comment_media_video)

        status = 200
        message = "Done"
    else:
        status = 400
        message = "Такого сообщения нет"

    return {
        "status": status,
        "message": message
    }


@comment_router.delete("/DeleteComment")
async def del_message(comment_id: int):
    """
    API для удаления комментарий, в последствии API будет переписана так
    чтобы это мог сделать только сам пользователь, если авторизован,
    либо модерация
    """
    if await check_comment(comment_id):
        await delete_comment(comment_id)
        status = 200
        message = "Комментарий успешно удален"
    else:
        status = 400
        message = "Комментария нет в таблице"

    return {
        "status": status,
        "message": message
    }