"""Core endpoint."""

import logging
from typing import Optional

import httpx

from oembedpy import consumer, discovery
from oembedpy.provider import ProviderRegistry
from oembedpy.types import Content

logger = logging.getLogger(__name__)


class Oembed:
    """Application of oEmbed."""

    registry: ProviderRegistry

    def __init__(self):  # noqa: D107
        resp = httpx.get("https://oembed.com/providers.json")
        self.registry = ProviderRegistry.from_dict(resp.json())

    def fetch(
        self,
        url: str,
        max_width: Optional[int] = None,
        max_height: Optional[int] = None,
    ) -> Content:
        """Find endpoint from registry and content."""
        try:
            api_url, params = discovery.find_from_registry(url)
        except ValueError:  # TODO: Split error case?
            logger.warning("It is not found from registry. Try from content.")
            api_url, params = discovery.find_from_content(url)
        except Exception as err:
            logger.warning(f"oEmbed API is not found from URL: {err}")
        if max_width:
            params.max_width = max_width
        if max_height:
            params.max_height = max_height
        content = consumer.fetch_content(api_url, params)
        return content
