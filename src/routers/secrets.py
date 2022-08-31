from fastapi import APIRouter, Path
from starlette import status

from schema.secrets import Secret, UserSecret, Passphrase, SecretKey

from services.operations import (
    get_decrypted_secret_and_delete_from_db,
    encrypt_user_secret_and_add_to_db
)


router = APIRouter(
    tags=['Secrets'],

)


@router.post(
    '/generate',
    summary="Receives a secret and returns a secret key.",
    status_code=status.HTTP_201_CREATED,
    response_model=SecretKey,
    responses={
        "201": {
            "description": "Secret has been stored."
        }
    }
)
async def generate_secret_key(user_secret: UserSecret):
    """
    In the request body a client sends a `json` which must have
    two keys:
    - **secret** - A secret that will be stored
    - **passphrase** - A passphrase that in future can unlock the secret
    Client will receive a `json` with a **secret_key**.
    """
    added_secret_id = await encrypt_user_secret_and_add_to_db(user_secret.secret, user_secret.passphrase)
    return SecretKey(secret_key=added_secret_id)


@router.post(
    '/secrets/{secret_key}',
    summary="Return user secret.",
    response_model=Secret,
    responses={
        "200": {
            "description": "User receives the secret."
        },
        "400": {
            "description": "Invalid passphrase provided.",
            "content": {
                "application/json": {
                    "example": {"detail": "Wrong passphrase."}
                }
            }
        },
        "404": {
            "description": "Invalid secret key provided.",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid secret key."}
                }
            }
        },
    }
)
async def get_user_secret(
        passphrase: Passphrase,
        secret_key: str = Path(
            ..., example="630f871784705aa71edcf1d8"
        ),
):
    """
    User has to specify in path a **secret_key** which was given when
    the user sent a **secret** with a **passphrase**.
    In the request body a client sends a `json` with **passphrase**.

    - **secret_key** - A path parameter that user got when he
    had stored a secret
    - **passphrase** - A passphrase that unlocks user's secret

    If all credentials are correct the service will return a user's
    secret and deletes it from the tests_database.
    """
    user_secret = await get_decrypted_secret_and_delete_from_db(passphrase.passphrase, secret_key)
    return Secret(secret=user_secret)
