from pydantic import BaseSettings


class ProjectSettings(BaseSettings):
    """Project configuration."""

    host: str = '127.0.0.1'
    port: int = 8000

    class Config:
        allow_mutation = False


settings = ProjectSettings(
    _env_file='.env',
    _env_file_encoding='utf-8'
)
