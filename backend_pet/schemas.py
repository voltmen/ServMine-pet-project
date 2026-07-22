from pydantic import BaseModel
from datetime import datetime

# --- Item Schemas ---

class ItemBase(BaseModel):
    """Базові поля для предмета."""
    title: str
    description: str | None = None

class ItemCreate(ItemBase):
    pass 

class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True 

# --- User Schemas ---

class UserBase(BaseModel):
    username: str
    email: str 
    full_name: str | None = None 

class UserCreate(UserBase):
    password: str 

class UserUpdate(BaseModel):
    email: str | None = None
    username: str | None = None
    full_name: str | None = None

class User(UserBase):
    id: int
    disabled: bool = False 
    items: list[Item] | None = [] 
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class ReviewBase(BaseModel):
    text: str

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    class Config:
        from_attributes = True

class NewsItem(BaseModel):
    id: int
    title: str
    description: str
    image_url: str
    published_at: datetime

    class Config:
        from_attributes = True