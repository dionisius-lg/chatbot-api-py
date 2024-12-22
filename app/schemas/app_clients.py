from pydantic import BaseModel, RootModel, Field
from typing import Optional, Literal, List, Dict
from datetime import date

class _Auth(BaseModel):
    key: str = Field(min_length=4, max_length=50)
    value: str = Field(min_length=4, max_length=100)

class FetchData(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    is_active: Optional[Literal["0", "1"]] = None
    created_by: Optional[int] = None
    created_at: Optional[date] = None
    updated_by: Optional[int] = None
    updated_at: Optional[date] = None
    start: Optional[int] = None
    end: Optional[int] = None

class InsertData(BaseModel):
    name: str = Field(min_length=4, max_length=20)
    url: str = Field(min_length=4, max_length=20)
    auth: Optional[_Auth] = None

class UpdateData(BaseModel):
    name: Optional[str] = Field(default=None, min_length=4, max_length=20)
    url: Optional[str] = Field(default=None, min_length=4, max_length=20)
    auth: Optional[_Auth] = None
    is_active: Optional[Literal["0", "1"]] = None

class InsertManyData(RootModel):
    root: List[InsertData] = Field(None, min_length=1)

class InsertManyUpdateData(RootModel):
    class Data(BaseModel):
        id: Optional[int] = Field(default=None, min=1)
        name: str = Field(min_length=4, max_length=20)
        url: str = Field(min_length=4, max_length=20)
        auth: Optional[_Auth] = None
        is_active: Optional[Literal["0", "1"]] = None

    root: List[Data] = Field(None, min_length=1)