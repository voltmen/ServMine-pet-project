from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt, os
from jwt.exceptions import PyJWTError 
from dotenv import load_dotenv

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from pwdlib.exceptions import HasherNotAvailable

import crud
import schemas
import DB 

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256") 
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

try:
    password_hash = PasswordHash.recommended()
except HasherNotAvailable:
    print("Warning: Argon2 not available, falling back to Bcrypt.")
    password_hash = PasswordHash.recommended(algorithms=["bcrypt"])

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token") 

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Перевіряє відповідність пароля хешу."""
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Створює хеш пароля."""
    return password_hash.hash(password)

def authenticate_user(db: Session, identifier: str, password: str):
    """
    Перевіряє дані користувача у БД. 
    Ідентифікатор може бути username АБО email.
    """
    user = crud.get_user_by_username(db, username=identifier) 
    
    if not user:
        user = crud.get_user_by_email(db, email=identifier)
    
    if not user:
        return False
    
    if not verify_password(password, user.hashed_password):
        return False
        
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Створює JWT токен."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) 
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], 
    db: Session = Depends(DB.get_db) 
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) 
        username: str = payload.get("sub") 
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except PyJWTError: 
        raise credentials_exception
    
    user = crud.get_user_by_username(db, username=token_data.username) 
    
    if user is None:
        raise credentials_exception
        
    return user

async def get_current_active_user(
    current_user: Annotated[schemas.User, Depends(get_current_user)],
):
    """Перевіряє, чи активний користувач."""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(DB.get_db)
) -> schemas.Token:
    user = authenticate_user(db, form_data.username, form_data.password) 
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/", response_model=schemas.User)
async def read_users_me(
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
):
    return current_user