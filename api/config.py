from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    provider: str = "ollama"
    model: str = "tinyllama"
    api_key: str | None = None
    base_url: str | None = None

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
