from pydantic import BaseModel


class SaveTeam(BaseModel):
    team_name: str
    generation: str
    overlapping_weaknesses: dict
