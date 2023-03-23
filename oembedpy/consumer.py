"""For consumer request."""
import urllib.parse
from dataclasses import asdict, dataclass
from typing import Optional, Tuple


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
