"""Test cases for ``oembedpy.adapters.mkdocs``."""

import textwrap
from typing import Any, Callable, Optional

import pytest
from markdown import Markdown

from oembedpy.adapters import mkdocs as t


@pytest.fixture(scope="module")
def get_plugin() -> Callable[[dict[str, Any]], t.OembedPlugin]:
    def _get_plugin(config: Optional[dict[str, Any]] = None) -> t.OembedPlugin:
        plugin = t.OembedPlugin()
        plugin.config = config or {"fallback_type": False}
        plugin.on_startup(command="build", dirty=False)
        return plugin

    return _get_plugin


@pytest.fixture(scope="module")
def md() -> Markdown:
    md = Markdown()
    md.registerExtensions(
        ["fenced_code"],
        {
            "fenced_code": {"lang_prefix": "language-"},
        },
    )
    return md


def test_skip_other_lang_code(get_plugin, md: Markdown):
    plugin = get_plugin()
    source = textwrap.dedent("""
    # Help

    ```toml
    url = 'http://example.com'
    ```
    """)
    html = md.convert(source)
    output = plugin.on_page_content(html)
    assert html == output


@pytest.mark.webtest
def test_oembed_code__no_content(get_plugin, md: Markdown):
    plugin = get_plugin()
    source = textwrap.dedent("""
    # Help

    ```oembed
    url = 'http://example.com'
    ```
    """)
    html = md.convert(source)
    output = plugin.on_page_content(html)
    assert html == output


@pytest.mark.webtest
def test_oembed_code__valid_content(get_plugin, md: Markdown):
    plugin = get_plugin()
    source = textwrap.dedent("""
    # Help

    ```oembed
    url = 'https://www.youtube.com/watch?v=Oyh8nuaLASA'
    ```
    """)
    html = md.convert(source)
    output = plugin.on_page_content(html)
    assert html != output


@pytest.mark.webtest
def test_oembed_code__invalid_content(get_plugin, md: Markdown):
    plugin = get_plugin()
    source = textwrap.dedent("""
    # Help

    ```oembed
    url = 'https://www.reddit.com/r/Python/comments/vdopqj/sphinxrevealjs_html_presentation_builder_for/'
    ```
    """)
    html = md.convert(source)
    output = plugin.on_page_content(html)
    assert html == output


@pytest.mark.webtest
def test_oembed_code__fallback_invalid_content(get_plugin, md: Markdown):
    plugin = get_plugin({"fallback_type": True})
    source = textwrap.dedent("""
    # Help

    ```oembed
    url = 'https://www.reddit.com/r/Python/comments/vdopqj/sphinxrevealjs_html_presentation_builder_for/'
    ```
    """)
    html = md.convert(source)
    output = plugin.on_page_content(html)
    assert html != output
