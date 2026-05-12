# projectNUCLEUS Post-Interstadial Findings + Spring UniBin plasmidBin Readiness

**Date**: 2026-05-10
**From**: projectNUCLEUS (downstream deployer / gate operator)
**For**: plasmidBin maintainers, primalSpring coordination, spring teams, wateringHole
**Phase**: 60+ POST-INTERSTADIAL — zero open upstream gaps

---

## Purpose

This handoff captures findings from the projectNUCLEUS post-interstadial audit
and recommends that spring UniBin binaries be added to plasmidBin for tracked
deployment. The primordial extinction (8/8 springs → single UniBin) makes this
tractable for the first time.

---

## 1. Upstream Gap Closure Confirmed

projectNUCLEUS has verified that all 11 upstream gaps identified during the
deep debt sweep are resolved:

| ID | What | Verified |
|----|------|----------|
| JH-11 | Cross-primal token federation | bearDog `auth.public_key` + biomeOS `BearDogVerifier` |
| GAP-03 | `composition.deploy` route | biomeOS v3.51 route alias |
| GAP-06 | rhizoCrypt UDS transport | Operational since S23, integration test added |
| GAP-09 | `method.register` endpoint | biomeOS v3.51 |
| GAP-12 | ludoSpring IPC methods | 18 `game.*` registered (403 canonical) |
| U1-U3 | CHECKSUMS, deploy graphs, profiles | All resolved or false positives |
| DF-2/3, U5 | toadStool env, songbird TCP, sweetGrass port | All resolved May 8 |

Sovereignty horizons shipped upstream:
- **H2-10/11**: bearDog Wave 100 — rustls X.509 TLS + per-IP rate limiting
- **H2-13/15/16**: songbird Wave 196-197 — full NAT traversal chain (STUN/TURN/DDNS/fallback)
- **petalTongue PT-1→PT-5**: Web sovereignty (docroot, workers, NestGate backend)
- **biomeOS v3.51**: `composition.status`, token forwarding, `method.register`
- **skunkBat Phase 2**: All 7 event kinds instrumented

**JH-5 (audit forwarding) and Tier 4 rewiring are now unblocked.**

---

## 2. Spring UniBin → plasmidBin: Now Tractable

### The problem before

Before primordial extinction, each spring produced multiple binaries:
- Separate `validate_*`, `certify_*`, `scenario_*` executables
- Standalone `guidestone` binaries
- Spring-specific `*_primal` IPC server binaries
- Test harness binaries

This made plasmidBin tracking intractable — the binary surface per spring was
unbounded and changed with each refactor. plasmidBin correctly tracked only the
stable primal binaries and spring `*_primal` IPC servers.

### What changed

All 8 springs completed primordial extinction (May 9, 2026). Each now produces
a single **UniBin** — one binary with subcommands:

```
<spring> certify     — run certification layers
<spring> validate    — execute validation scenarios
<spring> serve       — start JSON-RPC server (IPC primal)
<spring> status      — report health/version/capabilities
<spring> version     — print version and build metadata
```

The UniBin **subsumes** the separate `*_primal` binary — `<spring> serve` is
the IPC server that was previously a standalone binary.

### Current spring UniBin inventory

| Spring | Binary name | Tests | gS Level | UniBin | musl-static ready |
|--------|-------------|------:|:--------:|:------:|:-----------------:|
| primalSpring | `primalspring` | 680 | L8 | Yes | Yes (already in plasmidBin) |
| hotSpring | `hotspring` | 1,002 | L5 | Yes | Likely (check barraCuda GPU features) |
| healthSpring | `healthspring` | 999+ | L5 | Yes | Likely |
| ludoSpring | `ludospring` | 665+ | L4 | Yes | Likely |
| wetSpring | `wetspring` | 1,209 | L4 | Yes | Likely |
| groundSpring | `groundspring` | 965+ | L4 | Yes | Likely |
| neuralSpring | `neuralspring` | 1,432 | L3 | Yes | Likely |
| airSpring | `airspring` | 1,364 | L2 | Yes | Check `aws-lc-sys` |

### Recommendation for plasmidBin

**Add spring UniBin binaries to `manifest.toml` under a new `[spring_binaries]`
section**, mirroring the existing `[binaries]` structure for primal ecoBins.

This gives:
1. **Tracked checksums** — BLAKE3 integrity for spring binaries via `checksums.toml`
2. **Cross-arch deployment** — same musl-static CI pipeline as primals
3. **Single binary per spring** — no more intractable multi-binary surface
4. **`fetch.sh` support** — deployers can `./fetch.sh hotspring` to get the binary
5. **Version pinning** — `manifest.toml` tracks latest version per spring

The `*_primal` binary entries in `manifest.toml` can be deprecated once
`<spring> serve` is confirmed equivalent. The UniBin is the successor.

