from pydantic import BaseModel


class LoginSettingsResponse(BaseModel):
    with_email: bool
    with_phone: bool
    with_username: bool
    remember: bool

class RegistrationSettingsResponse(BaseModel):
    require_username: bool
    require_phone: bool

class MFASettingsResponse(BaseModel):
    code_length: int
    max_attempts: int
    resend_timer: int
    remember_enabled: bool

class ResetPasswordSettingsResponse(BaseModel):
    code_length: int
    max_attempts: int
    resend_timer: int

class PublicSettingsResponse(BaseModel):
    login: LoginSettingsResponse
    registration: RegistrationSettingsResponse
    password_requirements: dict
    country_codes: list[dict]
    default_country_code: int
    default_language: str
    multi_factor_authentication: MFASettingsResponse
    reset_password: ResetPasswordSettingsResponse
