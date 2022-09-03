import os

from cryptography.fernet import Fernet
from pydantic import BaseSettings


class ProjectSettings(BaseSettings):
    """Project configuration."""

    host: str = '127.0.0.1'
    port: int = 8000
    secret_key: str = Fernet.generate_key()
    development: bool = os.getenv('DEVELOPMENT') == '1'

    mongo_location: str = 'mongodb://127.0.0.1:27017'

    class Config:
        allow_mutation = False


settings: ProjectSettings = ProjectSettings(
    _env_file='.env',
    _env_file_encoding='utf-8'
)
