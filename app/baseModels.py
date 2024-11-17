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


