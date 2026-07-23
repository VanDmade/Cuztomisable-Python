from fastapi import APIRouter

from cuztomisable.schemas.settings import (
    LoginSettingsResponse,
    MFASettingsResponse,
    PublicSettingsResponse,
    RegistrationSettingsResponse,
    ResetPasswordSettingsResponse,
)
from cuztomisable.settings import settings

router = APIRouter(tags=["Settings"])


@router.get("/cuztomisable/settings", response_model=PublicSettingsResponse)
def get_settings():
    return PublicSettingsResponse(
        login=LoginSettingsResponse(
            with_email=settings.login["with"]["email"],
            with_username=settings.login["with"]["username"],
            with_phone=settings.login["with"]["phone"],
            remember=settings.login["remember"],
        ),
        registration=RegistrationSettingsResponse(
            require_username=settings.registration["require_username"],
            require_phone=settings.registration["require_phone"],
        ),
        password_requirements=settings.password_requirements,
        country_codes=settings.country_codes,
        default_country_code=settings.default_country_code,
        default_language=settings.default_language,
        multi_factor_authentication=MFASettingsResponse(
            code_length=settings.multi_factor_authentication["code"]["length"],
            max_attempts=settings.multi_factor_authentication["code"]["max_attempts"],
            resend_timer=settings.multi_factor_authentication["resend_timer"],
            remember_enabled=settings.multi_factor_authentication["remember"],
        ),
        reset_password=ResetPasswordSettingsResponse(
            code_length=settings.reset_password["code"]["length"],
            max_attempts=settings.reset_password["code"]["max_attempts"],
            resend_timer=settings.reset_password["resend_timer"],
        ),
    )
