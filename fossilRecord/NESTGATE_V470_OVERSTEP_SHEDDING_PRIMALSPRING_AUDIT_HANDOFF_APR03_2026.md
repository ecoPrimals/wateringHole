# NestGate v0.4.70 — Overstep Shedding & primalSpring Audit Handoff

**Date:** April 3, 2026
**Commit:** 3d96c2dc
**Session:** 19 — primalSpring audit overstep resolution

## primalSpring Audit Finding

> NestGate — Heaviest overstep in ecosystem: crypto (nestgate-security),
> discovery (nestgate-discovery), network (nestgate-network), AI/MCP
> (nestgate-mcp), orchestration (nestgate-automation). Priority: Continue
> shedding crypto/network/AI modules to their owners.

## Actions Taken

### nestgate-network — DEPRECATED (entire crate)

- `#![deprecated(since = "4.7.0")]` added to crate root
- Cargo.toml description updated to reflect deprecated status
- **Zero workspace dependents** — no code imports this crate
- Test files given `#![allow(deprecated)]` to continue compiling
- Scheduled for removal once delegation to network capability provider is mature

### nestgate-mcp — CONFIRMED REMOVED

- Already removed from workspace in prior sessions
- No directory, no Cargo.toml entry

### nestgate-automation — CLEANED

- Removed dead `network-integration` feature (was default-on but `uuid` dep unused in code)
- Deleted `DiscoveryConfig` struct and `from_automation_config()` (orchestration overstep behind dead feature)
- Deleted `DiscoveryConfigCanonical` type alias
- nestgate-zfs: removed `network-integration` feature passthrough; simplified `check_zfs_ecosystem_availability`
- Remaining content is storage-legitimate: lifecycle policies, dataset analysis, tier prediction

### nestgate-security — DOCUMENTED DELEGATION MODEL

- Crate description updated to reflect delegation-first architecture
- Crate docs now explain: CryptoDelegate forwards crypto.* via IPC; local `sha2`/`x509-parser`
  are for certificate fingerprinting and validity checking, not cryptographic operations
- No code removed — the crate is already primarily delegation glue + cert parsing

### nestgate-discovery — OVERSTEP DOCUMENTED

- Crate docs now include overstep reduction status table
- `discovery_mechanism` (2,000 lines): deprecated, zero external consumers, mDNS/Consul/K8s belong with orchestration
- `service_discovery` (3,000 lines): deprecated, still coupled to `capability_resolver` — needs larger refactor to remove
- nestgate-core: `service_discovery` re-export now carries `#[deprecated]` warning

### NG-01 / NG-03 — CONFIRMED RESOLVED

- NG-01: `FileMetadataBackend` is production default in `SemanticRouter::new()`
- NG-03: `data.*` handlers return structured delegation errors; excluded from `capabilities.list`

## Overstep Matrix (Post-Session)

| Crate | Lines | Dependents | Status |
|-------|-------|------------|--------|
| nestgate-mcp | — | — | **Removed** |
| nestgate-network | ~8,898 | **Zero** | **Deprecated** (crate-level) |
| nestgate-automation | ~4,300 | api, zfs | **Cleaned** — storage-legitimate content remains |
| nestgate-security | ~7,425 | core, api | **Delegation documented** — local crypto is cert parsing only |
| nestgate-discovery | ~29,118 | core, security | **Deprecated modules documented** — active modules are legitimate |

## Remaining Overstep Debt

| Area | Effort | Blocked On |
|------|--------|-----------|
| Remove `nestgate-network` from workspace | Low | Confidence that no downstream test fixtures reference it |
| Remove `discovery_mechanism` module | Low | Already zero external consumers; just delete + update lib.rs |
| Decouple `service_discovery` from `capability_resolver` | Medium | Refactor `InMemoryRegistryAdapter` to use local types |
| Shed `nestgate-security` cert utilities | Low (optional) | Determine if cert fingerprinting should delegate to bearDog |

## Verification

```
cargo fmt --all           ✅ clean
cargo clippy -D warnings  ✅ clean
cargo test --workspace    ✅ 12,271 passed, 0 failed, 472 ignored
```
