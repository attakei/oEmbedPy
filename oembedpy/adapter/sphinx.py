"""Sphinx extension module."""

from datetime import datetime
from typing import Union, Tuple

try:
    import sphinx  # noqa
except ModuleNotFoundError as err:
    import logging

    msg = "To use it, install with Sphinx."
    logging.error(msg)
    raise err

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from oembedpy import __version__
from oembedpy.application import Oembed, Workspace
from oembedpy.types import Content
from sphinx.application import Sphinx
from sphinx.domains import Domain
from sphinx.environment import BuildEnvironment
from sphinx.util.logging import getLogger

logger = getLogger(__name__)


class OembedDomain(Domain):
    name = __name__
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
        if "cache_age" not in content._extra:
            return True
        return now < content._extra["cache_age"]


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
