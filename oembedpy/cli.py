"""Console entrypoint."""
import sys

try:
    import click
except ModuleNotFoundError:
    msg = "oEmbedPy's CLI need Click. Please use extra install."
    sys.stderr.write(f"\033[31m{msg}\033[0m\n")
    sys.exit(1)

from . import __version__


@click.command
@click.option(
    "--version", is_flag=True, default=False, help="Show version information and exit."
)
@click.pass_context
def cli(ctx: click.Context, version: bool):
    """Fetch and display oEmbed parameters from oEmbed provider."""
    if version:
        click.echo(f"{ctx.info_name} v{__version__}")
        ctx.exit(0)
        return


def main():
    """Entrypoint script."""
    cli()
