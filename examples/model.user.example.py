"""
Example: Extending the User model with app-specific fields.

Step 1 — Create a migration in your app that adds columns to the users table:

    def upgrade():
        op.add_column("users", sa.Column("loyalty_points", sa.Integer(), default=0))
        op.add_column("users", sa.Column("referral_code", sa.String(16), nullable=True))

Step 2 — Subclass User in your app with the new columns:
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from cuztomisable.db.models.users.user import User


class AppUser(User):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    loyalty_points: Mapped[int] = mapped_column(default=0)
    referral_code: Mapped[str | None] = mapped_column(String(16), nullable=True)

# Use AppUser instead of User throughout your app:
#   from app.models.user import AppUser
#   user = db.query(AppUser).filter(AppUser.id == user_id).first()
#   user.loyalty_points
#   user.permissions  # package relationships still available
