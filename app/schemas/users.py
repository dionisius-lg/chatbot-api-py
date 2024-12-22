from pydantic import BaseModel, RootModel, Field
from typing import Optional, Literal, List
from datetime import date

class FetchData(BaseModel):
    username: Optional[str] = None
    fullname: Optional[str] = None
    is_active: Optional[Literal["0", "1"]] = None
    created_by: Optional[int] = None
    created_at: Optional[date] = None
    updated_by: Optional[int] = None
    updated_at: Optional[date] = None
    start: Optional[int] = None
    end: Optional[int] = None

class InsertData(BaseModel):
    username: str = Field(min_length=4, max_length=20)
    password: str = Field(min_length=4, max_length=20)
    fullname: Optional[str] = Field(default=None, min_length=4, max_length=50)

class UpdateData(BaseModel):
    username: Optional[str] = Field(default=None, min_length=4, max_length=20)
    password: Optional[str] = Field(default=None, min_length=4, max_length=20)
    fullname: Optional[str] = Field(default=None, min_length=4, max_length=50)
    is_active: Optional[Literal["0", "1"]] = None

class InsertManyData(RootModel):
    root: List[InsertData] = Field(None, min_length=1)

class InsertManyUpdateData(RootModel):
    root: List[UpdateData] = Field(None, min_length=1)