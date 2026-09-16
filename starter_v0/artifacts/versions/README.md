# Artifact snapshots per version

Mỗi thư mục `vN/` chứa đúng cặp `system_prompt.md` + `tools.yaml` đã dùng cho
run `vN` trong `runs/`. UI (`app.py`) đọc thư mục này khi chọn version, và
`artifact_version` hiển thị phải trùng với `version_log.csv` / file run.

| Version | Nguồn | Trạng thái |
|---|---|---|
| v0 | commit `2c1a5ec` (starter gốc) | ✅ hash khớp run v0 |
| v1 | chưa có trong git — cần đội trưởng bổ sung | ⏳ prompt `f25b6f7a11eb…`, tools `f7e8e1dd7433…` |
| v2 | chưa có trong git — cần đội trưởng bổ sung | ⏳ prompt `d76f38e9dc1b…`, tools `301d53fc0b18…` |
| v3 | commit `0cc19d2` | ✅ hash khớp run v3 |
| v4 | `artifacts/` hiện tại (bản mới nhất) | ✅ |

Kiểm tra bằng:

```bash
python scripts/verify_versions.py
```

Không sửa nội dung trong `versions/`; đây là bằng chứng lịch sử, chỉ thêm
thư mục mới khi tạo version mới.
