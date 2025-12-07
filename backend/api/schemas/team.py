from pydantic import BaseModel
from typing import List
from backend.api.schemas.pokemon_in_team import PokemonInTeamModel


class TeamModel(BaseModel):
    team_id: int
    team_name: str
    pokemon: List[PokemonInTeamModel]
