"""MkDocs integration.

This provides as MkDocs pluing.
You can use by add it into your ``mkdocs.yml``.
"""

import logging
from typing import Optional

import lxml.html
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin

from ..application import Oembed

try:
    import tomllib  # type: ignore[import-not-found]
except ImportError:
    import tomli as tomllib

logger = logging.getLogger(__name__)


class OembedPlugin(BasePlugin):
    """Oembed injection plugin for MkDocs."""

    config_scheme = (
        (
            "fallback_type",
            config_options.Type(bool, default=False),
        ),
    )

    _client: Oembed

    def on_startup(self, *, command: str, dirty: bool) -> None:
        # TODO: It should cache responses
        self._client = Oembed(self.config["fallback_type"])
        self._client.init()

    def on_page_content(self, html: str, **kwargs) -> Optional[str]:
        """Find oembed code-blocks and inject embed contents."""
        root = lxml.html.fromstring(html)
        converted = False
        for code in root.find_class("language-oembed"):  # type: ignore[attr-defined]
            try:
                # Fetch content
                params = tomllib.loads(code.text)
                content = self._client.fetch(**params)
                if not hasattr(content, "html"):
                    # NOTE: It should not ignore 'photo' type.
                    logger.warning(
                        f"Embed content type is '{content.type}' that does not have 'html' property."
                    )
                    continue
                # Swap contents
                pre = code.getparent()
                parent = pre.getparent()
                parent.insert(parent.index(pre), lxml.html.fromstring(content.html))
                parent.remove(pre)
                converted = True
            except Exception as err:
                logger.warning(err)
        if converted:
            output = lxml.html.tostring(root, pretty_print=True, encoding="utf-8")
            return output.decode() if isinstance(output, bytes) else output
        return html
