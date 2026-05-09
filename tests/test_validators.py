from src.validators import is_valid_email
import pytest


@pytest.mark.parametrize("email, expected", [
    ("anna@test.com", True),
    ("", False),
    ("not_an_email", False),
    ("anna@testcom", False),
    ("anna@@test.com", False),
    ("@annatest.com", False),
    ("annatest.com@", False),
    ("  ", False)
])
def test_is_valid_email(email, expected):
    assert is_valid_email(email) == expected