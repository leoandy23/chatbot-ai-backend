from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from models.models import Conversation, Message, Document, User
from datetime import datetime
from core.config import Config
from uuid import UUID
from openai import OpenAI

client = OpenAI(api_key=Config.OPENAI_API_KEY)


def create_conversation(db: Session, user: User, query: str) -> Conversation:
    """
    Create a new conversation for the user. Optionally autogenerate title.
    """
    title = auto_generate_title(query)

    conversation = Conversation(
        user_id=user.id,
        title=title,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation


def list_conversations(db: Session, user: User) -> list[Conversation]:
    """
    Return all conversations belonging to a user.
    """
    return (
        db.query(Conversation)
        .filter(Conversation.user_id == user.id)
        .order_by(Conversation.updated_at.desc())
        .all()
    )


def get_conversation(db: Session, conversation_id: UUID, user: User) -> dict:
    """
    Fetch a conversation with all related messages and documents,
    ensuring ownership and returning a structured, JSON-serializable dict.
    """
    conversation = (
        db.query(Conversation)
        .options(
            joinedload(Conversation.messages).load_only(
                Message.id, Message.role, Message.content, Message.created_at
            ),
            joinedload(Conversation.documents).load_only(
                Document.id,
                Document.original_filename,
                Document.size,
                Document.status_message,
                Document.created_at,
                Document.file_path,
            ),
        )
        .filter(Conversation.id == conversation_id, Conversation.user_id == user.id)
        .first()
    )

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found"
        )

    # Sort messages chronologically
    sorted_messages = sorted(conversation.messages, key=lambda m: m.created_at)

    # Serialize messages
    messages_data = [
        {
            "id": str(m.id),
            "role": m.role,
            "content": m.content,
            "created_at": m.created_at.isoformat(),
        }
        for m in sorted_messages
    ]

    # Serialize attached documents
    documents_data = [
        {
            "id": str(d.id),
            "filename": d.original_filename,
            "size_kb": round(d.size / 1024, 2),
            "status": d.status_message,
            "uploaded_at": d.created_at.isoformat(),
            "file_path": d.file_path,
        }
        for d in conversation.documents
    ]

    # Structured response
    return {
        "id": str(conversation.id),
        "title": conversation.title,
        "created_at": conversation.created_at.isoformat(),
        "updated_at": conversation.updated_at.isoformat(),
        "messages": messages_data,
        "documents": documents_data,
    }


def add_message(
    db: Session,
    conversation: Conversation,
    role: str,
    content: str,
    metadata: dict | None = None,
) -> Message:
    """
    Add a message (user or assistant) to a conversation.
    """
    message = Message(
        conversation_id=conversation.id,
        role=role,
        content=content,
        message_metadata=metadata or {},
    )
    db.add(message)
    conversation.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(message)
    return message


def change_conversation_title(db: Session, conversation_id: UUID, new_title: str):
    """
    Change the title of a conversation.
    """
    conversation = (
        db.query(Conversation).filter(Conversation.id == conversation_id).first()
    )
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found"
        )
    conversation.title = new_title
    conversation.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(conversation)
    return conversation


def delete_conversation(db: Session, conversation_id: UUID):
    """
    Delete a conversation and all its related messages and documents.
    """
    conversation = (
        db.query(Conversation).filter(Conversation.id == conversation_id).first()
    )
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found"
        )

    db.delete(conversation)
    db.commit()


def attach_document(db: Session, conversation: Conversation, document_id: str):
    """
    Attach an already-uploaded document to a conversation.
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    document.conversation_id = conversation.id
    db.commit()
    db.refresh(document)
    return document


def auto_generate_title(question: str) -> str:
    """
    Generate a short conversation title using OpenAI (optional).
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Generate a concise 4-word title summarizing this question.",
                },
                {"role": "user", "content": question},
            ],
            max_tokens=10,
        )
        title = completion.choices[0].message.content.strip()
        return title[:50]
    except Exception:
        return "New Conversation"
