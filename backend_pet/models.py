from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from DB import Base 
from datetime import datetime

# 1. ОБ'ЄДНАНА МОДЕЛЬ КОРИСТУВАЧА
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String) 
    full_name = Column(String, nullable=True) 
    disabled = Column(Boolean, default=False)
    
    # Усі зв'язки в одному місці:
    items = relationship("Item", back_populates="owner")
    payments = relationship("Payment", back_populates="user")
    comments = relationship("Comment", back_populates="author")

# 2. МОДЕЛЬ ТОВАРІВ
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float, default=0.0)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")

# 3. МОДЕЛЬ ОПЛАТ (LiqPay)
class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    currency = Column(String, default="UAH")
    status = Column(String, default="pending") 
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="payments")

# 4. МОДЕЛЬ КОМЕНТАРІВ ТА РЕЙТИНГУ
class Comment(Base):
    __tablename__ = "comments" 

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    rating = Column(Integer, default=5)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="comments")

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)

class MinecraftNews(Base):
    __tablename__ = "minecraft_news"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    image_url = Column(String)
    url = Column(String)
    published_at = Column(DateTime, default=datetime.utcnow)