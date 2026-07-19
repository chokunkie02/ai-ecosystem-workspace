from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    redis_host: str
    redis_port: int
    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_db: str
    label_studio_url: str
    label_studio_api_key: str

    class Config:
        env_file = ".env"

settings = Settings()
