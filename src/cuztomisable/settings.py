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
        "unique_phone": True,
        # Logs the user in automatically after registration, if verification is not required
        "login_after_registration": True,
        "require_username": False,
        "require_phone": False,
    }

    forgot: dict = {
        "time_between_allowed_resets": 300, # seconds
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