from __future__ import annotations

from source_engine.extract import extract_domains_from_html, extract_domains_from_json


def test_html_extract_respects_suffix():
    html = """
    <html><a href="https://open.taobao.com/api">x</a>
    <a href="https://static.alicdn.com/x.js">cdn</a>
    <a href="https://evil.com">no</a></html>
    """
    domains = extract_domains_from_html(
        html, "https://open.taobao.com/", (), ("taobao.com",)
    )
    assert "open.taobao.com" in domains
    assert "evil.com" not in domains


def test_json_extract():
    body = b'{"api_endpoint": "https://api.example.taobao.com/v1"}'
    domains = extract_domains_from_json(body, (), ("taobao.com",))
    assert "api.example.taobao.com" in domains
