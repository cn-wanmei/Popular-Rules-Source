from __future__ import annotations

from source_engine.status import _render_blocked_board


def test_blocked_board_is_derived_from_lifecycle_report() -> None:
    report = {
        "services": {
            "cloudflare": {
                "state": "review",
                "release_state": "BLOCKED",
                "domain_count": 0,
            },
            "candidate-empty": {
                "state": "review",
                "release_state": "CANDIDATE",
                "domain_count": 0,
            },
            "ready": {
                "state": "verified",
                "release_state": "CANDIDATE",
                "domain_count": 3,
            },
        }
    }

    board = _render_blocked_board(report, generated_at="2026-11-10T12:00:00Z")

    assert "generated_at: `2026-11-10T12:00:00Z`" in board
    assert "| cloudflare | REVIEW | BLOCKED | 0 |" in board
    assert "| candidate-empty | REVIEW | CANDIDATE | 0 |" in board
    assert "| ready | VERIFIED | CANDIDATE | 3 |" not in board
    assert "禁止用空结果覆盖 Last Known Good" in board
