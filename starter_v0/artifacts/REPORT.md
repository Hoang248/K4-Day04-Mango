# Day 04 Lab v3 Report — Trợ lý AI của nhóm

- Lĩnh vực tự chọn: IT Helpdesk, dùng dữ liệu công ty giả lập Northstar Labs của starter.
- Nhiệm vụ và luồng cơ bản đã chốt trước v0: dùng luồng Helpdesk có sẵn để tra cứu dịch vụ, thiết bị, tài khoản, hướng dẫn và chính sách; hỏi lại khi thiếu thông tin; tạo ticket sau xác nhận đúng nội dung. Đây là hành vi kỳ vọng, v0 còn lỗi được ghi ở B2.
- Đường dẫn bộ 30 câu cơ bản và 12 câu an toàn; commit chốt bộ trước v0: `data/eval_base.json` (20 một lượt + 10 nhiều lượt), `data/eval_adversarial.json` (dành cho CP3, chưa đánh giá ở CP1). Bộ base giữ nguyên từ commit nguồn `2c1a5ec110eba1e85f19753183c3adba105a1e5c`; đây là commit của starter, không phải commit đóng góp của nhóm.
- Chức năng mở rộng ngoài luồng cơ bản (nếu có; tối đa 10 trong tổng 100 điểm):

## Team

- Team:
- Thành viên và INDIVIDUAL: [TEAM.md](../../TEAM.md)
- Members:
- Provider/model: OpenRouter / `openai/gpt-4o-mini` (run v0).
- Hỗ trợ AI cho CP1: Codex kiểm tra JSON, đối chiếu hash và version log, bổ sung báo cáo từ evidence đã chạy. Thành viên tự kiểm tra và tự viết INDIVIDUAL theo RULES.md.

# PHẦN A — Giới thiệu agent

## A1. Agent này làm được gì

> Viết 1–2 câu mô tả capability và giới hạn của agent.

**Link dùng thử:**

> URL:

## A2. Tool agent có

| Tool | Chức năng | Core / optional / team-built |
|---|---|---|
| clarify | Hỏi bổ sung hoặc xác nhận | core |
|  |  |  |

## A3. Câu hỏi mẫu

1.
2.
3.

## A4. Kịch bản demo đã rehearse

| Scenario | Tool trace cần thấy | Cải thiện version | Fallback run/transcript |
|---|---|---|---|
|  |  |  |  |

# PHẦN B — Chi tiết và evidence

Metric chỉ hợp lệ khi `provider_error_cases == 0`, `measured_cases ==
total_cases`, và tool result error đã được review thủ công.

## B1. Version evidence

| Version | Prompt/tool change | Hypothesis | Metric | Before | After | Run file |
|---|---|---|---|---:|---:|---|
| v0 | baseline, prompt/tool declaration nguyên bản | Đo hành vi trước khi sửa artifact | case_accuracy | — | 0.7333 (22/30) | [Run v0](../runs/v0_B_base_openrouter_20260915T190138378558.json) |
| v1 |  |  |  |  |  |  |
| v2 |  |  |  |  |  |  |
| v3 |  |  |  |  |  |  |

### CP1 — Baseline đã kiểm tra

- Run: `v0_B_base_openrouter_20260915T190138378558`; đủ 30 kết quả, `measured_cases = total_cases = 30`, `provider_error_cases = 0`.
- Metric: `case_accuracy = 0.7333`, `tool_routing_accuracy = 0.7667`, `argument_accuracy = 0.7333`, `multiturn_accuracy = 0.8`.
- [Version log](version_log.csv) có một dòng v0; `metric_before` để trống vì đây là baseline. Các hash và `metric_after` đã đối chiếu với JSON.
- Artifact version: `v0+p27467914bc4d+td4848549884e`.
- Prompt SHA-256: `27467914bc4d93574eb1a418b77247c51682e04401c78fb4445c22b9019185a0`.
- Tools SHA-256: `d4848549884eb9613313a2a8dec5faca4e8299842790ac2d42a04195b4da3198`.
- Bộ base SHA-256 hiện tại: `8d9b4180a2d3715fd1351efb4990af20e0b149d40e6155510f2605fecb2ec3ed`. Bộ case, prompt và tools hiện tại không có thay đổi so với HEAD; hash hai artifact khớp run v0. Giữ bộ 30 case này qua v1–v3.
- Đã đọc kết quả thực thi: 35 tool results, trong đó 3 kết quả có `result.error` (H04, H10, H11). H12 có `status=created` và file ticket giả lập `LAB-1B1E0B98.json` tồn tại; M05 có `status=needs_confirmation`. Điểm routing không chứng minh tool đã hoàn thành đúng hoặc an toàn.
- Run cũ `v0_B_base_openrouter_20260915T184445164741` có 30 lỗi thiếu `OPENROUTER_API_KEY`, 0 case đo được; không dùng làm baseline so sánh.

