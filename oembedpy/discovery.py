"""Discovery module.

This provides features to find oEmbed provider of contents.
"""

import logging
import urllib.parse
from typing import Tuple

import httpx
from bs4 import BeautifulSoup

from .consumer import RequestParameters
from .provider import ProviderRegistry

logger = logging.getLogger(__name__)


def find_from_content(url: str) -> Tuple[str, RequestParameters]:
    """Fetch html content and pick api URL.

    :params url: Target URL.
    """
    # Fetch content
    resp = httpx.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.content, "lxml")
    oembed_links = [
        elm
        for elm in soup.find_all("link", rel="alternate")
        if "type" in elm.attrs and elm["type"].endswith("+oembed")
    ]
    logger.debug(f"Found {len(oembed_links)} URLs for oEmbed")
    if not oembed_links:
        msg = "URL does not have oEmbed reference."
        logger.warning(msg)
        raise ValueError(msg)

    # Parse full-URL
    parts = urllib.parse.urlparse(oembed_links[0]["href"])
    qs = urllib.parse.parse_qs(parts.query)
    params = RequestParameters(url=qs["url"][0])
    if "maxwidth" in qs:
        params.max_width = int(qs["maxwidth"][0])
    if "maxheight" in qs:
        params.max_height = int(qs["maxheight"][0])
    if "format" in qs:
        params.format = qs["format"][0]
    return f"{parts.scheme}://{parts.netloc}{parts.path}", params


def find_from_registry(
    url: str, registry: ProviderRegistry
) -> Tuple[str, RequestParameters]:
    """Find endpoint matched for content from registry."""
    for provider in registry.providers:
        api_url = provider.find_endpoint(url)
        if api_url:
            return api_url, RequestParameters(url=url)

    msg = "Endpoint is not found from registry."
    logger.warning(msg)
    raise ValueError(msg)
