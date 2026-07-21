from .base import EmailTemplate


class EmailVerificationEmail(EmailTemplate):
    def subject(self, **context) -> str:
        return "Verify your email address"

    def body_html(self, *, link: str, **context) -> str:
        return f"""
        <p>Please verify your email address to finish setting up your account.</p>
        <p style="text-align:center;margin:24px 0;">
            <a href="{link}" style="background-color:#111827;color:#ffffff;padding:12px 24px;border-radius:6px;text-decoration:none;display:inline-block;">Verify Email</a>
        </p>
        """

    def body_text(self, *, link: str, **context) -> str:
        return f"Please verify your email address by visiting:\n\n{link}"
