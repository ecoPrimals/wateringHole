# Songbird v0.2.1 — Wave 141: primalSpring April 16 Audit Response

**Date**: April 16, 2026
**Primal**: Songbird
**Version**: v0.2.1
**Wave**: 141
**Contact**: primalSpring
**Previous**: Wave 140 (primalSpring Phase 43 audit + deep debt, Apr 15)

---

## Summary

Wave 141 addresses all 4 items from the primalSpring April 16 review.
`family_only` filtering is now live, ring lockfile chain is fully documented,
and async-trait count is accurately audited.

---

## Audit Items (4/4 Addressed)

### SB-01: `ring` in Cargo.lock — Documented Exception

**Status**: Documented. Cannot be cleaned without removing `kube` dependency.

Ring appears in `Cargo.lock` via two chains:
- **Chain A**: `songbird-cli` → `rustls-rustcrypto 0.0.2-alpha` → `rustls-webpki 0.102` → `ring`
- **Chain B**: `songbird-universal[k8s]` → `kube 0.95` → `kube-client` → `hyper-rustls[ring]` → `rustls[ring]` → `ring`

**Default build**: ring is NOT compiled (`cargo tree -i ring` = no match).
Chain A's ring dep is optional/unactivated; Chain B's kube is behind the `k8s`
feature flag (not default). `--all-features` builds DO compile ring (via kube).

**Upstream fixes needed**:
- `rustls-rustcrypto` master has dropped `webpki 0.102` → eliminates Chain A on release
- `kube-client` needs `hyper-rustls/aws-lc-rs` option → eliminates Chain B

`deny.toml` updated with complete chain documentation.

### SB-02: Content Distribution Federation — `family_only` Now Live

**Status**: Resolved.

`discovery.peers` `family_only` parameter was previously accepted but no-op
(SB-04 TODO). Now resolves own family via `FAMILY_ID` / `SONGBIRD_FAMILY_ID`
environment variables and filters peers to matching `family_id`. When no
env var is set, returns all peers (graceful degradation).

Implementation uses injectable `_with` pattern for testability. Two new tests:
- `list_peers_family_only_filters_by_env` — verifies filtering with `FAMILY_ID=nat0`
- `list_peers_family_only_no_env_returns_all` — verifies graceful fallback

**Transfer coordination** (deep seeder/leecher networking) remains future work —
requires content transfer protocol and chunk routing, which is a substantial
feature beyond discovery-layer scope.

### SB-03: Mito-Beacon Provider — Upstream Dependency

**Status**: Songbird-side complete. Waiting on upstream.

`SecurityBirdSongProvider` implements `beacon.encrypt`, `beacon.decrypt`,
`beacon.get_id` with graceful fallback to legacy `birdsong.*` RPCs when the
security provider returns `Method not found`. Beacon credential tier model
documented in `songbird-types/defaults/beacon.rs`.

**Blocker**: Security provider (BearDog) must expose `beacon.*` RPC methods
for beacon-tier credentials to be used. Until then, fallback to lineage-tier
`birdsong.*` methods is transparent and functional.

### SB-04: async-trait — Accurate Audit, No Migration Path

**Status**: Audited. All instances required.

**Count**: 145 effective `#[async_trait]` annotations (150 total, 5 in doc
comments). Every instance is either:
1. A trait definition used with `dyn Trait` dispatch (`Arc<dyn T>`, `Box<dyn T>`)
2. An impl block for such a trait
3. A supertrait of a dyn-dispatched trait (e.g., `Provider` tree)
4. An impl of axum's `FromRequestParts` (external trait requirement)

**No mechanical migration possible** without `async_fn_in_dyn_trait` stabilization
(rust-lang/rust#133119, still experimental as of April 2026). SB-06 tracking
comment updated in workspace `Cargo.toml`.

---

## Files Changed

| Crate | Files |
|-------|-------|
| `songbird-universal-ipc` | `handlers/discovery_handler.rs` (family_only impl + 2 tests) |
| `songbird-types` | `defaults/beacon.rs` (doc clarification) |
| workspace root | `Cargo.toml` (SB-06 count), `deny.toml` (ring chain), `Cargo.lock` (cargo update) |

---

## Verification

```bash
cargo check --workspace                                   # 0 errors, 0 warnings
cargo fmt --check                                         # Clean
cargo clippy --workspace --all-targets -- -D warnings     # 0 warnings
cargo test --workspace --lib                              # 7,336 passed, 0 failed, 22 ignored
cargo deny check                                          # advisories ok, bans ok, licenses ok, sources ok
```

---

## Status

All primalSpring April 16 audit items addressed (4/4).
`family_only` filtering live. Ring lockfile fully documented.
async-trait count accurately tracked (145 effective, all dyn-required).

Remaining: coverage (72.29% → 90%), BTSP Phase 3, Tor crypto (blocked),
TLS sovereign certs, content transfer coordination (future), upstream
beacon-tier RPCs from security provider.
