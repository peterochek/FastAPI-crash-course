from pydantic import BaseSettings


class Settings(BaseSettings):
    db_username: str
    db_password: str
    db_hostname: str
    db_port: int
    db_name: str

    expiration: int
    key: str
    algorithm: str

    class Config:
        env_file = ".env"


settings = Settings()
