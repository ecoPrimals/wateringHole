# NestGate Session 45c — Sovereignty, Port Constants, Deep Debt (April 25, 2026)

**From:** NestGate team  
**For:** primalSpring, BearDog, guidestone, all primals  
**Status:** Primal sovereignty enforced; magic numbers eliminated; mock terminology cleaned

---

## Sovereignty Evolution

### BearDog references removed from production code

All doc comments and inline comments in `btsp_server_handshake/mod.rs` that
named "BearDog" have been replaced with "security capability provider" or
"security provider." NestGate production code no longer references any specific
primal by name.

### `SECURITY_FAMILY_SEED` canonical env var

`resolve_family_seed()` now checks (in order):

1. `FAMILY_SEED` (canonical)
2. `SECURITY_FAMILY_SEED` (capability-scoped, new)
3. `BEARDOG_FAMILY_SEED` (backward compat)
4. `BIOMEOS_FAMILY_SEED` (backward compat)

Deployments should migrate to `SECURITY_FAMILY_SEED` over time. Existing
`BEARDOG_FAMILY_SEED` continues to work.

### Session field resilience

`btsp.session.create` response parsing accepts both `session_token` (canonical
per BTSP convergence doc) and `session_id` (some security provider versions).

---

## Port Constant Centralization

Added `runtime_fallback_ports::TARPC` (8091) to the central constants module.
All inline `8091u16` and `8443` magic numbers across `NetworkConfig::default()`,
`capability_port_discovery`, and `ports.rs` now reference named constants.

| Location | Before | After |
|----------|--------|-------|
| `NetworkConfig::default()` | `tarpc_port: 8091` | `runtime_fallback_ports::TARPC` |
| `NetworkConfig::from_env()` | `.unwrap_or(8091)` / `.unwrap_or(8443)` | `runtime_fallback_ports::TARPC` / `HTTPS` |
| `capability_port_discovery.rs` | `Ok(8091)` / `.unwrap_or(8091)` | `runtime_fallback_ports::TARPC` |
| `ports.rs` (2 functions) | `env_parsed(…, 8091u16)` | `runtime_fallback_ports::TARPC` |

---

## Mock Terminology Cleanup

Production comments updated to avoid "mock" terminology:

- `DevelopmentZfsService` doc: "Fast mock service" → "Development ZFS service"
- `create_development_zfs_service` doc: "mock" → "development"
- `ServiceConfigBuilder` doc: "(native, remote, mock)" → "(native, remote)"
- `collect_real_storage_datasets`: "Mock implementation" → "Probe local filesystem"
- `dev_stubs/zfs/types.rs`: "mock code" → "Shared type — used by production handlers"

---

## BTSP Mode-Aware Error Frames (Session 44b→45c)

The `perform_handshake` wrapper now catches all errors from
`run_handshake_protocol` and sends a mode-aware error frame matching the
client's framing (JSON-line or length-prefixed). Clients no longer see silent
EOF on handshake failures.

---

## Root Documentation Reconciliation

All 9 root `.md` files updated to Session 45c metrics:

- Tests: 8,819 passing (lib), 60 ignored, 0 failures
- Coverage: 84.12%+ line
- UDS methods: 51 (CAPABILITY_MAPPINGS wire example fixed from "47")
- Removed stale `data.*` from semantic naming lists
- Dates aligned across STATUS, README, CONTEXT, START_HERE, QUICK_START,
  QUICK_REFERENCE, CONTRIBUTING, DOCUMENTATION_INDEX, CAPABILITY_MAPPINGS

---

## Codebase Audit (Session 45c)

| Metric | Value |
|--------|-------|
| `unsafe` blocks | 0 (all crate roots: `#![forbid(unsafe_code)]`) |
| `#[allow()]` in production | 0 |
| `#[deprecated]` attributes | 0 |
| `unimplemented!()` | 0 |
| `todo!()` in actual code | 0 (only in doc examples) |
| Files > 800 lines | 0 (largest: 792) |
| `ring` in Cargo.lock | 0 |
| Primal names in production | 0 (BEARDOG_FAMILY_SEED kept as backward-compat env var only) |
| Inline magic port numbers | 0 (all centralized in runtime_fallback_ports) |

---

## Remaining Work

1. **Coverage 84% → 90%** target — focus on `nestgate-config` ports module and runtime fallback paths
2. **Vendored `rustls-rustcrypto`** — track upstream release to drop `vendor/` when compatible version publishes
3. **Cross-arch CI** — nestgate-bin binary on aarch64/armv7/riscv64 (workspace `default-members` fix in place)
4. **guidestone** — verify 13/13 BTSP after all primals converge

---

**Ref:** `BTSP_WIRE_CONVERGENCE_APR24_2026.md`, `NESTGATE_V470_SESSION44B_BTSP_WIRE_FIX_HANDOFF_APR2026.md`
