from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PLANETS_DB: str
    ENTITIES_DB: str
    DUPLICATE_ENTITY_ERROR: str
    DUPLICATE_PLANET_ERROR: str
    CREATION_FAILED: str
    NOT_FOUND_ERROR: str
    INSERT_EVENT_FAILED: str
    SEND_EVENT_FAILED: str
    SOCKET_HOSTNAME: str
    SOCKET_PORT: int
    SERVER_ERROR: str
    RUNNING_UNIX: str
    MONGO_CONNECTION_STRING: str
    MONGO_DB: str
    SOCKET_PATH: str
    INTERVAL_SECONDS: int
    CHECK_REPRODUCTION: int
    ENTITY_INTERVAL_SECONDS: int
    GETTING_OLD: float
    REPRODUCTION_MESSAGE: str
    AGE_MESSAGE: str
    HUNGER_MESSAGE: str
    GETTING_HUNGRY: int
    WRITE_TO_DB_MESSAGE: str
    MAX_HUNGRY: int
    CANCEL: str
    ERROR: str

    class Config:
        env_file = ".env"


settings = Settings()
