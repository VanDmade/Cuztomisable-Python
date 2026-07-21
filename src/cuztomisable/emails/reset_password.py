from .base import EmailTemplate


class ResetPasswordEmail(EmailTemplate):
    def subject(self, **context) -> str:
        return "Reset your password"

    def body_html(self, *, link: str, code: str, **context) -> str:
        return f"""
        <p>We received a request to reset your password.</p>
        <p style="text-align:center;margin:24px 0;">
            <a href="{link}" style="background-color:#111827;color:#ffffff;padding:12px 24px;border-radius:6px;text-decoration:none;display:inline-block;">Reset Password</a>
        </p>
        <p>Or enter this code: <strong>{code}</strong></p>
        <p>If you didn't request this, you can safely ignore this email.</p>
        """

    def body_text(self, *, link: str, code: str, **context) -> str:
        return (
            "We received a request to reset your password.\n\n"
            f"Reset link: {link}\n"
            f"Code: {code}\n\n"
            "If you didn't request this, you can safely ignore this email."
        )
