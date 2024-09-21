"""Register content data structure.

All typed classes are based from oEmbed specs.
Please see https://oembed.com/
"""

from dataclasses import asdict, dataclass
from inspect import signature
from typing import Any, Dict, NamedTuple, Optional, Type, TypeVar, Union

T = TypeVar("T", bound="_BaseType")


@dataclass
class _BaseType:
    """Base type of contents."""

    _extra: Dict[str, Any]

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        cls_fields = {field for field in signature(cls).parameters}
        cls_kwargs, extra = {}, {}
        for k, v in data.items():
            if k in cls_fields:
                cls_kwargs[k] = v
            else:
                extra[k] = v
        return cls(**cls_kwargs, _extra=extra)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to flat dict."""
        data = asdict(self)
        del data["_extra"]
        for k, v in self._extra.items():
            data[k] = v
        return data


@dataclass
class _Required(_BaseType):
    """Fields of required parameters for any types."""

    type: str
    version: str


@dataclass
class _Optionals:
    """Fields of optional parameters for any types."""

    title: Optional[str] = None
    author_name: Optional[str] = None
    author_url: Optional[str] = None
    provider_name: Optional[str] = None
    provider_url: Optional[str] = None
    cache_age: Optional[int] = None
    thumbnail_url: Optional[str] = None
    thumbnail_width: Optional[int] = None
    thumbnail_height: Optional[int] = None


@dataclass
class _Photo:
    """Required fields for ``photo`` types."""

    url: str
    width: int
    height: int


@dataclass
class _Video:
    """Required fields for ``video`` types."""

    html: str
    width: int
    height: int


@dataclass
class _Rich:
    """Required fields for ``rich`` types."""

    html: str
    width: int
    height: int


@dataclass
class _HtmlOnly(_BaseType):
    """Required fields for fallbacked content."""

    html: str


@dataclass
class Photo(_Optionals, _Photo, _Required):
    """oEmbed content for photo object."""


@dataclass
class Video(_Optionals, _Video, _Required):
    """oEmbed content for vhoto object."""


@dataclass
class Link(_Optionals, _Required):
    """oEmbed content for generic object."""


@dataclass
class Rich(_Optionals, _Rich, _Required):
    """oEmbed content for rich HTML object."""


@dataclass
class HtmlOnly(_Optionals, _HtmlOnly):
    """Fallback type for invalid scheme."""


Content = Union[Photo, Video, Link, Rich, HtmlOnly]
"""Collection of oEmbed content types."""


class CachedContent(NamedTuple):
    expired: float
    content: Content
