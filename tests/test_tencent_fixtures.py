from pathlib import Path
from source_engine.extract import extract_domains_from_html
from source_engine.policy import is_excluded, load_exclusion_suffixes


def test_dingding_fixture():
    html = Path('tests/fixtures/dingding/official_open_v1.html').read_text()
    expected = [x.strip() for x in Path('tests/fixtures/dingding/official_open_v1.expected.txt').read_text().splitlines() if x.strip()]
    domains = extract_domains_from_html(html, 'https://open.dingtalk.com/', (), ('dingtalk.com',))
    blocked = load_exclusion_suffixes()
    domains = [d for d in domains if not is_excluded(d, blocked)]
    assert domains == expected


def test_qqmusic_fixture():
    html = Path('tests/fixtures/qqmusic/official_y_v1.html').read_text()
    expected = [x.strip() for x in Path('tests/fixtures/qqmusic/official_y_v1.expected.txt').read_text().splitlines() if x.strip()]
    domains = extract_domains_from_html(html, 'https://y.qq.com/', (), ('y.qq.com',))
    blocked = load_exclusion_suffixes()
    domains = [d for d in domains if not is_excluded(d, blocked)]
    assert domains == expected


def test_tencentcloud_fixture():
    html = Path('tests/fixtures/tencentcloud/official_doc_v1.html').read_text()
    expected = [x.strip() for x in Path('tests/fixtures/tencentcloud/official_doc_v1.expected.txt').read_text().splitlines() if x.strip()]
    domains = extract_domains_from_html(
        html, 'https://cloud.tencent.com/', (), ('cloud.tencent.com', 'tencentcloudapi.com'),
    )
    blocked = load_exclusion_suffixes()
    domains = [d for d in domains if not is_excluded(d, blocked)]
    assert domains == expected
    assert 'gtimg.com' not in domains
