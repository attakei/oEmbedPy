"""eEmbed provider definiitons.

This module is complied for style of https://oembed.com/providers.json
"""

from dataclasses import dataclass
from fnmatch import fnmatch
from typing import Any, Dict, List, Optional


@dataclass
class Endpoint:
    """Endpoint spec."""

    url: str
    schemes: List[str]
    discovery: Optional[bool] = None
    formats: Optional[List[str]] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Endpoint":
        """Initialize object.

        JSON data format comples for style of https://oembed.com/providers.json
        """
        return cls(
            url=data["url"],
            schemes=data.get("schemes", []),
            discovery=data.get("discovery"),
            formats=data.get("discovery"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict object."""
        data: Dict[str, Any] = {
            "url": self.url,
        }
        if self.schemes:
            data["schemes"] = self.schemes
        if self.discovery:
            data["discovery"] = self.discovery
        if self.formats:
            data["formats"] = self.formats
        return data

    def is_match(self, url: str) -> bool:
        """Return if URL is target for schemes of endpoints."""
        return any(fnmatch(url, scheme) for scheme in self.schemes)


@dataclass
class Provider:
    """Provider spec."""

    name: str
    url: str
    endpoints: List[Endpoint]

    @classmethod
    def from_dict(cls, data: dict) -> "Provider":
        """Initialize object.

        JSON data format comples for style of https://oembed.com/providers.json
        """
        return cls(
            name=data["provider_name"],
            url=data["provider_url"],
            endpoints=[Endpoint.from_dict(d) for d in data["endpoints"]],
        )

    def to_dict(self) -> dict:
        """Convert to dict object."""
        return {
            "provider_name": self.name,
            "provider_url": self.url,
            "endpoints": [e.to_dict() for e in self.endpoints],
        }

    def find_endpoint(self, url) -> Optional[str]:
        """Find endpoint URL matched content and scheme."""
        for endpoint in self.endpoints:
            if endpoint.is_match(url):
                return endpoint.url
        return None


@dataclass
class ProviderRegistry:
    """Registry of providers."""

    providers: List[Provider]

    @classmethod
    def from_dict(cls, data: list) -> "ProviderRegistry":
        """Initialize object.

        JSON data format comples for style of https://oembed.com/providers.json
        """
        providers = [Provider.from_dict(d) for d in data]
        return cls(providers=providers)
