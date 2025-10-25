from pydantic import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DATABASE_URL: str

    # JWT_SECRET_KEY: str
    # ALGORITHM: str
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


settings = Settings()
