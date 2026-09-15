---
name: check_ticket_status
track: bonus
kind: local_status
provider: mock_ticket_store
requires_env: []
inputs: [ticket_id, include_history]
outputs: [ticket, history, source]
side_effect: false
---
# check_ticket_status (team-built bonus tool)

Tra cứu tiến độ của **một** ticket helpdesk theo mã `LAB-XXXXXXXX`. Ticket được
đọc từ dữ liệu giả lập `helpdesk_data/tickets.json` (5 ticket seed với các trạng
thái `open`, `in_progress`, `waiting_for_user`, `resolved`, `closed`) hoặc từ
`tickets/` — nơi `create_ticket` ghi ticket mới sau khi người dùng xác nhận.

## Vì sao là mở rộng

Luồng cơ bản của starter dừng ở *tạo* ticket. Người dùng thật luôn hỏi tiếp
"ticket của tôi tới đâu rồi?"; tool này đóng vòng đó mà không cần liên hệ
service desk.

## Hợp đồng

| Input | Kiểu | Bắt buộc | Ghi chú |
|---|---|---|---|
| `ticket_id` | string | có | Đúng dạng `LAB-XXXXXXXX`; không nhận `*`, `all` hay chuỗi rỗng |
| `include_history` | boolean | không | `true` để kèm lịch sử cập nhật; mặc định `false` |

Output thành công: `ticket` (`ticket_id, summary, priority, status, asset_id,
requester, assigned_team, created_at, updated_at, next_step`), `source`
(`seed` hoặc `local_ticket_store`), `snapshot_at`, và `history` khi được yêu cầu.

Lỗi trả về rõ ràng: `missing_ticket_id`, `invalid_ticket_id`, `ticket_not_found`,
`invalid_ticket_id_type`.

## Ranh giới an toàn

- Chỉ tra cứu theo **một** mã cụ thể; không liệt kê ticket của người khác hay
  toàn công ty (`invalid_ticket_id` cho mọi ký tự đại diện).
- Trường `internal_notes` trong dữ liệu (ghi chú nội bộ, liên hệ escalation,
  mã license) **không bao giờ** được trả về — chỉ các trường trong
  `PUBLIC_FIELDS` mới đi ra ngoài.
- Không có side effect: tool chỉ đọc file.

## Kiểm thử

```bash
python -m tools.check_ticket_status.smoke_test
python run_eval.py --provider openrouter --version v3 --suite group --eval-cases data/eval_bonus_ticket_status.json
```
