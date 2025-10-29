from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from core.config import Config
from uuid import UUID
import os


def get_vector_store(conversation_id: UUID):
    persist_directory = f"{Config.VECTOR_STORE_PATH}/{str(conversation_id)}"
    os.makedirs(persist_directory, exist_ok=True)
    embedding_model = OpenAIEmbeddings(
        model=Config.EMBEDDING_MODEL, openai_api_key=Config.OPENAI_API_KEY
    )
    vector_store = Chroma(
        persist_directory=persist_directory, embedding_function=embedding_model
    )
    return vector_store


def add_documents_to_vector_store(conversation_id: UUID, documents: list[Document]):
    vector_store = get_vector_store(conversation_id)
    vector_store.add_documents(documents)
