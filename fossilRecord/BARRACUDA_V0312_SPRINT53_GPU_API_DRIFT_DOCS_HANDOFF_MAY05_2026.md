# barraCuda v0.3.12 — Sprint 53 Handoff

**Date**: 2026-05-05
**Sprint**: 53 — Phase 58b GPU API Drift Documentation
**Trigger**: primalSpring downstream audit (GPU API drift MEDIUM + Discovery Escalation Hierarchy cross-cutting)

---

## Resolved

### 1. GPU API Drift — `submit_and_poll` → `submit_and_map` (MEDIUM)

**Status**: Documented in `BREAKING_CHANGES.md`

The old `WgpuDevice::submit_and_poll` was:
- Superseded by `submit_and_map<T>` (single-poll readback) in 0.3.5 (Mar 15)
- Made `pub(crate)` (renamed to `submit_and_poll_inner`) — no longer public API
- Formally removed as dead code in Sprint 42 (Apr 13)

**Migration for wetSpring `bio/pairwise_l2_gpu.rs`**:
```rust
// OLD (broken):
device.submit_and_poll(Some(encoder.finish()));
let data = device.map_staging_buffer::<f32>(&staging, count)?;

// NEW (one-line):
let data = device.submit_and_map::<f32>(Some(encoder.finish()), &staging, count)?;
```

Port confirmed at `9740` on ironGate.

### 2. Discovery Escalation Hierarchy (Cross-cutting awareness)

**Status**: Documented in `BREAKING_CHANGES.md` — no code changes needed

barraCuda already participates in 4 of 5 tiers:

| Tier | Mechanism | Status |
|------|-----------|--------|
| 1 | Songbird `ipc.resolve` | Supported since Sprint 47 (`register_with_discovery()`) |
| 2 | biomeOS Neural API | N/A (barraCuda is producer, not Neural API consumer) |
| 3 | UDS filesystem (`math.sock`) | Supported since inception |
| 4 | Socket registry / manifests | Supported (`write_discovery_file()`) |
| 5 | TCP probing (port 9740) | Supported since inception |

---

## Quality Gates

- `cargo fmt --all --check` — pass
- `cargo clippy -- -D warnings` — pass
- No code changes (documentation-only sprint)

---

## Files Changed

- `BREAKING_CHANGES.md` — added `submit_and_poll` deprecation entry + Discovery Escalation table
- `CHANGELOG.md` — Sprint 53 entry
- `WHATS_NEXT.md` — Sprint 53 summary
- `STATUS.md` — date bump
- `specs/REMAINING_WORK.md` — status through Sprint 53
