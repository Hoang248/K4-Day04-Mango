"""Streamlit chat UI for the IT Helpdesk agent.

Reuses the agent loop and transcript format from chat.py so the UI, the CLI
and run_eval.py all exercise the same tool registry and artifacts.

Run from starter_v0/:
    streamlit run app.py
"""
from __future__ import annotations

import html
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
VERSIONS_DIR = ARTIFACTS_DIR / "versions"
PROVIDERS = ["openrouter", "openai", "anthropic", "gemini"]
VERSION_PATTERN = re.compile(r"^v\d+$")


def list_versions() -> list[str]:
    """Versions with a snapshot in artifacts/versions/<vN>/, plus the current artifacts/ as the latest."""
    snapshots = sorted(
        (d.name for d in VERSIONS_DIR.iterdir() if d.is_dir() and VERSION_PATTERN.fullmatch(d.name)),
        key=lambda v: int(v[1:]),
    ) if VERSIONS_DIR.exists() else []
    latest = f"v{int(snapshots[-1][1:]) + 1}" if snapshots else "v0"
    return snapshots + [latest]


def artifact_paths(version: str) -> tuple[Path, Path]:
    """Snapshot folder if it exists and is complete; otherwise the live artifacts/ files."""
    folder = VERSIONS_DIR / version
    prompt, tools = folder / "system_prompt.md", folder / "tools.yaml"
    if prompt.exists() and tools.exists():
        return prompt, tools
    return ARTIFACTS_DIR / "system_prompt.md", ARTIFACTS_DIR / "tools.yaml"


def snapshot_missing(version: str) -> bool:
    folder = VERSIONS_DIR / version
    return folder.exists() and not ((folder / "system_prompt.md").exists() and (folder / "tools.yaml").exists())


# --------------------------------------------------------------------------- #
# Session helpers
# --------------------------------------------------------------------------- #
def new_session(provider_name: str, model: str | None, version: str, history_window: int, max_tool_rounds: int) -> None:
    system_prompt_path, tools_path = artifact_paths(version)
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
CSS = """
<style>
:root {
  --ok: #16a34a; --ok-bg: #f0fdf4;
  --err: #dc2626; --err-bg: #fef2f2;
  --wait: #d97706; --wait-bg: #fffbeb;
  --ink: #0f172a; --muted: #64748b; --line: #e2e8f0; --card: #ffffff; --soft: #f8fafc;
}
@media (prefers-color-scheme: dark) {
  :root { --ink: #e2e8f0; --muted: #94a3b8; --line: #334155; --card: #1e293b; --soft: #0f172a;
          --ok-bg: #052e16; --err-bg: #450a0a; --wait-bg: #451a03; }
}
.block-container { padding-top: 1.2rem; max-width: 1100px; }
.hd { display:flex; align-items:center; gap:14px; margin-bottom:.25rem; }
.hd .logo { font-size:34px; line-height:1; }
.hd h1 { margin:0; font-size:1.75rem; letter-spacing:-.01em; color:var(--ink); }
.hd .sub { color:var(--muted); font-size:.9rem; margin-top:2px; }
.chips { display:flex; flex-wrap:wrap; gap:6px; margin:.35rem 0 1rem; }
.chip { display:inline-flex; align-items:center; gap:6px; padding:3px 10px; border-radius:999px;
        font-size:.78rem; font-weight:600; border:1px solid var(--line); background:var(--card); color:var(--ink); }
.chip.v { background:#eef2ff; border-color:#c7d2fe; color:#3730a3; }
.chip.mono { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-weight:500; }
.chip.ok { background:var(--ok-bg); border-color:var(--ok); color:var(--ok); }
.chip.err { background:var(--err-bg); border-color:var(--err); color:var(--err); }
.chip.wait { background:var(--wait-bg); border-color:var(--wait); color:var(--wait); }
.tool { border:1px solid var(--line); border-left:4px solid var(--ok); border-radius:10px;
        background:var(--card); padding:10px 14px 4px; margin:8px 0 10px; }
.tool.err { border-left-color:var(--err); }
.tool.wait { border-left-color:var(--wait); }
.tool .row { display:flex; align-items:center; gap:10px; flex-wrap:wrap; }
.tool .name { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-weight:700; font-size:.95rem; color:var(--ink); }
.tool .arrow { color:var(--muted); }
.tool .lbl { font-size:.72rem; text-transform:uppercase; letter-spacing:.08em; color:var(--muted); margin:8px 0 2px; }
.round { font-size:.75rem; color:var(--muted); text-transform:uppercase; letter-spacing:.08em; margin-top:4px; }
.foot { display:flex; gap:6px; flex-wrap:wrap; margin-top:6px; }
.welcome { border:1px dashed var(--line); border-radius:14px; padding:22px 24px; background:var(--soft); }
.welcome h3 { margin:0 0 4px; color:var(--ink); }
.welcome p { margin:0 0 10px; color:var(--muted); }
[data-testid="stSidebar"] .kv { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size:.75rem;
  color:var(--muted); line-height:1.5; word-break:break-all; }
[data-testid="stSidebar"] .kv b { color:var(--ink); font-weight:600; }
div[data-testid="stCodeBlock"] pre { font-size:.8rem; white-space:pre; overflow-x:auto; }
</style>
"""

