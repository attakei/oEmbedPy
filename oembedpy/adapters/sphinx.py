"""Sphinx extension module."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Tuple, Union

try:
    import sphinx  # noqa
except ModuleNotFoundError as err:
    import logging

    msg = "To use it, install with Sphinx."
    logging.error(msg)
    raise err

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx.domains import Domain
from sphinx.util.logging import getLogger

from .. import __version__
from ..application import Oembed, Workspace

if TYPE_CHECKING:
    from sphinx.addnodes import pending_xref
    from sphinx.application import Sphinx
    from sphinx.builders import Builder
    from sphinx.environment import BuildEnvironment

    from ..types import Content

logger = getLogger(__name__)


class OembedDomain(Domain):
    name = "oembedpy"
    label = "oembedpy"

    def __init__(self, env: BuildEnvironment):
        super().__init__(env)
        use_workspace = self.env.app.config.oembed_use_workspace
        fallback_type = self.env.app.config.oembed_fallback_type
        self._client = (
            Workspace(fallback_type) if use_workspace else Oembed(fallback_type)
        )
        self._client.init()

    @property
    def caches(self) -> dict[Tuple[str, Union[int, None], Union[int, None]], Content]:
        return self.data.setdefault("caches", {})

    def process_doc(
        self, env: BuildEnvironment, docname: str, document: nodes.document
    ):
        for node in document.findall(oembed):
            params = node["params"]
            cache_key = (params["url"], params["max_width"], params["max_height"])
            logger.debug(f"Target content for {cache_key}")
            if self.has_cache(cache_key):
                logger.debug("Cache is found. Use this.")
                content = self.caches[cache_key]
            else:
                logger.debug("Cache is not exists. Fetching content from service.")
                content = self._client.fetch(**node["params"])
                self.caches[cache_key] = content
            node["content"] = content

    def has_cache(self, key: Tuple[str, Union[int, None], Union[int, None]]) -> bool:
        now = int(datetime.now().timestamp())
        if key not in self.caches:
            return False
        content: Content = self.caches[key]
        if hasattr(
            content, "_expired"
        ):  # NOTE: For if pickled object does not have _expired.
            return now < content._expired
        if "cache_age" not in content._extra:
            return True
        return now < content._extra["cache_age"]

    def resolve_any_xref(
        self,
        env: BuildEnvironment,
        fromdocname: str,
        builder: Builder,
        target: str,
        node: pending_xref,
        contnode: nodes.Element,
    ) -> list[tuple[str, nodes.Element]]:
        # NOTE: This domain will not resolve any cross-reference,
        # because this does not have roles and directives that are refered by outside.
        return []

    def merge_domaindata(self, docnames: list[str], otherdata) -> None:
        """Merge domain data from parallel builds.

        This method merges cached oEmbed content from parallel build environments.
        The merge strategy prioritizes entries with longer expiration times to ensure
        the most up-to-date and longest-lived cached content is retained.
        """
        other_caches = otherdata.get("caches", {})
        for cache_key, content in other_caches.items():
            if cache_key not in self.caches:
                self.caches[cache_key] = content
                continue
            exist = self.caches[cache_key]
            if content._expired > exist._expired:
                self.caches[cache_key] = content


class oembed(nodes.General, nodes.Element):  # noqa: D101,E501
    pass


class OembedDirective(Directive):  # noqa: D101
    has_content = False
    required_arguments = 1
    option_spec = {
        "maxwidth": directives.positive_int,
        "maxheight": directives.positive_int,
    }

    def run(self):  # noqa: D102
        oembed_kwags = {
            "url": self.arguments[0],
            "max_width": self.options.get("maxwidth", None),
            "max_height": self.options.get("maxheight", None),
        }
        node = oembed()
        node["params"] = oembed_kwags
        return [
            node,
        ]


def visit_oembed_node(self, node):  # noqa: D103
    if "content" in node and hasattr(node["content"], "html"):
        self.body.append(node["content"].html)


def depart_oembed_node(self, node):  # noqa: D103
    pass


def setup(app: Sphinx):  # noqa: D103
    app.add_config_value("oembed_use_workspace", False, "env")
    app.add_config_value("oembed_fallback_type", False, "env", bool)
    app.add_directive("oembed", OembedDirective)
    app.add_node(
        oembed,
        html=(visit_oembed_node, depart_oembed_node),
    )
    app.add_domain(OembedDomain)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
