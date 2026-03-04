from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENTITIES_DB: str
    DUPLICATE_ENTITY_ERROR: str

    class Config:
        env_file = ".env"


settings = Settings()
