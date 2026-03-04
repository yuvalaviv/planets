from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENTITIES_DB: str

    class Config:
        env_file = ".env"


settings = Settings()
