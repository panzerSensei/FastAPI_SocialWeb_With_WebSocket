from sqlalchemy import ForeignKey
from datetime import datetime
from sqlalchemy import func, String
import sqlalchemy.orm
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Annotated

from BD_Config import async_engine
from BD_BaseModel import Base_Model


intpk = Annotated[int, mapped_column(primary_key = True)]
strnotnull = Annotated[str, mapped_column(nullable = False)]


class UserModel(Base_Model):
    __tablename__ = "User"
    id: Mapped[intpk]
    username: Mapped[strnotnull] = mapped_column(String(30))
    password: Mapped[strnotnull] = mapped_column(String(30))
    email: Mapped[strnotnull] = mapped_column(String(100))


class ProfileModel(Base_Model):
    __tablename__ = "Profile"
    id: Mapped[intpk]
    user: Mapped[int] = mapped_column(ForeignKey("User.id", ondelete="CASCADE"), nullable=False)
    profile_name: Mapped[str] = mapped_column(String(30), nullable = False)
    profile_img: Mapped[str] = mapped_column(nullable = True)
    profile_info: Mapped[str] = mapped_column(String(1000), nullable=True)
    profile_hobbies: Mapped[str] = mapped_column(String(1000), nullable=True)
    profile_interest: Mapped[str] = mapped_column(String(1000), nullable=True)
    birthdate: Mapped[datetime] = mapped_column(nullable = False, server_default = func.now())
    registration_date: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())


class ChatModel(Base_Model):
    __tablename__ = "Chat"
    id: Mapped[intpk]
    chat_name: Mapped[str] = mapped_column(String(30), nullable=True)
    profile_from: Mapped[int] = mapped_column(ForeignKey("Profile.id", ondelete="CASCADE"), nullable=False)
    profile_to: Mapped[int] = mapped_column(ForeignKey("Profile.id", ondelete="CASCADE"), nullable=False)


class MessageModel(Base_Model):
    __tablename__ = "Message"
    id: Mapped[intpk]
    chat_id: Mapped[int] = mapped_column(ForeignKey("Chat.id", ondelete="CASCADE"), nullable=False)
    message_from: Mapped[int] = mapped_column(ForeignKey("Profile.id", ondelete="CASCADE"), nullable=False)
    message_text: Mapped[strnotnull] = mapped_column(String(500))
    message_media_img: Mapped[strnotnull] = mapped_column(nullable = True)
    message_media_sound: Mapped[strnotnull] = mapped_column(nullable=True)
    message_media_video: Mapped[strnotnull] = mapped_column(nullable=True)
    message_date: Mapped[datetime] = mapped_column(nullable = False, server_default = func.now())


class CommentModel(Base_Model):
    __tablename__ = "Comment"
    id: Mapped[intpk]
    profile_from: Mapped[int] = mapped_column(ForeignKey("Profile.id", ondelete="CASCADE"), nullable=False)
    profile_to: Mapped[int] = mapped_column(ForeignKey("Profile.id", ondelete="CASCADE"), nullable=False)
    comment_text: Mapped[strnotnull] = mapped_column(String(500))
    comment_media_img: Mapped[str] = mapped_column(nullable = True)
    comment_media_sound: Mapped[str] = mapped_column(nullable=True)
    comment_media_video: Mapped[str] = mapped_column(nullable=True)
    comment_date: Mapped[datetime] = mapped_column(nullable = False, server_default = func.now())


class TokenModel(Base_Model):
    __tablename__ = "token"
    id: Mapped[intpk]
    user: Mapped[int] = mapped_column(ForeignKey("User.id", ondelete="CASCADE"), nullable=False)
    access_token: Mapped[strnotnull]
    refresh_token: Mapped[strnotnull]
    expire_time: Mapped[datetime] = mapped_column(nullable = False)
    token_type: Mapped[strnotnull]