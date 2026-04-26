# primalSpring Phase 45 — Deployment Validation + Upstream Absorption Handoff

**Date**: April 20, 2026  
**From**: primalSpring v0.9.17  
**For**: All primal teams, spring teams, and downstream consumers  
**License**: AGPL-3.0-or-later

---

## Summary

Phase 45 validated the full deployment pipeline end-to-end: local NUCLEUS on x86_64,
benchScale Docker simulation, remote fetch from GitHub, and aarch64 Pixel payload
staging. All upstream primal evolutions were absorbed, closing multiple cross-architecture
gaps identified in Phase 44. The `start_primal.sh` launcher was audited and fixed for
every primal's actual CLI interface.

---

## 1. What Changed

### Upstream Evolution Absorbed

| Primal | Change | Impact |
|--------|--------|--------|
| **toadStool** | armv7 `usize` overflow fixed — `cfg(target_pointer_width)` gating: 8GB on 64-bit, 2GB on 32-bit | armv7 binary now builds and runs correctly |
| **biomeOS** | armv7/aarch64 rebuilt via `biomeos-unibin` workspace binary target (not root package) | Binary produced on all cross-targets |
| **nestgate** | `armv7-unknown-linux-musleabihf` Rust target installed, cross-arch builds restored | armv7 binary ships |
| **coralReef** | iter84: CLI changed `--port` → `--rpc-bind` for TCP bind | `start_primal.sh` updated |
| **beardog** | HSM session 43: BTSP production mode requires `BEARDOG_FAMILY_SEED` env var | `start_primal.sh` auto-sets from `--family-id` |
| **squirrel** | Upstream evolution pulled — deep debt, feature hygiene, cross-arch uname fix | Clean build on all targets |
| **songbird** | Upstream evolution pulled — deep debt, lint hardcode mock elimination | Clean build; security provider config documented |
| **petalTongue** | Upstream evolution pulled — doc refresh, cross-arch, reqwest elimination | Clean build on all targets |

### `start_primal.sh` CLI Audit Fixes

```
beardog:    auto-export BEARDOG_FAMILY_SEED from --family-id when not set
coralreef:  --port → --rpc-bind (iter84 CLI change)
songbird:   SONGBIRD_SECURITY_PROVIDER=beardog env var needed for production
nestgate:   NESTGATE_JWT_SECRET required (random Base64 generated at deploy time)
```

### genomeBin v5.1 Final State

- 46 binaries across 6 target triples (was 42 in Phase 44)
- Tier 1 (must-ship): **39/39** complete
- `checksums.toml` BLAKE3 hashes verified end-to-end
- `manifest.toml` v5.1.0

---

## 2. Deployment Validation Results

### Local NUCLEUS (x86_64-unknown-linux-musl)

| Primal | Status | Notes |
|--------|--------|-------|
| primalspring | alive | Coordination hub |
| beardog | alive | Required BEARDOG_FAMILY_SEED fix |
| songbird | alive | |
| biomeos | alive | Orchestrator |
| squirrel | alive | AI bridge |
| toadstool | alive | GPU/compute dispatch |
| coralreef | alive | Required --rpc-bind fix |
| nestgate | alive | Storage/auth gateway |
| barracuda | alive | Math/GPU compute |
| rhizocrypt | alive | Provenance DAG |
| loamspine | alive | Certificate authority |
| sweetgrass | alive | Provenance braids |

**Result**: 12/12 primals alive on single x86_64 node.

### benchScale Docker Lab (x86_64-unknown-linux-musl)

| Step | Result |
|------|--------|
| Binary deploy into container | 12/12 copied (symlink-resolved via `readlink -f`) |
| BLAKE3 checksum verification | 12/12 match `checksums.toml` |
| Primal startup (topological order) | 12/12 alive |
| Songbird security provider | Configured: `SONGBIRD_SECURITY_PROVIDER=beardog` |
| NestGate JWT | Auto-generated random Base64 secret |

### Remote Fetch Simulation

