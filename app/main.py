from fastapi import FastAPI
from app.api.v1 import auth, token
from app.db.session import init_db


def lifespan(app: FastAPI):
    init_db()

    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, prefix='/v1/auth', tags=['auth'])
app.include_router(token.router, prefix='/v1/token', tags=['token'])

@app.get('/')
def read_root():
    return {'message': ''}
