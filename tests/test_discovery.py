# flake8: noqa
from pytest import raises

from oembedpy import discovery


class TestFor_find_from_content:
    def test_ng(self, httpx_mock):
        httpx_mock.add_response(html="<html><head></head><body></body></html>")
        with raises(ValueError):
            discovery.find_from_content("http://example.com")

    def test_json_content(self, httpx_mock):
        html = """
            <html>
                <head>
                    <link
                        rel="alternate"
                        type="application/json+oembed"
                        href="https://example.com/oembed?format=json&url=https%3A%2F%2Fexample.com%2Fcontent"
                        title="Example"
                    >
                </head>
                <body></body>
            </html>
        """
        httpx_mock.add_response(text=html)
        url, params = discovery.find_from_content("http://example.com")
        assert url == "https://example.com/oembed"
        assert params.format == "json"

    def test_xml_content(self, httpx_mock):
        html = """
            <html>
                <head>
                    <link
                        rel="alternate"
                        type="text/xml+oembed"
                        href="https://example.com/oembed?format=xml&url=https%3A%2F%2Fexample.com%2Fcontent"
                        title="Example"
                    >
                </head>
                <body></body>
            </html>
        """
        httpx_mock.add_response(text=html)
        url, params = discovery.find_from_content("http://example.com")
        assert url == "https://example.com/oembed"
        assert params.format == "xml"

    def test_json_from_multiple(self, httpx_mock):
        html = """
            <html>
                <head>
                    <link
                        rel="alternate"
                        type="application/json+oembed"
                        href="https://example.com/oembed?format=json&url=https%3A%2F%2Fexample.com%2Fcontent"
                        title="Example"
                    >
                    <link
                        rel="alternate"
                        type="text/xml+oembed"
                        href="https://example.com/oembed?format=xml&url=https%3A%2F%2Fexample.com%2Fcontent"
                        title="Example"
                    >
                </head>
                <body></body>
            </html>
        """
        httpx_mock.add_response(text=html)
        url, params = discovery.find_from_content("http://example.com")
        assert url == "https://example.com/oembed"
        assert params.format == "json"

    def test_xml_from_multiple(self, httpx_mock):
        html = """
            <html>
                <head>
                    <link
                        rel="alternate"
                        type="text/xml+oembed"
                        href="https://example.com/oembed?format=xml&url=https%3A%2F%2Fexample.com%2Fcontent"
                        title="Example"
                    >
                    <link
                        rel="alternate"
                        type="application/json+oembed"
                        href="https://example.com/oembed?format=json&url=https%3A%2F%2Fexample.com%2Fcontent"
                        title="Example"
                    >
                </head>
                <body></body>
            </html>
        """
        httpx_mock.add_response(text=html)
        url, params = discovery.find_from_content("http://example.com")
        assert url == "https://example.com/oembed"
        assert params.format == "xml"
