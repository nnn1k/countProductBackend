from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent


class DbConfig(BaseModel):
    user: str
    password: str
    host: str
    port: int
    name: str

    @property
    def url(self) -> str:
        return f"postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class RunConfig(BaseModel):
    host: str
    port: int


class JWTConfig(BaseModel):
    private_key: str = BASE_DIR / 'certs' / 'jwt-private.pem'
    public_key: str = BASE_DIR / 'certs' / 'jwt-public.pem'


class Settings(BaseSettings):
    db: DbConfig
    run: RunConfig
    jwt: JWTConfig = JWTConfig()

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="APP_",  # Опционально, если нужен общий префикс
        env_nested_delimiter="__",  # Для вложенных переменных
    )


settings = Settings()

