from fastapi import HTTPException
from langchain_openai import ChatOpenAI
from services.vector_db_service import get_vector_store
from sqlalchemy.orm import Session
from models.models import Message, Conversation
from core.config import Config
from uuid import UUID

llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=Config.OPENAI_API_KEY)


def get_response(db: Session, query: str, conversation_id: UUID) -> str:
    """
    Get a response from the LLM for the given query.
    """
    conversation = (
        db.query(Conversation).filter(Conversation.id == conversation_id).first()
    )

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    vector_store = get_vector_store(conversation_id)
    retriever = vector_store.as_retriever(
        search_type="similarity", search_kwargs={"k": 5}
    )
    relevant_docs = retriever.invoke(query)

    if not relevant_docs:
        context_text = "No relevant documents found."
    else:
        context_text = "\n\n".join([doc.page_content for doc in relevant_docs])

    chat_history = []
    messages_records = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .all()
    )

    for msg in messages_records:
        chat_history.append({"role": msg.role, "content": msg.content})

    chat_history.append({"role": "user", "content": query})

    system_prompt = (
        "You are an AI assistant that answers user questions based on the retrieved context.\n"
        "Use only the context provided below to answer accurately.\n\n"
        f"### Retrieved Context ###\n{context_text}\n\n"
        "If the answer cannot be found in the context, say you don't know."
    )

    full_messages = [{"role": "system", "content": system_prompt}, *chat_history]

    response = llm.invoke(full_messages)

    new_user_message = Message(
        conversation_id=conversation_id,
        role="user",
        content=query,
    )
    db.add(new_user_message)
    db.commit()
    db.refresh(new_user_message)
    new_ai_message = Message(
        conversation_id=conversation_id,
        role="assistant",
        content=response.content,
    )
    db.add(new_ai_message)
    db.commit()
    db.refresh(new_ai_message)

    return response.content
