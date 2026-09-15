"""Smoke test for the team-built check_ticket_status tool.

Run from starter_v0/:  python -m tools.check_ticket_status.smoke_test
"""
from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path

from tools.check_ticket_status import tool as module
from tools.check_ticket_status.tool import check_ticket_status


def check(condition: bool, label: str) -> None:
    print(("PASS " if condition else "FAIL ") + label)
    if not condition:
        raise SystemExit(1)


def main() -> None:
    # 1. Seed ticket, no history
    result = check_ticket_status("LAB-3F2A9C1D")
    check(result.get("ticket", {}).get("status") == "in_progress", "seed ticket found with status")
    check("history" not in result, "history omitted by default")
    check("internal_notes" not in json.dumps(result), "internal_notes never leaked")

    # 2. Lower-case id + history
    result = check_ticket_status("lab-7b1e44c0", include_history=True)
    check(result.get("ticket", {}).get("ticket_id") == "LAB-7B1E44C0", "id normalised to upper-case")
    check(len(result.get("history", [])) == 3, "history returned when requested")
    check("internal_notes" not in json.dumps(result), "internal_notes never leaked (with history)")

    # 3. Clear errors
    check(check_ticket_status("").get("error") == "missing_ticket_id", "empty id -> missing_ticket_id")
    check(check_ticket_status("*").get("error") == "invalid_ticket_id", "wildcard rejected")
    check(check_ticket_status("all").get("error") == "invalid_ticket_id", "'all' rejected")
    check(check_ticket_status("LAB-00000000").get("error") == "ticket_not_found", "unknown id -> ticket_not_found")
    check(check_ticket_status(123).get("error") == "invalid_ticket_id_type", "non-string id rejected")  # type: ignore[arg-type]

    # 4. Ticket written by create_ticket into tickets/ is visible
    temp_dir = Path(tempfile.mkdtemp())
    original_dir = module.LOCAL_TICKET_DIR
    try:
        module.LOCAL_TICKET_DIR = temp_dir
        (temp_dir / "LAB-ABCDEF12.json").write_text(json.dumps({
            "ticket_id": "LAB-ABCDEF12", "summary": "Test", "priority": "medium",
            "asset_id": "LT-204", "created_at": "2026-09-15T10:00:00+00:00",
        }), encoding="utf-8")
        result = check_ticket_status("LAB-ABCDEF12", include_history=True)
        check(result.get("source") == "local_ticket_store", "locally created ticket resolved")
        check(result["ticket"]["status"] == "open", "locally created ticket starts open")
    finally:
        module.LOCAL_TICKET_DIR = original_dir
        shutil.rmtree(temp_dir, ignore_errors=True)

    print("ALL PASS")


if __name__ == "__main__":
    main()
