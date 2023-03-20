"""Console entrypoint."""
import sys

import httpx
from bs4 import BeautifulSoup

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
@click.argument("url")
@click.pass_context
def cli(ctx: click.Context, version: bool, url: str):
    """Fetch and display oEmbed parameters from oEmbed provider."""
    if version:
        click.echo(f"{ctx.info_name} v{__version__}")
        ctx.exit(0)
        return

    # Fetch content to find meta tags.
    resp = httpx.get(url)
    soup = BeautifulSoup(resp.content, "html.parser")
    oembed_links = [
        elm
        for elm in soup.find_all("link", rel="alternate")
        if "type" in elm.attrs and elm["type"].endswith("application/json+oembed")
    ]
    if not oembed_links:
        click.echo(
            click.style(
                "URL is not provided oEmbed or is supported by JSON style response.",
                fg="yellow",
            )
        )
        ctx.abort()

    # Fetch oEmbed content
    resp = httpx.get(oembed_links[0]["href"])
    data = resp.json()

    # Display data
    keylen = max(len(k) for k in data.keys()) + 2
    for k, v in data.items():
        click.echo(f"{(k+':'):<{keylen}}{v}")


def main():
    """Entrypoint script."""
    cli()
