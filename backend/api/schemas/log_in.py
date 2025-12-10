from pydantic import BaseModel


class LogIn(BaseModel):
    username: str
    password: str
