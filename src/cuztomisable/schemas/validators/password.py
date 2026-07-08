from typing import Optional

from pydantic import BaseModel, field_validator, model_validator

from cuztomisable.lang import trans
from cuztomisable.settings import settings


class PasswordMixin(BaseModel):
    password: Optional[str] = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, password):
        if password is None:
            return password
        # Validate password against the requirements defined in settings
        if requirements := getattr(
            settings,
            "password_requirements",
            {"min_length": 6}
        ):
            min_length = requirements.get("min_length") or 6
            # Prevents min length from being set less than 6
            if min_length < 6:
                min_length = 6
            max_length = requirements.get("max_length") or 72
            # Prevents max lenght from being set more than BCRYPT can handle (72)
            if (max_length is not None and max_length > 72) or max_length is None:
                max_length = 72
            uppercase = requirements.get("uppercase") or None
            digits = requirements.get("digits") or None
            special = requirements.get("special") or None
            if min_length and len(password) < min_length:
                raise ValueError(trans("validation.errors.password_too_short", min_length=min_length))
            if max_length and len(password) > max_length:
                raise ValueError(trans("validation.errors.password_too_long", max_length=max_length))
            if uppercase and sum(1 for c in password if c.isupper()) < uppercase:
                raise ValueError(trans("validation.errors.password_missing_uppercase", uppercase=uppercase))
            if digits and sum(1 for c in password if c.isdigit()) < digits:
                raise ValueError(trans("validation.errors.password_missing_digits", digits=digits))
            if special and sum(1 for c in password if not c.isalnum()) < special:
                raise ValueError(trans("validation.errors.password_missing_special", special=special))
        # Add password validation logic here if needed
        return password
