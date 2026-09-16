# TEAM — Day04, K4-L3B

**Làm nhóm.** Mỗi người tự viết và commit phần INDIVIDUAL của mình.

## Thông tin bài nộp

- Tên nhóm:Mango
- Người đại diện / MSSV: Nguyễn Việt Hoàng / 2A202602424
- Tên repo: `K4-Day04-Mango`
- URL repo: https://github.com/Hoang248/K4-Day04-Mango
- Nhánh nộp: `Chưa xác minh (repo local hiện chưa có thư mục .git)`
- Commit chốt: `Chưa xác minh (cần lấy sau khi push repo)`
- Deadline áp dụng và link thông báo đổi hạn nếu có:

## Thành viên

| Họ và tên | MSSV | GitHub | Vai trò và công việc | File/commit/PR |
|---|---|---|---|---|
|Nguyễn Việt Hoàng |2A202602424 |Hoang248 |Đại diện/leader; Người 2 — Experiment & Safety: phụ trách thí nghiệm v0–v3 và đánh giá adversarial | `starter_v0/artifacts/version_log.csv`, `starter_v0/data/eval_adversarial.json`, `starter_v0/runs/`; chạy v0→v3, ghi hypothesis/metrics trước–sau/đường dẫn run, đánh giá đủ 12 adversarial cases và phân tích data leakage; commit/PR: cập nhật sau khi push |
|Nguyễn Đình Thái |2A202602718 |chocolinho |Người 1 — Prompt & Evaluation: phụ trách system prompt, tool declaration và test cases | `starter_v0/artifacts/system_prompt.md`, `starter_v0/artifacts/tools.yaml`, `starter_v0/data/eval_group.json`; tối ưu prompt/tool schema, làm 10 team cases (5 single-turn + 5 multi-turn), ghi nhận failure mode của v0; commit/PR: thành viên cập nhật |
|Nguyễn Tiến Phát |2A202602387 |phatnguyen2004s |Người 3 — UI & Bonus Tool: Streamlit UI, transcript, bonus tool `lookup_ticket` và báo cáo UI | `starter_v0/app.py`, `starter_v0/tools/lookup_ticket/`, `starter_v0/transcripts/`, `starter_v0/runs/v4_*`; branch `phat/cp4-ui-bonus-tool`; commits `a541639`, `2e53f40`, `aed9ed6` |
## Nhận xét chung

- Kết quả và bằng chứng: Base accuracy v0→v1→v2→v3 là 0.70→0.80→0.9333→0.90; group v2/v3 đạt 10/10; adversarial v3 đạt 8/12. Evidence nằm trong `starter_v0/runs/`, `starter_v0/artifacts/version_log.csv` và `starter_v0/artifacts/REPORT.md`.
- Thay đổi hiệu quả nhất: mapping category cho `search_kb` và quy tắc hỏi lại/confirmation giúp group đạt 10/10 và base v2 đạt 28/30.
- Giới hạn còn lại: v3 còn A03, A04, A10, A11; cần bổ sung snapshot v1/v2 cho UI và hoàn tất commit/INDIVIDUAL của các thành viên trước khi nộp.
- Cách phân công và tích hợp: Thái phụ trách Prompt & Evaluation; Hoàng phụ trách Experiment & Safety và hỗ trợ prompt; Phát phụ trách UI, transcript và báo cáo. Mỗi người cần review, commit và tự viết INDIVIDUAL của mình.

## INDIVIDUAL

### Họ và tên — MSSV

- Phần việc và file/commit/PR:
- Quyết định, khó khăn và cách xử lý:
- Điều đã học:
- AI/công cụ đã dùng và cách kiểm tra:
- Thời điểm đã tự nộp URL repo chung trên VLearn:

### Nguyễn Việt Hoàng — 2A202602424

- Phần việc và file/commit/PR: Đại diện/leader và Người 2 — Experiment & Safety; chạy v0–v3, đánh giá 12 adversarial cases, ghi `starter_v0/artifacts/version_log.csv`, cập nhật `starter_v0/artifacts/REPORT.md`, review các thay đổi prompt/tool và hợp nhất deliverables Người 3. Commit/PR: điền hash thật sau khi push.
- Quyết định, khó khăn và cách xử lý: Giữ cùng bộ case qua các version; phân biệt provider error với lỗi routing/argument/boundary; ghi trung thực 4 adversarial boundary còn fail ở v3 thay vì sửa số liệu.
- Điều đã học: `case_accuracy` không đủ để chứng minh safety; phải đọc tool calls, args, tool result/error và kiểm tra dữ liệu có bị ghi/gửi ra ngoài. V2 đạt base 28/30 và group 10/10; v3 adversarial đạt 8/12.
- AI/công cụ đã dùng và cách kiểm tra: Codex hỗ trợ đọc rubric, kiểm tra JSON/hash, phân tích run và soạn artifact; tự kiểm tra bằng preflight thành công, run v0–v3 với `provider_error_cases=0`, đối chiếu metrics và trace trong các file JSON.
- Thời điểm đã tự nộp URL repo chung trên VLearn: chưa nộp.

### Nguyễn Đình Thái — 2A202602718

- Phần việc và file/commit/PR: Người 1 — Prompt & Evaluation; phụ trách `starter_v0/artifacts/system_prompt.md`, `starter_v0/artifacts/tools.yaml`, `starter_v0/data/eval_group.json`; commit/PR: thành viên cập nhật hash thật.
- Quyết định, khó khăn và cách xử lý: Tối ưu prompt/tool schema dựa trên log v0–v3; kiểm tra routing, argument và boundary thay vì chỉ nhìn case accuracy.
- Điều đã học: Schema rõ ràng và quy tắc hỏi lại giúp giảm gọi tool sai; cần đánh giá cả single-turn và multi-turn.
- AI/công cụ đã dùng và cách kiểm tra: Codex hỗ trợ rà rubric và phân tích run; đối chiếu kết quả với JSON trong `starter_v0/runs/`.
- Thời điểm đã tự nộp URL repo chung trên VLearn: thành viên cập nhật sau khi nộp.

### Nguyễn Tiến Phát — 2A202602387

- Phần việc và file/commit/PR: Người 3 — Streamlit UI và bonus `lookup_ticket`; `starter_v0/app.py`, `starter_v0/tools/lookup_ticket/`, `starter_v0/transcripts/`, `starter_v0/runs/v4_*`; branch `phat/cp4-ui-bonus-tool`; commits `a541639`, `2e53f40`, `aed9ed6`.
- Quyết định, khó khăn và cách xử lý: Tái sử dụng `run_model_tool_loop` để UI, CLI và eval dùng chung hành vi; thêm bonus tool đọc ticket seed và ticket local; sửa lỗi UI khi render expander.
- Điều đã học: UI phải hiển thị cả tool, args, result/error, version và transcript; routing PASS không thay thế kiểm tra hội thoại nhiều lượt.
- AI/công cụ đã dùng và cách kiểm tra: Claude Code hỗ trợ triển khai; đã kiểm tra smoke test 8/8, bonus eval 3/3, group v4 10/10, base v4 26/30 và đối chiếu transcript UI.
- Thời điểm đã tự nộp URL repo chung trên VLearn: thành viên cập nhật sau khi nộp.
