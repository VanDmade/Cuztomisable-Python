from .base import EmailTemplate


class NewLoginDetectedEmail(EmailTemplate):
    def subject(self, **context) -> str:
        return "New login to your account"

    def body_html(self, *, ip_address: str = "unknown", when: str = "", **context) -> str:
        time_row = f"<li>Time: {when}</li>" if when else ""
        return f"""
        <p>We noticed a new login to your account.</p>
        <ul>
            <li>IP address: {ip_address}</li>
            {time_row}
        </ul>
        <p>If this wasn't you, please reset your password immediately.</p>
        """

    def body_text(self, *, ip_address: str = "unknown", when: str = "", **context) -> str:
        lines = ["We noticed a new login to your account.", f"IP address: {ip_address}"]
        if when:
            lines.append(f"Time: {when}")
        lines.append("If this wasn't you, please reset your password immediately.")
        return "\n".join(lines)
