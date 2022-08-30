from motor.core import AgnosticCollection

from database.db import MongoDB


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
        secrets_list = await self.collection.find(filters).to_list(None)
        return secrets_list

    async def get_secret(self, filters: dict = None) -> dict:
        """
        Return a specific secret that matches given filters.
        """
        return await self.collection.find_one(filters)

    async def add_secret(self, secret: str, passphrase: str, secret_key: str, **kwargs):
        """
        Store the `secret` with given `secret_key`.
        """
        secret_dict = {
            "secret": secret,
            "passphrase": passphrase,
            "secret_key": secret_key,
            **kwargs
        }
        return await self.collection.insert_one(secret_dict)

    @property
    def collection(self) -> AgnosticCollection:
        """
        Returns the `secrets` collection if some operations
        must be performed.
        """
        return self._secrets_collection

    def __init__(self, collection_name='secrets'):
        self._secrets_collection: AgnosticCollection = (
            MongoDB()
            .get_database('one_time_secret')
            .get_collection(collection_name)
        )
