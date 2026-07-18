from passlib.context import CryptContext
import secrets

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return _pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return _pwd_context.verify(plain_password, hashed_password)


def generate_token(
    length: int = 8,
    characters: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
) -> str:
    return ''.join(secrets.choice(characters) for _ in range(length))