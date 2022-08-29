import pytest

from database.collections import SecretsCollection


@pytest.fixture
def secrets_collection():
    """Yield `secret` collection and drop it after use."""
    collection = SecretsCollection('test_collection')
    try:
        yield collection
    finally:
        collection.secrets_collection.drop()
