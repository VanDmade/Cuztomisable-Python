from contextvars import ContextVar
from typing import Optional

from cuztomisable.settings import settings

current_locale: ContextVar[str] = ContextVar("current_locale", default="en")


def trans(key: str, **kwargs) -> str:
    """
    Translate a key.

    Format: "file.key" or "file.nested.key" or just "key" (defaults to global file).
    Example: trans("global.errors.unauthorized") or trans("errors.unauthorized")

    Supports variable substitution:
    Example: trans("global.welcome", name="Michael")
    """
    locale = current_locale.get()
    if "." in key:
        file_name, lookup_key = key.split(".", 1)
    else:
        file_name = "global"
        lookup_key = key
    translation = _lookup(locale, file_name, lookup_key)
    if translation is None and locale != settings.default_language:
        translation = _lookup(settings.default_language, file_name, lookup_key)
    if translation is None and locale != "en":
        translation = _lookup("en", file_name, lookup_key)
    if translation is None:
        return key
    return translation.format(**kwargs) if kwargs else translation


def _lookup(locale: str, file_name: str, key: str) -> Optional[str]:
    try:
        module = __import__(
            f"cuztomisable.lang.{locale}.{file_name}",
            fromlist=["translations"],
        )
        data = getattr(module, "translations", {})
        for part in key.split("."):
            if not isinstance(data, dict):
                return None
            data = data.get(part)
            if data is None:
                return None
        return data if isinstance(data, str) else None
    except ImportError:
        return None
