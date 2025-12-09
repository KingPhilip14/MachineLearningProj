import os
import bcrypt

from typing import List
from fastapi import FastAPI, HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError
from fastapi.middleware.cors import CORSMiddleware
from backend.api.db import engine, SessionLocal
from backend.api.schemas.account_teams_response import AccountTeamsResponse
from backend.api.schemas.create_account import CreateAccount
from backend.api.models.ability_table import ability
from backend.api.models.account_table import account
from backend.api.models.move_table import move
from backend.api.models.movepool_table import movepool
from backend.api.models.moveset_table import moveset
from backend.api.models.pokemon_in_team_table import pokemon_in_team
from backend.api.models.pokemon_ability_table import pokemon_ability
from backend.api.models.pokemon_table import pokemon
from backend.api.models.team_table import team
from backend.api.schemas.delete_team import DeleteTeam
from backend.api.schemas.get_account import GetAccount
from backend.api.schemas.save_team import SaveTeam
from backend.api.schemas.team_request import TeamRequest
from backend.api.schemas.update_team_name import UpdateTeamName
from backend.api.schemas.team_prefs import TeamPrefs
from backend.ml.learning.team_builder import TeamBuilder
from backend.api.utils import nest_team_data
from config import POKEMON_DATA_DIR

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# dependency to get DB session
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get('/')
async def root():
    return 'Hello world!'