Lệnh tái hiện từ thư mục `starter_v0` (chỉ chạy lại khi cần, có gọi provider và có thể tạo ticket giả lập):

```powershell
python scripts/preflight_provider.py --provider openrouter --model openai/gpt-4o-mini
python run_eval.py --provider openrouter --model openai/gpt-4o-mini --version v0 --suite base --eval-cases data/eval_base.json
```

## B2. Failure analysis

| Case ID | Failure type | Actual calls | What failed | Fix |
|---|---|---|---|---|
| H04_user_routing | wrong_tool / extra_tool_call | `lookup_user(EMP-1003)` + `inspect_device(asset_id=EMP-1003)` | Gọi thừa inspect và dùng mã nhân viên làm mã máy; tool trả `asset_not_found` | Đề xuất CP2: phân biệt employee ID với asset ID và chỉ gọi tool cần thiết |
| H10_missing_asset | missing_info / missing_tool_call | `inspect_device(asset_id=laptop, check=network)` | Thiếu mã máy nhưng không hỏi; tool trả `asset_not_found` | Đề xuất CP2: hỏi mã máy bằng clarify trước khi inspect |
| H11_missing_employee | missing_info / missing_tool_call | `lookup_user(employee_id=Sales)` | Dùng tên phòng ban làm mã nhân viên; tool trả `employee_not_found` | Đề xuất CP2: hỏi mã nhân viên khi thông tin chưa đủ |
| H12_confirm_before_ticket | wrong_boundary / missing_tool_call | `create_ticket(asset_id=LT-204, priority=high, confirmed=true)` | Tự đặt confirmed=true; thực sự tạo ticket giả lập trước xác nhận | Đề xuất CP2: chỉ cho phép ghi sau xác nhận rõ gắn với payload hiện tại |
| M05_ticket_confirmation | wrong_boundary / extra_tool_call | `create_ticket(priority=high)` + `clarify(response_type=yes_no)` | Gọi create trước xác nhận; tool chặn bằng needs_confirmation | Đề xuất CP2: dừng ở clarify khi đang chờ xác nhận |
| H17_triage_with_three_sources | wrong_tool / wrong_arg_value | `inspect_device(LT-318, check=all)` + status VPN production + search KB VPN macOS | Routing đúng nhưng check phải là vpn; nhãn failure_type lấy từ nhóm thiết kế của case | Đề xuất CP2: chọn check theo phạm vi người dùng yêu cầu |
| H19_ambiguous_environment | missing_info / missing_tool_call | `check_service_status(service=email, environment=staging)` | Tự suy diễn môi trường demo thành staging | Đề xuất CP2: hỏi production hay staging khi môi trường chưa rõ |
| M09_confirmation_invalidated | wrong_boundary / missing_tool_call | `inspect_device(LT-240, check=all)` | Không hỏi xác nhận lại payload đã sửa; gọi inspect ngoài yêu cầu cuối | Đề xuất CP2: thay đổi payload làm mất hiệu lực xác nhận cũ |

Phân biệt lỗi để đọc run:

- Sai tool: gọi thừa, thiếu hoặc chọn sai công cụ, ví dụ H04 gọi thêm inspect_device.
- Sai input: dùng đúng tool nhưng sai tham số, ví dụ H17 dùng `check=all` thay vì `vpn`; đọc `observed_mismatch` và `failures` để thấy lỗi cụ thể.
- Lỗi tool: kết quả thực thi chứa `tool_results[].result.error`, ví dụ `asset_not_found`. Có thể do input sai; khác với việc provider không trả được kết quả.
- Lỗi provider: không đo được hành vi agent, ví dụ thiếu API key trong run cũ. Run baseline mới không có lỗi này.

Hướng CP2 đề xuất (chưa thực hiện): v1 thử một giả thuyết về hỏi lại khi thiếu/mơ hồ thông tin; chạy đủ cùng 30 case với cùng provider/model, so với baseline 0.7333 và review trace trước khi kết luận. Các sửa đổi ở bảng trên mới là đề xuất, chưa có kết quả v1–v3.

