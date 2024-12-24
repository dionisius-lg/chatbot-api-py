from pydantic import BaseModel, RootModel, Field
from typing import Optional, Literal, List
from datetime import date

class FetchData(BaseModel):
    response: Optional[str] = None
    intent_id: Optional[int] = None
    tag: Optional[str] = None
    is_active: Optional[Literal["0", "1"]] = None
    created_by: Optional[int] = None
    created_at: Optional[date] = None
    updated_by: Optional[int] = None
    updated_at: Optional[date] = None
    start: Optional[int] = None
    end: Optional[int] = None

class InsertData(BaseModel):
    response: str = Field(min_length=4, max_length=20)
    intent_id: int = Field(ge=1)

class UpdateData(BaseModel):
    response: Optional[str] = Field(default=None, min_length=4, max_length=20)
    intent_id: Optional[int] = Field(default=None, ge=1)
    is_active: Optional[Literal["0", "1"]] = None

class InsertManyData(RootModel):
    root: List[InsertData] = Field(None, min_length=1)

class InsertManyUpdateData(RootModel):
    class Data(BaseModel):
        id: Optional[int] = Field(default=None, ge=1)
        response: str = Field(min_length=4, max_length=20)
        intent_id: int = Field(ge=1)
        is_active: Optional[Literal["0", "1"]] = None

    root: List[Data] = Field(None, min_length=1)