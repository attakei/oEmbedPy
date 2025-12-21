"""Test cases for ``revealjs-fragments`` directive."""

from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from sphinx.environment import BuildEnvironment
from sphinx.testing.util import SphinxTestApp

from oembedpy.adapters import sphinx as T
from oembedpy.types import Link


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
    assert len(app.env.get_domain("oembedpy").caches) == 3  # type: ignore[attr-defined]


@pytest.mark.webtest
@pytest.mark.sphinx("html", testroot="for-sphinx-cached")
def test_use_caches(app: SphinxTestApp):  # noqa
    app.build()
    assert len(app.env.get_domain("oembedpy").caches) == 1  # type: ignore[attr-defined]


@pytest.mark.webtest
@pytest.mark.sphinx("html", testroot="parallel", parallel=2)
def test_build_parallel(app: SphinxTestApp, status):  # noqa
    app.build()


class TestFor_OembedDomain__merge_domaindata:
    CACHE_KEY = ("http://example.com", 1, 1)

    @pytest.mark.sphinx("html", testroot="default")
    def test_difference_items(self, app: SphinxTestApp):
        domain1 = T.OembedDomain(app.env)
        domain1.caches[self.CACHE_KEY] = Link(type="link", version="1.0", _extra={})
        domain2 = T.OembedDomain(BuildEnvironment(app))
        domain2.caches[("http://example.com", 1, 2)] = Link(
            type="link", version="1.0", _extra={}
        )
        domain1.merge_domaindata([], domain2.data)
        assert len(domain1.caches) == 2

    @pytest.mark.sphinx("html", testroot="default")
    def test_keep_main_domain(self, app: SphinxTestApp):
        domain1 = T.OembedDomain(app.env)
        domain1.caches[self.CACHE_KEY] = Link(
            type="link", version="1.0", title="Hello", _extra={}
        )
        domain2 = T.OembedDomain(BuildEnvironment(app))
        domain2.caches[self.CACHE_KEY] = Link(
            type="link", version="1.0", title="World", _extra={}
        )
        print(domain1.caches)
        domain1.merge_domaindata([], domain2.data)
        assert len(domain1.caches) == 1
        print(domain1.caches)
        assert domain1.caches[self.CACHE_KEY].title == "Hello"

    @pytest.mark.sphinx("html", testroot="default")
    def test_keep_overrides(self, app: SphinxTestApp):
        domain1 = T.OembedDomain(app.env)
        link1 = Link(type="link", version="1.0", title="Hello", _extra={})
        link1._expired = 3600
        domain1.caches[self.CACHE_KEY] = link1
        domain2 = T.OembedDomain(BuildEnvironment(app))
        link2 = Link(type="link", version="1.0", title="World", _extra={})
        link2._expired = 3601
        domain2.caches[self.CACHE_KEY] = link2
        domain1.merge_domaindata([], domain2.data)
        assert len(domain1.caches) == 1
        assert domain1.caches[("http://example.com", 1, 1)].title == "World"
