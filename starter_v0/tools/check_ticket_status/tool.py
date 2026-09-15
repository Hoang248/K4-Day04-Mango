from __future__ import annotations

import json
import re
from typing import Any

from tools._shared import ROOT, err


SEED_FILE = ROOT / "helpdesk_data" / "tickets.json"
LOCAL_TICKET_DIR = ROOT / "tickets"
TICKET_ID_PATTERN = re.compile(r"^LAB-[A-Z0-9]{8}$")

# Fields that are safe to show to the requester. Everything else in a ticket
# record (for example internal_notes) stays inside the helpdesk.
PUBLIC_FIELDS = (
    "ticket_id", "summary", "priority", "status", "asset_id", "requester",
    "assigned_team", "created_at", "updated_at", "next_step",
)


def _load_seed_tickets() -> tuple[list[dict[str, Any]], str]:
    data = json.loads(SEED_FILE.read_text(encoding="utf-8"))
    return data["tickets"], data.get("snapshot_at", "")


def _load_local_ticket(ticket_id: str) -> dict[str, Any] | None:
    """Tickets written by create_ticket live under tickets/ and start as open."""
    path = LOCAL_TICKET_DIR / f"{ticket_id}.json"
    if not path.exists():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    created_at = payload.get("created_at", "")
    return {
        "ticket_id": payload.get("ticket_id", ticket_id),
        "summary": payload.get("summary", ""),
        "priority": payload.get("priority", "medium"),
        "status": "open",
        "asset_id": payload.get("asset_id") or "",
        "requester": "",
        "assigned_team": "Service Desk (chờ phân công)",
        "created_at": created_at,
        "updated_at": created_at,
        "next_step": "Ticket vừa được tạo và đang chờ service desk tiếp nhận.",
        "history": [{"at": created_at, "status": "open", "note": "Ticket được tạo từ trợ lý helpdesk."}],
    }


def check_ticket_status(ticket_id: str = "", include_history: bool = False) -> dict[str, Any]:
    if not isinstance(ticket_id, str):
        return {"tool": "check_ticket_status", "error": "invalid_ticket_id_type"}
    wanted = ticket_id.strip().upper()
    if not wanted:
        return {"tool": "check_ticket_status", "error": "missing_ticket_id",
                "message": "Cần một mã ticket cụ thể dạng LAB-XXXXXXXX."}
    if not TICKET_ID_PATTERN.fullmatch(wanted):
        # Also rejects wildcard/list requests such as "*", "all" or "tất cả".
        return {"tool": "check_ticket_status", "ticket_id": wanted, "error": "invalid_ticket_id",
                "message": "Mã ticket phải có dạng LAB-XXXXXXXX. Công cụ không liệt kê toàn bộ ticket."}
    try:
        seed_tickets, snapshot_at = _load_seed_tickets()
        ticket = next((item for item in seed_tickets if item["ticket_id"] == wanted), None)
        source = "seed"
        if ticket is None:
            ticket = _load_local_ticket(wanted)
            source = "local_ticket_store"
        if ticket is None:
            return {"tool": "check_ticket_status", "ticket_id": wanted, "error": "ticket_not_found"}

        result: dict[str, Any] = {
            "tool": "check_ticket_status",
            "ticket": {key: ticket.get(key, "") for key in PUBLIC_FIELDS},
            "source": source,
            "snapshot_at": snapshot_at,
        }
        if include_history is True:
            result["history"] = [
                {"at": item.get("at", ""), "status": item.get("status", ""), "note": item.get("note", "")}
                for item in ticket.get("history", [])
            ]
        return result
    except Exception as exc:
        return err("check_ticket_status", exc)
