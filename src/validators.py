def is_valid_email(email: str) -> bool:
    """Check if email contains @ and is not empty."""
    if not email:
        return False
    if "@" not in email:
        return False
    if "." not in email:
        return False
    if email.count("@") > 1:
        return False
    if email.startswith("@") or email.endswith("@"):
        return False
    return True


def validate_amount(amount: float) -> float:
    """Validate amount is positive number. Raises ValueError if not."""
    if amount is None:
        raise ValueError("Amount cannot be None")
    if not isinstance(amount, (int, float)):
        raise TypeError("Amount must be number")
    if amount <=0:
        raise ValueError("Amount must be positive")
    return amount

def validate_phone_number(phone_number: str) -> str:
    """Validate phone number. Raises ValueError if not."""

    if phone_number is None:
        raise ValueError("Phone cannot be None")
    if not isinstance(phone_number, str):
        raise TypeError("Phone number must be string")

    stripped = phone_number.strip()

    if stripped == "":
        raise ValueError("Phone cannot be empty")
    if len(stripped) < 9:
        raise ValueError("Phone must have at least 9 digits")
    if not stripped.isdigit():
        raise ValueError("Phone cannot contain letters")
    return stripped



