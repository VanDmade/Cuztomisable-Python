import re
from typing import Optional

from pydantic import BaseModel, field_validator, model_validator

from cuztomisable.settings import settings


def clean_phone(value: str) -> str:
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

        if country_code := values.get("country_code"):
            values["country_code"] = int(str(country_code).lstrip("+"))

        return values

    @field_validator("country_code")
    @classmethod
    def validate_country_code(cls, v):
        if v is None:
            return v

        country_codes = getattr(settings, "country_codes", [])
        valid_codes = [row["value"] for row in country_codes if "value" in row]

        if valid_codes and v not in valid_codes:
            raise ValueError(f"Invalid country code: {v}")

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
                raise ValueError(f"Phone must be {required_length} digits for this country code")
        else:
            if not (6 <= len(v) <= 15):
                raise ValueError("Phone must be between 6 and 15 digits")

        return v
