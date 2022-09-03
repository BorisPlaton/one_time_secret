import datetime

from pydantic import BaseModel, root_validator


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
            'examples': {
                "With time to live": {
                    'secret': "Some secret phrase",
                    'passphrase': "This will return the stored secret",
                    'time_to_live': {
                        'months': 4,
                        'days': 2,
                        'seconds': 34,
                    },
                },
                "Plain secret": {
                    'secret': "Some secret phrase",
                    'passphrase': "This will return the stored secret",
                }
            }
        }


class TimeToLive(BaseModel):
    """
    Represents a time range during which the secret will exist
    in the database.
    """

    months: int | None
    days: int | None
    hours: int | None
    minutes: int | None
    seconds: int | None

    @root_validator
    def check_at_least_one_value_provided(cls, values: dict):
        """Checks that user has provided at least one value."""
        provided_values = [value for value in values.values() if value]
        if not provided_values:
            raise ValueError("You have to specify at least one value in the `time_to_live` option.")
        return values

    def convert_month_to_days(self) -> int:
        """
        Converts months amount to days. If months is not provided
        returns 0.
        """
        return self.months * 30 if self.months else 0

    def get_expiration_time(self) -> datetime.datetime:
        """
        Returns a `datetime.datetime` object that specifies
        the time when an item should be deleted.
        """
        provided_values = {key: value for key, value in self.dict().items() if value and key != 'months'}
        provided_values.update({'days': provided_values.get('days', 0) + self.convert_month_to_days()})
        print(provided_values)

        return datetime.datetime.utcnow() + datetime.timedelta(**provided_values)


class UserSecret(BaseModel):
    """
    The model for receiving a secret from a client with
    a passphrase to unlock the given secret.
    """

    secret: str
    passphrase: str
    time_to_live: TimeToLive | None

    class Config:
        schema_extra = {
            "example": {
                'secret': "Some secret phrase",
                'passphrase': "This will return the stored secret",
                'time_to_live': {
                    'months': 4,
                    'days': 2,
                    'hours': 4,
                    'minutes': 4,
                    'seconds': 34,
                }
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
                'secret_key': "630f871784705aa71edcf1d8"
            }
        }
