import re
from typing import Optional

from pydantic import BaseModel, field_validator, model_validator

from cuztomisable.lang import trans
from cuztomisable.settings import settings


def clean_phone(value: str) -> str:
    # Removes all non-numbers to normalize the phone number
    return re.sub(r"\D", "", str(value))


class PhoneMixin(BaseModel):
    phone: Optional[str] = None
    country_code: Optional[int] = None

    @model_validator(mode="before")
    @classmethod
    def prepare_phone(cls, values):
        if not isinstance(values, dict):
            return values
        if phone := values.get("phone"):
            values["phone"] = clean_phone(phone)
        # Sets the country_code variable with := operator
        if country_code := values.get("country_code"):
            values["country_code"] = int(str(country_code).lstrip("+"))
        elif values.get("phone"):
            values["country_code"] = settings.default_country_code
        return values

    @field_validator("country_code")
    @classmethod
    def validate_country_code(cls, v):
        if v is None:
            return v
        country_codes = getattr(settings, "country_codes", [])
        # Validates the country code against the list within settings
        valid_codes = [row["value"] for row in country_codes if "value" in row]
        if valid_codes and v not in valid_codes:
            raise ValueError(trans("validation.errors.invalid_country_code", code=v))
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v, info):
        if v is None:
            return v
        country_code = info.data.get("country_code")
        country_codes = getattr(settings, "country_codes", [])
        required_length = None
        for row in country_codes:
            if row.get("value") == country_code:
                required_length = row.get("required_length")
                break
        if required_length is not None:
            if len(v) != required_length:
                raise ValueError(trans("validation.errors.invalid_phone_length_for_country", required_length=required_length))
        else:
            if not (6 <= len(v) <= 15):
                raise ValueError(trans("validation.errors.invalid_phone_length"))
        return v
