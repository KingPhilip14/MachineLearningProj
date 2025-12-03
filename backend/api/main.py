from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from backend.api.db.db import engine, SessionLocal

app = FastAPI()

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

# @app.post('/users/')
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     db_user =

@app.get('/get_message/')
async def read_root():
    return {'Message': 'Congrats! This is your API!'}

@app.get('/get_message_param/')
def hello(name: str):
    # in URL, add "?name=<name_here>"
    return {'Message': f'Congrats, {name}! This is your API!'}

@app.post('/create_user/')
def create_user():
    pass
