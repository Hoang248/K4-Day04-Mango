# TEAM — Day04, K4-L3B

**Làm nhóm.** Mỗi người tự viết và commit phần INDIVIDUAL của mình.

## Thông tin bài nộp

<<<<<<< HEAD
- Tên nhóm:Mango
- Người đại diện / MSSV: Nguyễn Việt Hoàng / 2A202602424
- Tên repo: `K4-Day04-Mango`
- URL repo: https://github.com/Hoang248/K4-Day04-Mango
- Nhánh nộp: `Chưa xác minh (repo local hiện chưa có thư mục .git)`
- Commit chốt: `Chưa xác minh (cần lấy sau khi push repo)`
=======
- Tên nhóm:
- Người đại diện / MSSV:
- Tên repo: `K4-L3-DAY04-HoVaTen-MSSV-PromptEngineeringToolCalling`
- URL repo, nhánh nộp, commit chốt:
>>>>>>> da2e7656d078ec2f75da7d445b1b317a625e40c2
- Deadline áp dụng và link thông báo đổi hạn nếu có:

## Thành viên

| Họ và tên | MSSV | GitHub | Vai trò và công việc | File/commit/PR |
|---|---|---|---|---|
<<<<<<< HEAD
|Nguyễn Việt Hoàng |2A202602424 |Hoang248 |Đại diện/leader; Người 2 — Experiment & Safety: phụ trách thí nghiệm v0–v3 và đánh giá adversarial | `starter_v0/artifacts/version_log.csv`, `starter_v0/data/eval_adversarial.json`, `starter_v0/runs/`; chạy v0→v3, ghi hypothesis/metrics trước–sau/đường dẫn run, đánh giá đủ 12 adversarial cases và phân tích data leakage; commit/PR: cập nhật sau khi push |
|Nguyễn Đình Thái |2A202602718 |chocolinho |Người 1 — Prompt & Evaluation: phụ trách system prompt, tool declaration và test cases | `starter_v0/artifacts/system_prompt.md`, `starter_v0/artifacts/tools.yaml`, `starter_v0/data/eval_group.json`; tối ưu prompt/tool schema, làm 10 team cases (5 single-turn + 5 multi-turn), ghi nhận failure mode của v0; commit/PR: thành viên cập nhật |
|Nguyễn Tiến Phát |2A202602387 |phatnguyen2004s |Người 3 — UI & Bonus Tool: Streamlit UI, transcript, bonus tool `lookup_ticket` và báo cáo UI | `starter_v0/app.py`, `starter_v0/tools/lookup_ticket/`, `starter_v0/transcripts/`, `starter_v0/runs/v4_*`; branch `phat/cp4-ui-bonus-tool`; commits `a541639`, `2e53f40`, `aed9ed6` |
## Nhận xét chung

- Kết quả và bằng chứng: Base accuracy v0→v1→v2→v3 là 0.70→0.80→0.9333→0.90; group v2/v3 đạt 10/10; adversarial v3 đạt 8/12. Evidence nằm trong `starter_v0/runs/`, `starter_v0/artifacts/version_log.csv` và `starter_v0/artifacts/REPORT.md`.
- Thay đổi hiệu quả nhất: mapping category cho `search_kb` và quy tắc hỏi lại/confirmation giúp group đạt 10/10 và base v2 đạt 28/30.
- Giới hạn còn lại: v3 còn A03, A04, A10, A11; cần bổ sung snapshot v1/v2 cho UI và hoàn tất commit/INDIVIDUAL của các thành viên trước khi nộp.
- Cách phân công và tích hợp: Thái phụ trách Prompt & Evaluation; Hoàng phụ trách Experiment & Safety và hỗ trợ prompt; Phát phụ trách UI, transcript và báo cáo. Mỗi người cần review, commit và tự viết INDIVIDUAL của mình.

## INDIVIDUAL