Cloned `plasmidBin` from GitHub, verified all x86_64 binaries:
- 13/13 binaries present in `primals/x86_64-unknown-linux-musl/`
- 13/13 BLAKE3 checksums match `checksums.toml`
- Found and fixed 1 typo in `checksums.toml` (nestgate: `a7a` → `a7c`)

### Pixel Payload (aarch64-unknown-linux-musl)

- 13 binaries staged in `primals/aarch64-unknown-linux-musl/`
- All validated: ELF 64-bit LSB executable, ARM aarch64, statically linked, stripped
- `deploy_pixel.sh` updated to resolve from genomeBin layout

---

## 3. Composition Patterns for NUCLEUS

### Topological Startup Order

NUCLEUS primals must start in dependency order. `start_primal.sh` handles this,
but teams building custom launchers need to respect the topology:

```
Wave 1: beardog (security — no deps)
Wave 2: songbird (federation — needs beardog for security provider)
         nestgate (storage — standalone, but needs JWT secret)
         rhizocrypt (provenance DAG — standalone)
         loamspine (certificates — standalone)
         sweetgrass (braids — standalone)
Wave 3: biomeos (orchestrator — discovers all primals)
         toadstool (compute — uses beardog crypto)
         coralreef (GPU/shader — standalone compute)
         barracuda (math — standalone compute)
Wave 4: squirrel (AI bridge — needs biomeos for discovery)
         primalspring (coordination — validates everything)
```

### Per-Primal CLI Map (from `start_primal.sh` audit)

| Primal | Socket Arg | TCP Arg | Extra Env |
|--------|-----------|---------|-----------|
| primalspring | `--socket` | `--port` | — |
| beardog | `--socket` | `--port` | `BEARDOG_FAMILY_SEED` (required in production) |
| songbird | `--socket` | `--port` | `SONGBIRD_SECURITY_PROVIDER=beardog` |
| biomeos | `--socket` | `--port` | — |
| squirrel | `--socket` | `--port` | — |
| toadstool | `--socket` | `--port` | — |
| coralreef | `--tarpc-bind unix://` | `--rpc-bind` | — |
| nestgate | `--socket` | `--port` | `NESTGATE_JWT_SECRET` (required) |
| barracuda | `--socket` | `--port` | — |
| rhizocrypt | `--socket` | `--port` | — |
| loamspine | `--socket` | `--port` | — |
| sweetgrass | `--socket` | `--port` | — |
| petaltongue | `--socket` | `--port` | `PETALTONGUE_HEADLESS=true` for servers |

### Socket Discovery

All primals register at `$XDG_RUNTIME_DIR/biomeos/{primal}[-{family-id}].sock`.
biomeOS discovers via filesystem scan + `ipc.discover` JSON-RPC method.

### TCP Fallback

When UDS is unavailable (cross-platform, containers without shared `/run`), primals
bind TCP on well-known ports from `tolerances::tcp_fallback_table()`:

| Primal | Default TCP Port |
|--------|-----------------|
| primalspring | 9100 |
| beardog | 9101 |
| songbird | 9102 |
| biomeos | 9103 |
| squirrel | 9104 |
| toadstool | 9105 |
| coralreef | 9106 |
| nestgate | 9107 |
| barracuda | 9108 |
| rhizocrypt | 9109 |
| loamspine | 9110 |
| sweetgrass | 9111 |
| petaltongue | 9112 |

---

## 4. neuralAPI Deployment via biomeOS

### `biomeos deploy --graph`

biomeOS is the primary deployment substrate. Deploy NUCLEUS via:

```bash
biomeos deploy --graph nucleus_complete.toml --family-id my-family
```

This reads the TOML graph, resolves fragments (`resolve = true`), topologically sorts
nodes via `topological_waves()`, and starts primals in wave order. Each node specifies
`by_capability` for capability-based discovery.

### Fragment-First Composition

Deploy graphs are composed from fragments:

