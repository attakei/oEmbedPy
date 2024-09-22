"""Core endpoint."""

import json
import logging
import pickle
import time
from typing import Dict, Optional

import httpx

from platformdirs import PlatformDirs

from oembedpy import consumer, discovery
from oembedpy.provider import ProviderRegistry
from oembedpy.types import CachedContent, Content

logger = logging.getLogger(__name__)


class Oembed:
    """Application of oEmbed."""

    _registry: ProviderRegistry
    _cache: Dict[consumer.RequestParameters, CachedContent]
    _fallback_type: bool

    def __init__(self, fallback_type: bool = False):  # noqa: D107
        self._fallback_type = fallback_type

    def init(self):
        resp = httpx.get("https://oembed.com/providers.json")
        self._registry = ProviderRegistry.from_dict(resp.json())
        self._cache = {}

    def fetch(
        self,
        url: str,
        max_width: Optional[int] = None,
        max_height: Optional[int] = None,
    ) -> Content:
        """Find endpoint from registry and content."""
        try:
            api_url, params = discovery.find_from_registry(url, self._registry)
        except ValueError:  # TODO: Split error case?
            logger.warning("It is not found from registry. Try from content.")
            api_url, params = discovery.find_from_content(url)
        except Exception as err:
            logger.warning(f"oEmbed API is not found from URL: {err}")
        if max_width:
            params.max_width = max_width
        if max_height:
            params.max_height = max_height
        #
        now = time.mktime(time.localtime())
        if params in self._cache and now <= self._cache[params].expired:
            return self._cache[params].content
        content = consumer.fetch_content(api_url, params, self._fallback_type)
        if content.cache_age:
            self._cache[params] = CachedContent(now + int(content.cache_age), content)
        return content


class Workspace(Oembed):
    """oEmbed client with workspace."""

    def __init__(self, fallback_type: bool = False):
        super().__init__(fallback_type)
        self._dirs = PlatformDirs("oembedpy")
        self._cache = {}

    def __del__(self):
        cache_db = self.cache_dir / "db.pickle"
        cache_db.write_bytes(pickle.dumps(self._cache))

    @property
    def cache_dir(self):
        return self._dirs.user_data_path

    def init(self):
        self.init_providers()
        self.init_caches()

    def init_providers(self):
        providers_json = self.cache_dir / "providers.json"
        use_cache = providers_json.exists()
        if use_cache:
            now_ts = time.mktime(time.localtime())
            file_ts = providers_json.stat().st_mtime
            # TODO: expired time is temporary value, refer settings or default after.
            use_cache = file_ts + (3600 * 24) > now_ts

        providers_data: dict
        if use_cache:
            providers_data = json.loads(providers_json.read_text())
        else:
            providers_json.parent.mkdir(parents=True, exist_ok=True)
            resp = httpx.get("https://oembed.com/providers.json")
            providers_data = resp.json()
            providers_json.write_text(resp.text)

        self._registry = ProviderRegistry.from_dict(providers_data)

    def init_caches(self):
        cache_db = self.cache_dir / "db.pickle"
        if cache_db.exists():
            self._cache = pickle.loads(cache_db.read_bytes())
