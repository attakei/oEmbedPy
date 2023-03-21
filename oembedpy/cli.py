"""Console entrypoint."""
import logging
import sys
import urllib.parse
from typing import List

try:
    import click
except ModuleNotFoundError:
    msg = "oEmbedPy's CLI need Click. Please use extra install."
    sys.stderr.write(f"\033[31m{msg}\033[0m\n")
    sys.exit(1)
import httpx
from bs4 import BeautifulSoup

from . import __version__

logger = logging.getLogger(__name__)


@click.command
@click.option(
    "--version", is_flag=True, default=False, help="Show version information and exit."
)
@click.option("--json", is_flag=True, default=False, help="Display JSON format.")
@click.option(
    "--extra-params",
    "-e",
    type=str,
    multiple=True,
    help="Appendix request parameter for oEmbed provider.",
)
@click.argument("url")
@click.pass_context
def cli(
    ctx: click.Context, version: bool, json: bool, extra_params: List[str], url: str
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
        parts = urllib.parse.urlparse(oembed_links[0]["href"])
        qs = urllib.parse.parse_qs(parts.query)
        for param in extra_params:
            k, v = param.split("=")
            qs[k] = [v]
        new_parts = parts._replace(query=urllib.parse.urlencode(qs, True))
        url = new_parts.geturl()
        logger.debug(f"oEmbed Content URL is {url}")
        resp = httpx.get(url, follow_redirects=True)
        resp.raise_for_status()
    except httpx.HTTPError as exc:
        logger.error(f"Failed to oEmbed URL for {exc}")
        click.echo(click.style(f"Failed to oEmbed URL for {exc}", fg="red"))
        ctx.abort()
    data = resp.json()

    # Display data
    if json:
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