```
graphs/fragments/tower.toml          → beardog + songbird + biomeos
graphs/fragments/provenance_trio.toml → rhizocrypt + loamspine + sweetgrass
graphs/fragments/compute.toml        → toadstool + coralreef + barracuda
graphs/nucleus_complete.toml          → resolves all fragments
```

### `capability.call` Routing

Neural API routes requests by capability domain:

```
crypto.*     → beardog
genetic.*    → beardog (identity management)
security.*   → beardog
beacon.*     → beardog (discovery beacons)
inference.*  → toadstool (compute) or squirrel (AI bridge)
storage.*    → nestgate
provenance.* → rhizocrypt
```

### TCP-Only for Non-UDS Platforms

On Windows, Android (Termux), and containers without shared `/run`, use:

```bash
biomeos deploy --graph nucleus_complete.toml --tcp-only
```

This forces all primals to TCP fallback ports instead of UDS.

---

## 5. Lessons for Primal Teams

### CLI Standardization Gaps

Every primal evolved its CLI independently. The audit found:
- **coralReef** uses `--rpc-bind` instead of `--port` for TCP (iter84 change broke deploy scripts)
- **coralReef** uses `--tarpc-bind unix://` instead of `--socket` for UDS
- All others use `--socket` / `--port` consistently

**Recommendation**: Adopt a shared CLI trait or argument convention across all primals.
At minimum, `--socket <path>` and `--port <number>` should work uniformly.

### BTSP FAMILY_SEED Requirement

beardog's BTSP production mode silently fails without `FAMILY_SEED` or `BEARDOG_FAMILY_SEED`
env var. This is not discoverable from `--help` alone. All deploy scripts and
documentation must mention this requirement prominently.

### coralReef iter84 CLI Change

The `--port` → `--rpc-bind` rename in coralReef iter84 broke `start_primal.sh`.
**Lesson**: CLI flag renames are breaking changes. If a primal renames a flag, it should:
1. Keep the old name as a deprecated alias for at least one release
2. Document the change in the handoff
3. Update `start_primal.sh` in plasmidBin

### songbird Security Provider

songbird requires `SONGBIRD_SECURITY_PROVIDER=beardog` to connect to beardog for
security operations. Without this, it fails with "No security provider configured".
This env var should be set automatically by biomeOS when deploying Tower compositions.

### NestGate JWT Secret

nestgate refuses to start with "insecure JWT configuration". A strong random secret
must be provided via `NESTGATE_JWT_SECRET`. In production, this should be generated
once per family and stored securely.

---

## 6. Absorption Checklist for Downstream Springs

### Immediate Actions

- [ ] Update `primalSpring` dependency to v0.9.17 in your `Cargo.toml`
- [ ] If using `build_ecosystem_musl.sh`, switch to `build_ecosystem_genomeBin.sh`
- [ ] If using `--port` for coralReef in deploy scripts, change to `--rpc-bind`
- [ ] If starting beardog, ensure `BEARDOG_FAMILY_SEED` is set
- [ ] If starting songbird in Tower, set `SONGBIRD_SECURITY_PROVIDER=beardog`
- [ ] Verify your deploy graphs still resolve after fragment-first changes

### Cross-Architecture Testing

- [ ] Test your spring's binary on at least Tier 1 targets (x86_64-musl, aarch64-musl, armv7-musl)
- [ ] If you have `usize` arithmetic with large constants, add `cfg(target_pointer_width)` gating
- [ ] Run `cargo check --target armv7-unknown-linux-musleabihf` to catch 32-bit issues

### Documentation

- [ ] Update your spring's version pins for primalSpring to v0.9.17
- [ ] Reference genomeBin v5.1 (not v5.0) in any deployment docs
- [ ] Update test counts if you reference primalSpring's metrics

---

*This handoff documents the state of primalSpring v0.9.17 as of April 20, 2026.
631 tests, 75 experiments, 46 cross-arch binaries, 56 deploy graphs, 0 clippy warnings,
0 unsafe, genomeBin v5.1 (Tier 1 39/39).*