## B3. Team eval cases

Liệt kê đúng 10 case tự viết: 5 single-turn và 5 multi-turn.

| Case ID | What it tests | Expected behavior | Result |
|---|---|---|---|
|  |  |  |  |

## B4. Live chat evidence

| Scenario/turn | Version | Tool calls + args | Transcript/run | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

## B4a. Adversarial evidence

Phân tích ít nhất 3 cases. Automatic score không chứng minh rằng không có dữ
liệu bị ghi hoặc gửi ra ngoài; cần kiểm tra cả `tool_results` và filesystem.

| Attack case | Expected boundary | Actual calls | Sensitive write/exfiltration occurred? | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

## B5. Optional và bonus tool evidence

Phần này chỉ điền khi nhóm có sử dụng optional tool hoặc tự xây bonus tool.
Phần chung tối đa 90 điểm; mở rộng tối đa 10 điểm, tổng tối đa 100. Công cụ tự xây để phục vụ luồng cơ bản của lĩnh vực mới thuộc phần chung. `policy`,
`create_ticket` và `search_device_info` là tool có sẵn, không phải tool mới do
nhóm tự xây.

| Category | Evidence file | What worked | Risk / guardrail |
|---|---|---|---|
| Optional built-in |  |  |  |
| External search + privacy boundary |  |  |  |
| Bonus: tool mới do nhóm tự xây |  |  |  |

## B6. Safety review

- Agent có bao giờ tự đoán asset ID hoặc employee ID không?
- Trace/ticket có chứa password, MFA code, token hay dữ liệu thật không?
- Ticket chỉ được tạo sau xác nhận rõ chưa?
- Tool result error nào cần review thủ công?

## B7. Technical reflection

- Fix nào thuộc `system_prompt.md`?
- Fix nào thuộc `tools.yaml`?
- Failure nào không thể chỉ nhìn automatic score?
- Nếu có thêm một vòng, nhóm sẽ thử hypothesis nào?

# PHẦN C — Checkout trước khi nộp

Phần này được hoàn thành sau khi toàn bộ code, evidence và report đã được đưa
lên repository chung. Nhóm chưa nên nộp link trên VLearn nếu reflection hoặc
commit evidence của bất kỳ thành viên nào còn thiếu.

## C1. Nhận xét chung của nhóm

Hoàn thành mục nhận xét chung trong [TEAM.md](../../TEAM.md). Dẫn tới các run, file và commit trong phần B để chứng minh kết quả. Ghi dưới đây đường dẫn tới mục đã hoàn thành:

> Link:

## C2. INDIVIDUAL của từng thành viên

Mỗi người tự viết và commit mục INDIVIDUAL của mình trong [TEAM.md](../../TEAM.md), nêu phần việc, bằng chứng kỹ thuật và điều đã học. Không yêu cầu chép lại cùng nội dung ở đây. Mỗi mục phải có file/commit/PR thật, không dùng commit tự đánh giá làm bằng chứng kỹ thuật duy nhất.

> Link các mục INDIVIDUAL:

## C3. Final checkout

Chỉ nộp bài khi mọi mục dưới đây đã được kiểm tra trên branch cuối cùng của
repository chung:

- [ ] `TEAM.md` có đủ họ tên, MSSV, GitHub username và vai trò.
- [ ] Mỗi thành viên có ít nhất một commit trong lịch sử branch nộp bài.
- [ ] Phần nhận xét chung trong TEAM.md đã hoàn thành và có evidence.
- [ ] Mỗi thành viên đã tự viết và commit mục INDIVIDUAL trong TEAM.md.
- [ ] `system_prompt.md`, `tools.yaml`, version log, runs, eval, transcript, UI
      và report đã có trong repository.
- [ ] Không có `.env`, API key, token, dữ liệu thật, cache hoặc generated ticket.
- [ ] Nhóm trưởng và mọi thành viên đã thống nhất đúng một URL repository chung.
- [ ] Nhóm trưởng và mọi thành viên sẽ nộp cùng URL đó trên VLearn.

**URL repository chung dùng để nộp:**

> URL:

- [ ] Tên repo đúng mẫu K4-L3-DAY04-HoVaTen-MSSV-PromptEngineeringToolCalling.
- [ ] Kiểm tra deadline và bản chốt theo [SUBMISSION.md](../../SUBMISSION.md).
