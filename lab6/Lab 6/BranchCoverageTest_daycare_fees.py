
import pytest
from daycare_fees import (
    extra_hours_fee,
    enrolment_allowed,
    pickup_status
)


# Extra hours fee - branch tests

def test_invalid_age_group():
    with pytest.raises(ValueError):
        extra_hours_fee("school", 30, False)


def test_valid_age_group():
    assert extra_hours_fee("infant", 20, False) == 0


def test_invalid_hours():
    with pytest.raises(ValueError):
        extra_hours_fee("toddler", -1, False)


def test_valid_hours():
    assert extra_hours_fee("toddler", 30, False) == 45


def test_sibling_discount_applied():
    assert extra_hours_fee("toddler", 31, True) == 9


def test_sibling_discount_not_applied():
    assert extra_hours_fee("toddler", 26, False) == 9


def test_infant_sibling_discount_not_applied():
    assert extra_hours_fee("infant", 21, True) == 14


def test_no_extra_hours():
    assert extra_hours_fee("toddler", 25, False) == 0


def test_infant_rate():
    assert extra_hours_fee("infant", 21, False) == 14


def test_non_infant_rate():
    assert extra_hours_fee("preschool", 31, False) == 9


def test_extra_hours_above_twenty_infant():
    assert extra_hours_fee("infant", 41, False) == 462


def test_extra_hours_above_twenty_non_infant():
    assert extra_hours_fee("toddler", 46, False) == 294


def test_extra_hours_at_twenty():
    assert extra_hours_fee("toddler", 45, False) == 180


# Enrolment - branch tests

def test_pending_immunisation_age_12():
    assert enrolment_allowed(12, 0, True) is True


def test_pending_immunisation_below_12():
    assert enrolment_allowed(11, 5, True) is False


def test_no_pending_immunisation_under_six():
    assert enrolment_allowed(5, 2, False) is False


def test_no_pending_immunisation_age_six():
    assert enrolment_allowed(6, 1, False) is True


def test_no_vacancies():
    assert enrolment_allowed(24, 0, False) is False


def test_vacancies_available():
    assert enrolment_allowed(24, 3, False) is True


# Pickup status - branch tests

@pytest.mark.parametrize(
    "minutes, aftercare, friday, expected",
    [
        (10, False, False, "on_time"),
        (9, False, False, "late"),
        (-5, False, False, "late"),
        (-6, False, False, "overdue"),

        (20, True, False, "on_time"),
        (5, True, False, "late"),
        (4, True, False, "overdue"),

        (20, False, True, "on_time"),
        (5, False, True, "late"),
        (4, False, True, "overdue"),

        (30, True, True, "on_time"),
        (15, True, True, "late"),
        (14, True, True, "overdue"),
    ]
)
def test_pickup_status_branches(minutes, aftercare, friday, expected):
    assert pickup_status(minutes, aftercare, friday) == expected
