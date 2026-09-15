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
- Hỗ trợ AI cho bản v1 và team eval: Codex soạn quy tắc hỏi lại, mô tả input và 10 case mới; đã kiểm tra cấu trúc bằng code. Nhóm cần review kỳ vọng và Người 2 chạy live eval để đo hiệu quả.

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
| v1 | Prompt và mô tả input trong tools.yaml: hỏi lại khi thiếu/mơ hồ thông tin | Quy tắc hỏi lại nhất quán giảm tự suy diễn input | case_accuracy | 0.7333 | Chưa đo | Chờ Người 2 chạy |
| v2 |  |  |  |  |  |  |
| v3 |  |  |  |  |  |  |

### CP1 — Baseline đã kiểm tra

- Run: `v0_B_base_openrouter_20260915T190138378558`; đủ 30 kết quả, `measured_cases = total_cases = 30`, `provider_error_cases = 0`.
- Metric: `case_accuracy = 0.7333`, `tool_routing_accuracy = 0.7667`, `argument_accuracy = 0.7333`, `multiturn_accuracy = 0.8`.
- [Version log](version_log.csv) có một dòng v0; `metric_before` để trống vì đây là baseline. Các hash và `metric_after` đã đối chiếu với JSON.
- Artifact version: `v0+p27467914bc4d+td4848549884e`.
- Prompt SHA-256: `27467914bc4d93574eb1a418b77247c51682e04401c78fb4445c22b9019185a0`.
- Tools SHA-256: `d4848549884eb9613313a2a8dec5faca4e8299842790ac2d42a04195b4da3198`.
- Bộ base SHA-256 khi chốt CP1: `8d9b4180a2d3715fd1351efb4990af20e0b149d40e6155510f2605fecb2ec3ed`. Tại commit CP1 `75d0145`, bộ case và hai artifact còn nguyên bản; hash hai artifact khớp run v0. Prompt/tools trong working tree sau CP1 đã được sửa để chuẩn bị v1. Giữ bộ 30 case này qua v1–v3.
- Đã đọc kết quả thực thi: 35 tool results, trong đó 3 kết quả có `result.error` (H04, H10, H11). H12 có `status=created` và file ticket giả lập `LAB-1B1E0B98.json` tồn tại; M05 có `status=needs_confirmation`. Điểm routing không chứng minh tool đã hoàn thành đúng hoặc an toàn.
- Run cũ `v0_B_base_openrouter_20260915T184445164741` có 30 lỗi thiếu `OPENROUTER_API_KEY`, 0 case đo được; không dùng làm baseline so sánh.

Lệnh tái hiện từ thư mục `starter_v0` tại commit CP1 `75d0145` (chỉ chạy lại khi cần, có gọi provider và có thể tạo ticket giả lập). Dùng checkout riêng của commit đó; không gắn nhãn v0 cho artifact v1 hiện tại:

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

### V1 — Giả thuyết và bàn giao cho Người 2

**Giả thuyết:** Yêu cầu hỏi lại khi thiếu định danh hoặc môi trường mơ hồ, đồng thời diễn đạt cùng quy tắc trong mô tả input của tool, sẽ giảm việc tự suy diễn tham số. Đây là một thay đổi hành vi được triển khai ở hai artifact; run v1 không tách riêng được tác động của từng file.

Failure tiêu biểu chọn từ v0:

- H10: `laptop` bị dùng làm asset ID; cần hỏi mã máy.
- H11: `Sales` bị dùng làm employee ID; cần hỏi mã nhân viên.
- H19: nhãn môi trường mơ hồ bị suy diễn thành staging; cần hỏi lựa chọn.
- H04: employee ID bị dùng cho inspect_device; theo dõi liệu phân biệt loại định danh có giảm call sai này không.

Đã chuẩn bị v1: thêm mục `Missing or ambiguous information` trong prompt; sửa mô tả clarify, asset_id, employee_id và environment trong tools.yaml. Tên tool, kiểu dữ liệu, enum, required và chữ ký hàm giữ nguyên. Các đề xuất về ticket confirmation và phạm vi check vẫn dành cho vòng tiếp theo, sau khi xem run v1.

