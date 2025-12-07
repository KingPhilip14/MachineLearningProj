from pydantic import BaseModel
from datetime import datetime


class DeleteTeam(BaseModel):
    team_id: int
    account_id: int
    team_name: str
    generation: str
    time_created: datetime
    last_time_used: datetime
    overlapping_weaknesses: dict
