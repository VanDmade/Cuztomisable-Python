from pydantic_settings import BaseSettings


class CuztomisableSettings(BaseSettings):
    app_domain: str = "localhost"

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
        "remember": False,
    }

    verification: dict = {
        "email": False,
        "phone": False,
    }

    registration: dict = {
        "disabled": {
            "web": False,
            "mobile": False,
        },
        # Logs the user in automatically after registration, if verification is not required
        "login_after_registration": True,
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
