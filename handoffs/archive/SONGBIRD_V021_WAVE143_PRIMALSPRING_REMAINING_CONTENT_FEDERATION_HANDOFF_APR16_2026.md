# Songbird v0.2.1 — Wave 143 Handoff

**Date**: April 16, 2026
**Wave**: 143
**Scope**: primalSpring remaining work — content distribution federation, ring documentation, async-trait re-audit

---

## Resolved Items

### 1. Content Distribution Federation (Wired)

- **`ContentAnnouncementStore`**: In-memory registry with TTL-based expiration (10min default), keyed by `(topic, node_id)` for de-duplicated seeder announcements
- **`discovery.announce` topic mode**: Now stores content announcements in the registry (was previously a stub that echoed params)
- **`discovery.content_peers`**: New JSON-RPC method for leechers to find seeders by topic, with `family_only` and `manifest_hash` filters
- **`ContentPeers` variant**: Added to `DiscoveryMethod` enum with full dispatch wiring
- **BLAKE3 addressing**: `manifest_hash` param flows through announce → store → query, compatible with NestGate `ContentManifest`
- **10 new tests**: announce storage, re-announce update, presence-no-store, content_peers query/filter/family/manifest/required-topic/empty-result, TTL gc, TTL query expiration

### 2. `ring` in Cargo.lock (Documentation Updated)

- `deny.toml` ban comment updated with April 2026 upstream status
- `rustls-rustcrypto` still at 0.0.2-alpha on crates.io (no release since Wave 140)
- kube 0.95 `aws-lc-rs` feature noted as also C/ASM — not ecoBin compliant
- `cargo deny check` passes clean; ring is never compiled in default builds
- No binary impact — lockfile entry is metadata artifact

### 3. `async-trait` Re-Audit (141 Annotations)

- Down from 145 (Wave 141) to 141 — reduction from code evolution
- Exhaustive trait-by-trait analysis confirmed all are genuinely dyn-dispatched
- ~16 in test/mock code implementing dyn-dispatched traits
- SB-06 tracking in `Cargo.toml` updated
- Blocked on `async_fn_in_dyn_trait` stabilization (rust-lang/rust#133119)

---

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 7,360 lib passed, 0 failed |
| Clippy | 30/30 crates clean (pedantic + nursery) |
| Formatting | clean |
| cargo-deny | advisories ok, bans ok, licenses ok, sources ok |
| New tests this wave | 10 |

---

## What's Next

- **Transfer coordination**: Wire actual byte-level transfer signaling between seeders/leechers (currently Songbird handles discovery; NestGate handles storage)
- **BTSP Phase 3**: Cipher negotiation + encrypted framing
- **Coverage**: Push toward 90% target (currently 72.29%)
- **async-trait**: Reassess when `async_fn_in_dyn_trait` stabilizes
