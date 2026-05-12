# NestGate Session 44b — BTSP Wire Fix + Deep Debt (April 24, 2026)

**From:** NestGate team  
**For:** primalSpring, BearDog, guidestone  
**Status:** BTSP BearDog wire contract fully aligned; deep debt resolved

---

## BTSP Wire Fix (primalSpring Phase 45c response)

### Root cause

`btsp_server_handshake/mod.rs` was sending `"family_seed_ref": "env:FAMILY_SEED"`
to BearDog. BearDog expects `"family_seed": "<base64>"` — the actual seed, not a
reference. BearDog silently failed, causing `guidestone` to report
`BTSP: server closed connection (no ServerHello)`.

### Changes

1. **`btsp.session.create`** — now sends only `{ "family_seed": "<base64>" }`.
   Added `resolve_family_seed()` helper. Removed `client_ephemeral_pub` and
   `challenge` (BearDog generates those server-side).

2. **Create response parsing** — now reads `session_token` (not `session_id`),
   `challenge`, and `server_ephemeral_pub` from BearDog's response.

3. **`btsp.session.verify`** — params aligned to BearDog wire contract:
   `session_token`, `response`, `client_ephemeral_pub`, `preferred_cipher`.
   Was sending wrong field names (`session_id`, `client_response`) plus extra
   params (`server_ephemeral_pub`, `challenge`).

4. **`btsp.negotiate` eliminated** — BearDog returns `session_id` and `cipher`
   directly from verify. Reduces BTSP from 3 to 2 IPC connections per handshake.

5. **Dead code cleanup** — `base64` import removed, `generate_challenge()` moved
   to `#[cfg(test)]`, `ChallengeResponse::session_token` field removed (used
   create-response token instead).

### Verification

- `socat` BTSP ClientHello should now return a ServerHello JSON line
- guidestone should report `btsp:Nest:storage: BTSP authenticated`
- All 26 BTSP handshake tests pass (including new `handshake_fails_without_family_seed`)

---

## Deep Debt Resolution

| Item | Before | After |
|------|--------|-------|
| `isomorphic_ipc/server.rs` | 847 lines | 469 lines (tests → `server/server_tests.rs`) |
| Files >800 lines | 1 | **0** (max 794) |
| `ZfsBackendType::Mock` | In production enum | Removed (dead code) |
| `"beardog.sock"` in XDG discovery | Hardcoded primal name | Capability-based: `["security.sock", "crypto.sock"]` |
| Dev stub "mock" terminology | Comments said "Mock routing" | Cleaned; algorithm `"dev_round_robin"` |
| Canonical alias noise | 47 lines boilerplate | 6 lines |
| `Cargo.toml.orig` in vendor/ | 2 leftover files | Removed |

---

## Metrics

| Metric | Value |
|--------|-------|
| Tests (lib) | 8,816 passing, 0 failures, 60 ignored |
| Coverage | 84.12%+ line (wateringHole 80% met; 90% target) |
| Clippy (pedantic+nursery) | 0 own-code warnings |
| Files >800L | 0 |
| `#[deprecated]` | 0 |
| `TODO`/`FIXME`/`HACK` | 0 in production |
| `#[allow]` in production | 0 |
| `unsafe` | `#![forbid(unsafe_code)]` on all crate roots |

---

## Remaining Work

1. **Coverage 84% → 90%** — focus on `nestgate-config` ports module and runtime fallback paths
2. **Vendored rustls-rustcrypto** — track upstream for drop opportunity
3. **Cross-arch CI** — aarch64/armv7/riscv64 pipeline wiring
4. **guidestone convergence** — verify NestGate hits 13/13 BTSP authenticated after BearDog/Songbird/toadStool also fix their wire issues

---

**Ref:** `BTSP_WIRE_CONVERGENCE_APR24_2026.md` (NestGate section: resolved)
