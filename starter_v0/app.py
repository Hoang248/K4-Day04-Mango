"""Streamlit chat UI for the IT Helpdesk agent.

Reuses the agent loop and transcript format from chat.py so the UI, the CLI
and run_eval.py all exercise the same tool registry and artifacts.

Run from starter_v0/:
    streamlit run app.py
"""
from __future__ import annotations

import json
import re
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


TRANSCRIPTS_DIR = ROOT / "transcripts"
PROVIDERS = ["openrouter", "openai", "anthropic", "gemini"]
DEFAULT_VERSION = "v4"
VERSION_PATTERN = re.compile(r"^v\d+$")


# --------------------------------------------------------------------------- #
# Session helpers
# --------------------------------------------------------------------------- #
def new_session(provider_name: str, model: str | None, version: str, history_window: int, max_tool_rounds: int) -> None:
    system_prompt_path = ARTIFACTS_DIR / "system_prompt.md"
    tools_path = ARTIFACTS_DIR / "tools.yaml"
    artifact_version = build_artifact_version(version, system_prompt_path, tools_path)
    provider = make_provider(provider_name)
    selected_model = model or getattr(provider, "default_model", None)

    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    transcript_id = "_".join(["ui", safe_slug(version), safe_slug(provider_name), timestamp])
    transcript: dict[str, Any] = {
        "transcript_id": transcript_id,
        **artifact_version_dict(artifact_version),
        "provider": provider_name,
        "model": selected_model,
        "system_prompt": str(system_prompt_path),
        "tools": str(tools_path),
        "history_window": history_window,
        "max_tool_rounds": max_tool_rounds,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "turns": [],
    }

    st.session_state.update({
        "provider_name": provider_name,
        "provider": provider,
        "model": model,
        "selected_model": selected_model,
        "version": version,
        "artifact_version": artifact_version,
        "system_prompt": system_prompt_path.read_text(encoding="utf-8"),
        "openai_tools": to_openai_tools(load_tool_declarations(tools_path)),
        "history_window": history_window,
        "max_tool_rounds": max_tool_rounds,
        "history": [],
        "turns": [],
        "transcript": transcript,
        "transcript_path": TRANSCRIPTS_DIR / f"{transcript_id}.transcript.json",
        "error": None,
    })


def session_ready() -> bool:
    return "provider" in st.session_state


def run_turn(user_text: str) -> dict[str, Any]:
    state = st.session_state
    messages = [
        {"role": "system", "content": state.system_prompt},
        *trim_history(state.history, state.history_window),
        {"role": "user", "content": user_text},
    ]
    turn_record: dict[str, Any] = {
        "turn_index": len(state.turns) + 1,
        "started_at": now_iso(),
        "user": user_text,
        "status": "started",
        "assistant_text": None,
        "rounds": [],
        "tool_events": [],
    }
    try:
        result = run_model_tool_loop(
            provider=state.provider,
            messages=messages,
            tools=state.openai_tools,
            model=state.model,
            max_tool_rounds=state.max_tool_rounds,
        )
        turn_record.update(result)
        state.history.append({"role": "user", "content": user_text})
        state.history.append({"role": "assistant", "content": result["assistant_text"]})
    except Exception as exc:  # provider/network failure must be visible, not hidden
        turn_record.update({"status": "provider_error", "error": f"{type(exc).__name__}: {exc}"})

    turn_record["ended_at"] = now_iso()
    state.turns.append(turn_record)
    state.transcript["turns"].append(turn_record)
    write_transcript(state.transcript_path, state.transcript)
    return turn_record


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #
def result_is_error(result: Any) -> bool:
    return isinstance(result, dict) and ("error" in result)


def render_tool_event(event: dict[str, Any], key: str) -> None:
    tool = event.get("tool", "?")
    args = event.get("args", {})
    result = event.get("result", {})
    is_error = result_is_error(result)
    awaiting = bool(isinstance(result, dict) and result.get("awaiting_user"))

    if is_error:
        label = f"🔴 `{tool}` → error: `{result.get('error')}`"
    elif awaiting:
        label = f"🟡 `{tool}` → đang chờ bạn trả lời"
    else:
        label = f"🟢 `{tool}` → ok"

    with st.expander(label, expanded=is_error or awaiting):
        st.markdown("**Args**")
        st.code(json.dumps(args, ensure_ascii=False, indent=2), language="json")
        st.markdown("**Error**" if is_error else "**Result**")
        st.code(json.dumps(result, ensure_ascii=False, indent=2, default=str), language="json")


