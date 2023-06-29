from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "DataCose Code Challenge API"
    database_user: str
    database_password: str
    database_host: str
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str
    access_token_expires_in: int

    class Config:
        env_file = ".env"

settings = Settings()