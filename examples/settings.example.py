"""
Example: Overriding cuztomisable settings in your app.

Call configure() once at startup before init_app(). Settings can also be set
via environment variables with the CUZTOMISABLE_ prefix — env vars are loaded
first, then configure() overrides them if called.

Environment variable equivalents are shown in the comments below.
"""

from fastapi import FastAPI

from cuztomisable import Cuztomisable
from cuztomisable.config import CuztomisableConfig
from cuztomisable.settings import configure

configure(
    # Tokens
    # env: CUZTOMISABLE_JWT_SECRET
    jwt_secret="super-secret-key-change-in-production",

    # env: CUZTOMISABLE_ACCESS_TOKEN_EXPIRE_MINUTES
    access_token_expire_minutes=60,

    # env: CUZTOMISABLE_REFRESH_TOKEN_EXPIRE_DAYS
    refresh_token_expire_days=30,

    # Localisation
    # env: CUZTOMISABLE_DEFAULT_LANGUAGE
    default_language="en",

    # env: CUZTOMISABLE_DEFAULT_COUNTRY_CODE
    default_country_code=1,

    # Login behavior
    # env: CUZTOMISABLE_LOGIN (JSON object)
    login={
        "with": {"email": True, "phone": False},
        "remember": False,
    },

    # Which fields registration requires
    # env: CUZTOMISABLE_REGISTRATION (JSON object)
    registration={
        "require_username": False,
        "require_phone": False,
    },

    # Password strength rules, enforced server-side regardless of max_length —
    # bcrypt itself hard-caps input at 72 bytes.
    # env: CUZTOMISABLE_PASSWORD_REQUIREMENTS (JSON object)
    password_requirements={
        "min_length": 6,
        "max_length": None,
        "uppercase": 1,
        "digits": 1,
        "special": 1,
    },

    # Number of previous passwords to check against on password change/reset
    # env: CUZTOMISABLE_REUSE_PASSWORD_AFTER
    reuse_password_after=3,

    # Mobile agent validation
    # env: CUZTOMISABLE_MOBILE (JSON object)
    mobile={
        "enabled": True,
        "log_invalid": True,
        # Allowed platforms in the User-Agent string
        "platforms": ["Android", "iOS"],
        # Each app entry is matched against the User-Agent.
        # Pattern: "AppName/vX.Y.Z (Platform)"
        # min_version triggers a 426 Upgrade Required if the client is below it.
        "apps": [
            {"name": "MyApp", "min_version": "2.0.0"},
            {"name": "MyApp-Beta", "min_version": "1.0.0"},
        ],
    },
)

app = FastAPI()

cuzt = Cuztomisable(
    app,
    config=CuztomisableConfig(
        cors_origins=["https://myapp.com"],
        cors_allow_credentials=True,
        cors_allow_methods=["*"],
        cors_allow_headers=["*"],
    ),
)
