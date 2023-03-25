"""For consumer request."""
import logging
import urllib.parse
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

import httpx
from bs4 import BeautifulSoup, Tag

from . import errors, types

logger = logging.getLogger(__name__)


@dataclass
class RequestParameters:
    """Supported query parameters."""

    url: str
    maxwidth: Optional[int] = None
    maxheight: Optional[int] = None
    format: Optional[str] = None

    def to_dict(self) -> Dict[str, str]:
        """Make dict object from properties."""
        data = {"url": self.url}
        if self.maxwidth:
            data["maxwidth"] = str(self.maxwidth)
        if self.maxheight:
            data["maxheight"] = str(self.maxheight)
        if self.format:
            data["format"] = self.format
        return data


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
        if "type" in elm.attrs and elm["type"].endswith("+oembed")
    ]
    logger.debug(f"Found {len(oembed_links)} URLs for oEmbed")
    if not oembed_links:
        msg = "URL is not provided oEmbed or is supported by JSON style response."
        logger.warn(msg)
        raise errors.URLNotFound(msg)

    return oembed_links[0]["href"]


def fetch_content(url: str, params: RequestParameters) -> types.Content:
    """Call API and generate content object.

    This accept only response that has content-type  header explicited as json or xml.
    * OK: ``application/json``
    * OK: ``text/xml``
    * NG: ``text/plain`` (even if body is JSON string)
    """
    resp = httpx.get(url, params=params.to_dict())
    resp.raise_for_status()
    if resp.headers.get("content-type", "").endswith("/json"):
        logging.debug("Parse JSON content.")
        data = resp.json()
    elif resp.headers.get("content-type", "").endswith("/xml"):
        logging.debug("Parse XML content.")
        soup = BeautifulSoup(resp.content, "lxml-xml")
        data = {}
        if not soup.oembed:
            raise ValueError("Invalid XML format.")
        for elm in soup.oembed.children:
            if not isinstance(elm, Tag):
                continue
            data[elm.name] = elm.string.strip()
    else:
        raise ValueError("oEmbed content must be only JSON or XML.")
    Type = data.get("type", "").title()
    if not (Type and hasattr(types, Type)):
        raise ValueError("Invalid type")
    return getattr(types, data["type"].title())(**data)
