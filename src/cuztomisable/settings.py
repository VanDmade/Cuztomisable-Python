from pydantic_settings import BaseSettings


class CuztomisableSettings(BaseSettings):
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 30

    default_language: str = "en"
    default_country_code: int = 1

    mobile_agent_enabled: bool = True
    mobile_agent_log_invalid: bool = False
    mobile_agent_platforms: list[str] = ["Android", "iOS", "Other"]
    mobile_agent_apps: list[dict] = []

    country_codes: list[dict] = [
        {"value": 1, "label": "United States / Canada", "required_length": 10},
        {"value": 44, "label": "United Kingdom", "required_length": 10},
    ]
    model_config = {"env_prefix": "CUZTOMISABLE_"}


settings = CuztomisableSettings()


def configure(**overrides) -> None:
    for key, value in overrides.items():
        if not hasattr(settings, key):
            raise ValueError(f"Unknown cuztomisable setting: '{key}'")
        setattr(settings, key, value)
