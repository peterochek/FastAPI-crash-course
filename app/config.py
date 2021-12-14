from pydantic import BaseSettings


class Settings(BaseSettings):
    db_link: str
    expiration: int


settings = Settings()
