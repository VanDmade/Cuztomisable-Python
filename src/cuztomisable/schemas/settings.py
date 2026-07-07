from pydantic import BaseModel


class LoginSettingsResponse(BaseModel):
    with_email: bool
    with_phone: bool
    remember: bool


class RegistrationSettingsResponse(BaseModel):
    require_username: bool
    require_phone: bool


class PublicSettingsResponse(BaseModel):
    login: LoginSettingsResponse
    registration: RegistrationSettingsResponse
    password_requirements: dict
    country_codes: list[dict]
    default_country_code: int
    default_language: str
