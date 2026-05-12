# BearDog v0.9.0 — Wave 34: Deep Debt Evolution — Hardcoding, Mocks, Refactoring

| Field | Value |
|-------|-------|
| Date | 2026-04-11 |
| From | BearDog v0.9.0 (deep debt evolution session) |
| To | primalSpring, all downstream primals |
| License | AGPL-3.0-or-later |
| Supersedes | BEARDOG_V090_WAVE33_DEEP_DEBT_EVOLUTION_HANDOFF_APR9_2026 (archived) |

---

## 1. What Happened

A comprehensive deep debt cleanup and code evolution pass across the entire BearDog codebase, targeting hardcoded values, production mocks, dead code, config placeholders, and oversized files.

**All identified items were resolved in-session.** All four quality gates pass clean.

---

## 2. Hardcoding Eliminated (4 sites)

| File | Was | Now |
|------|-----|-----|
| `beardog-types/.../system.rs` | Static `/etc`, `/var`, `/tmp` paths | `resolve_config_dir()`, `resolve_data_dir()`, etc. via XDG Base Directory Spec |
| `beardog-core/socket_config.rs` | `unwrap_or(1000)` UID default | `/proc/self/status` safe resolution (no `unsafe`, no FFI) |
| `beardog-tower-atomic/discovery.rs` | Same UID 1000 default | Same `/proc/self/status` resolution |
| `beardog-config/.../network_ports.rs` | `https://localhost:8080` UPA fallback | `resolve_upa_fallback_base_url()` from `BEARDOG_UPA_URL` / `BEARDOG_EXTERNAL_HOST` / `BEARDOG_API_PORT` |

**For other primals**: If you resolve filesystem paths, use XDG env vars (`XDG_CONFIG_HOME`, `XDG_DATA_HOME`, `XDG_CACHE_HOME`, `XDG_RUNTIME_DIR`) before falling back to FHS defaults.

---

## 3. Production Mocks → Real Implementations (8 items)

| Component | Was | Now |
|-----------|-----|-----|
| Ionic bond proposal signature | SHA-256 placeholder digest | Ed25519 signature (deterministic key from primal name + node ID via HKDF-SHA256) |
| Capability announcements | HMAC-SHA256 digest | Ed25519 signature with verifiable public key |
| Compliance metrics | Hardcoded `95.0` score | Dynamic computation from audit trail pass/fail ratio |
| HSM unimplemented ops | `success: true` with empty result | `success: false` with descriptive error message |
| ML threat analysis (no models) | Hardcoded fake events with IPs | Honest empty `Vec<ThreatEvent>` |
| ML threat analysis (with models) | Same hardcoded data | Dynamic events from model scoring |
| Health check (external subsystems) | Blanket "unknown" status | Only report subsystems with actual probes |
| Config placeholders | No-op methods returning stale data | `#[deprecated]` with migration notes |

---

## 4. Dead Code Removed

- `crates/beardog-core/src/external_functions/grafana.rs` — simulated Grafana stub, never in module tree
- `crates/beardog-core/src/external_functions/prometheus.rs` — simulated Prometheus stub, never in module tree
- `PLACEHOLDER` comment in `beardog-threat/src/threat/tests.rs` — cleaned

---

## 5. Smart Refactoring (2 large files)

| File | Before | After |
|------|--------|-------|
| `monitoring.rs` | 978 LOC single file | `monitoring/mod.rs` + `alerts.rs` + `metrics.rs` |
| `self_knowledge.rs` | 832 LOC single file | `self_knowledge/mod.rs` + `identity.rs` + `endpoints.rs` + `capabilities.rs` |

All public re-exports preserved — no API breakage.

---

## 6. Gate Table

| Gate | Status |
|------|--------|
| `cargo fmt --check` | PASS |
| `cargo clippy` (pedantic+nursery, `-D warnings`) | 0 warnings |
| `cargo doc` (`-D warnings`) | 0 warnings |
| `cargo test --workspace` | 14,756+ pass, 0 fail |
| Coverage | 90.51% line (llvm-cov) |
| Files > 1000 LOC | 0 |
| TODO/FIXME | 0 |
| Rust files | 2,128 |

---

## 7. Ecosystem Impact

- **XDG path resolution pattern**: Other primals should adopt `resolve_*_dir()` functions instead of hardcoded FHS paths. Template available in `beardog-types/constants/domains/system.rs`.
- **`/proc/self/status` UID resolution**: Safe, zero-FFI alternative to `libc::geteuid()` for Linux. Pattern available in `beardog-core/socket_config.rs`.
- **Ed25519 identity signing**: Ionic bonds and capability announcements are now cryptographically signed. Other primals implementing BTSP proposals should use Ed25519 with deterministic key derivation from primal identity.
- **Honest subsystem reporting**: Primals should only report health for subsystems they can actually probe — do not default external subsystems to "unknown".

---

## 8. Debt Remaining

| Item | Status |
|------|--------|
| 75 `#[allow(` remaining | Documented with `reason`; `expect` unfulfilled on these |
| plasmidBin harvest | Ecosystem-wide — needs musl-static rebuild |
| BTSP Phase 2 rollout | Ecosystem-wide — other primals need handshake enforcement |
| `#[deprecated]` cleanup | ~80 deprecated type aliases pending v0.10.0 removal wave |
