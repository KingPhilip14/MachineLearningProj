from pydantic import BaseModel


class GetAccount(BaseModel):
    account_id: int
    username: str
