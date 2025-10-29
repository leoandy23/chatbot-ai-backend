from sqlalchemy.orm import Session
from models.models import Document
from uuid import UUID


def save_document(
    db: Session,
    conversation_id: UUID,
    original_filename: str,
    file_path: str,
    extracted_text: str,
    size: int,
    processed: bool,
    status_message: str,
) -> Document:
    new_document = Document(
        conversation_id=conversation_id,
        original_filename=original_filename,
        file_path=file_path,
        extracted_text=extracted_text,
        size=size,
        processed=processed,
        status_message=status_message,
    )
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    return new_document
