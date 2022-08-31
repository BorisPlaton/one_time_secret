from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException
from starlette import status

from database.collections import SecretsCollection
from services.data_cryptography import decrypt_data


def get_object_id_or_404(secret_key: str | bytes) -> ObjectId:
    """Returns an `ObjectId` instance or raises a 404 Http error."""
    try:
        object_id_instance = ObjectId(secret_key)
    except InvalidId:
        raise HTTPException(detail="Invalid secret key.", status_code=status.HTTP_404_NOT_FOUND)
    return object_id_instance


async def get_decrypted_secret_and_delete_from_db(passphrase: str, secret_key: str) -> str:
    """Decrypts user stored secret and deletes from the database."""
    secrets_collection = SecretsCollection()
    secret_filter = {"_id": get_object_id_or_404(secret_key)}
    secret_data = await secrets_collection.get_secret(secret_filter)
    if not secret_data:
        raise HTTPException(detail="Invalid secret key.", status_code=status.HTTP_404_NOT_FOUND)
    if decrypt_data(secret_data['passphrase']) != passphrase:
        raise HTTPException(detail="Wrong passphrase.", status_code=status.HTTP_400_BAD_REQUEST)
    decrypted_secret = decrypt_data(secret_data['secret'])
    await secrets_collection.delete(secret_filter)
    return decrypted_secret
