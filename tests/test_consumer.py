# flake8: noqa
from oembedpy import consumer, types


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

    def test_json_from_multiple(self, httpx_mock):
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
        assert url.startswith("https://example.com/oembed?format=json")
