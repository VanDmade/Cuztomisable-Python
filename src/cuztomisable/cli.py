from pathlib import Path

import typer
from alembic import command
from alembic.config import Config

app = typer.Typer(help="Cuztomisable — user management initializer for FastAPI.")

MIGRATIONS_DIR = Path(__file__).parent / "db" / "migrations"


def _alembic_config(database_url: str) -> Config:
    cfg = Config()
    cfg.set_main_option("script_location", str(MIGRATIONS_DIR))
    cfg.set_main_option("sqlalchemy.url", database_url)
    return cfg


@app.command()
def init(
    database_url: str = typer.Option(
        ...,
        "--database-url",
        "-d",
        help="Database connection URL"
    ),
):
    cfg = _alembic_config(database_url)
    command.upgrade(cfg, "head")
    typer.echo("Cuztomisable initialized successfully.")


@app.command()
def create_migration(
    database_url: str = typer.Option(
        ...,
        "--database-url",
        "-d",
        help="Database connection URL"
    ),
    message: str = typer.Option(
        ...,
        "--message",
        "-m",
        help="Migration message"
    ),
):
    cfg = _alembic_config(database_url)
    command.revision(cfg, message=message, autogenerate=True)
    typer.echo("Migration created.")


@app.command()
def downgrade(
    database_url: str = typer.Option(
        ...,
        "--database-url",
        "-d",
        help="Database connection URL"
    ),
    revision: str = typer.Argument(
        default="-1",
        help="Target revision (default: one step back)"
    ),
):
    cfg = _alembic_config(database_url)
    command.downgrade(cfg, revision)
    typer.echo(f"Downgraded to {revision}.")
