from typing import Optional

from pydantic import BaseModel, model_validator


class UserMixin(BaseModel):
    user: Optional[dict] = None


class NullStringMixin(BaseModel):
    @model_validator(mode="before")
    @classmethod
    def convert_null_strings(cls, values):
        if isinstance(values, dict):
            return {k: None if v == "null" else v for k, v in values.items()}
        return values
