from app import app, cache
import click


@app.cli.command()
def cc() -> None:
    """Clear the cache."""
    click.echo('Clearing cache')

    cache.clear()

    click.secho('Done', fg='green')
