import datetime

import pytest

from schema.secrets import TimeToLive


def test_at_least_one_value_provided():
    with pytest.raises(ValueError) as e:
        TimeToLive()


@pytest.mark.parametrize(
    'month_quantity',
    [
        1,
        2,
        3,
        4,
    ]
)
def test_one_month_to_days_converting(month_quantity):
    assert TimeToLive(months=month_quantity).convert_month_to_days() == month_quantity * 30


@pytest.mark.parametrize(
    'months, days',
    [
        (1, 2),
        (1, 55),
        (0, 31),
        (2, 2),
        (4, 7),
    ]
)
def test_expiration_time(months, days):
    assert (
            TimeToLive(months=months, days=days).get_expiration_time().replace(second=0, microsecond=0) ==
            (datetime.datetime.utcnow() + datetime.timedelta(days=months * 30 + days)).replace(second=0, microsecond=0)
    )