def render_turn(turn: dict[str, Any]) -> None:
    idx = turn["turn_index"]
    with st.chat_message("user"):
        st.write(turn["user"])

    with st.chat_message("assistant"):
        status = turn.get("status")
        if status == "provider_error":
            st.error(f"Provider error: {turn.get('error')}")
            return

        for round_record in turn.get("rounds", []):
            round_no = round_record.get("round")
            events = round_record.get("tool_results", [])
            if events:
                st.caption(f"Round {round_no} · {len(events)} tool call(s)")
                for event_index, event in enumerate(events):
                    render_tool_event(event, key=f"t{idx}-r{round_no}-e{event_index}")

        text = turn.get("assistant_text") or ""
        if status == "waiting_for_user":
            st.info(f"❓ {text}")
        elif status == "max_tool_rounds":
            st.warning(text)
        else:
            st.markdown(text)
        st.caption(f"status: `{status}` · version: `{st.session_state.artifact_version.artifact_version}`")


def render_sidebar() -> None:
    st.sidebar.title("IT Helpdesk Agent")

    with st.sidebar.form("session_form"):
        provider_name = st.selectbox("Provider", PROVIDERS, index=PROVIDERS.index(st.session_state.get("provider_name", "openrouter")))
        model = st.text_input("Model (để trống = mặc định của provider)", value=st.session_state.get("model") or "")
        version = st.text_input("Nhãn version", value=st.session_state.get("version", DEFAULT_VERSION))
        history_window = st.number_input("History window (cặp lượt)", min_value=0, max_value=20, value=st.session_state.get("history_window", 5))
        max_tool_rounds = st.number_input("Max tool rounds", min_value=1, max_value=10, value=st.session_state.get("max_tool_rounds", 4))
        submitted = st.form_submit_button("🔄 Phiên mới", use_container_width=True)

    if submitted:
        if not VERSION_PATTERN.fullmatch(version.strip()):
            st.sidebar.error("Nhãn version phải dạng v0, v1, v2 …")
        else:
            try:
                new_session(provider_name, model.strip() or None, version.strip(), int(history_window), int(max_tool_rounds))
                st.rerun()
            except Exception as exc:
                st.sidebar.error(f"Không khởi tạo được provider: {type(exc).__name__}: {exc}")

    if session_ready():
        av = st.session_state.artifact_version
        st.sidebar.divider()
        st.sidebar.markdown("**Phiên đang chạy**")
        st.sidebar.code(
            f"version          : {av.version}\n"
            f"artifact_version : {av.artifact_version}\n"
            f"prompt_hash      : {av.prompt_hash[:16]}…\n"
            f"tools_hash       : {av.tools_hash[:16]}…\n"
            f"provider/model   : {st.session_state.provider_name} / {st.session_state.selected_model}\n"
            f"tools declared   : {len(st.session_state.openai_tools)}",
            language="text",
        )
        st.sidebar.markdown("**Transcript**")
        st.sidebar.code(str(st.session_state.transcript_path.relative_to(ROOT)), language="text")
        st.sidebar.caption(f"{len(st.session_state.turns)} lượt đã lưu")


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main() -> None:
    st.set_page_config(page_title="IT Helpdesk Agent", page_icon="🛠️", layout="wide")
    render_sidebar()

    st.title("🛠️ IT Helpdesk Agent — Northstar Labs (mock)")
    st.caption("Mỗi lượt hiển thị tool → args → result/error, phiên bản artifact và được ghi ra transcript.")

    if not session_ready():
        st.info("Chọn provider/version ở sidebar rồi bấm **Phiên mới** để bắt đầu. Cần API key trong `starter_v0/.env`.")
        return

    for turn in st.session_state.turns:
        render_turn(turn)

    last_status = st.session_state.turns[-1]["status"] if st.session_state.turns else None
    placeholder = "Trả lời câu hỏi của agent…" if last_status == "waiting_for_user" else "Nhập yêu cầu…"
    user_text = st.chat_input(placeholder)
    if user_text and user_text.strip():
        with st.spinner("Agent đang xử lý…"):
            run_turn(user_text.strip())
        st.rerun()


if __name__ == "__main__" or True:  # streamlit executes the module top-level
    main()
