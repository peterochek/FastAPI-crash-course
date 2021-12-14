from fastapi import FastAPI

from app import models, auth
from .database import engine
from .routers import post, user, vote

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='App',
    version='0.0.1',
    contact={
        'name': 'peterochek',
        'url': 'https://github.com/peterochek',
        'email': 'peterkkor@gmail.com',
    }
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get('/')
def root():
    return {'message': 'root'}
