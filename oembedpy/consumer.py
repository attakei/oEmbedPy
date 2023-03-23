"""For consumer request."""
import logging
import urllib.parse
from dataclasses import asdict, dataclass
from typing import Optional, Tuple

import httpx
from bs4 import BeautifulSoup

from . import errors

logger = logging.getLogger(__name__)


@dataclass
class RequestParameters:
    """Supported query parameters."""

    url: str
    maxwidth: Optional[int] = None
    maxheight: Optional[int] = None
    format: Optional[str] = None

    def to_dict(self) -> dict:
        """Make dict object from properties."""
        return asdict(self)


def parse(url: str) -> Tuple[str, RequestParameters]:
    """Parse from full-URL (passed from content HTML).

    You can use to change params for request API.
    """
    parts = urllib.parse.urlparse(url)
    qs = urllib.parse.parse_qs(parts.query)
    params = RequestParameters(url=qs["url"][0])
    if "maxwidth" in qs:
        params.maxwidth = int(qs["maxwidth"][0])
    if "maxheight" in qs:
        params.maxheight = int(qs["maxheight"][0])
    if "format" in qs:
        params.format = qs["format"][0]
    return f"{parts.scheme}://{parts.netloc}{parts.path}", params


def discover(url: str) -> str:
    """Find oEmbed URL from content URL.

    Argument URL must be response HTML included link tag for oEmbed.
    """
    try:
        resp = httpx.get(url, follow_redirects=True)
        resp.raise_for_status()
    except httpx.HTTPError as exc:
        msg = f"Failed to content URL for {exc}"
        logger.warn(msg)
        raise errors.URLNotFound(msg)
    soup = BeautifulSoup(resp.content, "html.parser")
    oembed_links = [
        elm
        for elm in soup.find_all("link", rel="alternate")
        if "type" in elm.attrs and elm["type"].endswith("application/json+oembed")
    ]
    logger.debug(f"Found {len(oembed_links)} URLs for oEmbed")
    if not oembed_links:
        msg = "URL is not provided oEmbed or is supported by JSON style response."
        logger.warn(msg)
        raise errors.URLNotFound(msg)

    return oembed_links[0]["href"]
