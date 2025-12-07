from pydantic import BaseModel


class PokemonInTeamModel(BaseModel):
    pit_id: int
    pokemon_id: int
    pokemon_name: str
    chosen_ability_id: int
    nickname: str
