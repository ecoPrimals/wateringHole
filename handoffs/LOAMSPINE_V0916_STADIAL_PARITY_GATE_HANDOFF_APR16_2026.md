<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->

# LoamSpine v0.9.16 — Stadial Parity Gate Compliance

**Date**: April 16, 2026  
**Primal**: loamSpine  
**Version**: 0.9.16  
**Previous handoff**: `LOAMSPINE_V0916_CRYPTO_WIRE_ADAPTER_HANDOFF_APR16_2026.md` (archived)

---

## What

**Stadial parity gate compliance** for loamSpine: remove blocked storage backends and dependency ghosts, upgrade DNS resolver stack, and verify policy (`cargo deny`), `dyn` audit, and test/quality metrics.

---

## Removed

| Area | Scope |
|------|--------|
| **sled** storage backend | ~500 lines production + ~891 lines test |
| **SQLite / rusqlite** storage backend | ~646 lines production + ~682 lines test |

---

## Upgraded

- **hickory-resolver** `0.24` → `0.26` (drops `async-trait` from **hickory-proto** in this path).

---

## Lockfile ghosts eliminated

`sled`, `libsqlite3-sys`, `rusqlite`, `instant`, `fxhash` removed from the dependency graph for this workspace.

---

## Remaining upstream (outside our control)

- **`async-trait`** still appears transitively via **hickory-net** `0.26` (not authored in loamSpine).
- **`ring`** only under optional features (not default production path).

---

## Deep debt — post-gate (April 16, 2026)

| Area | Detail |
|------|--------|
| **bincode v1 → rmp-serde** | Replaced unmaintained `bincode` (RUSTSEC-2025-0141) with `rmp-serde` (MessagePack, pure Rust). `bincode`, `postcard`, `bitcode`, `heapless`, `atomic-polyfill` all absent from lockfile. Advisory ignore removed from `deny.toml`. |
| **biomeOS doc genericization** | 29 literal `biomeOS` references in production doc comments → 0. Replaced with "orchestration layer", "ecosystem pipeline", etc. Self-knowledge compliance: primal code references only `BIOMEOS` IPC protocol constants, not peer names. |
| **PG-33 / GAP-07 startup panic** | **Structurally eliminated**: `mdns` 3.0 (async-std) replaced with `mdns-sd` 0.19 (pure Rust, own daemon thread). No `block_on`, no runtime nesting. `async-std`, `net2`, `proc-macro-error` gone; 3 RUSTSEC advisories removed. Unblocks ludoSpring exp095. |

---

## Policy & audits

- **`cargo deny check`**: **bans** and **advisories** both **PASS** (bincode advisory eliminated).
- **`dyn` audit**: **72** total — **28** doc/comment, **37** `Pin<Box<dyn Future>>` (object safety), **7** `Arc<dyn>` finite-implementor. **Non-blocking.**

---

## Metrics

| Metric | Value |
|--------|--------|
| Tests | **1,442** |
| Rust source files | **178** |
| `clippy` warnings | **0** |
| `#[async_trait]` attributes in our code | **0** |
| Rust edition | **2024** |
| Serialization | `rmp-serde` (MessagePack) — pure Rust, zero advisories |
| biomeOS prod doc refs | **0** (self-knowledge compliant) |

---

## Post-gate deep debt sweep (April 20, 2026)

