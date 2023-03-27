# flake8: noqa

import httpx
import pytest

from oembedpy import provider


@pytest.mark.webtest
def test_configure_from_http():
    data_json = httpx.get("https://oembed.com/providers.json").json()
    provider.ProviderRegistry.from_dict(data_json)


class TestFor_Endpoint:
    target = provider.Endpoint(
        url="https://example.com/oembed",
        schemes=["https://example.com/contents/*"],
    )

    @pytest.mark.parametrize(
        "url,expected",
        [
            ("https://example.com/", False),
            ("https://example.com/contents/first", True),
        ],
    )
    def test__is_match(self, url, expected):
        assert self.target.is_match(url) is expected


class TestFor_Provider:
    target = provider.Provider(
        name="Example",
        url="https://example.com",
        endpoints=[
            provider.Endpoint(
                url="https://example.com/oembed",
                schemes=["https://example.com/contents/*"],
            ),
        ],
    )

    @pytest.mark.parametrize(
        "url,expected",
        [
            ("https://example.com/", False),
            ("https://example.com/contents/first", True),
        ],
    )
    def test__find_endpoint(self, url, expected):
        assert isinstance(self.target.find_endpoint(url), str) is expected
