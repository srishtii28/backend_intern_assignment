from pydantic import BaseSettings

class Settings(BaseSettings):
    mongo_uri: str
    jwt_secret: str
    jwt_algorithm: str
    access_token_expire_minutes: int
    master_db: str

    class Config:
        env_file = ".env"

settings = Settings()
