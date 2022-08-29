from schema.secrets import UserSecret, SecretKey


def get_user_secret(secret: str, passphrase: str) -> UserSecret:
    return UserSecret(
        secret=secret,
        passphrase=passphrase
    )


def get_secret_key(secret_key: str) -> SecretKey:
    return SecretKey(secret_key=secret_key)
