from pydantic_settings import BaseSettings

from cuztomisable.emails import (
    DefaultLayout,
    EmailVerificationEmail,
    MfaCodeEmail,
    NewLoginDetectedEmail,
    NewRegistrationEmail,
    ResetPasswordEmail,
)

CHARACTERS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class CuztomisableSettings(BaseSettings):
    app_domain: str = "localhost"

    mail_from_address: str = "no-reply@localhost"
    mail_from_name: str = "Cuztomisable"
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_use_tls: bool = True

    # "smtp" sends for real. "log" (or leaving smtp_username blank) writes the
    # rendered email to mail_log_path instead — handy for testing without SES set up.
    mail_driver: str = "log"
    mail_log_path: str = "storage/emails"

    email: dict = {
        "sanitize_keys": ["password", "code", "token"],
        "notify_on_new_ip_address": True,
    }

    # Swap any of these out via configure(email_templates={"reset_password": MyTemplate})
    email_templates: dict = {
        "layout": DefaultLayout,
        "reset_password": ResetPasswordEmail,
        "mfa_code": MfaCodeEmail,
        "new_registration": NewRegistrationEmail,
        "email_verification": EmailVerificationEmail,
        "new_login": NewLoginDetectedEmail,
    }

    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 30

    login: dict = {
        "with": {
            "email": True,
            "phone": False,
            "username": True,
        },
        "attempt_timer": 300,
        "max_attempts": 5,
        "lock_on_max_attempts": False,
    }

    reset_password: dict = {
        "with": {
            "email": True,
            "phone": False,
        },
        "code": {
            "length": 6,
            "characters": CHARACTERS,
            "max_attempts": 5,
        },
        "on_change_clear_sessions": True,
        "login_after": False,
        "resend_timer": 60,
        "expires_after": 300,
    }

    multi_factor_authentication: dict = {
        "enabled": True,
        "with": {
            "email": True,
            "phone": True,
        },
        "code": {
            "length": 6,
            "characters": CHARACTERS,
            "regenerate_on_resend": False,
            "max_attempts": 5,
        },
        "resend_timer": 60,
        "expires_after": 300,
        "remember_for_days": 30,
        "remember": True,
    }

    registration: dict = {
        "disabled": {
            "web": False,
            "mobile": False,
        },
        "unique_phone": True,
        # Logs the user in automatically after registration, if verification is not required
        "login_after": True,
        "require_username": False,
        "require_phone": False,
    }

    password_requirements: dict = {
        "min_length": 6,
        "max_length": None,
        "uppercase": 1,
        "digits": 1,
        "special": 1,
    }
    # Password reuse prevention: number of previous passwords to check against
    reuse_password_after: int = 3

    default_language: str = "en"
    default_country_code: int = 1

    mobile: dict = {
        "enabled": True,
        "log_invalid": False,
        "platforms": ["Android", "iOS", "Other"],
        "apps": [],
    }

    country_codes: list[dict] = [
        {"value": 1, "label": "US", "name": "United States / Canada", "required_length": 10},
        {"value": 44, "label": "UK", "name": "United Kingdom", "required_length": 10},
    ]
    model_config = {"env_prefix": "CUZTOMISABLE_"}

    tablelify: dict = {
        "filtered": True,
        "page_details": True,
        "max_size": 100,
        "default": {
            "size": 10,
            "order_by": "id",
            "order_direction": "desc",
        },
    }

    errors: dict = {
        "debug_code": {
            "length": 8,
            "characters": "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        },
        # Leave this list empty to log all errors, or specify a list of HTTP status codes to log only those errors.
        "log_codes": [500, 501, 502, 503, 504],
    }

    def __call__(self, key: str, default=None):
        """Dotted-path lookup, e.g. settings("registration.unique_phone", False)."""
        current = self
        for part in key.split("."):
            if isinstance(current, dict):
                if part not in current:
                    return default
                current = current[part]
            elif hasattr(current, part):
                current = getattr(current, part)
            else:
                return default
        return current


settings = CuztomisableSettings()


def _deep_merge(base: dict, overrides: dict) -> dict:
    merged = dict(base)
    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def configure(**overrides) -> None:
    for key, value in overrides.items():
        if not hasattr(settings, key):
            raise ValueError(f"Unknown cuztomisable setting: '{key}'")
        current = getattr(settings, key)
        # Merge dict settings (at any nesting depth) so overriding one key
        # (e.g. login={"with": {"phone": True}}) doesn't silently drop
        # sibling defaults (e.g. login["with"]["email"]).
        if isinstance(current, dict) and isinstance(value, dict):
            setattr(settings, key, _deep_merge(current, value))
        else:
            setattr(settings, key, value)