@app.post('/register')
def create_account(payload: CreateAccount):
    password: bytes = bytes(payload.password, 'utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)

    stmt = (
        insert(account)
        .values(username=payload.username, password=hashed_password)
        .returning(
            account.c.account_id, account.c.username, account.c.password
        )
    )

    try:
        with engine.begin() as conn:
            row = conn.execute(stmt).fetchone()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")

    if not row:
        raise HTTPException(status_code=400, detail="Username already exists")

    return dict(row._mapping)


@app.get('/account/{account_id}', response_model=GetAccount)
async def get_account(account_id: int):
    stmt = select(account).where(account.c.account_id == account_id)

    try:
        with engine.begin() as conn:
            row = conn.execute(stmt).fetchone()
    except IntegrityError:
        raise HTTPException(status_code=404, detail="Account not found")

    if not row:
        raise HTTPException(status_code=404, detail="Account not found")

    return dict(row._mapping)


@app.post('/generate-team')
async def generate_team(payload: TeamRequest):
    file_path = os.path.join(POKEMON_DATA_DIR, f'{payload.gen_file_name.lower()}_data.json')

    print(f'Using babies: {payload.using_little_cup}')
    print(f'Using legends: {payload.using_legends}')
    print(f'Composition: {payload.composition}')

    tb = TeamBuilder(
        payload.using_little_cup,
        payload.using_legends,
        file_path,
        payload.composition
    )

    team_json, weaknesses = tb.generate_team_json()

    if not team_json:
        raise HTTPException(
            status_code=400,
            detail='A team could not be generated. Malformed inputs may have been provided.'
        )

    return team_json, weaknesses


@app.post('/')
@app.get('/pokemon-ability/by-id/{pokemon_id}/{ability_id}')
async def get_pokemon_ability(pokemon_id: int, ability_id: int):
    stmt = (
        select(
            pokemon.c.pokemon_id,
            pokemon.c.pokemon_name,

            ability.c.ability_id,
            ability.c.ability_name,

            pokemon_ability.c.is_hidden,
        )
        .select_from(
            pokemon
            .join(pokemon_ability, pokemon_ability.c.pokemon_id == pokemon.c.pokemon_id)
            .join(ability, pokemon_ability.c.ability_id == ability.c.ability_id)
        )
        .where(
            (pokemon_ability.c.pokemon_id == pokemon_id) & (pokemon_ability.c.ability_id == ability_id)
        )
    )

    with engine.connect() as conn:
        row = conn.execute(stmt).fetchone()

    if not row:
        raise HTTPException(status_code=400,
                            detail=f'Could not find ability with ID {ability_id} for Pokemon with ID {pokemon_id}')

    return dict(row._mapping)


@app.get('/pokemon-ability/by-name/{pokemon_name}/{ability_name}')
async def get_pokemon_ability(pokemon_name: str, ability_name: str):
    pokemon_name = pokemon_name.lower()
    ability_name = ability_name.lower()

    stmt = (
        select(
            pokemon.c.pokemon_id,
            pokemon.c.pokemon_name,

            ability.c.ability_id,
            ability.c.ability_name,

            pokemon_ability.c.is_hidden,
        )
        .select_from(
            pokemon
            .join(pokemon_ability, pokemon_ability.c.pokemon_id == pokemon.c.pokemon_id)
            .join(ability, pokemon_ability.c.ability_id == ability.c.ability_id)
        )
        .where(
            (pokemon.c.pokemon_name == pokemon_name) & (ability.c.ability_name == ability_name)
        )
    )

    with engine.connect() as conn:
        row = conn.execute(stmt).fetchone()

    if not row:
        raise HTTPException(status_code=400,
                            detail=f'Could not find {ability_name} ability for {pokemon_name}')

    return dict(row._mapping)


@app.post('/account/{account_id}/save-team')
async def save_team(account_id: int, team_name: str, team_json: dict,
                    generation: str, overlapping_weaknesses: dict):
    team_stmt = (
        insert(team)
        .values(account_id=account_id, team_name=team_name, generation=generation,
                overlapping_weaknesses=overlapping_weaknesses)
        .returning(
            team.c.team_id, team.c.account_id, team.c.team_name, team.c.generation, team.c.time_created,
            team.c.last_time_used, team.c.overlapping_weaknesses
        )
    )

    with engine.begin() as conn:
        team_row = conn.execute(team_stmt).fetchone()

        if not team_row:
            raise HTTPException(status_code=400, detail="Something went wrong when saving the team")

        # get the team ID
        team_id: int = team_row._mapping['team_id']

        # insert Pokemon in PokemonInTeam by using the team_id
        for pkmn_name, pkmn_info in team_json.items():
            if pkmn_name == 'weaknesses':
                continue

            # find the pokemon ID from the Pokemon table
            pkmn_id_stmt = select(pokemon.c.pokemon_id).where(pokemon.c.pokemon_name == pkmn_name)
            pkmn_id = conn.execute(pkmn_id_stmt).scalar_one_or_none()

            if pkmn_id is None:
                raise HTTPException(
                    status_code=400,
                    detail=f'Pokémon "{pkmn_name}" was not found.'
                )

            # will modify later to support the full list
            abilities: str = pkmn_info['abilities']
            chosen_ability: str = abilities[0].lower()
            chosen_ability = chosen_ability.replace(' ', '-')

            # find ability from ability table
            ability_stmt = select(ability.c.ability_id).where(ability.c.ability_name == chosen_ability)
            ability_id = conn.execute(ability_stmt).scalar_one_or_none()

            if ability_id is None:
                raise HTTPException(
                    status_code=400,
                    detail=f'The {chosen_ability} ability was not found.'
                )

            # make a new nickname by only getting the first part of the name and capitalizing the first letter
            new_nickname: str = pkmn_name.split('-')[0]
            new_nickname = new_nickname[0].upper() + new_nickname[1:]

            pkmn_stmt = (
                insert(pokemon_in_team)
                .values(
                    team_id=team_id,
                    pokemon_id=pkmn_id,
                    chosen_ability_id=ability_id,
                    nickname=new_nickname,
                )
            )

            conn.execute(pkmn_stmt)

    return dict(team_row._mapping)


@app.get('/account/{account_id}/saved-teams', response_model=List[AccountTeamsResponse])
async def get_teams(account_id: int):
    stmt = (
        select(
            account.c.account_id,
            account.c.username,

            team.c.team_id,
            team.c.team_name,

            pokemon_in_team.c.pit_id,

            pokemon.c.pokemon_id,
            pokemon.c.pokemon_name,
            pokemon_in_team.c.chosen_ability_id,
            pokemon_in_team.c.nickname
        )
        .select_from(
            account
            .join(team, team.c.account_id == account.c.account_id)
            .join(pokemon_in_team, pokemon_in_team.c.team_id == team.c.team_id)
            .join(pokemon, pokemon_in_team.c.pokemon_id == pokemon.c.pokemon_id)
        )
        .where(account.c.account_id == account_id)
        .order_by(team.c.team_id)
    )

    with engine.connect() as conn:
        rows = conn.execute(stmt).fetchall()

    # return an empty list if no rows were returned; the given account has no teams
    if len(rows) == 0:
        return []

    return nest_team_data(rows)


@app.put('/account/{account_id}/team/{team_id}')
async def update_team_name(account_id: int, team_id: int, payload: UpdateTeamName):
    stmt = (
        update(team)
        .where(
            (team.c.team_id == team_id) & (team.c.account_id == account_id)
        )
        .values(team_name=payload.team_name)
        .returning(team.c.team_id, team.c.account_id, team.c.team_name, team.c.generation, team.c.time_created,
                   team.c.last_time_used, team.c.overlapping_weaknesses)
    )

    with engine.begin() as conn:
        row = conn.execute(stmt).fetchone()

    if not row:
        raise HTTPException(status_code=400,
                            detail=f'Could not find team with ID {team_id} for account with ID {account_id}')

    return dict(row._mapping)


@app.delete('/account/{account_id}/delete-team/{team_id}', response_model=DeleteTeam)
async def delete_team(account_id: int, team_id: int):
    stmt = (
        delete(team)
        .where(
            (team.c.team_id == team_id) & (team.c.account_id == account_id)
        )
        .returning(
            team.c.team_id, team.c.account_id, team.c.team_name, team.c.generation, team.c.time_created,
            team.c.last_time_used, team.c.overlapping_weaknesses
        )
    )

    with engine.begin() as conn:
        row = conn.execute(stmt).fetchone()

    if not row:
        raise HTTPException(status_code=400,
                            detail=f'Could not find team with ID {team_id} for account with ID {account_id}')

    return dict(row._mapping)


@app.get('/get-message')
async def read_root():
    return {'Message': 'Congrats! This is your API!'}


@app.get('/get-message-param')
def hello(name: str):
    # in URL, add "?name=<name_here>"
    return {'Message': f'Congrats, {name}! This is your API!'}