- Artifact version dự kiến: `v1+pe98102928bb0+t6b85488e3d91`.
- Prompt SHA-256: `e98102928bb0f9b1238b151bec598fbdb09807ae8e7132ab1e8ddd40ef7711db`.
- Tools SHA-256: `6b85488e3d912b067b9ac364df3788f199669667bff5e188efb164fb337c4020`.
- Đã kiểm tra tĩnh: 9 declaration khớp chữ ký tool; 10 case nhóm đúng 5+5; expected args dùng tên/enum hợp lệ; bộ base/adversarial/extension không đổi. Kiểm tra fixture với evaluator chỉ chứng minh cấu trúc tương thích, không phải điểm model.
- Chưa chạy provider, chưa có run hoặc metric v1. Version log vẫn chỉ ghi v0 đã đo.

Người 2 lấy đúng commit bàn giao sau khi tác giả commit/push, rồi chạy trong `starter_v0`:

```powershell
.\.venv\Scripts\python.exe scripts/preflight_provider.py --provider openrouter --model openai/gpt-4o-mini
.\.venv\Scripts\python.exe run_eval.py --provider openrouter --model openai/gpt-4o-mini --version v1 --suite base --eval-cases data/eval_base.json
```

Điều kiện nhận kết quả: `measured_cases = total_cases = 30`, `provider_error_cases = 0`; hash trong run khớp artifact bàn giao. Đối chiếu case_accuracy với 0.7333, xem bốn failure trên và mọi case PASS→FAIL; đọc `tool_results[].result.error` và các status tạo ticket. Sau đó thêm dòng v1 vào version_log.csv bằng dữ liệu JSON thật và cập nhật B1. Nếu không cải thiện, ghi trung thực trước khi quyết định v2; chưa kết luận hiệu quả từ bản sửa này.

## B3. Team eval cases

[Bộ case nhóm](../data/eval_group.json) đã có đúng 10 tình huống mới: G01–G05 single-turn, G06–G10 multi-turn. Chốt kỳ vọng trước khi chạy; mọi kết quả dưới đây đang chờ live eval.

| Case ID | What it tests | Expected behavior | Result |
|---|---|---|---|
| G01_choose_shared_device | Hai máy hợp lệ, chưa biết chọn máy nào | clarify choice với hai mã máy | Chưa chạy |
| G02_employee_not_asset | Người mượn máy khác chủ máy; thiếu mã nhân viên | clarify text hỏi mã nhân viên | Chưa chạy |
| G03_independent_status_and_question | Hai việc độc lập, một môi trường chưa rõ | printing production status + clarify môi trường SSO | Chưa chạy |
| G04_two_checks_same_device | Hai phạm vi riêng trên cùng máy | Hai inspect RM-501: security và software | Chưa chạy |
| G05_policy_and_local_guide | Quy định và hướng dẫn là hai nguồn | policy data_privacy + KB security | Chưa chạy |
| G06_resolve_candidate_by_os | Chọn máy theo ánh xạ OS ở lượt trước | inspect LT-411 network | Chưa chạy |
| G07_partial_answer_still_missing | Đã trả lời OS nhưng vẫn thiếu mã máy | clarify text hỏi asset ID | Chưa chạy |
| G08_cancel_only_ticket_branch | Hủy riêng ticket, giữ yêu cầu KB | Chỉ search_kb printing | Chưa chạy |
| G09_confirmation_wrong_ticket | Xác nhận A không áp dụng cho B | clarify yes_no cho ticket B | Chưa chạy |
| G10_correct_finding_before_format | Sửa một finding rồi format | format handoff với nội dung mới | Chưa chạy |

Mỗi case có `metadata.manual_review` để chỉ rõ nội dung cần đọc trong trace. Đặc biệt G09 phải hỏi đúng payload B; G10 phải dùng finding đã sửa. Bộ chấm chỉ so tên tool và subset arguments, nên PASS tự động chưa chứng minh các nội dung này đúng. Multi-turn trong runner chấm phản hồi cho lượt cuối với lịch sử làm ngữ cảnh; không thay thế transcript UI nhiều lượt của CP4.

Sau khi nhóm review case, Người 2 có thể đo bộ group trên cùng bản v1:

```powershell
.\.venv\Scripts\python.exe run_eval.py --provider openrouter --model openai/gpt-4o-mini --version v1 --suite group --eval-cases data/eval_group.json
```

Run group phải có `measured_cases = total_cases = 10`, `provider_error_cases = 0`. Lưu run và phân tích vào B3; cuối CP2 chạy lại bộ group trên bản nhóm chốt (ví dụ v3) và ghi đúng nhãn phiên bản. Phần viết case đã chuẩn bị; phần evidence Eval CP4 chưa hoàn tất cho đến khi có run và review thật.

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
