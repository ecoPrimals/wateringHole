# barraCuda v0.3.11 — BTSP Socket Naming & GAP-MATRIX Resolution Handoff

**Date:** April 8, 2026
**Sprint:** 34
**Version:** 0.3.11
**Scope:** GAP-MATRIX-12 (FAMILY_ID socket scoping + BIOMEOS_INSECURE guard) + GAP-MATRIX-06 (plasmidBin metadata freshness)
**Source:** primalSpring downstream audit → `BTSP_PROTOCOL_STANDARD.md` §Compliance, `PRIMAL_SELF_KNOWLEDGE_STANDARD.md` §3-4

---

## GAP-MATRIX-12: FAMILY_ID Socket Scoping + BIOMEOS_INSECURE Guard

### Problem

barraCuda always created `barracuda.sock` regardless of `FAMILY_ID`. The only env var
checked was `BIOMEOS_FAMILY_ID` (non-standard). No `BIOMEOS_INSECURE` guard existed —
setting both `FAMILY_ID` and `BIOMEOS_INSECURE=1` was silently accepted.

### Resolution

**`resolve_family_id()`** — New public function in `transport.rs`. Reads env vars in
standard precedence order:
1. `BARRACUDA_FAMILY_ID` (primal-specific override)
2. `FAMILY_ID` (composition-wide)
3. `BIOMEOS_FAMILY_ID` (legacy compat)

Returns `None` when unset, empty, or `"default"`.

**`resolve_socket_dir()`** — New public function. Reads `BIOMEOS_SOCKET_DIR` → falls
back to `$XDG_RUNTIME_DIR/biomeos` → `$TMPDIR/biomeos`.

**`validate_insecure_guard()`** — New public function. Returns `Err` when `FAMILY_ID`
is set (non-default) AND `BIOMEOS_INSECURE=1`. Per BTSP §Compliance: cannot claim a
family and skip authentication.

**`default_socket_path()`** — Refactored to use `resolve_socket_dir()` and
`resolve_family_id()`. Socket is `barracuda.sock` in dev, `barracuda-{fid}.sock` in prod.

**Binary integration** — `validate_insecure_guard()` called at startup in both `server`
and `service` commands. Primal refuses to start with a clear error message citing the
BTSP standard.

### Files Changed (barracuda-core)

| File | Change |
|------|--------|
| `crates/barracuda-core/src/ipc/transport.rs` | `resolve_family_id()`, `resolve_socket_dir()`, `validate_insecure_guard()`, refactored `default_socket_path()` |
| `crates/barracuda-core/src/ipc/mod.rs` | Updated module docs for BTSP socket naming |
| `crates/barracuda-core/src/bin/barracuda.rs` | Insecure guard in `run_server()` + `run_service_mode()`, CLI help update, `discovery_dir()` uses `resolve_socket_dir()` |
| `crates/barracuda-core/tests/btsp_socket_compliance.rs` | **New** — 20 integration tests covering family ID resolution, socket dir, insecure guard, socket path scoping |

---

## GAP-MATRIX-06: plasmidBin Metadata Freshness

### Problem

`plasmidBin/barracuda/metadata.toml` was stale: v0.1.0 (March 31), domain "compute",
minimal capability list, old build ref.

### Resolution

Updated to:
- Version: 0.3.11
- Domain: "math" (per `PRIMAL_SELF_KNOWLEDGE_STANDARD.md` §2)
- Provenance: Sprint 34, April 8, 2026
- Wire Standard: L2
- Capabilities: expanded with FHE, noise, activation, health, readiness, identity

Binary build + `harvest.sh` GitHub Release deferred to CI pipeline (requires musl
cross-compilation toolchain).

---

## Quality Gates

| Gate | Result |
|------|--------|
| `cargo fmt --all --check` | ✅ |
| `cargo clippy --workspace --all-targets --all-features -- -D warnings` | ✅ |
| `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` | ✅ |
| `cargo nextest run --workspace --profile ci` | ✅ 4,207 pass, 0 fail, 14 skipped |

---

## BTSP Compliance Checklist (Phase 1)

```
BTSP_PROTOCOL_STANDARD v1.0 — Audit Checklist

Primal: barraCuda  Version: 0.3.11  Date: April 8, 2026

Socket Naming:
  [x] Reads FAMILY_ID (and BARRACUDA_FAMILY_ID) from environment
  [x] Creates barracuda-{family_id}.sock when FAMILY_ID is set
  [x] Creates barracuda.sock when FAMILY_ID is not set (development)
  [x] Refuses to start when both FAMILY_ID and BIOMEOS_INSECURE are set

Handshake (Phase 2+):
  [ ] BTSP handshake runs on every incoming connection when FAMILY_ID is set
  [ ] Challenge-response verifies family membership via HKDF-SHA256
  [ ] Connection refused on handshake failure
  [ ] Ephemeral X25519 keys generated per connection

Cipher Negotiation (Phase 2+):
  [ ] Supports BTSP_CHACHA20_POLY1305
  [ ] Supports BTSP_HMAC_PLAIN
  [ ] Supports BTSP_NULL
  [ ] Enforces minimum cipher per BondingPolicy
```

Phase 1 (Socket Naming Alignment) is complete. Phases 2-3 depend on BearDog
implementing `btsp.session.create` / `btsp.session.verify` / `btsp.negotiate`.

---

## Future Work

- **BTSP Phase 2**: Handshake integration when BearDog ships `btsp.session.*` methods
- **BTSP Phase 3**: Cipher negotiation + encrypted JSON-RPC frames
- **Domain-based socket naming**: Evolve from `barracuda.sock` to `math.sock` per
  `PRIMAL_SELF_KNOWLEDGE_STANDARD.md` §3 (requires ecosystem-wide socket discovery migration)
- **Erasure coding**: L3 covalent mesh backup pattern (from primalSpring audit)
- **Wire Standard L3**: Full compliance when ecosystem composition patterns stabilize
- **ecoBin binary harvest**: `harvest.sh` with musl-static build for plasmidBin GitHub Release

---

**License:** AGPL-3.0-or-later
