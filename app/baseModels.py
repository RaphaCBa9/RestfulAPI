import os
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import jwt
from datetime import datetime, timedelta
import bcrypt
import requests
from pydantic import BaseModel


# Pydantic models
class userRegister(BaseModel):
    nome: str
    email: str
    senha: str


class userLogin(BaseModel):
    email: str
    senha: str


class chuckNorrisFact(BaseModel):
    id: str
    fact: str


