from pydantic import BaseModel


class UpdateTeamName(BaseModel):
    team_name: str
