from sqlalchemy.orm import Session
import models 
import schemas 


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    db_user = models.User(
        email=user.email,
        username=user.username, 
        full_name=user.full_name, 
        hashed_password=hashed_password 
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, update_data: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    user_data = update_data.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
        
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, db_user: models.User):
    db.delete(db_user)
    db.commit()

def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.model_dump(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def create_transaction(db: Session, user_id: int, amount: float, order_id: str, description: str):
    pass

from models import Payment
from sqlalchemy.orm import Session

def create_payment(db: Session, user_id: int, amount: float, order_id: str, description: str):
    db_payment = Payment(
        user_id=user_id,
        amount=amount,
        order_id=order_id,
        description=description,
        status="pending" 
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def get_payment_by_order_id(db: Session, order_id: str):
    return db.query(Payment).filter(Payment.order_id == order_id).first()

def update_payment_status(db: Session, order_id: str, new_status: str):
    db_payment = get_payment_by_order_id(db, order_id)
    if db_payment:
        db_payment.status = new_status
        db.commit()
        db.refresh(db_payment)
    return db_payment

def get_reviews(db: Session):

    return db.query(models.Review).order_by(models.Review.id.desc()).all()

def create_review(db: Session, review: schemas.ReviewCreate):
    db_review = models.Review(text=review.text)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review