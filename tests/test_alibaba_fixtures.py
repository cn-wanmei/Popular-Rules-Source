from pathlib import Path
from source_engine.extract import extract_domains_from_html
from source_engine.policy import is_excluded, load_exclusion_suffixes


def _check(name: str, suffix: str, html_name: str, expected_name: str):
    root = Path(f"tests/fixtures/{name}")
    html = (root / html_name).read_text(encoding="utf-8")
    expected = [x.strip() for x in (root / expected_name).read_text().splitlines() if x.strip()]
    domains = extract_domains_from_html(html, f"https://example.{suffix}/", (), (suffix,))
    blocked = load_exclusion_suffixes()
    domains = [d for d in domains if not is_excluded(d, blocked)]
    assert domains == expected


def test_taobao_fixture():
    _check("taobao", "taobao.com", "official_open_v1.html", "official_open_v1.expected.txt")


def test_tmall_fixture():
    _check("tmall", "tmall.com", "official_www_v1.html", "official_www_v1.expected.txt")


def test_cainiao_fixture():
    _check("cainiao", "cainiao.com", "official_open_v1.html", "official_open_v1.expected.txt")