QUICK_PROMPTS = [
    ("🌐 Trạng thái dịch vụ", "Dịch vụ VPN production hiện có đang gặp sự cố không?"),
    ("❓ Thiếu thông tin", "Kiểm tra VPN trên máy của tôi giúp, nó không kết nối được."),
    ("💻 Kiểm tra thiết bị", "Chỉ xem phần network của máy LT-240."),
    ("📚 Tìm hướng dẫn", "Outlook không mở được profile, tìm hướng dẫn xử lý."),
    ("🎫 Tạo ticket", "Tạo ticket cho lỗi VPN AUTH_TIMEOUT trên LT-204, mức high."),
    ("🔎 Tra cứu ticket", "Ticket LAB-1A2B3C4D đang ở trạng thái nào và ai đang xử lý?"),
]

STATUS_META = {
    "answered": ("ok", "✔ answered"),
    "waiting_for_user": ("wait", "⏳ waiting for user"),
    "max_tool_rounds": ("wait", "⚠ max tool rounds"),
    "provider_error": ("err", "✖ provider error"),
}


def esc(text: Any) -> str:
    return html.escape(str(text), quote=True)


def chip(text: str, kind: str = "") -> str:
    return f'<span class="chip {kind}">{esc(text)}</span>'


def result_is_error(result: Any) -> bool:
    return isinstance(result, dict) and ("error" in result)


def parse_model_json(text: str) -> dict[str, Any] | None:
    """v0-style replies are raw JSON; surface `reply` nicely but keep the raw text available."""
    candidate = text.strip()
    if not (candidate.startswith("{") and candidate.endswith("}")):
        return None
    try:
        data = json.loads(candidate)
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) and "reply" in data else None


def render_tool_event(event: dict[str, Any], key: str) -> None:
    tool = event.get("tool", "?")
    args = event.get("args", {})
    result = event.get("result", {})
    is_error = result_is_error(result)
    awaiting = bool(isinstance(result, dict) and result.get("awaiting_user"))
    kind = "err" if is_error else "wait" if awaiting else "ok"
    status = (
        f"error: {result.get('error')}" if is_error
        else "đang chờ bạn trả lời" if awaiting
        else "ok"
    )

    st.markdown(
        f'<div class="tool {kind}"><div class="row">'
        f'<span class="name">{esc(tool)}</span><span class="arrow">→</span>{chip(status, kind)}'
        f"</div></div>",
        unsafe_allow_html=True,
    )
    with st.expander("Xem args / result", expanded=is_error or awaiting):
        col_args, col_res = st.columns([1, 2])
        with col_args:
            st.markdown('<div class="lbl">Args</div>', unsafe_allow_html=True)
            st.code(json.dumps(args, ensure_ascii=False, indent=2), language="json")
        with col_res:
            st.markdown(f'<div class="lbl">{"Error" if is_error else "Result"}</div>', unsafe_allow_html=True)
            st.code(json.dumps(result, ensure_ascii=False, indent=2, default=str), language="json")


