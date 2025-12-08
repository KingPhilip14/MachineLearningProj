from pydantic import BaseModel


class SaveTeam(BaseModel):
    team_name: str = 'My Team'
    generation: str
    overlapping_weaknesses: dict
