# TEAM — Day04, K4-L3B

**Nhóm:** Mango  
**Người đại diện:** Nguyễn Việt Hoàng — 2A202602424

## Thông tin bài nộp

- Tên repo: `K4-Day04-Mango`
- URL repo: https://github.com/Hoang248/K4-Day04-Mango
- Nhánh nộp: `main`
- Commit chốt hiện tại: `7259e31`
- Thời điểm đã tự nộp URL trên VLearn: chưa nộp

## Thành viên và phân công

| Thành viên | MSSV | GitHub | Vai trò | File phụ trách | Commit/PR |
|---|---|---|---|---|---|
| Nguyễn Việt Hoàng | 2A202602424 | Hoang248 | Đại diện/leader; Người 2 — Experiment & Safety | `starter_v0/artifacts/version_log.csv`, `starter_v0/data/eval_adversarial.json`, `starter_v0/runs/` | `7259e31` |
| Nguyễn Đình Thái | 2A202602718 | chocolinho | Người 1 — Prompt & Evaluation | `starter_v0/artifacts/system_prompt.md`, `starter_v0/artifacts/tools.yaml`, `starter_v0/data/eval_group.json` | Thành viên cập nhật hash thật |
| Nguyễn Tiến Phát | 2A202602387 | phatnguyen2004s | Người 3 — UI & Bonus Tool | `starter_v0/app.py`, `starter_v0/tools/lookup_ticket/`, `starter_v0/transcripts/`, `starter_v0/runs/v4_*` | `a541639`, `2e53f40`, `aed9ed6` |

## Kết quả chung

- Base accuracy v0→v1→v2→v3: `0.70 → 0.80 → 0.9333 → 0.90`.
- Group v2/v3: `10/10`.
- Adversarial v3: `8/12`; còn các boundary case A03, A04, A10, A11 chưa đạt.
- Bonus `lookup_ticket`: smoke test `8/8`, bonus eval `3/3`.
- Evidence: `starter_v0/runs/`, `starter_v0/artifacts/version_log.csv`, `starter_v0/artifacts/REPORT.md`.

## B7. Reflection cá nhân

### B7.1 Nguyễn Việt Hoàng — 2A202602424

- Nhiệm vụ: Đại diện/leader và Người 2 — Experiment & Safety; chạy v0–v3, đánh giá 12 adversarial cases, ghi version log, cập nhật REPORT và hợp nhất deliverables.
- Commit/PR: `7259e31`.
- Failure mode đã phân tích: wrong tool, wrong argument và boundary/data leakage; phân biệt provider error với lỗi đánh giá.
- Bài học: `case_accuracy` không đủ để chứng minh safety; cần kiểm tra tool call, arguments, tool result/error và dữ liệu có bị rò rỉ.
- Công cụ kiểm tra: preflight thành công; các run v0–v3 có `provider_error_cases=0`.
- Thời điểm đã tự nộp URL trên VLearn: chưa nộp.

### B7.2 Nguyễn Đình Thái — 2A202602718

- Nhiệm vụ: Người 1 — Prompt & Evaluation; tối ưu system prompt, tool schema và 10 team cases.
- File phụ trách: `starter_v0/artifacts/system_prompt.md`, `starter_v0/artifacts/tools.yaml`, `starter_v0/data/eval_group.json`.
- Failure mode đã phân tích: wrong tool, wrong argument và boundary trong single-turn/multi-turn.
- Bài học: Schema rõ ràng và quy tắc hỏi lại giúp giảm gọi tool sai.
- Commit/PR: thành viên cập nhật hash thật.
- Thời điểm đã tự nộp URL trên VLearn: thành viên cập nhật sau khi nộp.

### B7.3 Nguyễn Tiến Phát — 2A202602387

- Nhiệm vụ: Người 3 — Streamlit UI, transcript và bonus tool `lookup_ticket`.
- File phụ trách: `starter_v0/app.py`, `starter_v0/tools/lookup_ticket/`, `starter_v0/transcripts/`.
- Branch/commit: `phat/cp4-ui-bonus-tool`; `a541639`, `2e53f40`, `aed9ed6`.
- Kiểm tra: smoke test `8/8`, bonus eval `3/3`, group v4 `10/10`, base v4 `26/30`.
- Thời điểm đã tự nộp URL trên VLearn: thành viên cập nhật sau khi nộp.
