from pydantic import BaseModel, Field
from typing import Optional

class Chat(BaseModel):
    chat_session_id: Optional[str] = Field(default=None, min_length=1, max_length=50)
    message: str = Field(min_length=1)
