from pydantic import BaseModel
from typing import Optional

class UserConfig(BaseModel):
    #user_id: str
    #agent_name: str
    keyword: str
    language: str
    article_tone: str
    model: str
    word_count: int
    additional_prompt: Optional[str]
