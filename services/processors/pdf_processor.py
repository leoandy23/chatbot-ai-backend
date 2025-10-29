from services.document_service import save_document
from services.vector_db_service import add_documents_to_vector_store
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sqlalchemy.orm import Session
import os
from uuid import UUID


def process_pdf(
    db: Session, conversation_id: UUID, filename: str, file_path: str
) -> list[Document]:
    file_size = 0
    with open(file_path, "rb") as file:

        from PyPDF2 import PdfReader

        reader = PdfReader(file)
        file_size = os.path.getsize(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""],
    )
    chunks = text_splitter.split_text(text)

    documents = []
    for i, chunk in enumerate(chunks):
        metadata = {
            "conversation_id": str(conversation_id),
            "source": filename,
            "chunk_index": i,
        }
        document = Document(page_content=chunk, metadata=metadata)
        documents.append(document)

    add_documents_to_vector_store(conversation_id, documents)

    save_document(
        db,
        conversation_id,
        filename,
        file_path,
        text,
        file_size,
        True,
        "Processed successfully",
    )

    return documents
