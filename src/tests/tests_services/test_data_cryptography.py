from base64 import urlsafe_b64encode

import pytest
from cryptography.fernet import Fernet

from config.settings import settings
from services.data_cryptography import get_encrypter, encrypt_data, decrypt_data


def test_get_encrypter_returns_fernet_instance():
    encrypter = get_encrypter()
    assert isinstance(encrypter, Fernet)


def test_encrypter_has_secret_key_from_settings():
    encrypter = get_encrypter()
    encoded_fernet_key = urlsafe_b64encode(encrypter._signing_key + encrypter._encryption_key).decode()
    assert encoded_fernet_key == settings.secret_key


@pytest.mark.parametrize(
    "initial_data",
    [
        "XFARFA",
        "S",
        "",
        "111111111124566",
        "AR--0000000000",
        "dfQKFQ=C01111111",
        "=====================",
        "4190419akfafa9fq9319341",
    ]
)
def test_encrypted_data_doesnt_equal_initial_data(initial_data):
    encrypted_data = encrypt_data(initial_data)
    assert encrypted_data != initial_data


@pytest.mark.parametrize(
    "initial_data",
    [
        "XFARFA",
        "S",
        "",
        "111111111124566",
        "AR--0000000000",
        "dfQKFQ=C01111111",
        "=====================",
        "4190419akfafa9fq9319341",
    ]
)
def test_decrypted_data_equals_initial(initial_data):
    encrypted_data = encrypt_data(initial_data)
    assert encrypted_data != initial_data
    decrypted_data = decrypt_data(encrypted_data)
    assert initial_data == decrypted_data
