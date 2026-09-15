# TEAM — Day04, K4-L3B

**Làm nhóm.** Mỗi người tự viết và commit phần INDIVIDUAL của mình.

## Thông tin bài nộp

- Tên nhóm:
- Người đại diện / MSSV:
- Tên repo: `K4-L3-DAY04-HoVaTen-MSSV-PromptEngineeringToolCalling`
- URL repo, nhánh nộp, commit chốt:
- Deadline áp dụng và link thông báo đổi hạn nếu có:

## Thành viên

| Họ và tên | MSSV | GitHub | Vai trò và công việc | File/commit/PR |
|---|---|---|---|---|
| | | | | |
| Nguyen Phat (điền họ tên đầy đủ) | (điền MSSV) | phatnguyen2004s | Người 3 — UI & Bonus Tool: Streamlit UI, transcript, bonus tool `lookup_ticket` | `starter_v0/app.py`, `starter_v0/tools/lookup_ticket/`, `starter_v0/transcripts/`, runs v4; branch `phat/cp4-ui-bonus-tool` |

## Nhận xét chung

- Kết quả và bằng chứng:
- Thay đổi hiệu quả nhất:
- Giới hạn còn lại:
- Cách phân công và tích hợp:

## INDIVIDUAL

Sao chép mục này cho từng thành viên.

### Họ và tên — MSSV

- Phần việc và file/commit/PR:
- Quyết định, khó khăn và cách xử lý:
- Điều đã học:
- AI/công cụ đã dùng và cách kiểm tra:
- Thời điểm đã tự nộp URL repo chung trên VLearn:

### Nguyen Phat (điền họ tên đầy đủ) — (điền MSSV)

- Phần việc và file/commit/PR: Người 3 — UI & Bonus Tool. Branch `phat/cp4-ui-bonus-tool`, PR về `main` của repo nhóm. Commit: `a541639` (bonus tool `lookup_ticket` + smoke test + case G11–G13), `2e53f40` (Streamlit `app.py`), `aed9ed6` (run v4 base/group, 2 transcript UI, fix bug expander), commit tài liệu (version_log v4, REPORT B4/B5, README mục UI, TEAM). File: `starter_v0/app.py`, `starter_v0/tools/lookup_ticket/{tool.py,TOOL.md,smoke_test.py}`, `starter_v0/helpdesk_data/tickets.json`, `starter_v0/transcripts/ui_v4_*.json`, `starter_v0/runs/v4_B_*.json`.
- Quyết định, khó khăn và cách xử lý: (1) Chọn bonus tool `lookup_ticket` vì luồng cơ bản chỉ *tạo* ticket, chưa *theo dõi* được — đúng tinh thần "ngoài luồng cơ bản" của RUBRIC; tool đọc cả seed mock lẫn ticket do `create_ticket` ghi nên tích hợp thật. (2) UI tái dùng `run_model_tool_loop` của `chat.py` thay vì viết lại agent loop, để UI/CLI/eval cùng một hành vi và một format transcript. (3) Thêm tool làm đổi hash artifact nên ghi thành v4 riêng trong version_log, giữ nguyên v0–v3 của nhóm; chạy lại base để kiểm tra regression: 26/30 so với v3 27/30, case fail mới (H19) không liên quan tool vì không có call `lookup_ticket` nào trong bộ base — ghi trung thực trong REPORT B1/B5. (4) Gặp bug `st.expander(expanded=None)` khi chạy UI thật, sửa bằng `bool()`. (5) File run của nhóm có CRLF nên `git status` báo đổi dù không sửa; không đưa vào commit để PR sạch.
- Điều đã học: routing PASS trong eval one-shot chưa chứng minh hành vi trong chat nhiều lượt — model hay hỏi lại/xác nhận bằng text thay vì gọi `clarify`, và với ID lạ có xu hướng tự phán thay vì tra hệ thống; transcript phải hiện cả tool error để thấy điều này.
- AI/công cụ đã dùng và cách kiểm tra: Claude Code (Anthropic) hỗ trợ đọc repo, viết `app.py`, tool, smoke test và soạn nháp report/TEAM. Tự kiểm tra bằng: smoke test 8/8, `run_eval.py` v4 group 13/13 và base 26/30 (`provider_error_cases=0`), thao tác UI thật 9 lượt và đối chiếu transcript JSON với những gì thấy trên màn hình; grep transcript/run để chắc không có key hay credential.
- Thời điểm đã tự nộp URL repo chung trên VLearn: (điền sau khi nộp)
