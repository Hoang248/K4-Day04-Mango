from __future__ import annotations

import json
import re
from typing import Any

from tools._shared import ROOT, err


TICKET_SEED_FILE = ROOT / "helpdesk_data" / "tickets.json"
LOCAL_TICKET_DIR = ROOT / "tickets"
TICKET_ID_PATTERN = re.compile(r"^LAB-[0-9A-F]{8}$", re.IGNORECASE)
# Fields that stay inside the service desk; never returned to the requester.
INTERNAL_FIELDS = {"internal_notes"}


def _load_seed_tickets() -> tuple[list[dict[str, Any]], str | None]:
    if not TICKET_SEED_FILE.exists():
        return [], None
    data = json.loads(TICKET_SEED_FILE.read_text(encoding="utf-8"))
    return data.get("tickets", []), data.get("snapshot_at")


def _load_local_ticket(ticket_id: str) -> dict[str, Any] | None:
    """Tickets written by create_ticket live under tickets/<id>.json (gitignored)."""
    path = LOCAL_TICKET_DIR / f"{ticket_id}.json"
    if not path.exists():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {
        "ticket_id": payload.get("ticket_id", ticket_id),
        "summary": payload.get("summary", ""),
        "priority": payload.get("priority", "medium"),
        "asset_id": payload.get("asset_id"),
        "requester": None,
        "status": "open",
        "assignee": None,
        "created_at": payload.get("created_at"),
        "updated_at": payload.get("created_at"),
        "linked_incident": None,
        "history": [{"at": payload.get("created_at"), "event": "created", "note": "Ticket opened from helpdesk chat"}],
        "source": "local_ticket_store",
    }


def lookup_ticket(ticket_id: str = "", include_history: bool = False) -> dict[str, Any]:
    if not isinstance(ticket_id, str):
        return {"tool": "lookup_ticket", "error": "invalid_ticket_id_type"}
    wanted = (ticket_id or "").strip().upper()
    if not wanted:
        return {"tool": "lookup_ticket", "error": "missing_ticket_id", "message": "Provide a ticket ID such as LAB-1A2B3C4D."}
    if not TICKET_ID_PATTERN.fullmatch(wanted):
        return {
            "tool": "lookup_ticket",
            "ticket_id": wanted,
            "error": "invalid_ticket_id_format",
            "message": "Ticket IDs look like LAB-XXXXXXXX (8 hex characters).",
        }
    try:
        seed, snapshot_at = _load_seed_tickets()
        ticket = next((item for item in seed if item["ticket_id"].upper() == wanted), None)
        source = "helpdesk_data/tickets.json"
        if ticket is None:
            ticket = _load_local_ticket(wanted)
            source = "local_ticket_store"
        if ticket is None:
            return {"tool": "lookup_ticket", "ticket_id": wanted, "error": "ticket_not_found"}

        public = {key: value for key, value in ticket.items() if key not in INTERNAL_FIELDS and key != "history"}
        result: dict[str, Any] = {"tool": "lookup_ticket", "source": source, **public}
        if include_history is True:
            result["history"] = ticket.get("history", [])
        if snapshot_at:
            result["snapshot_at"] = snapshot_at
        return result
    except Exception as exc:
        return err("lookup_ticket", exc)
