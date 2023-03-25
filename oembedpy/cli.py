"""Console entrypoint."""
import dataclasses
import logging
import sys
from typing import Literal, Optional

from oembedpy.errors import URLNotFound

try:
    import click
except ModuleNotFoundError:
    msg = "oEmbedPy's CLI need Click. Please use extra install."
    sys.stderr.write(f"\033[31m{msg}\033[0m\n")
    sys.exit(1)
import httpx

from . import __version__
from .consumer import discover, fetch_content, parse

logger = logging.getLogger(__name__)

OUTPUT_FORMAT = Literal["text", "json"]


@click.command
@click.option(
    "--version", is_flag=True, default=False, help="Show version information and exit."
)
@click.option(
    "--format",
    type=click.Choice(["text", "json"]),
    default="text",
    help="Display JSON format.",
)
@click.option("--max-width", type=int, help="Max width for oEmbed content.")
@click.option("--max-height", type=int, help="Max height for oEmbed content.")
@click.argument("url")
@click.pass_context
def cli(
    ctx: click.Context,
    version: bool,
    url: str,
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
    try:
        oembed_url = discover(url)
    except URLNotFound as err:
        logger.warn(f"oEmbed API is not found from URL: {err}")
        ctx.abort()

    # Fetch oEmbed content
    try:
        api_url, params = parse(oembed_url)
        if max_width:
            params.max_width = max_width
        if max_height:
            params.max_height = max_height
        content = fetch_content(api_url, params=params)
    except httpx.HTTPError as exc:
        logger.error(f"Failed to oEmbed URL for {exc}")
        click.echo(click.style(f"Failed to oEmbed URL for {exc}", fg="red"))
        ctx.abort()

    # Display data
    if format == "json":
        logger.debug("Display as raw JSON")
        click.echo(dataclasses.asdict(content))
    else:
        logger.debug("Display as formatted text")
        data = dataclasses.asdict(content)
        keylen = max(len(k) for k in data.keys()) + 2
        for k, v in data.items():
            click.echo(f"{(k+':'):<{keylen}}{v}")


def main():
    """Entrypoint script."""
    cli()