def render_turn(turn: dict[str, Any]) -> None:
    idx = turn["turn_index"]
    with st.chat_message("user", avatar="🧑‍💻"):
        st.write(turn["user"])

    with st.chat_message("assistant", avatar="🛠️"):
        status = turn.get("status")
        if status == "provider_error":
            st.error(f"Provider error: {turn.get('error')}")
            return

        for round_record in turn.get("rounds", []):
            round_no = round_record.get("round")
            events = round_record.get("tool_results", [])
            if events:
                st.markdown(f'<div class="round">Round {round_no} · {len(events)} tool call(s)</div>', unsafe_allow_html=True)
                for event_index, event in enumerate(events):
                    render_tool_event(event, key=f"t{idx}-r{round_no}-e{event_index}")

        text = turn.get("assistant_text") or ""
        if status == "waiting_for_user":
            st.info(f"❓ {text}")
        elif status == "max_tool_rounds":
            st.warning(text)
        else:
            parsed = parse_model_json(text)
            if parsed:
                st.markdown(parsed.get("reply") or "")
                with st.expander("Raw model output (JSON)"):
                    st.code(json.dumps(parsed, ensure_ascii=False, indent=2), language="json")
            else:
                st.markdown(text)

        kind, label = STATUS_META.get(status, ("", str(status)))
        st.markdown(
            '<div class="foot">' + chip(label, kind)
            + chip(st.session_state.artifact_version.artifact_version, "v mono")
            + chip(f"turn {idx}", "mono") + "</div>",
            unsafe_allow_html=True,
        )


def render_sidebar() -> None:
    st.sidebar.markdown("### ⚙️ Phiên chat")

    with st.sidebar.form("session_form", border=False):
        provider_name = st.selectbox("Provider", PROVIDERS, index=PROVIDERS.index(st.session_state.get("provider_name", "openrouter")))
        model = st.text_input("Model", value=st.session_state.get("model") or "", placeholder="để trống = mặc định của provider")
        versions = list_versions()
        current_version = st.session_state.get("version", versions[-1])
        version = st.selectbox(
            "Version (artifact snapshot)",
            versions,
            index=versions.index(current_version) if current_version in versions else len(versions) - 1,
            help="v0–v3 đọc từ artifacts/versions/<vN>/; version mới nhất đọc artifacts/ hiện tại.",
        )
        c1, c2 = st.columns(2)
        history_window = c1.number_input("History window", min_value=0, max_value=20, value=st.session_state.get("history_window", 5))
        max_tool_rounds = c2.number_input("Tool rounds", min_value=1, max_value=10, value=st.session_state.get("max_tool_rounds", 4))
        submitted = st.form_submit_button("🔄 Phiên mới", use_container_width=True, type="primary")

    if submitted:
        if snapshot_missing(version):
            st.sidebar.error(
                f"Chưa có artifact cho {version}: cần system_prompt.md + tools.yaml trong "
                f"artifacts/versions/{version}/ (xem artifacts/versions/README.md)."
            )
        else:
            try:
                new_session(provider_name, model.strip() or None, version.strip(), int(history_window), int(max_tool_rounds))
                st.rerun()
            except Exception as exc:
                st.sidebar.error(f"Không khởi tạo được provider: {type(exc).__name__}: {exc}")

    if session_ready():
        av = st.session_state.artifact_version
        tr = st.session_state.transcript
        st.sidebar.divider()
        st.sidebar.markdown("### 🧾 Phiên đang chạy")
        st.sidebar.markdown(
            chip(av.version, "v") + chip(f"{len(st.session_state.openai_tools)} tools") + chip(f"{len(st.session_state.turns)} lượt"),
            unsafe_allow_html=True,
        )
        st.sidebar.markdown(
            '<div class="kv">'
            f"<b>artifact</b> {esc(av.artifact_version)}<br>"
            f"<b>prompt</b> {esc(av.prompt_hash[:16])}…<br>"
            f"<b>tools</b> {esc(av.tools_hash[:16])}…<br>"
            f"<b>model</b> {esc(st.session_state.provider_name)} / {esc(st.session_state.selected_model)}<br>"
            f"<b>prompt file</b> {esc(Path(tr['system_prompt']).relative_to(ROOT))}<br>"
            f"<b>tools file</b> {esc(Path(tr['tools']).relative_to(ROOT))}<br>"
            f"<b>transcript</b> {esc(st.session_state.transcript_path.relative_to(ROOT))}"
            "</div>",
            unsafe_allow_html=True,
        )
        if st.session_state.turns:
            st.sidebar.download_button(
                "⬇️ Tải transcript",
                data=json.dumps(tr, ensure_ascii=False, indent=2, default=str),
                file_name=st.session_state.transcript_path.name,
                mime="application/json",
                use_container_width=True,
            )


