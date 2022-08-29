from motor.core import AgnosticCollection

from database.db import MongoDB
from schema.secrets import UserSecret, SecretKey


class SecretsCollection:
    """
    The class represents a `secrets` collection and provides
    operations to communicate with it.
    """

    async def get_secrets(self, filters: dict = None) -> list[dict]:
        """
        Return all students in db. If a `filters` parameter
        provided will use it to filter data.
        """
        secrets_list = await self.secrets_collection.find(filters).to_list(None)
        return secrets_list

    async def get_secret(self, filters: dict = None) -> dict:
        """
        Return a specific secret that matches given filters.
        """
        return await self.secrets_collection.find_one(filters)

    async def add_secret(self, secret: UserSecret, secret_key: SecretKey):
        """
        Store the `secret` with given `secret_key`.
        """
        secret_dict = secret.dict()
        secret_dict.update(secret_key.dict())
        return await self.secrets_collection.insert_one(secret_dict)

    def __init__(self, collection_name='secrets'):
        self.secrets_collection: AgnosticCollection = (
            MongoDB()
            .get_database('one_time_secret')
            .get_collection(collection_name)
        )
