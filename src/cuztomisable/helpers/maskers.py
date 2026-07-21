def mask_email(email: str) -> str:
    local, _, domain = email.partition("@")
    if len(local) <= 2:
        return f"{'*' * 4}@{domain}"
    return f"{local[0]}{'*' * 4}{local[-1]}@{domain}"


def mask_phone(phone: str) -> str:
    if len(phone) <= 4:
        return "*" * 6
    return f"{phone[0]}{'*' * 6}{phone[-4:]}"
