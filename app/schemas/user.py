from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: Optional[str]
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False

    class Config:
        orm_mode = True
