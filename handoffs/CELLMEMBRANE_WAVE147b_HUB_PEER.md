# cellMembrane Wave 147b — Hub-Side Peer Addition + WG Refactor

**Date:** 2026-07-17
**From:** eastGate (primalSpring overwatch)
**Commit:** `118f116` (cellMembrane main)

---

## Delivery

### `hub.peer` phase — hub-side peer addition

`gate.enroll` is now a **6-phase** enrollment pipeline (was 5):

| # | Phase | What |
|---|-------|------|
| 1 | `manifest.resolve` | Read gate profile from manifest — IP, transport, roles |
| 2 | `wg.keygen` | Generate WireGuard keypair (0600 perms) |
| 3 | `wg.config` | Render wg-quick config from manifest peers |
| 4 | `mesh.verify` | Ping hub via WireGuard tunnel |
| 5 | `forgejo.verify` | SSH test to Forgejo via mesh |
| 6 | `git.remotes` | Configure Forgejo-first remotes on all repos |
| **7** | **`hub.peer`** | **SSH to hub, `wg set` to register new peer** |

The `hub.peer` phase:
- Reads the local WG public key (derives from stored private key)
- Resolves the hub gate's SSH target from manifest (`topology.inner_membrane` → gate profile host/wg_ip)
- SSHs to hub as root
- Runs `wg set wg0 peer <pubkey> allowed-ips <mesh_ip>/32 && wg-quick save wg0`
- Eliminates the manual SSH step that required operator access to golgiBody

### WG helpers extraction (smart refactor)

WireGuard key/config functions extracted from `enroll.rs` into `gate/wg.rs`:
- `wg_keygen_phase`, `derive_wg_pubkey`, `wg_private_key_path` — key management
- `wg_config_phase`, `wg_config_file_path`, `manifest_to_wg_config` — config generation
- `read_local_pubkey` — pubkey derivation from stored private key

Result: `enroll.rs` 503L, `wg.rs` 370L (both well under 800L threshold).

### Deep debt

- Const assertion for `HUB_SSH_TIMEOUT` bounds (compile-time check, not runtime)
- Test manifest TOML deduplication via `test_manifest()` helper
- Zero `unsafe` code, zero mocks in production, zero TODO/FIXME/HACK markers

## Files Changed

| File | Change |
|------|--------|
| `crates/membrane-shadow/src/gate/enroll.rs` | Add `hub.peer` phase, import WG from `wg.rs` |
| `crates/membrane-shadow/src/gate/wg.rs` | **NEW** — WG helpers + 7 tests |
| `crates/membrane-shadow/src/gate/mod.rs` | Register `wg` module |
| `README.md` | Wave 147b, 1089 tests |
| `GLACIAL_SHIFT_TRACKER.md` | Wave 147b entry |
| `VPS_STATE.md`, `RUNBOOKS.md`, `IRONGATE_VERIFICATION.md` | Wave bump |
| `lib.rs` | Add 4 timestamp helpers + 2 HTTP client helpers + 6 tests |
| 14 files across plasmid/, gate/, cloudflare/, etc. | Replace inline chrono/reqwest with helpers |

## Deep Debt: Timestamp Centralization

12 inline `chrono::Utc::now().format(...)` and `.to_rfc3339()` sites → 4 centralized helpers:

| Helper | Format | Sites replaced |
|--------|--------|---------------|
| `utc_now_iso8601()` | `2026-07-17T13:45:00Z` | 7 (integrity, drift, depot×2, signing, bootstrap, post_sync, wave×2) |
| `utc_today()` | `2026-07-17` | 1 (freshness) |
| `utc_now_rfc3339()` | `2026-07-17T13:45:00.123+00:00` | 3 (canary×2, canary_remote, provision) |
| `utc_now_compact()` | `20260717T134500` | 2 (sovereignty_ledger×2) |

## Deep Debt: HTTP Client Centralization

8 `reqwest::Client::builder()` sites → 2 centralized helpers:

| Helper | Purpose | Sites replaced |
|--------|---------|---------------|
| `http_client(timeout)` | Standard TLS client | 7 (cloudflare, sovereignty×2, checksum, download, signing, digitalocean) |
| `http_client_insecure(timeout)` | Loopback testing only | 1 (gateway/shadow) |

## Test Coverage

- **1,089 tests**, 0 failures, 0 clippy warnings (pedantic)
- Commits: `118f116` (hub.peer + WG refactor), `b5e7c51` (timestamp + HTTP dedup)

## Next

- songBird beacon protocol (BTSP self-enrollment) — trustless enrollment without SSH
- northGate NUCLEUS deploy + benchScale validation
- Garden evolution: lithoSpore (ironGate), esotericWebb (flockGate)
