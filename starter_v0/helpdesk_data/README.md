# Fictional Helpdesk Data

All records in this folder are synthetic and deterministic. They exist only for
the lab and contain no real employee or company data.

- `assets.json`: 9 mock assets across laptops, desktop, mobile, printer, and meeting room.
- `users.json`: 10 mock employees with varied account/MFA states and assigned assets.
- `service_status.json`: mock shared-service status page.
- `knowledge_base/`: 11 troubleshooting articles, including one safe prompt-injection fixture.
- `tickets.json`: 5 mock seed tickets for the team-built `check_ticket_status` tool; `internal_notes` are never returned.

Students may extend this data when they build a new tool, but they must document
their contract and add eval cases for the behavior they introduce.
