from typing import NamedTuple

from schema.secrets import UserSecret
from cryptography.fernet import Fernet

from services.errors import DecryptionError


class EncryptedUserSecret(NamedTuple):
    secret: str
    passphrase: str


def get_secret_key() -> str:
    """Generates a unique secret key."""
    return Fernet.generate_key().decode()


def encrypt_user_secret(user_secret: UserSecret, secret_key: str) -> EncryptedUserSecret:
    """
    Encrypts the user secret and the passphrase via secret_key.
    """
    encrypted_secret, encrypted_passphrase = (
        encrypt_data(user_secret.secret, secret_key),
        encrypt_data(user_secret.passphrase, secret_key)
    )
    return EncryptedUserSecret(
        secret=encrypted_secret,
        passphrase=encrypted_passphrase
    )


def decrypt_data(encrypted_data: str, secret_key: str) -> str:
    """
    Decrypts the `encrypted_data`. If it is impossible raises an
    error.
    """
    cryptographer = Fernet(secret_key)
    try:
        decrypted_value = cryptographer.decrypt(encrypted_data.encode())
        return decrypted_value.decode()
    except ValueError:
        raise DecryptionError


def encrypt_data(data: str, secret_key: str) -> str:
    """
    Encrypts the `data` with `secret_key` and returns an
    encrypted value.
    """
    cryptographer = Fernet(secret_key)
    return cryptographer.encrypt(data.encode()).decode()
