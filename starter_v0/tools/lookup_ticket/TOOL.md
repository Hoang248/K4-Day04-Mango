---
name: lookup_ticket
track: bonus
kind: local_status
provider: local_ticket_store
requires_env: []
inputs: [ticket_id, include_history]
outputs: [ticket_id, status, priority, summary, asset_id, assignee, updated_at, linked_incident, history]
side_effect: false
requires_confirmation: false
---
# lookup_ticket (team-built bonus tool)

Tra cứu trạng thái một ticket helpdesk theo `ticket_id`. Đây là chức năng **ngoài
luồng cơ bản** đã chốt (luồng cơ bản chỉ *tạo* ticket sau xác nhận, chưa có cách
*theo dõi* ticket đã tạo).

## Nguồn dữ liệu

1. `helpdesk_data/tickets.json` — 3 ticket giả lập ở các trạng thái
   `in_progress`, `waiting_for_user`, `resolved`.
2. `tickets/<id>.json` — ticket vừa được `create_ticket` ghi trong phiên chat
   (tích hợp thật với tool có sẵn; thư mục này gitignored).

## Hợp đồng

| Input | Kiểu | Bắt buộc | Ghi chú |
|---|---|---|---|
| `ticket_id` | string | có | dạng `LAB-XXXXXXXX`; không phân biệt hoa/thường |
| `include_history` | boolean | không | mặc định `false`; `true` trả thêm mảng `history` |

Output luôn có `tool`, `ticket_id`, `status`. Lỗi trả về trường `error`:

| `error` | Khi nào |
|---|---|
| `missing_ticket_id` | không truyền hoặc chuỗi rỗng |
| `invalid_ticket_id_format` | không đúng dạng `LAB-` + 8 hex |
| `ticket_not_found` | không có trong seed lẫn local store |

## Guardrail

- Chỉ đọc, không ghi; không cần xác nhận.
- Trường `internal_notes` **không bao giờ** được trả về (giữ ghi chú nội bộ trong hệ thống).
- Không tự đoán ID: nếu người dùng chưa cung cấp `ticket_id`, agent phải gọi `clarify` trước.

## Smoke test

```bash
python -m tools.lookup_ticket.smoke_test
```
