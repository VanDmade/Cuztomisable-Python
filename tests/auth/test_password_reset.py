from datetime import datetime, timedelta, timezone

from cuztomisable.helpers.security import hash_password, verify_password
from cuztomisable.services.users.passwords.password import UserPasswordService
from cuztomisable.services.users.passwords.reset import UserPasswordResetService
from cuztomisable.services.users.tokens.access import UserAccessTokenService


def test_forgot_password_creates_reset_record_for_existing_user(client, db, user):
    response = client.post("/api/password/forgot", json={"username": user.email})

    assert response.status_code == 200

    record = UserPasswordResetService(db).get_lastest_by_user(user.id)
    assert record is not None
    assert record.code is not None
    assert record.sent_via == "email"


def test_forgot_password_is_identical_for_nonexistent_user(client, db, user):
    real_response = client.post("/api/password/forgot", json={"username": user.email})
    fake_response = client.post("/api/password/forgot", json={"username": "nobody@example.com"})

    # The response shape must not reveal whether the account exists —
    # otherwise this endpoint becomes a user-enumeration oracle.
    assert real_response.status_code == fake_response.status_code
    assert set(real_response.json().keys()) == set(fake_response.json().keys())

    # And no record should have been created for the nonexistent user.
    from cuztomisable.services.users.auth import AuthService

    assert AuthService(db).find_by_login_type("email", "nobody@example.com") is None


def test_verify_valid_code_succeeds(client, db, user):
    record = UserPasswordResetService(db).create(user.id)

    response = client.get(
        f"/api/password/forgot/{record.code}/verify",
        params={"username": user.email},
    )

    assert response.status_code == 200


def test_verify_fails_with_mismatched_username(client, db, user):
    record = UserPasswordResetService(db).create(user.id)

    # Correct code, but for a different account — should not be treated as
    # valid just because the code string matches something in the table.
    response = client.get(
        f"/api/password/forgot/{record.code}/verify",
        params={"username": "someoneelse@example.com"},
    )

    assert response.status_code == 400


def test_verify_fails_when_code_expired(client, db, user):
    record = UserPasswordResetService(db).create(user.id)
    record.expires_at = datetime.now(timezone.utc) - timedelta(minutes=1)
    db.flush()

    response = client.get(
        f"/api/password/forgot/{record.code}/verify",
        params={"username": user.email},
    )

    assert response.status_code == 400


def test_reset_password_success_flow(client, db, user):
    record = UserPasswordResetService(db).create(user.id)
    _, old_access_token = UserAccessTokenService(db).create(user.id)
    db.flush()

    response = client.post(
        "/api/password/forgot/",
        json={
            "username": user.email,
            "code": record.code,
            "password": "BrandNewPass1!",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body

    # The stored password hash should now match the new password.
    db.refresh(user)
    assert verify_password("BrandNewPass1!", user.password)

    # The code is single-use.
    db.refresh(record)
    assert record.used_at is not None

    # A password reset should kill every other existing session.
    db.refresh(old_access_token)
    assert old_access_token.revoked is True


def test_reset_password_rejects_recently_used_password(client, db, user):
    record = UserPasswordResetService(db).create(user.id)
    # Simulate "OldPass1!" being in this user's recent password history.
    UserPasswordService(db).create(user.id, {"password": hash_password("OldPass1!")})
    db.flush()

    response = client.post(
        "/api/password/forgot/",
        json={
            "username": user.email,
            "code": record.code,
            "password": "OldPass1!",
        },
    )

    assert response.status_code == 400
