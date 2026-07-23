from typing import Literal, Tuple

_PHONE_STRIP_CHARS = ("/", "_", "-", "(", ")", " ")

LoginType = Literal["email", "phone", "username"]


def detect_login_type(username: str, *, allow_email: bool, allow_phone: bool) -> Tuple[str, LoginType]:
    """Cleans a raw identifier and figures out whether it's an email, phone
    number, or bare username, based on which types the caller allows."""
    raw = username.strip()
    wants_phone = allow_phone and "@" not in raw
    login_type: LoginType = "phone" if wants_phone else ("email" if allow_email else "username")

    if login_type == "phone":
        for char in _PHONE_STRIP_CHARS:
            raw = raw.replace(char, "")
        # Falls back to email if the cleaned value isn't actually a phone number
        if not raw.isdigit():
            login_type = "email"
    elif login_type == "email":
        raw = raw.lower()

    return raw, login_type
