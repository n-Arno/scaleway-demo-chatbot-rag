from llama_index.core import VectorStoreIndex
from app.settings import get_vector_store


def get_chat_engine():
    vector_store = get_vector_store()
    index = VectorStoreIndex.from_vector_store(vector_store)
    return index.as_chat_engine(chat_mode="condense_plus_context")
