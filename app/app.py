import os
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import jwt
from datetime import datetime, timedelta
import bcrypt
import requests
from pydantic import BaseModel
from baseModels import *
from config import *
import hashlib


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    nome = Column(String)
    email = Column(String, unique=True)
    senha = Column(String)
    hashSenha = Column(String)


# FastAPI app
app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.on_event("startup")
def startup_event():
    print("Starting up...")
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.now(datetime.timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authUserPassword(email: str, senha: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid email")
    
    hashPassword = hashlib.sha256(senha.encode()).hexdigest()

    return user.hashSenha == hashPassword


@app.post("/registrar")
def registerUser(user: userRegister, db: Session = Depends(get_db)):
    

    userAlreadyExists = (
        db.query(User).filter(User.email == user.email).first() is not None
    )
    if userAlreadyExists:
        raise HTTPException(status_code=409, detail="Email already registered")

    hashed_password = bcrypt.hashpw(user.senha.encode("utf-8"), bcrypt.gensalt())
    newUser = User(
        nome=user.nome, email=user.email, senha=user.senha, hashSenha=hashed_password
    )
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    jwtData = {
        "sub": newUser.email,
        "id": newUser.id,
    }

    return {"jwt": create_access_token(jwtData)}

@app.post("/login")
def login(user: userLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user.email).first()

    userExists = user is not None

    if not userExists:
        raise HTTPException(status_code=401, detail="Invalid email")
    
    correctPassword = authUserPassword(user.email, user.senha, db)

    if not correctPassword:
        raise HTTPException(status_code=401, detail="Invalid password")
    jwtData = {
        "sub": user.email,
        "id": user.id,
    }
    return {"jwt": create_access_token(jwtData)}

@app.get("/consultar")
def consultar(request: Request, token: str = Depends(oauth2_scheme)):
    chuckNorris = requests.get("https://api.chucknorris.io/jokes/random")
    chuckNorrisJson = chuckNorris.json()

    consultaBody = {
        "id": chuckNorrisJson["id"],
        "fact": chuckNorrisJson["value"],
    }
    
    return consultaBody