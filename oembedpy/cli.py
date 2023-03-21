"""Console entrypoint."""
import sys

try:
    import click
except ModuleNotFoundError:
    msg = "oEmbedPy's CLI need Click. Please use extra install."
    sys.stderr.write(f"\033[31m{msg}\033[0m\n")
    sys.exit(1)
import httpx
from bs4 import BeautifulSoup

from . import __version__


@click.command
@click.option(
    "--version", is_flag=True, default=False, help="Show version information and exit."
)
@click.option("--json", is_flag=True, default=False, help="Display JSON format.")
@click.argument("url")
@click.pass_context
def cli(ctx: click.Context, version: bool, json: bool, url: str):
    """Fetch and display oEmbed parameters from oEmbed provider."""
    if version:
        click.echo(f"{ctx.info_name} v{__version__}")
        ctx.exit(0)
        return

    # Fetch content to find meta tags.
    try:
        resp = httpx.get(url, follow_redirects=True)
        resp.raise_for_status()
    except httpx.HTTPError as exc:
        click.echo(click.style(f"Failed to content URL for {exc}", fg="red"))
        ctx.abort()
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
    try:
        resp = httpx.get(oembed_links[0]["href"], follow_redirects=True)
        resp.raise_for_status()
    except httpx.HTTPError as exc:
        click.echo(click.style(f"Failed to oEmbed URL for {exc}", fg="red"))
        ctx.abort()
    data = resp.json()

    # Display data
    if json:
        click.echo(resp.content)
    else:
        keylen = max(len(k) for k in data.keys()) + 2
        for k, v in data.items():
            click.echo(f"{(k+':'):<{keylen}}{v}")


def main():
    """Entrypoint script."""
    cli()
