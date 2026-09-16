# TEAM — Day04, K4-L3B

**Nhóm:** Mango  
**Người đại diện:** Nguyễn Việt Hoàng — 2A202602424

## Thông tin bài nộp

- Tên repo: `K4-Day04-Mango`
- URL repo: https://github.com/Hoang248/K4-Day04-Mango
- Nhánh nộp: `main`
- Commit chốt hiện tại: cập nhật sau khi PR cuối được merge vào `main`
- Thời điểm đã tự nộp URL trên VLearn: chưa nộp

## Thành viên và phân công

| Thành viên | MSSV | GitHub | Vai trò | File phụ trách | Commit/PR |
|---|---|---|---|---|---|
| Nguyễn Việt Hoàng | 2A202602424 | Hoang248 | Đại diện/leader; Người 2 — Experiment & Safety | `starter_v0/artifacts/version_log.csv`, `starter_v0/data/eval_adversarial.json`, `starter_v0/runs/` | `7259e31` |
| Nguyễn Đình Thái | 2A202602718 | chocolinho | Người 1 — Prompt & Evaluation | `starter_v0/artifacts/system_prompt.md`, `starter_v0/artifacts/tools.yaml`, `starter_v0/data/eval_group.json` | `75d0145`, `a1be488`; PR #1, #2 |
| Nguyễn Tiến Phát | 2A202602387 | phatnguyen2004s | Người 3 — UI & Bonus Tool | `starter_v0/app.py`, `starter_v0/tools/lookup_ticket/`, `starter_v0/transcripts/`, `starter_v0/runs/v4_*` | `a541639`, `2e53f40`, `aed9ed6` |

<a id="team-summary"></a>

## Kết quả chung

- Base accuracy v0→v1→v2→v3: `0.70 → 0.80 → 0.9333 → 0.90`.
- Group v2/v3: `10/10`.
- Adversarial v3: `8/12`; còn các boundary case A03, A04, A10, A11 chưa đạt.
- Bonus `lookup_ticket`: smoke test `8/8`, bonus eval `3/3`.
- Evidence: `starter_v0/runs/`, `starter_v0/artifacts/version_log.csv`, `starter_v0/artifacts/REPORT.md`.

## B7. Reflection cá nhân

<a id="individual-nguyen-viet-hoang"></a>

### B7.1 Nguyễn Việt Hoàng — 2A202602424

- Nhiệm vụ: Đại diện/leader và Người 2 — Experiment & Safety; chạy v0–v3, đánh giá 12 adversarial cases, ghi version log, cập nhật REPORT và hợp nhất deliverables.
- Commit/PR: `7259e31`.
- Failure mode đã phân tích: wrong tool, wrong argument và boundary/data leakage; phân biệt provider error với lỗi đánh giá.
- Bài học: `case_accuracy` không đủ để chứng minh safety; cần kiểm tra tool call, arguments, tool result/error và dữ liệu có bị rò rỉ.
- Công cụ kiểm tra: preflight thành công; các run v0–v3 có `provider_error_cases=0`.
- Thời điểm đã tự nộp URL trên VLearn: chưa nộp.

<a id="individual-nguyen-dinh-thai"></a>

### B7.2 Nguyễn Đình Thái — 2A202602718

- Nhiệm vụ: Người 1 — Prompt & Evaluation; chạy và phân tích baseline v0 trước khi thay đổi artifact, tối ưu system prompt/tool schema, đồng thời xây bộ 10 team cases gồm đúng 5 single-turn và 5 multi-turn.
- File phụ trách: `starter_v0/artifacts/system_prompt.md`, `starter_v0/artifacts/tools.yaml`, `starter_v0/data/eval_group.json`; đóng góp thêm evidence baseline và failure analysis trong `starter_v0/runs/`, `starter_v0/artifacts/version_log.csv` và `starter_v0/artifacts/REPORT.md`.
- Quyết định và cách xử lý: giữ nguyên bộ base để có thể so sánh công bằng giữa các version; từ trace v0, bổ sung quy tắc hỏi lại khi thiếu hoặc mơ hồ asset ID, employee ID và environment; làm rõ mô tả input trong tool schema nhưng không hard-code case ID hay nội dung eval vào prompt. Bộ group được tách riêng và expected calls được đối chiếu với tên tool, required fields và enum trong `tools.yaml`.
- Failure mode đã phân tích: chọn sai tool, truyền sai argument, tự suy diễn identifier/environment khi thiếu dữ kiện và xử lý sai boundary/confirmation trong hội thoại nhiều lượt.
- Kết quả kiểm tra: bộ group có đúng 10 case (5 single-turn + 5 multi-turn); group v1 đạt 8/10 và sau các vòng cải tiến v2/v3 đạt 10/10. Baseline, hash artifact và trace lỗi được lưu để đối chiếu thay đổi trước/sau.
- Bài học: điểm tổng không đủ để giải thích chất lượng agent; cần đọc tool trace để phân biệt lỗi routing, argument và boundary. System prompt và tool schema phải diễn đạt nhất quán, còn multi-turn cần kiểm tra việc giữ ngữ cảnh, hủy nhánh và fresh confirmation.
- AI/công cụ đã dùng và cách kiểm tra: Codex hỗ trợ soạn nháp quy tắc prompt, mô tả tool và team eval cases. Tự kiểm tra cấu trúc JSON, số lượng single/multi-turn, tên tool/argument, hash artifact và đọc run trace; kết quả live eval do Người 2 chạy và được đối chiếu trong report.
- Commit/PR: `75d0145` (baseline v0, version log và failure analysis), `a1be488` (system prompt, tools.yaml, report và team eval cases); PR #1 và PR #2 từ branch `thai/cp1-v0-baseline` đã được merge vào `main`.
- Thời điểm đã tự nộp URL trên VLearn: chưa nộp; sẽ cập nhật thời điểm sau khi tự nộp URL repo chung.

<a id="individual-nguyen-tien-phat"></a>

### B7.3 Nguyễn Tiến Phát — 2A202602387

- Nhiệm vụ: Người 3 — Streamlit UI, transcript và bonus tool `lookup_ticket`.
- File phụ trách: `starter_v0/app.py`, `starter_v0/tools/lookup_ticket/`, `starter_v0/transcripts/`.
- Branch/commit: `phat/cp4-ui-bonus-tool`; `a541639`, `2e53f40`, `aed9ed6`.
- Kiểm tra: smoke test `8/8`, bonus eval `3/3`, group v4 `10/10`, base v4 `26/30`.
- Thời điểm đã tự nộp URL trên VLearn: chưa nộp; thành viên cập nhật sau khi tự nộp URL repo chung.