| Area | Detail |
|------|--------|
| **Socket naming aligned** | Primary socket `permanence.sock` → `loamspine.sock` per `{primal}-{FAMILY_ID}.sock` ecosystem convention. `ledger.sock` capability symlink, `permanence.sock` legacy backward-compat symlink. `"ledger"` added to CAPABILITIES — fixes `discover_by_capability("ledger")` failure (primalSpring Phase 45 item 4). |
| **mdns-sd `ResolvedService` API** | `resolved_to_discovered` and `mdns_discover_service_impl` updated to `ResolvedService` field access (`.port`, `.addresses`) instead of `ServiceInfo` getters — fixes compile error with `--all-features`. |
| **`ServerError::Bind` structured** | Evolved from `Bind(String)` to `Bind { context, #[source] source: io::Error }` — preserves underlying I/O error for introspection. All call sites in jsonrpc/uds.rs, jsonrpc/server.rs, tarpc_server.rs updated. |
| **`bond_ops.rs` error propagation** | Replaced `.map_err(\|e\| ApiError::Internal(e.to_string()))` with `?` via existing `From<LoamSpineError> for ApiError` impl. |
| **`deny.toml` license cleanup** | Removed 5 stale license allowances with no matching dependencies. |
| **Orphan bench wired** | `crates/loam-spine-core/benches/storage_ops.rs` wired into Cargo.toml `[[bench]]`. |
| **BTSP NDJSON wire-format aligned** | UDS accept loop auto-detects primalSpring-style BTSP (`{"protocol":"btsp",...}\n`) and routes to `perform_ndjson_server_handshake` (newline-delimited JSON, `session_id` in ServerHello). Resolves primalSpring Phase 45b BTSP escalation gap. 12 new tests (1,454 total). |
| **Capability/path constant unification** | `"permanence"`/`"ledger"` literals in `neural_api/mod.rs` → `primal_names::LEGACY_DOMAIN`/`CAPABILITY_DOMAIN`. `"biomeos"` path segment in `network.rs` → `primal_names::BIOMEOS_SOCKET_DIR`. Single source of truth for all identity/path constants. |
| **`specs/ARCHITECTURE.md` updated** | Stale SQLite/sled/RocksDB storage layer references replaced with current redb + in-memory backends. Code examples updated. |
| **Deep debt audit clean** | Zero files >800L (max 783 test, 605 prod). Zero `unsafe`. Zero `todo!`/`FIXME`/`HACK`. Zero hardcoded primal names in production. All mocks `#[cfg(test)]` gated. `cargo deny check` clean. 2 `#[allow]` justified (feature-conditional async). All `#[expect]` have `reason` strings. Lockfile refreshed. |
| **BTSP provider socket wired** | Static BTSP mode (`btsp_config = Some`) now peeks first byte via `BufReader::fill_buf()` and auto-detects NDJSON vs binary. Previously, NDJSON connections were misrouted to length-prefixed handshake. `perform_server_handshake` refactored to split reader/writer. 2 new integration tests. |
| **BTSP Step 3→4 verification relay fixed** | All three BearDog relay calls aligned with `beardog_types::btsp::rpc`: `create` sends `family_seed` (base64) instead of `family_seed_ref`; `verify` uses `session_token`/`response`/`preferred_cipher`; `negotiate` uses `session_token`/`cipher`. Challenge generated by BearDog, not loamSpine. `generate_challenge()` removed, `resolve_family_seed()` added. Same pattern as sweetGrass April 22 fix. 5 new tests. |
| **BTSP HandshakeComplete wire fix** | `HandshakeComplete` was missing `"status":"ok"` discriminator field required by primalSpring. Both length-prefixed and NDJSON paths updated. Resolves Phase 45c "incomplete handshake" gap. 1 new test (1,503 total). |

---

## Status

**loamSpine clears the stadial gate** for **`sled`** and **`libsqlite3-sys`**, and **eliminates** the `bincode` RUSTSEC advisory via migration to `rmp-serde`. Transitive **`async-trait`** via **hickory-net** is **not under our control**; tracked as upstream-only. Post-gate deep debt sweep (April 20–22) resolved primalSpring Phase 45 socket naming gap, Phase 45b BTSP wire-format alignment, BTSP provider socket wiring, and additional error quality improvements.

---

*Previous handoffs archived in `handoffs/archive/LOAMSPINE_V0916_*`*

---

**License**: AGPL-3.0-or-later
