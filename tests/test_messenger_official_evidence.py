from source_engine.build import _source_bindings, load_services


def test_messenger_priority_wave_requires_official_evidence_and_keeps_upstream_binding():
    messenger = load_services()["services"]["messenger"]
    bindings = _source_bindings(messenger)
    policy = messenger["source_policy"]

    assert bindings[0] == {
        "url": "https://www.messenger.com/",
        "adapter": "self_built",
    }
    assert any(item["adapter"] == "upstream_rule" for item in bindings)
    assert policy["official_required"] is True
    assert set(policy["allowed_authorities"]) == {"official", "upstream"}
