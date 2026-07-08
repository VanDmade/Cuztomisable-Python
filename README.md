# Cuztomisable

Authentication and user management for FastAPI.

## Installation

```bash
pip install cuztomisable
```

## Setup

### 1. Apply migrations to your database

Run this once when setting up a new project:

```bash
cuztomisable init --database-url "postgresql://{username}:{password}@{host}/{database}"
```

This runs every Cuztomisable migration against your database (users, roles/permissions, images, addresses, registrations, codes, passwords, tokens, and logs). Phone number is a single `phone`/`country_code` column pair directly on `users` — there's no separate phones table.

### 2. Integrate with your FastAPI app

`CuztomisableConfig` only controls CORS — the database connection is wired up separately via `configure_db`, using your own `sessionmaker`:

```python
from fastapi import FastAPI
from cuztomisable import Cuztomisable
from cuztomisable.config import CuztomisableConfig
from cuztomisable.dependencies import configure_db

from app.db.session import SessionLocal

app = FastAPI()

configure_db(SessionLocal)

auth = Cuztomisable(
    app,
    config=CuztomisableConfig(
        cors_origins=["https://myapp.com"],
    ),
)
```

Every route Cuztomisable adds is mounted under an `/api` prefix (e.g. `/api/login`).

### 3. (Optional) Configure behavior

Call `configure()` once at startup, before building your `FastAPI` app, to override login/registration/password/mobile-agent behavior. Every setting can also be set via an env var prefixed `CUZTOMISABLE_`. See [`examples/settings.example.py`](examples/settings.example.py) for the full list with explanations.

```python
from cuztomisable.settings import configure

configure(
    registration={"require_username": True, "require_phone": False},
    password_requirements={"min_length": 10, "uppercase": 1, "digits": 1, "special": 1},
)
```

### 4. (Optional) Read settings from your frontend

`GET /api/cuztomisable/settings` returns the subset of the above that's safe to expose to a client (login/registration requirements, password rules, country codes) — never secrets like `jwt_secret`. See [`examples/cuztomisable.example.ts`](examples/cuztomisable.example.ts) for a copy-paste-ready client, adjustable to whatever frontend framework/API client you're using.

## Endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/login` | Authenticate with email/phone/username + password, returns access/refresh tokens |
| `POST` | `/api/register` | Self-registration. Pass `?code=` to redeem an admin-issued invite (`UserRegistration`) instead of an open signup |
| `GET` | `/api/cuztomisable/settings` | Public, client-safe subset of app settings |
| `GET`/`POST`/`PUT`/`DELETE` | `/api/roles`, `/api/roles/{id}` | Role CRUD (admin-only) |
| `GET`/`POST`/`DELETE` | `/api/roles/{id}/permissions`, `/api/roles/{id}/permissions/{permission_id}` | Role-permission assignment (admin-only) |

## Extending the User model

If your app needs extra columns on `users`, subclass the model rather than forking the package. See [`examples/model.user.example.py`](examples/model.user.example.py) for the migration + subclass pattern.

## CLI Reference

| Command | Description |
|---|---|
| `cuztomisable init -d <url>` | Apply all migrations to the database |
| `cuztomisable create-migration -d <url> -m <message>` | Autogenerate a new migration from model changes |
| `cuztomisable downgrade -d <url> [revision]` | Roll back migrations (default: one step back) |
| `cuztomisable seed -d <url>` | Seed the system user |

## Contributing

### Adding a new migration

After modifying or adding a model, generate a migration against your local database:

```bash
cuztomisable create-migration --database-url "postgresql://{username}:{password}@{host}/{database}" --message "describe_your_change"
```
