from datetime import datetime, timezone

from .base import LayoutTemplate


class DefaultLayout(LayoutTemplate):
    def wrap_html(self, inner_html: str, *, company_name: str = "Cuztomisable", year: int = None, **context) -> str:
        year = year or datetime.now(timezone.utc).year
        return f"""<!DOCTYPE html>
<html>
  <body style="margin:0;padding:0;background-color:#f4f4f5;font-family:Arial,Helvetica,sans-serif;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f4f5;padding:24px 0;">
      <tr>
        <td align="center">
          <table role="presentation" width="480" cellpadding="0" cellspacing="0" style="background-color:#ffffff;border-radius:8px;overflow:hidden;">
            <tr>
              <td style="background-color:#111827;padding:20px 32px;">
                <span style="color:#ffffff;font-size:18px;font-weight:bold;">{company_name}</span>
              </td>
            </tr>
            <tr>
              <td style="padding:32px;color:#111827;font-size:14px;line-height:1.6;">
                {inner_html}
              </td>
            </tr>
            <tr>
              <td style="padding:16px 32px;color:#9ca3af;font-size:12px;border-top:1px solid #e5e7eb;">
                &copy; {year} {company_name}. All rights reserved.
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>"""

    def wrap_text(self, inner_text: str, *, company_name: str = "Cuztomisable", year: int = None, **context) -> str:
        year = year or datetime.now(timezone.utc).year
        return f"{inner_text}\n\n---\n{company_name} © {year}"
