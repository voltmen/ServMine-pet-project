import os
import requests 
import json
import base64
import hashlib
import uuid
from typing import Annotated
from datetime import datetime, timedelta, date 

from fastapi import FastAPI, Depends, HTTPException, status, Form, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import DB 
import crud
import models
import schemas
from auth import router as auth_router, get_password_hash, get_current_active_user


models.Base.metadata.create_all(bind=DB.engine)

app = FastAPI()


origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)


def get_db():
    db = DB.Sessionlocal()
    try:
        yield db
    finally:
        db.close()

def generate_liqpay_signature(private_key, data):
    sign_str = private_key + data + private_key
    sha1_binary = hashlib.sha1(sign_str.encode('utf-8')).digest()
    return base64.b64encode(sha1_binary).decode('utf-8')

# Твої ключі (краще винести в .env файл)
LIQPAY_PUBLIC_KEY = "sandbox_i4499919954"
LIQPAY_PRIVATE_KEY = "sandbox_yEOoAa0cjYBJlZmPVU5w5wX1QguAkvlgfvYNDNKO"


app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

DONATION_VARIANTS = {
    1: {"price": 52.0, "title": "Стартовий донат (ServMine)", "desc": "Підтримка проекту"},
    2: {"price": 100.0, "title": "Покращений донат (ServMine)", "desc": "Для розвитку сервера"},
    3: {"price": 200.0, "title": "Мега донат (ServMine)", "desc": "Ти справжній меценат!"}
}

@app.post("/liqpay/params", tags=["Payments"])
def get_liqpay_params(
    item_id: int = Body(..., embed=True),
    current_user: Annotated[schemas.User, Depends(get_current_active_user)] = None,
    db: Session = Depends(get_db)
):
    if item_id in DONATION_VARIANTS:
        variant = DONATION_VARIANTS[item_id]
        price = variant["price"]
        title = variant["title"]
        description = variant["desc"]
    else:
        db_item = crud.get_item(db, item_id=item_id)
        if not db_item:
            raise HTTPException(status_code=404, detail="Товар або варіант донату не знайдено")
        price = float(db_item.price)
        title = db_item.title
        description = f"Оплата за {db_item.title}"

    order_id = f"uid{current_user.id}_item{item_id}_{uuid.uuid4().hex[:6]}"

    crud.create_payment(
        db=db,
        user_id=current_user.id,
        amount=price,
        order_id=order_id,
        description=description
    )

    params = {
        "public_key": LIQPAY_PUBLIC_KEY,
        "version": 3,
        "action": "pay",
        "amount": price,
        "currency": "UAH",
        "description": description,
        "order_id": order_id,
        "sandbox": 1,
        "result_url": "http://localhost:3000/payment-success",
        "server_url": "https://твій-домен.com/liqpay/callback" 
    }

    data_json = json.dumps(params)
    data = base64.b64encode(data_json.encode('utf-8')).decode('utf-8')
    signature = generate_liqpay_signature(LIQPAY_PRIVATE_KEY, data)

    return {"data": data, "signature": signature}

@app.post("/users/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED, tags=["User Management"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
      raise HTTPException(status_code=400, detail="Email already registered")
      
    hashed_password = get_password_hash(user.password) 
    return crud.create_user(db=db, user=user, hashed_password=hashed_password)

@app.get("/users/", response_model=list[schemas.User], tags=["User Management"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Отримати список усіх користувачів"""
    return crud.get_users(db, skip=skip, limit=limit)

@app.get("/users/me", response_model=schemas.User, tags=["User Management"])
def read_user_me(current_user: schemas.User = Depends(get_current_active_user)):
    """Отримати дані поточного авторизованого користувача"""
    return current_user

@app.get("/users/{user_id}", response_model=schemas.User, tags=["User Management"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Отримати конкретного користувача за його ID"""
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/items/", response_model=schemas.Item, tags=["Items"])
def create_item_for_user(
    item: schemas.ItemCreate, 
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=current_user.id)

@app.get("/items/", response_model=list[schemas.Item], tags=["Items"])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_items(db, skip=skip, limit=limit)

@app.delete("/users/{user_id}", tags=["User Management"])
def delete_user(
    user_id: int, 
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not authorized to delete this user"
        )
        
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    crud.delete_user(db, db_user)
    return {"detail": "User deleted"}

@app.post("/liqpay/callback", tags=["Payments"])
async def liqpay_callback(
    data: str = Form(...), 
    signature: str = Form(...), 
    db: Session = Depends(get_db)
):
    expected_signature = generate_liqpay_signature(LIQPAY_PRIVATE_KEY, data)
    if signature != expected_signature:
        raise HTTPException(status_code=400, detail="Invalid signature")

    decoded_data = json.loads(base64.b64decode(data).decode('utf-8'))
    status = decoded_data.get("status")
    order_id = decoded_data.get("order_id")

    if status in ["success", "sandbox"]:
        print(f"Order{order_id} Successfully paid!")
    
    return {"status": "ok"}

@app.patch("/users/{user_id}", response_model=schemas.User, tags=["User Management"])
def update_user_email(
    user_id: int, 
    update_data: schemas.UserUpdate, 
    db: Session = Depends(get_db)
):
    return crud.update_email_user(db=db, user_id=user_id, update_data=update_data)

@app.get("/reviews", response_model=list[schemas.Review], tags=["Content"])
def read_reviews(db: Session = Depends(get_db)):
    return crud.get_reviews(db)

@app.post("/reviews", response_model=schemas.Review, tags=["Content"])
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    """Зберегти новий відгук у базу"""
    return crud.create_review(db=db, review=review)

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

if not NEWS_API_KEY:
    print("WARNING: The NEWS_API_KEY key was not found in the environment.!")

@app.get("/news/minecraft", tags=["Content"])
def get_minecraft_news(db: Session = Depends(get_db)):
    last_news = db.query(models.MinecraftNews).first()
    
    if not last_news or last_news.published_at < datetime.utcnow() - timedelta(days=1):
        api_url = f"https://newsapi.org/v2/everything?q=minecraft+update&pageSize=3&apiKey={NEWS_API_KEY}"
        response = requests.get(api_url).json()
        
        if response.get("articles"):
            db.query(models.MinecraftNews).delete()
            for art in response["articles"]:
                new_item = models.MinecraftNews(
                    title=art["title"],
                    description=art["description"] or "",
                    image_url=art["urlToImage"] or "https://via.placeholder.com/300",
                    url=art["url"] 
                )
                db.add(new_item)
            db.commit()
            
    return db.query(models.MinecraftNews).all()
