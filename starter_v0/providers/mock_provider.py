from __future__ import annotations

import re
from typing import Any

from providers.base import ModelResponse, ToolCall


class MockProvider:
    """Deterministic, key-less provider for exercising the UI and tool loop.

    It is NOT a language model and its output is NOT evidence. run_eval.py does
    not accept it. It only routes a few obvious phrasings to tools so the UI can
    be demonstrated offline (tool → args → result → error rendering).
    """

    default_model = "mock-router"

    def complete(
        self,
        messages: list[dict[str, str]],
        tools: list[dict[str, Any]] | None = None,
        *,
        model: str | None = None,
        temperature: float = 0.0,
        tool_choice: Any | None = None,
    ) -> ModelResponse:
        last = messages[-1]["content"] if messages else ""
        if last.startswith("TOOL_RESULTS_JSON:"):
            return ModelResponse(text="(mock) Đã nhận kết quả tool ở trên; xem panel tool để đọc chi tiết.")

        text = last.lower()
        ticket = re.search(r"\blab-[a-z0-9]{8}\b", text)
        asset = re.search(r"\b(lt|dt|mb|pr|rm)-\d+\b", text)

        if ticket:
            return self._call("check_ticket_status", {
                "ticket_id": ticket.group(0).upper(),
                "include_history": "lịch sử" in text or "history" in text,
            })
        if "xác nhận" in text and "ticket" in text:
            return self._call("create_ticket", {
                "summary": last, "priority": "high" if "high" in text else "medium",
                "asset_id": asset.group(0).upper() if asset else "", "confirmed": True,
            })
        if "ticket" in text and ("tạo" in text or "mở" in text):
            return self._call("create_ticket", {
                "summary": last, "priority": "high" if "high" in text else "medium",
                "asset_id": asset.group(0).upper() if asset else "", "confirmed": False,
            })
        if "vpn" in text and "production" in text:
            return self._call("check_service_status", {"service": "vpn", "environment": "production"})
        if asset:
            check = "vpn" if "vpn" in text else "network" if "wi-fi" in text or "wifi" in text else "all"
            return self._call("inspect_device", {"asset_id": asset.group(0).upper(), "check": check})
        if "laptop" in text or "máy" in text:
            return self._call("clarify", {"question": "Bạn cho mình mã tài sản (ví dụ LT-204) nhé?", "response_type": "text"})
        return ModelResponse(text="(mock) Mình chỉ mô phỏng vài luồng; hãy dùng provider thật để có evidence.")

    @staticmethod
    def _call(name: str, args: dict[str, Any]) -> ModelResponse:
        return ModelResponse(text=None, tool_calls=[ToolCall(name=name, args=args)])
