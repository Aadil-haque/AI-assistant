from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from .db import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(String, index=True)

    sender = Column(String)

    text = Column(Text)

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )
class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(String, unique=True, index=True)

    title = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
