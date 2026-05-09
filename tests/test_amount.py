from src.validators import validate_amount
import pytest

def test_validate_amount_returns_value():
    assert validate_amount(100) == 100


@pytest.mark.parametrize("invalid_amount", [
    -5,
    None,
    0,
])
def test_validate_amount_raises_value_error(invalid_amount):
    with pytest.raises(ValueError):
        validate_amount(invalid_amount)


@pytest.mark.parametrize("invalid_amount", [
     "100",
     [1,2,3],
 ])
def test_validate_amount_raises_type_error(invalid_amount):
    with pytest.raises(TypeError):
        validate_amount(invalid_amount)

