from pydantic import BaseModel
from typing import Dict, Any


class SaveTeamRequest(BaseModel):
    team_name: str
    team_json: Dict[str, Any]
    generation: str
    overlapping_weaknesses: Dict[str, Any]
