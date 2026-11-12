from pathlib import Path


def test_cloudflare_candidate_artifacts_do_not_trigger_durable_seal() -> None:
    root = Path(__file__).resolve().parents[1]
    workflow = (root / ".github" / "workflows" / "durable-source-bridge.yml").read_text(encoding="utf-8")
    assert '"generated/source/cloudflare/**"' in workflow
    assert '"snapshots/snap-cloudflare-*/**"' in workflow
    assert '"tests/**"' in workflow


def test_messenger_candidate_artifacts_do_not_trigger_durable_seal() -> None:
    root = Path(__file__).resolve().parents[1]
    workflow = (root / ".github" / "workflows" / "durable-source-bridge.yml").read_text(encoding="utf-8")
    assert '"generated/source/messenger/**"' in workflow
    assert '"snapshots/snap-messenger-*/**"' in workflow
    assert "workflow_dispatch:" in workflow
