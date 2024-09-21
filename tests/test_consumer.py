# flake8: noqa
from copy import deepcopy

import pytest

from oembedpy import consumer, types


class TestFor_RequestParameters:
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

    def test_invalid_json_with_fallback(self, httpx_mock):
        data = deepcopy(self.content_json)
        del data["version"]
        httpx_mock.add_response(json=data)
        content = consumer.fetch_content(
            "https://www.youtube.com/oembed",
            consumer.RequestParameters(
                format="xml", url="https://www.youtube.com/watch&v=Oyh8nuaLASA"
            ),
            True,
        )
        assert isinstance(content, types.HtmlOnly)

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
