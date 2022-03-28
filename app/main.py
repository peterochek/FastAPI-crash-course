from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app import models, auth
from .database import engine
from .routers import post, user, vote

# models.Base.metadata.create_all(bind=engine)  (alembic)

app = FastAPI(
    title="App",
    version="0.0.1",
    contact={
        "name": "peterochek",
        "url": "https://github.com/peterochek",
        "email": "peterkkor@gmail.com",
    },
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": engine.table_names()}
