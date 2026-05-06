# skunkBat v0.2.0-dev — primalSpring Audit Response (Cross-Primal Phase)

**Date**: May 6, 2026
**From**: skunkBat team
**To**: primalSpring, Songbird, coralReef, ecosystem
**Triggered by**: primalSpring cross-primal upstream debt audit

---

## Summary

Addressed three cross-cutting findings from primalSpring's audit of all primals.
Wire Standard L3 was already complete on `capabilities.list`; applied it to
`identity.get` for consistency. BufReader post-negotiate bug class resolved.
Songbird tier-1 registration probe path added. 338 tests, all gates green.

---

## Audit Triage

| Finding | Source | Resolution |
|---------|--------|-----------|
| Wire Standard L3 on `capabilities.list` | coralReef | **Already done** — `protocol: "jsonrpc-2.0"`, `transport: ["uds", "tcp"]` present |
| Wire Standard L3 on `identity.get` | coralReef (consistency) | **DONE** — added `protocol` + `transport` fields |
| BufReader post-negotiate corruption | barraCuda/coralReef cross-cutting | **DONE** — pass inner stream via `buf_reader.into_inner()` |
| Discovery escalation hierarchy docs | skunkBat-specific | **Already done** (CONTEXT.md, now README.md too) |
| Tier-1 Songbird registration | skunkBat/petalTongue | **DONE** — `SONGBIRD_SOCKET` + `songbird.sock` probe in registration |
| Port fix (9750→9140) | primalSpring-side only | No action needed — our `DEFAULT_PORT` is 9140 |
| sweetGrass whitespace-tolerant detection | cross-cutting | N/A — we `trim()` all NDJSON lines; no TCP multiplexer needed |
| ipc.register identity verification | Songbird | Awareness only — we're the registrant, not the registry |

---

## Code Changes

### BufReader Post-Negotiate Fix (`server.rs`)

```rust
// BEFORE: passed BufReader (could contain leftover NDJSON bytes)
let buf_reader = lines.into_inner();
run_encrypted_frame_loop(state, sessions, buf_reader, writer, &keys).await;

// AFTER: drain BufReader, pass raw stream
let buf_reader = lines.into_inner();
if !buf_reader.buffer().is_empty() {
    tracing::warn!("leftover bytes at negotiate boundary — protocol violation");
}
let inner_reader = buf_reader.into_inner();
run_encrypted_frame_loop(state, sessions, inner_reader, writer, &keys).await;
```

### Songbird Registration Probe (`registration.rs`)

Discovery socket resolution now probes (first existing wins):
1. `DISCOVERY_SOCKET` env var
2. `SONGBIRD_SOCKET` env var
3. `{socket_dir}/songbird.sock`
4. `{socket_dir}/discovery-{FAMILY_ID}.sock`
5. `{socket_dir}/discovery.sock`

This ensures tier-1 Songbird registration activates automatically when Songbird
is available, without requiring explicit configuration.

---

## Build Health

| Metric | Value |
|--------|-------|
| Tests | 338 passing / 0 failures / 15 ignored |
| Clippy | CLEAN (pedantic + nursery, `-D warnings`) |
| Format | CLEAN |
| Source files | 43 |
| Max file | 790 lines (`negotiate.rs`) |
| Version | 0.2.0-dev |

---

## For Ecosystem Teams

### Songbird
- skunkBat now probes for `songbird.sock` directly (not just generic discovery)
- When Songbird is reachable, `ipc.register` fires automatically on startup
- Capabilities registered: `security`, `baseline`, `metadata`, `response`, `lineage`, `health`

### coralReef / barraCuda
- Confirmed the BufReader pattern fix — we had the same class of bug
- Our test helper (`server_tests.rs`) already used `reader.into_inner()` — production now matches

### primalSpring
- No action items remain from this audit cycle
- Wire L3, discovery hierarchy, Songbird registration, BufReader audit all resolved
