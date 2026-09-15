"""Streamlit chat UI for the IT Helpdesk agent.

Shows, for every turn, the real agent behaviour: which tool was called, with
which arguments, what the tool returned (or which error it raised) and which
artifact version (prompt/tools hash) produced the answer. Every turn is written
to transcripts/<id>.transcript.json in the same format as chat.py.

Run from starter_v0/:
    streamlit run app.py
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st

from chat import (
    ARTIFACTS_DIR,
    ROOT,
    now_iso,
    run_model_tool_loop,
    safe_slug,
    trim_history,
    write_transcript,
)
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version


PROVIDERS = ["openrouter", "openai", "anthropic", "gemini", "mock"]
TRANSCRIPTS_DIR = ROOT / "transcripts"
SYSTEM_PROMPT_PATH = ARTIFACTS_DIR / "system_prompt.md"
TOOLS_PATH = ARTIFACTS_DIR / "tools.yaml"

SCENARIOS = {
    "Yêu cầu bình thường": "Dịch vụ VPN production hiện có đang gặp sự cố không?",
    "Thiếu thông tin": "Kiểm tra Wi-Fi trên laptop của mình.",
    "Nhiều lượt (sửa ý)": "Kiểm tra tổng thể LT-204.  →  sau đó: 'Chỉ kiểm tra VPN thôi.'",
    "Ghi dữ liệu (tạo ticket)": "Tạo ticket VPN lỗi AUTH_TIMEOUT trên LT-204, priority high.  →  sau đó xác nhận.",
    "Bonus: tiến độ ticket": "Ticket LAB-3F2A9C1D của mình xử lý tới đâu rồi?",
}


def json_block(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, default=str)


def is_error_result(result: Any) -> bool:
    return isinstance(result, dict) and "error" in result


def new_transcript(version: str, provider_name: str, model: str | None, history_window: int, max_tool_rounds: int) -> dict[str, Any]:
    artifact_version = build_artifact_version(version, SYSTEM_PROMPT_PATH, TOOLS_PATH)
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    transcript_id = "_".join([safe_slug(version), safe_slug(provider_name), "ui", timestamp])
    return {
        "transcript_id": transcript_id,
        **artifact_version_dict(artifact_version),
        "provider": provider_name,
        "model": model,
        "system_prompt": str(SYSTEM_PROMPT_PATH.relative_to(ROOT)),
        "tools": str(TOOLS_PATH.relative_to(ROOT)),
        "history_window": history_window,
        "max_tool_rounds": max_tool_rounds,
        "interface": "streamlit",
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "turns": [],
    }


def reset_conversation() -> None:
    for key in ("transcript", "history", "messages", "provider_obj", "provider_name_loaded"):
        st.session_state.pop(key, None)


def render_tool_events(turn: dict[str, Any]) -> None:
    rounds = turn.get("rounds", [])
    if not rounds and turn.get("status") == "provider_error":
        st.error(f"Provider error: {turn.get('error')}")
        return
    for round_record in rounds:
        calls = round_record.get("tool_calls", [])
        results = round_record.get("tool_results", [])
        if not calls:
            st.caption(f"Round {round_record['round']}: model trả lời trực tiếp, không gọi tool.")
            continue
        for index, call in enumerate(calls):
            event = results[index] if index < len(results) else {}
            result = event.get("result", {})
            failed = is_error_result(result)
            icon = "❌" if failed else "🔧"
            with st.expander(f"{icon} Round {round_record['round']} · `{call['name']}`", expanded=failed):
                col_args, col_result = st.columns(2)
                with col_args:
                    st.markdown("**Input (args)**")
                    st.code(json_block(call.get("args", {})), language="json")
                with col_result:
                    st.markdown("**Kết quả / lỗi tool**")
                    if failed:
                        st.error(f"error: `{result.get('error')}` — {result.get('message', '')}")
                    st.code(json_block(result), language="json")


def render_turn(turn: dict[str, Any]) -> None:
    with st.chat_message("user"):
        st.write(turn["user"])
    with st.chat_message("assistant"):
        status = turn.get("status", "started")
        badge = {
            "answered": "🟢 answered",
            "waiting_for_user": "🟡 waiting_for_user (đang hỏi lại)",
            "max_tool_rounds": "🟠 max_tool_rounds",
            "provider_error": "🔴 provider_error",
        }.get(status, status)
        st.caption(f"{badge} · turn {turn['turn_index']} · {st.session_state.transcript['artifact_version']}")
        if turn.get("assistant_text"):
            st.write(turn["assistant_text"])
        render_tool_events(turn)


def get_provider(provider_name: str):
    if st.session_state.get("provider_name_loaded") != provider_name:
        st.session_state.provider_obj = make_provider(provider_name)
        st.session_state.provider_name_loaded = provider_name
    return st.session_state.provider_obj


def main() -> None:
    st.set_page_config(page_title="IT Helpdesk Agent — Day04", page_icon="🛠️", layout="wide")

    with st.sidebar:
        st.header("Cấu hình")
        provider_name = st.selectbox("Provider", PROVIDERS, index=0)
        if provider_name == "mock":
            st.warning("`mock` không phải LLM — chỉ để thử UI offline. Transcript từ mock không dùng làm evidence.")
        model = st.text_input("Model (để trống = mặc định của provider)", value="") or None
        version = st.text_input("Nhãn phiên bản artifact", value="v0", help="v0, v1, v2, v3 … khớp với version_log.csv")
        history_window = st.slider("History window (cặp user/assistant)", 0, 10, 5)
        max_tool_rounds = st.slider("Số vòng tool tối đa", 1, 8, 4)

        artifact_version = build_artifact_version(version, SYSTEM_PROMPT_PATH, TOOLS_PATH)
        st.divider()
        st.subheader("Phiên bản artifact")
        st.code(artifact_version.artifact_version, language="text")
        st.caption(f"prompt sha256 `{artifact_version.prompt_hash[:12]}…`  \ntools sha256 `{artifact_version.tools_hash[:12]}…`")

        declared = [item["name"] for item in load_tool_declarations(TOOLS_PATH)]
        with st.expander(f"{len(declared)} tool đã khai báo"):
            st.write(", ".join(f"`{name}`" for name in declared))
        with st.expander("Kịch bản gợi ý cho transcript"):
            for label, hint in SCENARIOS.items():
                st.markdown(f"**{label}**  \n{hint}")

        st.divider()
        if st.button("🆕 Hội thoại mới", use_container_width=True):
            reset_conversation()
            st.rerun()

    # Session state ----------------------------------------------------------
    transcript_stale = (
        "transcript" not in st.session_state
        or st.session_state.transcript["version"] != version
        or st.session_state.transcript["provider"] != provider_name
    )
    if transcript_stale:
        st.session_state.transcript = new_transcript(version, provider_name, model, history_window, max_tool_rounds)
        st.session_state.history = []
    transcript: dict[str, Any] = st.session_state.transcript
    transcript_path = TRANSCRIPTS_DIR / f"{transcript['transcript_id']}.transcript.json"

    st.title("🛠️ IT Helpdesk Agent — Northstar Labs (mock)")
    st.caption(
        f"artifact `{transcript['artifact_version']}` · provider `{provider_name}` · "
        f"transcript `{transcript_path.relative_to(ROOT)}`"
    )

    for turn in transcript["turns"]:
        render_turn(turn)

    user_text = st.chat_input("Nhập yêu cầu helpdesk…")
    if not user_text:
        return

    system_prompt = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
    openai_tools = to_openai_tools(load_tool_declarations(TOOLS_PATH))

    turn_index = len(transcript["turns"]) + 1
    messages = [
        {"role": "system", "content": system_prompt},
        *trim_history(st.session_state.history, history_window),
        {"role": "user", "content": user_text},
    ]
    turn_record: dict[str, Any] = {
        "turn_index": turn_index,
        "started_at": now_iso(),
        "user": user_text,
        "status": "started",
        "assistant_text": None,
        "rounds": [],
        "tool_events": [],
    }

    with st.chat_message("user"):
        st.write(user_text)
    with st.chat_message("assistant"), st.spinner("Agent đang xử lý…"):
        try:
            provider = get_provider(provider_name)
            result = run_model_tool_loop(
                provider=provider,
                messages=messages,
                tools=openai_tools,
                model=model,
                max_tool_rounds=max_tool_rounds,
            )
            turn_record.update(result)
            st.session_state.history.append({"role": "user", "content": user_text})
            st.session_state.history.append({"role": "assistant", "content": result["assistant_text"]})
        except Exception as exc:  # provider/config failures are evidence too
            turn_record.update({"status": "provider_error", "error": f"{type(exc).__name__}: {exc}"})

    turn_record["ended_at"] = now_iso()
    transcript["model"] = model or getattr(st.session_state.get("provider_obj"), "default_model", None)
    transcript["turns"].append(turn_record)
    write_transcript(transcript_path, transcript)
    st.rerun()


if __name__ == "__main__":
    main()
