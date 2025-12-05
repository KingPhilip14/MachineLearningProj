from fastapi import FastAPI, HTTPException
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from fastapi.middleware.cors import CORSMiddleware
from backend.api.db import engine, SessionLocal
from backend.api.schemas.create_account import CreateAccount
from backend.api.models.account_table import account
from werkzeug.security import generate_password_hash

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
async def create_account(payload: CreateAccount):
    stmt = (
        insert(account)
        .values(username=payload.username, password=payload.password)
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


@app.get('/get_message')
async def read_root():
    return {'Message': 'Congrats! This is your API!'}


@app.get('/get_message_param')
def hello(name: str):
    # in URL, add "?name=<name_here>"
    return {'Message': f'Congrats, {name}! This is your API!'}
