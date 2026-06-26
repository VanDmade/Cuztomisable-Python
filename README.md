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

This creates the `users` and `images` tables in your database.

### 2. Integrate with your FastAPI app

```python
from fastapi import FastAPI
from cuztomisable import Cuztomisable, CuztomisableConfig

app = FastAPI()

auth = Cuztomisable(
    app=app,
    config=CuztomisableConfig(
        database_url="postgresql://{username}:{password}@{host}/{database}"
    )
)
```

## CLI Reference

| Command | Description |
|---|---|
| `cuztomisable init -d <url>` | Apply all migrations to the database |
| `cuztomisable downgrade -d <url>` | Roll back the last migration |

## Contributing

### Adding a new migration

After modifying or adding a model, generate a migration against your local database:

```bash
cuztomisable create-migration --database-url "postgresql://{username}:{password}@{host}/{database}" --message "describe_your_change"
```
