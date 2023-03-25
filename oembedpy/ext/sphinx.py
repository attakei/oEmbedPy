"""Sphinx extension module."""
import logging

try:
    from docutils import nodes
    from docutils.parsers.rst import Directive, directives
    from sphinx.application import Sphinx

    logger = logging.getLogger(__name__)
except ModuleNotFoundError as err:
    logger = logging.getLogger(__name__)

    msg = "To use it, install with Sphinx."
    logging.error(msg)
    raise err

from oembedpy import consumer


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
        url = consumer.discover(self.arguments[0])
        url, params = consumer.parse(url)
        if "maxwidth" in self.options:
            params.max_width = self.options["maxwidth"]
        if "maxheight" in self.options:
            params.max_height = self.options["maxheight"]
        node = oembed()
        node["content"] = consumer.fetch_content(url, params)
        return [
            node,
        ]


def visit_oembed_node(self, node):  # noqa: D103
    if "content" in node and hasattr(node["content"], "html"):
        self.body.append(node["content"].html)


def depart_oembed_node(self, node):  # noqa: D103
    pass


def setup(app: Sphinx):  # noqa: D103
    app.add_directive("oembed", OembedDirective)
    app.add_node(
        oembed,
        html=(visit_oembed_node, depart_oembed_node),
    )
