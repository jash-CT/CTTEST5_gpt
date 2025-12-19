from marshmallow import ValidationError


def ensure_positive(value):
    try:
        v = float(value)
    except Exception:
        raise ValidationError("Must be a number")
    if v <= 0:
        raise ValidationError("Must be positive")
    return v