def render_header() -> None:
    st.markdown(
        '<div class="hd"><div class="logo">🛠️</div><div>'
        "<h1>IT Helpdesk Agent</h1>"
        '<div class="sub">Northstar Labs (dữ liệu giả lập) · mỗi lượt hiển thị tool → args → result/error và phiên bản artifact</div>'
        "</div></div>",
        unsafe_allow_html=True,
    )
    if session_ready():
        av = st.session_state.artifact_version
        st.markdown(
            '<div class="chips">' + chip(av.version, "v") + chip(av.artifact_version, "mono")
            + chip(f"{st.session_state.provider_name} · {st.session_state.selected_model}")
            + chip(f"{len(st.session_state.openai_tools)} tools declared") + "</div>",
            unsafe_allow_html=True,
        )


def render_welcome() -> None:
    st.markdown(
        '<div class="welcome"><h3>Bắt đầu một phiên</h3>'
        "<p>Chọn provider và version ở sidebar rồi bấm <b>Phiên mới</b>. Cần API key trong <code>starter_v0/.env</code>. "
        "Chọn <b>v0</b> để xem baseline, <b>v4</b> để xem bản có bonus tool <code>lookup_ticket</code>.</p></div>",
        unsafe_allow_html=True,
    )


def render_quick_prompts() -> str | None:
    st.markdown('<div class="round">Gợi ý thử nhanh</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, (label, prompt) in enumerate(QUICK_PROMPTS):
        if cols[i % 3].button(label, key=f"qp{i}", use_container_width=True, help=prompt):
            return prompt
    return None


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main() -> None:
    st.set_page_config(page_title="IT Helpdesk Agent", page_icon="🛠️", layout="wide")
    st.markdown(CSS, unsafe_allow_html=True)
    render_sidebar()
    render_header()

    if not session_ready():
        render_welcome()
        return

    quick = None
    if not st.session_state.turns:
        quick = render_quick_prompts()

    for turn in st.session_state.turns:
        render_turn(turn)

    last_status = st.session_state.turns[-1]["status"] if st.session_state.turns else None
    placeholder = "Trả lời câu hỏi của agent…" if last_status == "waiting_for_user" else "Nhập yêu cầu…"
    user_text = st.chat_input(placeholder) or quick
    if user_text and user_text.strip():
        with st.spinner("Agent đang xử lý…"):
            run_turn(user_text.strip())
        st.rerun()


main()  # streamlit executes the module top-level
