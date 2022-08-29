from motor.core import AgnosticDatabase
from motor.motor_asyncio import AsyncIOMotorClient

from config.settings import settings


class MongoDB:
    """The class represents communication with `MongoDB`."""

    def get_database(self, database_name: str) -> AgnosticDatabase:
        """
        Return tests_database which name matches `database_name`
        or create a new one.
        """
        return self.client[database_name]

    def __init__(self, mongodb_location: str = None):
        self.client = AsyncIOMotorClient(mongodb_location or settings.mongo_location)
