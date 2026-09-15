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

### <Họ và tên> — <MSSV> (Người 3 — UI & Bonus Tool, GitHub `phatnguyen2004s`)

- Phần việc và file/commit/PR:
  - Streamlit UI `starter_v0/app.py` hiện tool → input → kết quả/lỗi → artifact version, ghi transcript; provider `mock` (`providers/mock_provider.py`) để thử UI offline; hướng dẫn chạy trong README.
  - Bonus tool `starter_v0/tools/check_ticket_status/` (TOOL.md, tool.py, smoke_test.py 13/13), dữ liệu `helpdesk_data/tickets.json`, 6 case `data/eval_bonus_ticket_status.json`, đăng ký trong `tools/__init__.py` + `artifacts/tools.yaml`.
  - Evidence: run `runs/v0_B_group_gemini_20260915T191536192560.json` (6/6, `provider_error_cases=0`), 3 transcript `transcripts/v0_gemini_ui_*.json` phủ 5 kịch bản; điền REPORT A2/A4/B4/B5/B6.
  - Fix hạ tầng: retry 429 trong `providers/gemini_provider.py`.
  - PR: https://github.com/phatnguyen2004s/K4-Day04-Mango/pull/1 (commit `690d828`, `2ff4e90`, `7876ff5`, `f7127ff`).
- Quyết định, khó khăn và cách xử lý:
  - Chọn `check_ticket_status` vì nó nằm ngoài luồng cơ bản (starter dừng ở *tạo* ticket) và có ranh giới an toàn rõ để kiểm thử (không liệt kê, không lộ `internal_notes`).
  - Chỉ append 1 entry cuối `tools.yaml` để hạn chế conflict với Người 1; case bonus để file riêng, Người 1 chọn đưa vào `eval_group.json`.
  - Free tier Gemini bị 429 liên tục → run đầu có `provider_error_cases>0`, không dùng làm evidence; thêm backoff-retry rồi chạy lại đến khi `provider_error_cases=0`.
- Điều đã học:
  - Routing PASS chưa chứng minh hành động đúng: v0 tự đặt `confirmed=true` và ghi ticket mà không hỏi — chỉ thấy khi đọc transcript và thư mục `tickets/`.
  - Mô tả tool là "prompt" cho model: mô tả `check_ticket_status` nêu rõ "không liệt kê, thiếu mã thì hỏi" và model làm đúng ngay ở v0 (T03, T06).
- AI/công cụ đã dùng và cách kiểm tra: Claude Code hỗ trợ viết app.py/tool/case; kiểm tra bằng smoke test, `run_eval.validate_expected_tools` cho cả 4 bộ case, chạy UI thật trong browser và đọc từng `tool_results` trong transcript.
- Thời điểm đã tự nộp URL repo chung trên VLearn: <điền sau khi nộp>
