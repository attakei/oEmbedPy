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
import httpx
from bs4 import BeautifulSoup

from . import __version__
from .consumer import ConsumerRequest

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
@click.option("--maxwidth", type=int, help="Max width for oEmbed content.")
@click.option("--maxheight", type=int, help="Max height for oEmbed content.")
@click.argument("url")
@click.pass_context
def cli(
    ctx: click.Context,
    version: bool,
    url: str,
    format: OUTPUT_FORMAT,
    maxwidth: Optional[int] = None,
    maxheight: Optional[int] = None,
):
    """Fetch and display oEmbed parameters from oEmbed provider."""
    if version:
        click.echo(f"{ctx.info_name} v{__version__}")
        ctx.exit(0)

    # Fetch content to find meta tags.
    logger.debug(f"Target Content URL is {url}")
    try:
        resp = httpx.get(url, follow_redirects=True)
        resp.raise_for_status()
    except httpx.HTTPError as exc:
        logger.error(f"Failed to content URL for {exc}")
        click.echo(click.style(f"Failed to content URL for {exc}", fg="red"))
        ctx.abort()
    soup = BeautifulSoup(resp.content, "html.parser")
    oembed_links = [
        elm
        for elm in soup.find_all("link", rel="alternate")
        if "type" in elm.attrs and elm["type"].endswith("application/json+oembed")
    ]
    logger.debug(f"Found {len(oembed_links)} URLs for oEmbed")
    if not oembed_links:
        click.echo(
            click.style(
                "URL is not provided oEmbed or is supported by JSON style response.",
                fg="yellow",
            )
        )
        ctx.abort()

    # Fetch oEmbed content
    try:
        req = ConsumerRequest.parse(oembed_links[0]["href"])
        if maxwidth:
            req.query.maxwidth = maxwidth
        if maxheight:
            req.query.maxheight = maxheight
        resp = req.get()
        resp.raise_for_status()
    except httpx.HTTPError as exc:
        logger.error(f"Failed to oEmbed URL for {exc}")
        click.echo(click.style(f"Failed to oEmbed URL for {exc}", fg="red"))
        ctx.abort()
    data = resp.json()

    # Display data
    if format == "json":
        logger.debug("Display as raw JSON")
        click.echo(resp.content)
    else:
        logger.debug("Display as formatted text")
        keylen = max(len(k) for k in data.keys()) + 2
        for k, v in data.items():
            click.echo(f"{(k+':'):<{keylen}}{v}")


def main():
    """Entrypoint script."""
    cli()
