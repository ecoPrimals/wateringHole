# Songbird v0.2.1 — Wave 136: Deep Debt Hardcoding Evolution Handoff

**Date**: April 11, 2026
**Primal**: Songbird
**Version**: v0.2.1
**Wave**: 136
**Contact**: primalSpring

---

## Summary

Wave 136 completes the deep debt overstep cleanup and evolution phase. A comprehensive
audit found zero actionable items for unsafe code, production mocks, TODO/FIXME in Rust
source, production `.unwrap()`/`panic!()`, or large files (>800 LOC). Three categories
of hardcoding evolution were executed.

---

## Changes

### 1. `DEFAULT_SONGBIRD_PORT` Canonical Constant

Added `DEFAULT_SONGBIRD_PORT: u16 = 3492` to `songbird_types::defaults::ports` — the
well-known Songbird service port now has a single source of truth. Replaces 30+ magic-
number `3492` fallbacks across:

- `songbird-universal-ipc`: `onion_handler.rs` (start + connect), `igd_handler.rs`
  (map/unmap/auto_configure), `meta.rs` (onion endpoint assembly)

### 2. `BIOMEOS_RUNTIME_SUBDIR` Constant Propagation

Replaced 12+ hardcoded `"biomeos"` path strings with the canonical
`songbird_types::defaults::paths::BIOMEOS_RUNTIME_SUBDIR` constant across 8 crates:

- `songbird-crypto-provider` (2 sites: neural + security socket fallbacks)
- `songbird-lineage-relay` (XDG socket scan)
- `songbird-orchestrator` (crypto discovery + socket env config)
- `songbird-nfc` (security socket probe)
- `songbird-cli` (status command socket dir)
- `songbird-tls` (XDG biomeOS socket scan)
- `songbird-config` (service locator scan)

### 3. `MDNS_MULTICAST_GROUP` Constant

`songbird-discovery` `NetworkConfig::default()` mDNS multicast address fallback now uses
`songbird_types::constants::MDNS_MULTICAST_GROUP` constant instead of literal `"224.0.0.251"`.

### 4. Contextual Dead-Code Reason Strings

All 25+ generic `"dead code retained intentionally (reserved or API surface)"` reason
strings replaced with specific contextual reasons per-item across 16 files in 10 crates:

- JSON-RPC envelope fields: "deserialized from JSON-RPC envelope; protocol field not read by client"
- Sovereignty router cache: "cache populated by assess_path(); read path reserved for sovereignty scoring"
- Connection pool age: "tracked for connection age eviction and pool health metrics"
- TLS profiler: "reserved for adaptive TLS strategy learning from server behavior"
- Plugin health: "health aggregation for composition dashboard; wired when lifecycle.composition ships"

Zero generic `"reserved or API surface"` reasons remain in the codebase.

---

## Audit Findings (No Action Required)

| Category | Result |
|----------|--------|
| `unsafe` blocks | 0 (`#![forbid(unsafe_code)]` all 30 crates) |
| TODO/FIXME/HACK in Rust | 0 |
| Mocks in production | 0 (all in `#[cfg(test)]`) |
| `.unwrap()` in production | 0 |
| `panic!()`/`unreachable!()` in production | 0 / 2 (provably unreachable QUIC VarInt) |
| Files >800 LOC | 0 (largest 763L) |
| C dependencies in default build | 0 |
| Stale files/debris | 0 |

---

## Verification

```bash
cargo fmt --all                                           # clean
cargo clippy --workspace --all-targets -- -D warnings     # 0 warnings
cargo test --workspace                                    # 13,030 passed, 0 failed, 252 ignored
cargo deny check                                          # advisories ok, bans ok, licenses ok, sources ok
grep -rn 'dead code retained intentionally' crates/       # 0 matches
grep -rn '\.join("biomeos")' crates/ | grep -v test       # 0 production matches
```

---

## Status

**Songbird has zero open gaps in primalSpring `PRIMAL_GAPS.md`.**
All deep debt categories (hardcoding, mocks, unsafe, large files, deps) are at S+ tier.

Remaining work: coverage expansion (72.29% → 90% target), BTSP Phase 3,
Tor onion service crypto (blocked on security provider), TLS sovereign certs.
