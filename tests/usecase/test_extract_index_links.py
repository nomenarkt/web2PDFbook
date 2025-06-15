from unittest.mock import Mock, patch

from web2pdfbook.crawler.usecase.extract_index_links import extract_index_links


def test_extract_index_links_sitemap():
    html_index = '<link rel="sitemap" href="/sitemap.xml">'
    sitemap_xml = (
        "<urlset>"
        "<url><loc>https://example.com/index.html</loc></url>"
        "<url><loc>https://example.com/page.html</loc></url>"
        "<url><loc>https://other.com/out.html</loc></url>"
        "<url><loc>https://example.com/img.png</loc></url>"
        "</urlset>"
    )

    responses = {
        "https://example.com/": Mock(
            status_code=200, text=html_index, headers={"Content-Type": "text/html"}
        ),
        "https://example.com/sitemap.xml": Mock(
            status_code=200,
            text=sitemap_xml,
            headers={"Content-Type": "text/xml"},
        ),
    }

    def fake_get(url, *args, **kwargs):
        return responses[url]

    with patch(
        "web2pdfbook.crawler.usecase.extract_index_links.requests.get",
        side_effect=fake_get,
    ):
        result = extract_index_links("https://example.com/")

    assert result.links == [
        "https://example.com/index.html",
        "https://example.com/page.html",
    ]


def test_extract_index_links_nav():
    html_index = (
        '<nav><a href="/index.html">idx</a></nav>'
        '<div id="sidebar"><a href="/page.html">p</a><a href="/skip.png">i</a></div>'
        '<div class="sphinxsidebar"><a href="https://example.com/foo.html">f</a></div>'
        '<div role="navigation"><a href="http://example.com/bar.html">b</a></div>'
        '<a href="https://other.com/out.html">o</a>'
    )

    responses = {
        "https://example.com/": Mock(
            status_code=200, text=html_index, headers={"Content-Type": "text/html"}
        ),
    }

    def fake_get(url, *args, **kwargs):
        return responses[url]

    with patch(
        "web2pdfbook.crawler.usecase.extract_index_links.requests.get",
        side_effect=fake_get,
    ):
        result = extract_index_links("https://example.com/")

    assert result.links == [
        "https://example.com/index.html",
        "https://example.com/page.html",
        "https://example.com/foo.html",
        "http://example.com/bar.html",
    ]


def test_extract_index_links_fallback():
    responses = {
        "https://example.com/": Mock(
            status_code=200, text="<p>empty</p>", headers={"Content-Type": "text/html"}
        ),
    }

    def fake_get(url, *args, **kwargs):
        return responses[url]

    with patch(
        "web2pdfbook.crawler.usecase.extract_index_links.requests.get",
        side_effect=fake_get,
    ):
        with patch(
            "web2pdfbook.crawler.usecase.extract_index_links.extract_links"
        ) as fallback:
            fallback.return_value = Mock(links=["https://example.com/"])
            result = extract_index_links("https://example.com/")
            fallback.assert_called_once_with("https://example.com/")

    assert result.links == ["https://example.com/"]
