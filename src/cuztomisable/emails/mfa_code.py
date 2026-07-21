from .base import EmailTemplate


class MfaCodeEmail(EmailTemplate):
    def subject(self, **context) -> str:
        return "Your login verification code"

    def body_html(self, *, code: str, **context) -> str:
        return f"""
        <p>Use the code below to finish logging in:</p>
        <p style="text-align:center;margin:24px 0;font-size:28px;font-weight:bold;letter-spacing:4px;">{code}</p>
        <p>If you didn't try to log in, you should change your password immediately.</p>
        """

    def body_text(self, *, code: str, **context) -> str:
        return (
            f"Use this code to finish logging in: {code}\n\n"
            "If you didn't try to log in, you should change your password immediately."
        )
