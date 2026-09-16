"""Smoke test for the team-built lookup_ticket tool.

Run from starter_v0/:  python -m tools.lookup_ticket.smoke_test
Exit code 0 when every check passes.
"""
from __future__ import annotations

import sys

from tools.create_ticket.tool import TICKET_DIR, create_ticket
from tools.lookup_ticket.tool import lookup_ticket


def check(name: str, condition: bool, detail: object = "") -> bool:
    print(f"[{'PASS' if condition else 'FAIL'}] {name}" + (f" -> {detail}" if not condition else ""))
    return condition


def main() -> int:
    ok = True

    r = lookup_ticket(ticket_id="LAB-1A2B3C4D")
    ok &= check("seed ticket found", r.get("status") == "in_progress" and r.get("asset_id") == "LT-204", r)
    ok &= check("internal_notes never returned", "internal_notes" not in r, r)
    ok &= check("history hidden by default", "history" not in r, r)

    r = lookup_ticket(ticket_id="lab-9c0d1e2f", include_history=True)
    ok &= check("case-insensitive id + history", r.get("status") == "resolved" and len(r.get("history", [])) == 2, r)

    r = lookup_ticket(ticket_id="")
    ok &= check("missing id -> error", r.get("error") == "missing_ticket_id", r)

    r = lookup_ticket(ticket_id="EMP-1001")
    ok &= check("wrong format -> error", r.get("error") == "invalid_ticket_id_format", r)

    r = lookup_ticket(ticket_id="LAB-00000000")
    ok &= check("unknown id -> not found", r.get("error") == "ticket_not_found", r)

    # Integration: a ticket written by create_ticket is visible to lookup_ticket.
    created = create_ticket(summary="Smoke test ticket", priority="low", asset_id="LT-318", confirmed=True)
    tid = created.get("ticket_id", "")
    r = lookup_ticket(ticket_id=tid)
    ok &= check("create_ticket -> lookup_ticket integration", r.get("status") == "open" and r.get("source") == "local_ticket_store", r)
    try:
        (TICKET_DIR / f"{tid}.json").unlink()
    except FileNotFoundError:
        pass

    print("\nRESULT:", "ALL PASS" if ok else "SOME FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
