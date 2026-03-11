from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.infrastructure.db.connection import Base
from datetime import datetime
from typing import Optional


class UserModel(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    user_name: Mapped[str] = mapped_column(String(100), index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(50), default="user")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    registration_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    documents = relationship("DocumentModel", back_populates="user")
    conversations = relationship("ConversationModel", back_populates="user")


class DocumentModel(Base):
    __tablename__ = "documents"

    document_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    title: Mapped[str] = mapped_column(String(255))
    file_path: Mapped[str] = mapped_column(String(255))
    page_count: Mapped[int] = mapped_column(Integer, default=0)
    processed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )
    tags: Mapped[Optional[list[str]]] = mapped_column(String(255), nullable=True)

    user = relationship("UserModel", back_populates="documents")
    conversations = relationship("ConversationModel", back_populates="document")


class ConversationModel(Base):
    __tablename__ = "conversations"

    conversation_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, index=True
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.document_id"))
    title: Mapped[str] = mapped_column(String(255), default="Untitled Conversation")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    user = relationship("UserModel", back_populates="conversations")
    document = relationship("DocumentModel", back_populates="conversations")
    messages = relationship("MessageModel", back_populates="conversation")


class MessageModel(Base):
    __tablename__ = "messages"

    message_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    conversation_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("conversations.conversation_id")
    )
    role: Mapped[str] = mapped_column(String(50))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    conversation = relationship("ConversationModel", back_populates="messages")
