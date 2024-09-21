"""For consumer request."""

import logging
from dataclasses import dataclass
from typing import Dict, Optional

import httpx
from bs4 import BeautifulSoup, Tag

from . import types

logger = logging.getLogger(__name__)


@dataclass
class RequestParameters:
    """Supported query parameters."""

    url: str
    format: Optional[str] = None
    max_width: Optional[int] = None
    max_height: Optional[int] = None

    def __hash__(self):
        return hash((self.url, self.format, self.max_width, self.max_height))

    def to_dict(self) -> Dict[str, str]:
        """Make dict object from properties."""
        data = {"url": self.url}
        if self.max_width:
            data["maxwidth"] = str(self.max_width)
        if self.max_height:
            data["maxheight"] = str(self.max_height)
        if self.format:
            data["format"] = self.format
        return data


def fetch_content(
    url: str,
    params: RequestParameters,
    fallback_type: bool = False,
) -> types.Content:
    """Call API and generate content object.

    This accept only response that has content-type  header explicit as json or xml.
    * OK: ``application/json``
    * OK: ``text/xml``
    * NG: ``text/plain`` (even if body is JSON string)
    """
    resp = httpx.get(url, params=params.to_dict(), follow_redirects=True)
    resp.raise_for_status()
    content_type = resp.headers.get("content-type", "").split(";")[0]  # Exclude chaset
    if content_type.endswith("/json"):
        logging.debug("Parse JSON content.")
        data = resp.json()
    elif content_type.endswith("/xml"):
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
    try:
        content = getattr(types, data["type"].title()).from_dict(data)
    except TypeError as err:
        if not fallback_type:
            raise err
        content = types.HtmlOnly.from_dict(data)
    return content
