"""Console entrypoint."""

import logging
import sys
from typing import Literal, Optional

try:
    import click
except ModuleNotFoundError:
    msg = "oEmbedPy's CLI need Click. Please use extra install."
    sys.stderr.write(f"\033[31m{msg}\033[0m\n")
    sys.exit(1)

from . import __version__, application

logger = logging.getLogger(__name__)

OUTPUT_FORMAT = Literal["text", "json"]


@click.command
@click.option(
    "--version", is_flag=True, default=False, help="Show version information and exit."
)
@click.option(
    "-w", "--workspace", is_flag=True, default=False, help="Use caching workspace."
)
@click.option(
    "--format",
    type=click.Choice(["text", "json"]),
    default="text",
    help="Display JSON format.",
)
@click.option("--max-width", type=int, help="Max width for oEmbed content.")
@click.option("--max-height", type=int, help="Max height for oEmbed content.")
@click.option(
    "--fallback",
    type=bool,
    is_flag=True,
    default=False,
    help="Fallback simple type if response is invalid",
)
@click.argument("url")
@click.pass_context
def cli(
    ctx: click.Context,
    version: bool,
    workspace: bool,
    url: str,
    fallback: bool,
    format: OUTPUT_FORMAT,
    max_width: Optional[int] = None,
    max_height: Optional[int] = None,
):
    """Fetch and display oEmbed parameters from oEmbed provider."""
    if version:
        click.echo(f"{ctx.info_name} v{__version__}")
        ctx.exit(0)

    # Fetch content to find meta tags.
    logger.debug(f"Target Content URL is {url}")
    oembed = (
        application.Workspace(fallback) if workspace else application.Oembed(fallback)
    )
    oembed.init()
    try:
        content = oembed.fetch(url, max_width, max_height)
    except Exception as err:
        click.echo(click.style(f"Failed to oEmbed URL for {err}", fg="red"))
        ctx.abort()

    # Display data
    if format == "json":
        logger.debug("Display as raw JSON")
        click.echo(content.to_dict())
    else:
        logger.debug("Display as formatted text")
        data = content.to_dict()
        keylen = max(len(k) for k in data.keys()) + 2
        for k, v in data.items():
            click.echo(f"{(k+':'):<{keylen}}{v}")


def main():
    """Entrypoint script."""
    cli()
