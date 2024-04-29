"""Sphinx extension module."""

import logging

try:
    from docutils import nodes
    from docutils.parsers.rst import Directive, directives
    from sphinx.application import Sphinx
    from sphinx.config import Config

    logger = logging.getLogger(__name__)
except ModuleNotFoundError as err:
    logger = logging.getLogger(__name__)

    msg = "To use it, install with Sphinx."
    logging.error(msg)
    raise err

from oembedpy import __version__
from oembedpy.application import Oembed, Workspace

_oembed: Oembed


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
        node["content"] = _oembed.fetch(**oembed_kwags)
        return [
            node,
        ]


def visit_oembed_node(self, node):  # noqa: D103
    if "content" in node and hasattr(node["content"], "html"):
        self.body.append(node["content"].html)


def depart_oembed_node(self, node):  # noqa: D103
    pass


def _init_client(app: Sphinx, config: Config):
    global _oembed
    _oembed = Workspace() if config.oembed_use_workspace else Oembed()
    _oembed.init()


def setup(app: Sphinx):  # noqa: D103
    app.add_config_value("oembed_use_workspace", False, "env")
    app.add_directive("oembed", OembedDirective)
    app.add_node(
        oembed,
        html=(visit_oembed_node, depart_oembed_node),
    )
    app.connect("config-inited", _init_client)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
