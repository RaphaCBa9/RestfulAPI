from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import jwt
from datetime import datetime, timedelta
from baseModels import *
from config import *
import hashlib
from dotenv import load_dotenv
import requests


load_dotenv()

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

oauth2_scheme = HTTPBearer()


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


# Função para criar o token JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Função para autenticar o usuário
def auth_user_password(email: str, senha: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid email")

    hash_password = hashlib.sha256(senha.encode()).hexdigest()
    return hash_password == user.hashSenha


# Endpoint para registrar usuário
@app.post("/registrar")
def register_user(user: userRegister, db: Session = Depends(get_db)):
    user_already_exists = db.query(User).filter(User.email == user.email).first()
    if user_already_exists:
        raise HTTPException(status_code=409, detail="Email already registered")

    hashed_password = hashlib.sha256(user.senha.encode()).hexdigest()
    new_user = User(nome=user.nome, email=user.email, senha=user.senha, hashSenha=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    jwt_data = {"sub": new_user.email, "id": new_user.id}
    return {"jwt": create_access_token(jwt_data)}


# Endpoint para login
@app.post("/login")
def login(user: userLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email")

    correct_password = auth_user_password(user.email, user.senha, db)
    if not correct_password:
        raise HTTPException(status_code=401, detail="Invalid password")

    jwt_data = {"sub": db_user.email, "id": db_user.id}
    return {"jwt": create_access_token(jwt_data)}


# Middleware para validar o token JWT
async def JWTBearer(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=403, detail="Invalid token")

        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(status_code=403, detail="User not found")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token")
    return user


# Rota protegida
@app.get("/consultar")
def consultar(request: Request, authorization=[Depends(HTTPBearer)]):
    chuck_norris = requests.get("https://api.chucknorris.io/jokes/random")
    chuck_norris_json = chuck_norris.json()

    consulta_body = {"id": chuck_norris_json["id"], "fact": chuck_norris_json["value"]}
    return consulta_body