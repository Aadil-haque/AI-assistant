from sqlalchemy.orm import Session

from backend.database.db import SessionLocal
from backend.database.models import Message
from .models import Conversation


def save_message(session_id, sender, text):
    db: Session = SessionLocal()

    try:
        conversation = (
            db.query(Conversation)
            .filter(Conversation.session_id == session_id)
            .first()
        )

        if conversation is None:

            # Only use the FIRST USER message as the title
            title = text.strip()

            title = title.replace("\n", " ")

            if len(title) > 60:
                title = title[:60] + "..."

            conversation = Conversation(
                session_id=session_id,
                title=title
            )

            db.add(conversation)

        db.add(conversation)
        msg = Message(
            session_id=session_id,
            sender=sender,
            text=text
        )

        db.add(msg)
        db.commit()

    finally:
        db.close()


def get_history(session_id, limit=10):
    db: Session = SessionLocal()

    try:
        messages = (
            db.query(Message)
            .filter(Message.session_id == session_id)
            .order_by(Message.timestamp.desc())
            .limit(limit)
            .all()
        )

        messages.reverse()

        return [
            {
                "sender": m.sender,
                "text": m.text
            }
            for m in messages
        ]

    finally:
        db.close()

def get_conversations():
    db = SessionLocal()

    conversations = (
        db.query(Conversation)
        .order_by(Conversation.updated_at.desc())
        .all()
    )

    db.close()

    return [
        {
            "session_id": c.session_id,
            "title": c.title,
            "updated_at": c.updated_at
        }
        for c in conversations
    ]

def get_conversation(session_id):
    db = SessionLocal()

    messages = (
        db.query(Message)
        .filter(Message.session_id == session_id)
        .order_by(Message.timestamp.asc())
        .all()
    )

    db.close()

    return [
        {
            "sender": m.sender,
            "text": m.text,
            "timestamp": m.timestamp
        }
        for m in messages
    ]