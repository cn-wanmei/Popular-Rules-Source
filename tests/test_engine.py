from source_engine.extract import extract_domains
from source_engine.normalize import host_allowed, normalize_domain
from source_engine.policy import assess_count_change


def test_normalize_domain():
    assert normalize_domain("HTTPS://Example.COM/foo") == "example.com"
    assert normalize_domain("8.8.8.8") is None
    assert normalize_domain("https://example.com") is None


def test_host_allowed():
    assert host_allowed("api.taobao.com", tuple(), ("taobao.com",))
    assert not host_allowed("analytics.google.com", tuple(), ("taobao.com",))


def test_extract_domains():
    html = '''
      <a href="https://api.taobao.com/v1">API</a>
      <script src="https://cdn.taobao.com/a.js"></script>
      <a href="https://analytics.google.com/x">third party</a>
      api.taobao.com
    '''
    domains = extract_domains(
        html.encode(),
        "text/html",
        "https://open.taobao.com/",
        tuple(),
        ("taobao.com",),
    )
    assert domains == ["api.taobao.com", "cdn.taobao.com"]


def test_no_example_domain():
    assert normalize_domain("www.example.com") is None


def test_change_gate():
    assert assess_count_change(100, 40, 0.50, 5.0).status == "OK"
    assert assess_count_change(100, 20, 0.50, 5.0).status == "REVIEW_REMOVAL"
    assert assess_count_change(100, 0, 0.50, 5.0).status == "BLOCK_EMPTY"