**Note on `airSpring`**: Workspace-root `deny.toml` is still missing (only
sub-crate deny files exist). `aws-lc-sys` should be added to the explicit ban
list for pure Rust alignment before plasmidBin inclusion.

---

## 3. projectNUCLEUS Local Debt Resolved

### Static observer surface

Voila replaced with pre-rendered HTML via pappusCast + `observer_server.py` on
port 8866. Centralized dark theme (`observer_theme.css`). Source stripping,
navigation injection, Voila link rewriting all automated.

### darkforest v0.2.1

New `observer.rs` module — 9 check groups (OBS-01→OBS-09):

| Check | What it validates |
|-------|-------------------|
| OBS-01 | HTML files exist |
| OBS-02 | Dark theme CSS injected |
| OBS-03 | Navigation bar with Home link |
| OBS-04 | No legacy `/voila/render/` links |
| OBS-05 | No Python tracebacks in output |
| OBS-06 | Source code stripped (`--no-input`) |
| OBS-07 | Root index serves HTTP 200 |
| OBS-08 | Security headers (X-Robots-Tag, X-Frame-Options, etc.) |
| OBS-09 | Internal directories blocked |

Observer tier test migrated from Python to Rust — runs in 11s vs 3.5min.
`tier_test_all.sh` now invokes `darkforest --suite observer`.

### Hardcoded ports eliminated

`security_validation.sh` had 5 hardcoded primal ports (9100, 9140, 9400, 9500,
9601, 9850). All replaced with `$BEARDOG_PORT`, `$SKUNKBAT_PORT`, etc. from
`nucleus_config.sh`.

### Workload TOML debt cleared

3 stale `TODO` comments in workload validation TOMLs (healthSpring, airSpring,
hotSpring) removed. Paths updated from pre-UniBin `validate_*` binaries to
UniBin `<spring> validate` subcommands using `$SPRINGS_ROOT`.

**Zero TODO/FIXME/HACK across all `.rs`, `.py`, `.sh`, `.toml` files in projectNUCLEUS.**

---

## 4. Absorption Targets for projectNUCLEUS (Next Wave)

These are now unblocked and documented in `specs/EVOLUTION_GAPS.md`:

| Target | Source | Effort |
|--------|--------|--------|
| `composition.deploy(graph)` | biomeOS v3.51, primalSpring `graphs/fragments/*.toml` | Medium |
| `composition.status` | biomeOS v3.51 → monitoring/dashboard | Low |
| `method.register` | biomeOS v3.51 → dynamic spring registration | Low |
| Tier 4 rewiring | JH-11 resolved → IPC-first, `CompositionContext` | High |
| skunkBat audit forwarding | Phase 2 complete → Phase 3 cross-primal IPC | Medium |
| BearDog TLS shadow run | H2-10/11 shipped → local `btsp_tls_parity.sh` | Ops |
| Songbird NAT integration | H2-13-16 shipped → VPS relay provisioning | Medium |

---

## 5. plasmidBin Stale Docs

Minor finding: `CONTEXT.md` references older naming (`metadata.toml` vs
`checksums.toml`, SHA-256 vs BLAKE3, primal counts) that diverges from current
`README.md` and `manifest.toml`. Recommend reconciling during next docs pass.

The `manifest.toml` spring sections (lines 237-340) still list pre-UniBin
versions and test counts. These should be updated to reflect post-extinction
UniBin reality (e.g., primalSpring latest = "0.9.25" not "0.9.17", tests = 680
not 666).

---

## 6. Key File References

| What | Path |
|------|------|
| NUCLEUS evolution tracker | `sporeGarden/projectNUCLEUS/specs/EVOLUTION_GAPS.md` |
| darkforest observer suite | `sporeGarden/projectNUCLEUS/validation/darkforest/src/observer.rs` |
| Observer theme | `sporeGarden/projectNUCLEUS/deploy/observer_theme.css` |
| pappusCast static export | `sporeGarden/projectNUCLEUS/deploy/pappusCast.py` (export command) |
| primalSpring gap tracker | `springs/primalSpring/docs/PRIMAL_GAPS.md` |
| Cross-spring scorecard | `springs/primalSpring/docs/CROSS_SPRING_PARITY_SCORECARD.md` |
| plasmidBin manifest | `infra/plasmidBin/manifest.toml` |
| Upstream handoff | `infra/wateringHole/handoffs/PRIMALSPRING_POST_INTERSTADIAL_DOWNSTREAM_HANDOFF_MAY10_2026.md` |

---

*This handoff documents projectNUCLEUS findings from the post-interstadial
review. The primary recommendation is to add spring UniBin binaries to
plasmidBin — the primordial extinction made this tractable for the first time.
All upstream gaps are confirmed resolved. Zero local debt remains.*
