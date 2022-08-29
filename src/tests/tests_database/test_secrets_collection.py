import pytest

from tests.tests_database.utils import get_user_secret, get_secret_key


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "secret, passphrase, secret_key",
    [
        ("some secret", "it will work", "1234dafar2"),
        ("some secret2", "1", "123fafas4"),
        ("415dae315", "-", "1234232"),
        ("-", "it__________", "12345"),
        ("1", "3", "1234"),
    ]
)
async def test_add_secret_to_collection(secrets_collection, secret, passphrase, secret_key):
    user_secret = get_user_secret(secret, passphrase)
    secret_key_instance = get_secret_key(secret_key)
    assert not await secrets_collection.secrets_collection.find().to_list(None)
    await secrets_collection.add_secret(user_secret, secret_key_instance)
    assert len(await secrets_collection.secrets_collection.find().to_list(None)) == 1
    user_secret_with_secret_key = await secrets_collection.secrets_collection.find_one({"secret": secret})
    assert user_secret_with_secret_key
    assert isinstance(user_secret_with_secret_key, dict)


@pytest.mark.asyncio
async def test_get_all_secrets_in_db(secrets_collection):
    secrets_data = [
        ("some secret", "it will work", "1234dafar2"),
        ("some secret2", "1", "123fafas4"),
        ("415dae315", "-", "1234232"),
        ("-", "it__________", "12345"),
        ("1", "3", "1234"),
    ]
    for secret, passphrase, secret_key in secrets_data:
        await secrets_collection.add_secret(
            get_user_secret(secret, passphrase), get_secret_key(secret_key)
        )
    assert len(await secrets_collection.get_secrets()) == len(secrets_data)
    for secret, passphrase, secret_key in secrets_data:
        user_secret_db = await secrets_collection.secrets_collection.find_one({'secret_key': secret_key})
        assert user_secret_db
        assert user_secret_db['secret'] == secret
        assert user_secret_db['passphrase'] == passphrase


@pytest.mark.asyncio
async def test_get_all_secrets_in_db_with_filter(secrets_collection):
    secrets_data = [
        ("some secret", "it will work", "1234dafar2"),
        ("some secret2", "1", "123fafas4"),
        ("415dae315", "-", "1234232"),
        ("-", "it__________", "12345"),
        ("1", "3", "1234"),
    ]
    for secret, passphrase, secret_key in secrets_data:
        await secrets_collection.add_secret(
            get_user_secret(secret, passphrase), get_secret_key(secret_key)
        )
    secrets_with_filter = await secrets_collection.get_secrets({"secret": "some secret"})
    assert len(secrets_with_filter) == 1
    assert isinstance(secrets_with_filter, list)
    secrets_with_filter = await secrets_collection.get_secrets(
        {
            "secret": {"$regex": "^some *"}
        }
    )
    assert len(secrets_with_filter) == 2
    assert isinstance(secrets_with_filter, list)


@pytest.mark.asyncio
async def test_get_secret_from_collection_with_filters(secrets_collection):
    secrets_data = [
        ("some secret", "it will work", "1234dafar2"),
        ("some secret2", "1", "123fafas4"),
        ("415dae315", "-", "1234232"),
        ("-", "it__________", "12345"),
        ("1", "3", "1234"),
    ]
    for secret, passphrase, secret_key in secrets_data:
        await secrets_collection.add_secret(
            get_user_secret(secret, passphrase), get_secret_key(secret_key)
        )
    secrets_with_filter = await secrets_collection.get_secret({"secret": "some secret"})
    assert secrets_with_filter
    assert isinstance(secrets_with_filter, dict)


@pytest.mark.asyncio
async def test_get_secret_from_collection_without_filters(secrets_collection):
    secrets_data = [
        ("some secret", "it will work", "1234dafar2"),
        ("some secret2", "1", "123fafas4"),
        ("415dae315", "-", "1234232"),
        ("-", "it__________", "12345"),
        ("1", "3", "1234"),
    ]
    for secret, passphrase, secret_key in secrets_data:
        await secrets_collection.add_secret(
            get_user_secret(secret, passphrase), get_secret_key(secret_key)
        )
    secrets_without_filter = await secrets_collection.get_secret()
    secrets_list = await secrets_collection.get_secrets()
    assert secrets_without_filter == secrets_list[0]
