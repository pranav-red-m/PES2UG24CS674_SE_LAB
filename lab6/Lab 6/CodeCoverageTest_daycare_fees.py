
import pytest
from daycare_fees import (
    extra_hours_fee,
    enrolment_allowed,
    pickup_status
)


# Extra hours fee tests

def test_unknown_age_group():
    with pytest.raises(ValueError):
        extra_hours_fee("school", 30, False)


def test_negative_hours():
    with pytest.raises(ValueError):
        extra_hours_fee("toddler", -5, False)


def test_within_included_hours():
    assert extra_hours_fee("toddler", 20, False) == 0


def test_sibling_discount():
    assert extra_hours_fee("toddler", 26, True) == 0


def test_infant_extra_hours():
    assert extra_hours_fee("infant", 21, False) == 14


def test_infant_large_extra_hours():
    assert extra_hours_fee("infant", 41, False) == 462


def test_toddler_extra_hours():
    assert extra_hours_fee("toddler", 26, False) == 9


def test_toddler_large_extra_hours():
    assert extra_hours_fee("toddler", 51, False) == 364


def test_preschool_extra_hours():
    assert extra_hours_fee("preschool", 31, False) == 9


# Enrolment tests

def test_enrolment_allowed_with_pending_immunisation():
    assert enrolment_allowed(24, 2, True) is True


def test_enrolment_rejected_with_pending_immunisation():
    assert enrolment_allowed(10, 2, True) is False


def test_enrolment_rejected_under_six_months():
    assert enrolment_allowed(5, 2, False) is False


def test_enrolment_allowed_with_vacancy():
    assert enrolment_allowed(12, 1, False) is True


# Pickup status tests

def test_pickup_on_time():
    assert pickup_status(10, False, False) == "on_time"


def test_pickup_late():
    assert pickup_status(5, False, False) == "late"


def test_pickup_overdue():
    assert pickup_status(-6, False, False) == "overdue"


def test_aftercare_pickup():
    assert pickup_status(20, True, False) == "on_time"


def test_friday_pickup():
    assert pickup_status(20, False, True) == "on_time"
