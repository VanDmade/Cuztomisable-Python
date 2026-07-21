import re
import smtplib
import uuid
from datetime import datetime, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from pathlib import Path
from typing import Iterable, List, Optional, Union

from sqlalchemy.orm import Session

from cuztomisable.services.logs.email import EmailLogService
from cuztomisable.settings import settings

Addresses = Union[str, Iterable[str]]


def _normalize(addresses: Optional[Addresses]) -> List[str]:
    if not addresses:
        return []
    if isinstance(addresses, str):
        return [addresses]
    return list(addresses)


def _log_locally(*, to_addresses: List[str], subject: str, text: str, html: Optional[str]) -> Path:
    """Writes the email to disk instead of sending it — used when mail_driver
    is 'log', or automatically when no SMTP username is configured, so flows
    like forgot-password can be exercised end-to-end without real SES creds."""
    directory = Path(settings.mail_log_path)
    directory.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    safe_to = re.sub(r"[^\w.@-]", "_", to_addresses[0]) if to_addresses else "unknown"
    path = directory / f"{timestamp}_{safe_to}.html"
    path.write_text(html or f"<pre>{text}</pre>", encoding="utf-8")

    print(f"[MailService] mail_driver=log - not sending via SMTP")
    print(f"  To: {', '.join(to_addresses)}")
    print(f"  Subject: {subject}")
    print(f"  Text:\n{text}")
    print(f"  HTML preview: {path.resolve()}")
    return path


class MailService:
    def __init__(self, db: Session):
        self.db = db

    def send(
        self,
        to: Addresses,
        subject: str,
        body: str,
        html: Optional[str] = None,
        cc: Optional[Addresses] = None,
        bcc: Optional[Addresses] = None,
        created_by: Optional[uuid.UUID] = None,
        parameters: Optional[dict] = None,
    ) -> None:
        to_addresses = _normalize(to)
        cc_addresses = _normalize(cc)
        bcc_addresses = _normalize(bcc)
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = formataddr((settings.mail_from_name, settings.mail_from_address))
        message["To"] = ", ".join(to_addresses)
        if cc_addresses:
            message["Cc"] = ", ".join(cc_addresses)
        message.attach(MIMEText(body, "plain"))
        if html:
            message.attach(MIMEText(html, "html"))

        if settings.mail_driver == "log" or not settings.smtp_username:
            _log_locally(to_addresses=to_addresses, subject=subject, text=body, html=html)
        else:
            with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
                if settings.smtp_use_tls:
                    server.starttls()
                server.login(settings.smtp_username, settings.smtp_password)
                server.sendmail(
                    settings.mail_from_address,
                    [*to_addresses, *cc_addresses, *bcc_addresses],
                    message.as_string(),
                )
        EmailLogService(self.db).create(created_by, {
            "to": ", ".join(to_addresses),
            "cc": ", ".join(cc_addresses) or None,
            "bcc": ", ".join(bcc_addresses) or None,
            "from_address": settings.mail_from_address,
            "subject": subject,
            "parameters": parameters,
        })

    def send_template(
        self,
        to: Addresses,
        template_name: str,
        context: Optional[dict] = None,
        *,
        cc: Optional[Addresses] = None,
        bcc: Optional[Addresses] = None,
        created_by: Optional[uuid.UUID] = None,
    ) -> None:
        templates = settings.email_templates
        layout_cls = templates["layout"]
        template_cls = templates[template_name]
        full_context = {
            "company_name": settings.mail_from_name,
            "year": datetime.now(timezone.utc).year,
            **(context or {}),
        }
        content = template_cls().render(layout_cls(), **full_context)
        self.send(
            to,
            content.subject,
            content.text,
            html=content.html,
            cc=cc,
            bcc=bcc,
            created_by=created_by,
            parameters=context,
        )
