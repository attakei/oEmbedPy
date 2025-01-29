"""Test cases for ``oembedpy.adapters.mkdocs``."""

import textwrap

import pytest
from markdown import Markdown

from oembedpy.adapters import mkdocs as t


@pytest.fixture(scope="module")
def plugin() -> t.OembedPlugin:
    plugin = t.OembedPlugin()
    plugin.on_startup(command="build", dirty=False)
    return plugin


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


def test_skip_other_lang_code(plugin: t.OembedPlugin, md: Markdown):
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
def test_oembed_code__no_content(plugin: t.OembedPlugin, md: Markdown):
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
def test_oembed_code__valid_content(plugin: t.OembedPlugin, md: Markdown):
    source = textwrap.dedent("""
    # Help

    ```oembed
    url = 'https://www.youtube.com/watch?v=Oyh8nuaLASA'
    ```
    """)
    html = md.convert(source)
    output = plugin.on_page_content(html)
    assert html != output
