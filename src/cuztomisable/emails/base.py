from dataclasses import dataclass


@dataclass
class EmailContent:
    subject: str
    html: str
    text: str


class LayoutTemplate:
    """Wraps a single email's content in the shared branded shell."""

    def wrap_html(self, inner_html: str, **context) -> str:
        raise NotImplementedError

    def wrap_text(self, inner_text: str, **context) -> str:
        raise NotImplementedError


class EmailTemplate:
    """Base class for a single email. Subclasses provide the copy; the
    configured layout provides the surrounding shell."""

    def subject(self, **context) -> str:
        raise NotImplementedError

    def body_html(self, **context) -> str:
        raise NotImplementedError

    def body_text(self, **context) -> str:
        raise NotImplementedError

    def render(self, layout: LayoutTemplate, **context) -> EmailContent:
        return EmailContent(
            subject=self.subject(**context),
            html=layout.wrap_html(self.body_html(**context), **context),
            text=layout.wrap_text(self.body_text(**context), **context),
        )
