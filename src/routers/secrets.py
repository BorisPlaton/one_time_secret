from fastapi import APIRouter, Path
from starlette import status

from schema.secrets import Secret, UserSecret, Passphrase


router = APIRouter(
    tags=['Secrets'],

)


@router.post(
    '/generate',
    summary="Receives a secret and returns a secret key.",
    status_code=status.HTTP_201_CREATED,
    response_model=UserSecret,
    responses={
        "201": {
            "description": "Secret has been stored."
        }
    }
)
async def generate_secret_key(secret: UserSecret):
    """
    In the request body a client sends a `json` which must have
    two keys:
    - **secret** - A secret that will be stored
    - **passphrase** - A passphrase that in future can unlock the secret
    Client will receive a `json` with **secret_key**.
    """


@router.get(
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
                    "example": {"detail": "`Wrong passphrase` isn't the correct passphrase."}
                }
            }
        },
        "404": {
            "description": "Secret key isn't correct.",
            "content": {
                "application/json": {
                    "example": {"detail": "`Wrong secret key` isn't the correct secret key."}
                }
            }
        }
    }
)
async def get_user_secret(
        passphrase: Passphrase,
        secret_key: str = Path(
            ..., example="iKpck5CgbcSJu8C9XdKHra1SWI8AR5hS"
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
    secret and deletes it from the database.
    """
