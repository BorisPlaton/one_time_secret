from pydantic import BaseSettings


class ProjectSettings(BaseSettings):
    """Project configuration."""

    host: str = '127.0.0.1'
    port: int = 8000
    mongo_location: str = 'mongodb://127.0.0.1:27017'

    class Config:
        allow_mutation = False


settings = ProjectSettings(
    _env_file='.env',
    _env_file_encoding='utf-8'
)
