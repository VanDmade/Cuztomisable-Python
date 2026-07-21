from .base import EmailTemplate


class NewRegistrationEmail(EmailTemplate):
    def subject(self, **context) -> str:
        return "Welcome!"

    def body_html(self, *, name: str, **context) -> str:
        return f"""
        <p>Hi {name},</p>
        <p>Thanks for creating an account. We're glad to have you!</p>
        """

    def body_text(self, *, name: str, **context) -> str:
        return f"Hi {name},\n\nThanks for creating an account. We're glad to have you!"
