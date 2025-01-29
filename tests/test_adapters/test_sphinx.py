"""Test cases for ``revealjs-fragments`` directive."""

from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from sphinx.testing.util import SphinxTestApp


@pytest.fixture(scope="module")
def rootdir():
    """Set root directory to use testing sphinx project."""
    return Path(__file__).parents[1].resolve() / "roots"


def soup_html(app: SphinxTestApp, path: str) -> BeautifulSoup:
    """Build application and parse content."""
    app.build()
    html = (app.outdir / path).read_text()
    return BeautifulSoup(html, "lxml-html")


@pytest.mark.webtest
@pytest.mark.sphinx("html", testroot="default")
def test_build(app: SphinxTestApp, status, warning):  # noqa
    soup = soup_html(app, "index.html")
    # YourTube iframe render with maxwidth,maxheight
    iframe = soup.find(
        "iframe", src="https://www.youtube.com/embed/Oyh8nuaLASA?feature=oembed"
    )
    assert iframe is not None
    assert iframe["width"] == "1200"


@pytest.mark.webtest
@pytest.mark.sphinx("html", testroot="with-fallback")
def test_build_with_fallback(app: SphinxTestApp):  # noqa
    soup = soup_html(app, "index.html")
    link = soup.find(
        "a",
        href="https://www.reddit.com/r/Python/comments/vdopqj/sphinxrevealjs_html_presentation_builder_for/",
    )
    assert link is not None


@pytest.mark.webtest
@pytest.mark.sphinx("html", testroot="default")
def test_caches(app: SphinxTestApp):  # noqa
    app.build()
    assert len(app.env.get_domain("oembedpy.adapters.sphinx").caches) == 3  # type: ignore[attr-defined]


@pytest.mark.webtest
@pytest.mark.sphinx("html", testroot="for-sphinx-cached")
def test_use_caches(app: SphinxTestApp):  # noqa
    app.build()
    assert len(app.env.get_domain("oembedpy.adapters.sphinx").caches) == 1  # type: ignore[attr-defined]
