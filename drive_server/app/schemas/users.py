from pydantic.typing import Optional
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: Optional[EmailStr] = None
    password: Optional[str] = None
    id: Optional[str] = None

    class Config:
        orm_mode = True
