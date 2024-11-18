import os
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import jwt
from datetime import datetime, timedelta
import bcrypt
import requests
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv(override=True)

# jwt consfiguration
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

# database configuration
USER= os.getenv("USER", "postgres")
PASSWORD= os.getenv("PASSWORD", "postgres")
HOST= os.getenv("HOST", "localhost")
PORT= os.getenv("PORT", "5432")
DATABASE= os.getenv("DB_NAME", "postgres")


# database connection
SQLALCHEMY_DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
