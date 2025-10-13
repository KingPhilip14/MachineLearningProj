from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def root():
    return 'Hello world!'

@app.get('/get_message')
async def read_root():
    return {'Message': 'Congrats! This is your API!'}

@app.get('/get_message_param')
def hello(name: str):
    return {'Message': f'Congrats, {name}! This is your API!'}