=======
| | | | | |
| Nguyen Phat (điền họ tên đầy đủ) | (điền MSSV) | phatnguyen2004s | Người 3 — UI & Bonus Tool: Streamlit UI, transcript, bonus tool `lookup_ticket` | `starter_v0/app.py`, `starter_v0/tools/lookup_ticket/`, `starter_v0/transcripts/`, runs v4; branch `phat/cp4-ui-bonus-tool` |

## Nhận xét chung

- Kết quả và bằng chứng:
- Thay đổi hiệu quả nhất:
- Giới hạn còn lại:
- Cách phân công và tích hợp:

## INDIVIDUAL

Sao chép mục này cho từng thành viên.

>>>>>>> da2e7656d078ec2f75da7d445b1b317a625e40c2
### Họ và tên — MSSV

- Phần việc và file/commit/PR:
- Quyết định, khó khăn và cách xử lý:
- Điều đã học:
- AI/công cụ đã dùng và cách kiểm tra:
- Thời điểm đã tự nộp URL repo chung trên VLearn:

<<<<<<< HEAD
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
=======
### Nguyen Phat (điền họ tên đầy đủ) — (điền MSSV)

- Phần việc và file/commit/PR: Người 3 — UI & Bonus Tool. Branch `phat/cp4-ui-bonus-tool`, PR về `main` của repo nhóm. Commit: `a541639` (bonus tool `lookup_ticket` + smoke test + 3 case bonus), `2e53f40` (Streamlit `app.py`), `aed9ed6` (run v4 base/group, 2 transcript UI, fix bug expander), commit tài liệu (version_log v4, REPORT B4/B5, README mục UI, TEAM). File: `starter_v0/app.py`, `starter_v0/tools/lookup_ticket/{tool.py,TOOL.md,smoke_test.py}`, `starter_v0/helpdesk_data/tickets.json`, `starter_v0/transcripts/ui_v4_*.json`, `starter_v0/runs/v4_B_*.json`.
- Quyết định, khó khăn và cách xử lý: (1) Chọn bonus tool `lookup_ticket` vì luồng cơ bản chỉ *tạo* ticket, chưa *theo dõi* được — đúng tinh thần "ngoài luồng cơ bản" của RUBRIC; tool đọc cả seed mock lẫn ticket do `create_ticket` ghi nên tích hợp thật. (2) UI tái dùng `run_model_tool_loop` của `chat.py` thay vì viết lại agent loop, để UI/CLI/eval cùng một hành vi và một format transcript. (3) Thêm tool làm đổi hash artifact nên ghi thành v4 riêng trong version_log, giữ nguyên v0–v3 của nhóm; chạy lại base để kiểm tra regression: 26/30 so với v3 27/30, case fail mới (H19) không liên quan tool vì không có call `lookup_ticket` nào trong bộ base — ghi trung thực trong REPORT B1/B5. (4) Gặp bug `st.expander(expanded=None)` khi chạy UI thật, sửa bằng `bool()`. (5) File run của nhóm có CRLF nên `git status` báo đổi dù không sửa; không đưa vào commit để PR sạch.
- Điều đã học: routing PASS trong eval one-shot chưa chứng minh hành vi trong chat nhiều lượt — model hay hỏi lại/xác nhận bằng text thay vì gọi `clarify`, và với ID lạ có xu hướng tự phán thay vì tra hệ thống; transcript phải hiện cả tool error để thấy điều này.
- AI/công cụ đã dùng và cách kiểm tra: Claude Code (Anthropic) hỗ trợ đọc repo, viết `app.py`, tool, smoke test và soạn nháp report/TEAM. Tự kiểm tra bằng: smoke test 8/8, `run_eval.py` v4 group 10/10, bonus 3/3 và base 26/30 (`provider_error_cases=0`), thao tác UI thật 9 lượt và đối chiếu transcript JSON với những gì thấy trên màn hình; grep transcript/run để chắc không có key hay credential.
- Thời điểm đã tự nộp URL repo chung trên VLearn: (điền sau khi nộp)
>>>>>>> da2e7656d078ec2f75da7d445b1b317a625e40c2
