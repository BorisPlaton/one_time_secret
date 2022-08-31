from typing import NamedTuple

from cryptography.fernet import Fernet

from config.settings import settings
from services.errors import DecryptionError


class EncryptedUserSecret(NamedTuple):
    secret: str
    passphrase: str


def get_encoder() -> Fernet:
    """Returns the instance of `Fernet` class."""
    return Fernet(settings.secret_key)


def encrypt_user_secret(secret: str, passphrase: str) -> EncryptedUserSecret:
    """
    Encrypts the user secret and the passphrase via secret_key.
    """
    encrypted_secret, encrypted_passphrase = (
        encrypt_data(secret),
        encrypt_data(passphrase)
    )
    return EncryptedUserSecret(
        secret=encrypted_secret,
        passphrase=encrypted_passphrase
    )


def decrypt_data(encrypted_data: str):
    """
    Decrypts the `encrypted_data`. If it is impossible raises an
    error.
    """
    try:
        decrypted_value = get_encoder().decrypt(encrypted_data.encode())
        return decrypted_value.decode()
    except ValueError:
        raise DecryptionError


def encrypt_data(data: str) -> str:
    """
    Encrypts the `data` with `secret_key` and returns an
    encrypted value.
    """
    return get_encoder().encrypt(data.encode()).decode()
