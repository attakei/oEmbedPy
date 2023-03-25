# flake8: noqa
import pytest

from oembedpy import consumer, types


class TestFor_RequestParamaters:
    def test__to_dict_default_only(self):
        params = consumer.RequestParameters(url="http://example.com")
        data = params.to_dict()
        assert data["url"] == "http://example.com"
        assert "format" not in data

    def test__to_dict_with_max_width(self):
        params = consumer.RequestParameters(url="http://example.com", max_width=100)
        data = params.to_dict()
        assert data["maxwidth"] == "100"

    def test__to_dict_with_max_height(self):
        params = consumer.RequestParameters(url="http://example.com", max_height=100)
        data = params.to_dict()
        assert data["maxheight"] == "100"

    def test__to_dict_with_format(self):
        params = consumer.RequestParameters(url="http://example.com", format="json")
        data = params.to_dict()
        assert data["format"] == "json"


class TestFor_fetch_content:
    content_json = {
        "type": "video",
        "version": "1.0",
        "html": '<iframe width="200" height="113" src="https://example.com" ></iframe>',
        "width": 200,
        "height": 113,
        "author_name": "attakei",
        "author_url": "https://www.youtube.com/@attakei",
    }

    def test_json_content(self, httpx_mock):
        httpx_mock.add_response(json=self.content_json)
        content = consumer.fetch_content(
            "https://www.youtube.com/oembed",
            consumer.RequestParameters(
                format="json", url="https://www.youtube.com/watch&v=Oyh8nuaLASA"
            ),
        )
        assert isinstance(content, types.Video)
        assert content.author_name == "attakei"

    def test_xml_content(self, httpx_mock):
        httpx_mock.add_response(
            content=b"""
                <?xml version="1.0" encoding="utf-8"?>
                <oembed>
                    <title>Example</title>
                    <author_name>attakei</author_name>
                    <author_url>https://www.youtube.com/@attakei</author_url>
                    <type>video</type>
                    <height>113</height>
                    <width>200</width>
                    <version>1.0</version>
                    <html>&lt;iframe width=&quot;200&quot; height=&quot;113&quot; src=&quot;https://example.com/&quot;&gt;&lt;/iframe&gt;</html>
                </oembed>
            """.strip(),
            headers={"Content-Type": "application/xml"},
        )
        content = consumer.fetch_content(
            "https://www.youtube.com/oembed",
            consumer.RequestParameters(
                format="xml", url="https://www.youtube.com/watch&v=Oyh8nuaLASA"
            ),
        )
        assert isinstance(content, types.Video)
        assert content.author_name == "attakei"

    def test_invalid_format(self, httpx_mock):
        httpx_mock.add_response(html="<html><head></head><doby></body></html>")
        with pytest.raises(ValueError):
            consumer.fetch_content(
                "https://www.youtube.com/oembed",
                consumer.RequestParameters(
                    format="xml", url="https://www.youtube.com/watch&v=Oyh8nuaLASA"
                ),
            )

    def test_invalid_json(self, httpx_mock):
        httpx_mock.add_response(json={})
        with pytest.raises(ValueError):
            consumer.fetch_content(
                "https://www.youtube.com/oembed",
                consumer.RequestParameters(
                    format="xml", url="https://www.youtube.com/watch&v=Oyh8nuaLASA"
                ),
            )

    def test_invalid_xml(self, httpx_mock):
        httpx_mock.add_response(
            content=b"""
                <?xml version="1.0" encoding="utf-8"?>
                <x>
                    <title>Example</title>
                </x>
            """.strip(),
            headers={"Content-Type": "application/xml"},
        )
        with pytest.raises(ValueError):
            consumer.fetch_content(
                "https://www.youtube.com/oembed",
                consumer.RequestParameters(
                    format="xml", url="https://www.youtube.com/watch&v=Oyh8nuaLASA"
                ),
            )


class TestFor_discover:
    def test_json_content(self, httpx_mock):
        html = """
            <html>
                <head>
                    <link
                        rel="alternate"
                        type="application/json+oembed"
                        href="https://example.com/oembed?format=json&amp;url=https%3A%2F%2Fexample.com%2Fcontent" 
                        title="Example"
                    >
                </head>
                <body></body>
            </html>
        """
        httpx_mock.add_response(text=html)
        url = consumer.discover("https://example.com/content")
        assert url.startswith("https://example.com/oembed?format=json")

    def test_xml_content(self, httpx_mock):
        html = """
            <html>
                <head>
                    <link
                        rel="alternate"
                        type="text/xml+oembed"
                        href="https://example.com/oembed?format=xml&amp;url=https%3A%2F%2Fexample.com%2Fcontent"
                        title="Example"
                    >
                </head>
                <body></body>
            </html>
        """
        httpx_mock.add_response(text=html)
        url = consumer.discover("https://example.com/content")
        assert url.startswith("https://example.com/oembed?format=xml")

    def test_json_from_multiple(self, httpx_mock):
        html = """
            <html>
                <head>
                    <link
                        rel="alternate"
                        type="application/json+oembed"
                        href="https://example.com/oembed?format=json&amp;url=https%3A%2F%2Fexample.com%2Fcontent" 
                        title="Example"
                    >
                    <link
                        rel="alternate"
                        type="text/xml+oembed"
                        href="https://example.com/oembed?format=xml&amp;url=https%3A%2F%2Fexample.com%2Fcontent"
                        title="Example"
                    >
                </head>
                <body></body>
            </html>
        """
        httpx_mock.add_response(text=html)
        url = consumer.discover("https://example.com/content")
        assert url.startswith("https://example.com/oembed?format=json")

    def test_xml_from_multiple(self, httpx_mock):
        html = """
            <html>
                <head>
                    <link
                        rel="alternate"
                        type="text/xml+oembed"
                        href="https://example.com/oembed?format=xml&amp;url=https%3A%2F%2Fexample.com%2Fcontent"
                        title="Example"
                    >
                    <link
                        rel="alternate"
                        type="application/json+oembed"
                        href="https://example.com/oembed?format=json&amp;url=https%3A%2F%2Fexample.com%2Fcontent" 
                        title="Example"
                    >
                </head>
                <body></body>
            </html>
        """
        httpx_mock.add_response(text=html)
        url = consumer.discover("https://example.com/content")
        assert url.startswith("https://example.com/oembed?format=xml")
