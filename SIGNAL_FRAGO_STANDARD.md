# Signal/FRAGO Standard — Inter-Gate Communication

**Authority**: primalSpring coordination
**Status**: Active (Wave 63)
**Capability domain**: `waterFall signal.*`

---

## Purpose

Signals are machine-readable, git-mediated messages that ride alongside code pushes. They enable teams working across multiple gates to communicate state changes, action requests, and coordination directives without relying on ad-hoc handoff blurbs or out-of-band communication.

A **FRAGO** (Fragmentary Order) is a signal subtype that amends an existing directive — short, actionable, and time-bounded.

---

## Architecture

Signals live in `infra/wateringHole/signals/`. They sync via the same WaterFall cascade-pull mechanism as all other wateringHole content. Gates discover new signals on their next pull; future Forgejo webhooks will enable near-realtime delivery.

```
Team pushes code → creates signal → commits to wateringHole → pushes
Other gates pull wateringHole → membrane signal.list → see pending signals
```

---

## File Location

| Path | Purpose |
|------|---------|
| `signals/active/*.toml` | Active signals awaiting acknowledgment or expiry |
| `signals/archive/wave{N}/*.toml` | Archived signals (completed, expired, or superseded) |

---

## Naming Convention

```
{ISO-timestamp}_{from-gate}_{slug}.toml
```

- **timestamp**: `YYYY-MM-DDTHH-MM` (colons replaced with dashes for filesystem safety)
- **from-gate**: the originating gate identity
- **slug**: lowercase-kebab summary (max 50 chars)

Example: `2026-05-30T18-44_biomeGate_compchem-solver-ready.toml`

---

## Schema

```toml
[signal]
id = "2026-05-30T18-44-biomeGate-compchem-solver-ready"
type = "frago"           # frago | status | request | announce
priority = "routine"     # routine | priority | flash
wave = 63

[from]
gate = "biomeGate"
team = "hotSpring"
project = "springs/hotSpring"
ref = "abc1234"          # commit SHA that prompted this signal

[to]
gates = ["strandGate"]   # target gates, or ["*"] for all gates
teams = ["hotSpring"]    # target teams (informational filtering)

[content]
subject = "CompChem solver v0.3 ready for bench validation"
body = """
New adaptive grid solver merged to main.
Run bench suite with --solver=adaptive flag.
Blocking: strandGate validation before Wave 64 close.
"""

[meta]
created = "2026-05-30T18:44:00-04:00"
expires = "2026-06-01T00:00:00-04:00"
ack_required = true
```

---

## Signal Types

| Type | Purpose | Typical TTL |
|------|---------|-------------|
| `frago` | Amends a standing order — action required | 24-48h |
| `status` | Informational state update — no action required | 12-24h |
| `request` | Asks for something from target gate(s) | Until fulfilled |
| `announce` | Broadcast to all gates — ecosystem-wide notice | Until next wave |

---

## Priority Levels

| Priority | Meaning | Expected response |
|----------|---------|-------------------|
| `routine` | Normal workflow coordination | Next work session |
| `priority` | Time-sensitive, blocking other work | Same day |
| `flash` | Critical — requires immediate attention | ASAP |

---

## Lifecycle

1. **Created**: `membrane signal.post` generates file in `signals/active/`, commits, pushes.
2. **Discovered**: Target gates pull wateringHole; `membrane signal.list` shows pending signals.
3. **Acknowledged**: `membrane signal.ack <id>` appends `[[acks]]` entry, commits, pushes.
4. **Archived**: `membrane signal.archive` moves expired or fully-acked signals to `signals/archive/wave{N}/`.

### Acknowledgment Format

Appended to the signal file by the receiving gate:

```toml
[[acks]]
gate = "strandGate"
timestamp = "2026-05-30T19:02:00-04:00"
note = "Bench suite queued, results by 21:00"
```

Multiple gates can ack independently; each appends its own `[[acks]]` entry.

---

## Membrane CLI Commands

| Command | Action |
|---------|--------|
| `membrane signal.post --to <gate> --type <type> --subject "..." [--body "..."] [--project <path>]` | Create and push a signal |
| `membrane signal.list [--all]` | List active signals for this gate (or all) |
| `membrane signal.ack <id> [--note "..."]` | Acknowledge a signal |
| `membrane signal.archive` | Archive expired/fully-acked signals |

---

## Conventions

- One signal per file. Do not batch unrelated messages.
- Keep subjects under 80 characters.
- Body is optional for simple status updates.
- `ref` should be the commit SHA that prompted the signal (for traceability).
- Signals are never deleted — they are archived to preserve the coordination fossil record.
- Ack notes should be brief (what you're doing, ETA if applicable).

---

## Phase 2: Near-Realtime Delivery (Future)

When Forgejo webhooks are deployed on wateringHole:

1. Forgejo post-receive detects new files in `signals/active/`
2. Webhook POSTs to peptidoglycan `signal-relay` service
3. `signal-relay` broadcasts via Songbird `mesh.publish` to subscribed gates
4. Subscribing gates' cascade-pull fires immediately

No schema changes required — signal files remain the durable store regardless of delivery mechanism.
