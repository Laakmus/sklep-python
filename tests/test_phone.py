from src.validators import validate_phone_number
import pytest


@pytest.mark.parametrize("phone_number", [
    None,
    "",
    "          ",
    "26234123",
    "23423423g",
])
def test_validate_phone_raises_value_error(phone_number):
    with pytest.raises(ValueError):
        validate_phone_number(phone_number)

@pytest.mark.parametrize("phone_number", [
    789225888,
])
def test_validate_phone_raises_type_error(phone_number):
    with pytest.raises(TypeError):
        validate_phone_number(phone_number)

def test_validate_phone_returns_value():
    assert validate_phone_number(" 789225888 ") == "789225888"