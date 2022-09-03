import pytest


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
    assert not await secrets_collection.collection.find().to_list(None)
    await secrets_collection.add_secret(secret, passphrase)
    assert len(await secrets_collection.collection.find().to_list(None)) == 1
    user_secret_with_secret_key = await secrets_collection.collection.find_one({"secret": secret})
    assert user_secret_with_secret_key
    assert isinstance(user_secret_with_secret_key, dict)


@pytest.mark.asyncio
async def test_add_secret_with_additional_keywords(secrets_collection):
    await secrets_collection.add_secret('1', '2', some_field='345')
    assert await secrets_collection.get_secret({'some_field': '345'})
    assert await secrets_collection.get_secret({'secret': '1'})
    assert await secrets_collection.get_secret({'passphrase': '2'})


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
        await secrets_collection.add_secret(secret, passphrase)
    assert len(await secrets_collection.get_secrets()) == len(secrets_data)
    for secret, passphrase, secret_key in secrets_data:
        user_secret_db = await secrets_collection.collection.find_one({'secret': secret})
        assert user_secret_db
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
        await secrets_collection.add_secret(secret, passphrase)
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
        await secrets_collection.add_secret(secret, passphrase)
    secrets_with_filter = await secrets_collection.get_secret({"secret": "some secret"})
    assert secrets_with_filter
    assert isinstance(secrets_with_filter, dict)


@pytest.mark.asyncio
async def test_get_secret_from_collection_without_filters(secrets_collection):
    secrets_data = [
        ("some secret", "it will work"),
        ("some secret2", "1"),
        ("415dae315", "-"),
        ("-", "it__________"),
        ("1", "3"),
    ]
    for secret, passphrase in secrets_data:
        await secrets_collection.add_secret(secret, passphrase)
    secrets_without_filter = await secrets_collection.get_secret()
    secrets_list = await secrets_collection.get_secrets()
    assert secrets_without_filter == secrets_list[0]


@pytest.mark.asyncio
async def test_delete_secret_with_filters(secrets_collection):
    assert not len(await secrets_collection.get_secrets())
    secrets_data = [
        ("some secret", "it will work"),
        ("some secret2", "1"),
    ]
    for secret, passphrase in secrets_data:
        await secrets_collection.add_secret(secret, passphrase)
    assert len(await secrets_collection.get_secrets()) == 2
    await secrets_collection.delete({"secret": {"$regex": "some *"}})
    assert len(await secrets_collection.get_secrets()) == 1


@pytest.mark.asyncio
async def test_default_ttl_index_name(secrets_collection):
    indexes_keys = []
    await secrets_collection.create_ttl_index_on()
    indexes_data: dict = await secrets_collection.collection.index_information()
    for index_data in indexes_data.values():
        indexes_keys.append(index_data['key'][0][0])
    assert 'created' in indexes_keys


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'index_field',
    (
        'ffaf',
        'f',
        'for field',
        'dqarq',
        '31z',
        's3141s',
    )
)
async def test_specified_ttl_index_name(secrets_collection, index_field):
    indexes_keys = []
    await secrets_collection.create_ttl_index_on(index_field)
    indexes_data: dict = await secrets_collection.collection.index_information()
    for index_data in indexes_data.values():
        indexes_keys.append(index_data['key'][0][0])
    assert index_field in indexes_keys
