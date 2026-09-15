# transcripts/

Hội thoại thật do `app.py` (Streamlit) hoặc `chat.py` ghi lại, cùng format với
`samples/transcripts/example_helpdesk.transcript.json`. Mỗi file chứa
`artifact_version`, `prompt_hash`, `tools_hash`, provider/model và từng turn với
`rounds[].tool_calls` / `tool_results` (kể cả lỗi tool).

Cần có ít nhất 4 transcript với provider thật và prompt bản chốt (v3):

| Kịch bản | Ví dụ mở đầu |
|---|---|
| Yêu cầu bình thường | "Dịch vụ VPN production hiện có đang gặp sự cố không?" |
| Thiếu thông tin → agent hỏi lại | "Kiểm tra Wi-Fi trên laptop của mình." → "Mã máy là LT-240." |
| Nhiều lượt, sửa/hủy ý | "Kiểm tra tổng thể LT-204." → "Chỉ kiểm tra VPN thôi." |
| Hành động ghi dữ liệu | "Tạo ticket VPN AUTH_TIMEOUT trên LT-204, priority high." → "Tôi xác nhận." |
| Bonus: tiến độ ticket | "Ticket LAB-3F2A9C1D của mình xử lý tới đâu rồi?" |

Transcript sinh bằng provider `mock` chỉ để thử UI, **không** commit làm evidence.
Kiểm tra file không chứa API key hay dữ liệu thật trước khi commit.
