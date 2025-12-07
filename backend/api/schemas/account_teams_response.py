from pydantic import BaseModel
from typing import List
from backend.api.schemas.team import TeamModel


class AccountTeamsResponse(BaseModel):
    account_id: int
    username: str
    teams: List[TeamModel]
