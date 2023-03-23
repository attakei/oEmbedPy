"""Register content data structure.

All typed classes are based from oEmbed specs.
Please see https://oembed.com/
"""
from dataclasses import dataclass
from typing import Optional, Union


@dataclass
class _Required:
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


Content = Union[Photo, Video, Link, Rich]
"""Collection of oEmbed content types."""
