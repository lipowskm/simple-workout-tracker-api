from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    first_name: str
    last_name: Optional[str]
    age: int
    email: str

    class Config:
        orm_mode = True
