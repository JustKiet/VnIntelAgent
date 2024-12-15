from langchain_openai import ChatOpenAI
from typing import Optional
from langchain_core.language_models.chat_models import BaseChatModel

def initialize_model(model_name: str, config: Optional[dict]) -> BaseChatModel:
    model = ChatOpenAI(
        model=model_name
    )
    return model