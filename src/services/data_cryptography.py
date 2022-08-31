from typing import NamedTuple

from cryptography.fernet import Fernet

from config.settings import settings


class EncryptedUserSecret(NamedTuple):
    secret: str
    passphrase: str


def get_encrypter() -> Fernet:
    """Returns the instance of `Fernet` class."""
    return Fernet(settings.secret_key)


def decrypt_data(encrypted_data: str):
    """
    Decrypts the `encrypted_data`. If it is impossible raises an
    error.
    """
    decrypted_value = get_encrypter().decrypt(encrypted_data.encode())
    return decrypted_value.decode()


def encrypt_data(data: str) -> str:
    """
    Encrypts the `data` with `secret_key` and returns an
    encrypted value.
    """
    return get_encrypter().encrypt(data.encode()).decode()
