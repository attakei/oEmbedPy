"""Test cases for ``revealjs-fragments`` directive."""

from pathlib import Path
from typing import AnyStr

import pytest
from bs4 import BeautifulSoup
from sphinx.testing.util import SphinxTestApp


@pytest.fixture(scope="module")
def rootdir():
    """Set root directory to use testing sphinx project."""
    return Path(__file__).parent.resolve() / "roots"


def soup_html(app: SphinxTestApp, path: str) -> BeautifulSoup:
    """Build application and parse content."""
    app.build()
    html: AnyStr = (app.outdir / path).read_text()
    return BeautifulSoup(html, "lxml-html")


@pytest.mark.sphinx("html", testroot="default")
def test_build(app: SphinxTestApp, status, warning):  # noqa
    soup = soup_html(app, "index.html")
    # YourTube iframe render with maxwidth,maxheight
    iframe = soup.find(
        "iframe", src="https://www.youtube.com/embed/Oyh8nuaLASA?feature=oembed"
    )
    assert iframe is not None
    assert iframe["width"] == "1200"
