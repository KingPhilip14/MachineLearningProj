import os

import bcrypt
import uvicorn

from fastapi import FastAPI, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError
from fastapi.middleware.cors import CORSMiddleware
from backend.api.db import engine, SessionLocal
from backend.api.schemas.create_account import CreateAccount
from backend.api.models.account_table import account
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from backend.api.schemas.get_account import GetAccount
from backend.ml.learning.team_builder import TeamBuilder
from config import POKEMON_DATA_DIR

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


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
async def generate_team(using_babies: bool, using_legends: bool, gen_file_name: str,
                        preferences: dict[str, bool] | None = None):
    file_path: str = os.path.join(POKEMON_DATA_DIR, f'{gen_file_name.lower()}_data.json')
    tb: TeamBuilder = TeamBuilder(using_babies, using_legends, file_path, preferences)
    team_json: dict = tb.generate_team_json()

    if not team_json:
        raise HTTPException(status_code=400,
                            detail="A team could not be generated. Malformed inputs may have been provided.")

    return team_json


@app.get('/get_message')
async def read_root():
    return {'Message': 'Congrats! This is your API!'}


@app.get('/get_message_param')
def hello(name: str):
    # in URL, add "?name=<name_here>"
    return {'Message': f'Congrats, {name}! This is your API!'}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
