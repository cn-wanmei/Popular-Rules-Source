from pathlib import Path
from adapters.official_json.mode_b import load_fixture, parse_official_endpoint_list


def test_taobao_mode_b_includes_apex_and_www():
    domains = load_fixture("taobao")
    assert "taobao.com" in domains
    assert "www.taobao.com" in domains
    assert "open.taobao.com" in domains
    expected = [
        x.strip()
        for x in Path("tests/fixtures/taobao/mode_b/official_endpoints_v1.expected.txt")
        .read_text()
        .splitlines()
        if x.strip()
    ]
    assert domains == sorted(expected)


def test_mode_b_parser_structured():
    body = {
        "endpoints": [
            {"hostname": "api.example.taobao.com"},
            {"hostname": "https://www.taobao.com/path"},
        ]
    }
    domains = parse_official_endpoint_list(body, (), ("taobao.com",))
    assert "api.example.taobao.com" in domains
    assert "www.taobao.com" in domains
