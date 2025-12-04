from pydantic import BaseModel


class CreateAccount(BaseModel):
    username: str
    password: str
