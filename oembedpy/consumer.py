"""For consumer request."""
import urllib.parse
from dataclasses import dataclass
from typing import Optional

import httpx


@dataclass
class RequestParameters:
    """Supported query parameters."""

    url: str
    maxwidth: Optional[int] = None
    maxheight: Optional[int] = None
    format: Optional[str] = None

    def as_qs(self) -> str:
        """Build as qyery-string."""
        params = [f"url={urllib.parse.quote_plus(self.url)}"]
        if self.maxwidth:
            params.append(f"maxwidth={self.maxwidth}")
        if self.maxheight:
            params.append(f"maxheight={self.maxheight}")
        if self.format:
            params.append(f"format={urllib.parse.quote_plus(self.format)}")
        return "&".join(params)


@dataclass
class ConsumerRequest:
    """oEmbed consumer request manage."""

    api_url: str
    params: RequestParameters

    def url(self) -> str:
        """Build full-URL to request for oEmbed provider."""
        return f"{self.api_url}?{self.params.as_qs()}"

    def get(self) -> httpx.Response:
        """Request by itself for oEmbed provider."""
        return httpx.get(self.url(), follow_redirects=True)

    @classmethod
    def parse(cls, url: str) -> "ConsumerRequest":
        """Parse from full-URL (passed from content HTML)."""
        parts = urllib.parse.urlparse(url)
        qs = urllib.parse.parse_qs(parts.query)
        params = RequestParameters(url=qs["url"][0])
        if "maxwidth" in qs:
            params.maxwidth = int(qs["maxwidth"][0])
        if "maxheight" in qs:
            params.maxheight = int(qs["maxheight"][0])
        if "format" in qs:
            params.format = qs["format"][0]
        return cls(
            api_url=f"{parts.scheme}://{parts.netloc}{parts.path}", params=params
        )
