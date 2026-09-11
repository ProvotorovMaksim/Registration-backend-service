from os import getenv
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = getenv("DATABASE_URL", "")
    DATABASE_DRIVER: str = getenv("DATABASE_DRIVER", "")
    POSTGRES_USER: str = getenv("POSTGRES_USER", "")
    POSTGRES_PASSWORD: str = getenv("POSTGRES_PASSWORD", "")
    POSTGRES_DB: str = getenv("POSTGRES_DB", "")

    KAFKA_BROKER_URL: str = getenv("KAFKA_BROKER_URL", "localhost:9092")
    KAFKA_BOOTSTRAP_SERVERS: str = getenv("KAFKA_BOOTSTRAP_SERVERS", "")

    JWT_SECRET_KEY: str = getenv("JWT_SECRET_KEY", "default_secret_key")
    ALGORITHM: str = getenv("ALGORITHM", "HS256")

    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    class Config: 
        env_file = ".env"

settings = Settings()