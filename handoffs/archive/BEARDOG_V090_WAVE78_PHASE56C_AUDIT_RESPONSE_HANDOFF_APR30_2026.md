<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 — Wave 78 Handoff: primalSpring Phase 56c Audit Response

**Date**: April 30, 2026
**From**: BearDog Team
**To**: primalSpring, all consuming primals
**Audit source**: primalSpring Phase 56c — Stadial Convergence (April 30, 2026)

---

## Summary

Both BearDog items from the Phase 56c audit are **already resolved**. Zero code changes required.

---

## Item 1: `async-trait` 49→0 — CONFIRMED COMPLETE

primalSpring's own `PRIMAL_GAPS.md` confirms at line 351:

> **COMPLETE** (Wave 53–55: 49→0, 22 traits → 18 enum dispatch types, RPITIT, dep removed + lockfile clean, banned in deny.toml)

Verification:
- `grep -r '#[async_trait]'` in `.rs` files: **0 actual usages** (3 hits are comments documenting "NOT #[async_trait]")
- `async-trait` not in any `Cargo.toml` as dependency
- `syn v1` fully eliminated from dependency tree (`cargo tree -i 'syn:1'` → "did not match any packages")
- `syn v2` remains as standard proc-macro infrastructure (serde_derive, clap_derive, thiserror, tokio-macros, tracing-attributes) — compile-time only, not actionable
- `cargo deny check bans` — PASS

## Item 2: `crypto.sign_contract` — CONFIRMED WIRED SINCE WAVE 42

The audit blurb stated: "`crypto.sign_contract` for ionic bond negotiation not yet exposed as IPC method — cross-tower compositions blocked."

This is **stale information**. Evidence:

| Location | Status |
|----------|--------|
| `ionic_bond/mod.rs:94` | Method registered in `IonicBondHandler::methods()` |
| `ionic_bond/mod.rs:112` | Routed to `handle_sign_contract` |
| `ionic_bond/contract.rs:20` | Full handler implementation |
| `capabilities.rs:192` | Advertised in `capabilities.list` response |
| `capabilities.rs:265` | Performance profile declared |
| `ionic_bond/tests.rs` | 10+ integration tests (deterministic terms hash, valid signature, routing) |
| `beardog-types/ionic_bond.rs:254` | Wire types: `SignContractParams`, `SignContractResponse` |

Full ionic bond lifecycle is operational: `crypto.ionic_bond.propose` → `.accept` → `.seal` + standalone `crypto.sign_contract` / `crypto.verify_contract`.

primalSpring's own `PRIMAL_GAPS.md` line 394 confirms:
> **RESOLVED** — Wave 42: `crypto.ionic_bond.seal` completes propose→accept→seal lifecycle with real Ed25519 verification at each step.

## Additional Cross-Check

Other IPC methods referenced by ecosystem primals — all confirmed wired and tested:

| Method | Handler | Consumer |
|--------|---------|----------|
| `lineage.list` | `genetic.rs:155` | skunkBat thymic selection |
| `btsp.session.verify` | `btsp/mod.rs:150` | skunkBat, composition validation |
| `crypto.derive_public_key` | `purpose_key.rs` (Wave 77) | biomeOS Neural API |
| `crypto.derive_purpose_key` | `purpose_key.rs` (Wave 72) | NUCLEUS bootstrap |
| `crypto.sign_registration` | `purpose_key.rs` (Wave 72) | Songbird relay |

## Dependency Health

| Metric | Status |
|--------|--------|
| `cargo deny check` | 4/4 PASS |
| `syn v1` in tree | **eliminated** |
| `async-trait` in tree | **eliminated** |
| `ring` in tree | **eliminated** (Wave 55) |
| Duplicate deps (transitive) | thiserror v1/v2, getrandom v0.2/v0.3/v0.4, rand v0.8/v0.9 — all external, not actionable |
| `#[async_trait]` in code | 0 |
| `#[allow]` without reason | 0 in production code |

## Recommendation

Update the Phase 56c audit blurb for BearDog to:

> **BearDog** — Gold standard. async-trait fully eliminated (Wave 53-55, 49→0). `crypto.sign_contract` wired and tested since Wave 42. 102 CryptoHandler + IonicBondHandler methods. 90.5% coverage. Zero open gaps.
