from pydantic import BaseModel


class Secret(BaseModel):
    """User's stored secret."""

    secret: str

    class Config:
        schema_extra = {
            'example': {
                'secret': "Some secret phrase",
            }
        }


class Passphrase(BaseModel):
    """A passphrase that unlocks user's secret."""

    passphrase: str

    class Config:
        schema_extra = {
            'example': {
                'passphrase': "This will unlock the stored secret",
            }
        }


class UserSecret(Secret, Passphrase):
    """
    The model for receiving a secret from a client with
    a passphrase to unlock the given secret.
    """

    class Config:
        schema_extra = {
            'example': {
                'secret': "Some secret phrase",
                'passphrase': "This will return the stored secret"
            }
        }


class SecretKey(BaseModel):
    """
    The secret key that user should specify when want to
    unlock stored secret.
    """

    secret_key: str

    class Config:
        schema_extra = {
            'example': {
                'secret_key': "iKpck5CgbcSJu8C9XdKHra1SWI8AR5hS"
            }
        }
