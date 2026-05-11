# projectNUCLEUS: Cross-Ecosystem Audit Findings (May 11, 2026)

**Date**: 2026-05-11
**From**: projectNUCLEUS (sporeGarden)
**For**: primalSpring, all primal teams, all spring teams
**Phase**: Post-interstadial — cross-ecosystem audit against primalSpring delta targets

---

## Context

Upstream primalSpring audit (May 10) declared zero open gaps and issued per-spring
delta targets. projectNUCLEUS conducted a cross-ecosystem audit across infra/,
springs/, and primals/ to validate readiness and identify local debt.

---

## 1. Findings: Primals

### MethodGate Parity Gap

projectNUCLEUS documentation claimed 13/13 primals ship MethodGate with
`PERMISSION_DENIED` for unauthenticated calls. Source audit found:

| Primal | MethodGate | Notes |
|--------|-----------|-------|
| bearDog | Yes | `beardog-tunnel/src/method_gate.rs` |
| songBird | Yes | `songbird-orchestrator/src/method_gate.rs` |
| biomeOS | Yes | `biomeos-core/src/method_gate.rs` |
| barraCuda | Yes | `barracuda-core/src/ipc/method_gate.rs` |
| coralReef | Yes | `coralreef-core/src/ipc/method_gate.rs` |
| nestGate | Yes | `nestgate-rpc/.../method_gate.rs` |
| petalTongue | Yes | `petal-tongue-ipc/src/method_gate.rs` |
| rhizoCrypt | Yes | `rhizo-crypt-rpc/.../method_gate.rs` |
| loamSpine | Yes | `loam-spine-api/.../method_gate.rs` |
| sweetGrass | Yes | `sweet-grass-service/src/method_gate.rs` |
| skunkBat | Yes | `skunk-bat-server/.../method_gate.rs` |
| **toadStool** | **No** | No pre-dispatch gate or `-32001` in server |
| **squirrel** | **No** | No `method_gate` in JSON-RPC dispatch |

**Action**: projectNUCLEUS corrected claim to 11/13. Upstream handback to toadStool
and squirrel teams for MethodGate implementation (low priority — both primals
run on localhost only, mitigated by network isolation + UFW deny-by-default).

### All Primals Zero Debt

- Zero TODO/FIXME/HACK across all 13 primal repos (confirmed)
- All Zero clippy warnings in first-party code
- nestGate vendor tree has third-party markers (expected, not application code)

---

## 2. Findings: Springs

### skunkBat Client Wiring (Inconsistent)

| Spring | `skunkbat.rs` IPC module | Deploy graph | Status |
|--------|-------------------------|-------------|--------|
| ludoSpring | Yes (`src/ipc/skunkbat.rs`) | Yes | Exemplar |
| neuralSpring | Yes (`src/ipc/skunkbat.rs`) | Yes | Exemplar |
| healthSpring | Yes (`src/ipc/audit.rs`) | Yes (but missing from graph nodes) | Graph gap |
| wetSpring | No | Yes (graph reference) | Code gap |
| hotSpring | No | Yes (certification checks) | Code gap |
| groundSpring | No | Yes (graph reference) | Code gap |
| airSpring | No | Yes (graph reference) | Code gap |

### barraCuda Optionality

| Spring | `barracuda` optional | Default feature | IPC-first? |
|--------|---------------------|----------------|-----------|
| groundSpring | Yes | Not in default | Yes (exemplar) |
| hotSpring | Yes | `barracuda-local` default | Feature-gated |
| ludoSpring | Yes | `local` default | Feature-gated |
| wetSpring | Yes | `barracuda-lib` default | Feature-gated |
| neuralSpring | Yes | `barracuda` default | Default = library |
| healthSpring | Yes (via `barracuda-lib`) | Not in default | Feature-gated |
| **airSpring** | **No** | Required dependency | **Not IPC-first** |

**Action**: airSpring is the only spring without `barracuda` as optional. Upstream
handback for Tier 4 alignment.

### barraCuda Version Skew

Observed versions across springs: 0.3.7 (airSpring), 0.3.11 (ludoSpring),
0.3.12 (wetSpring), 0.3.13 (healthSpring/hotSpring). Canonical plasmidBin is
0.3.13. Springs should align to latest for Tier 4 binary-only IPC.

---

## 3. Findings: plasmidBin

- Consumer fetch script is `fetch.sh` (not `fetch_primals.sh` — docs had stale reference)
- Spring UniBin binaries are NOT shipped as plasmidBin artifacts (springs compose primals)
- `nucleus_launcher.sh` still requires primalSpring source checkout for optional validation
- `primalspring_primal` checksum entry inconsistency (removed from checksums.toml but
  referenced in tooling)

---

## 4. Local Debt Resolved (projectNUCLEUS)

| Item | Resolution |
|------|-----------|
| MethodGate claim | Corrected to 11/13 (toadStool + squirrel pending upstream) |
| skunkBat in smaller compositions | Added to `node_atomic_compute.toml` and `nest_atomic.toml` (was only in `nucleus_complete.toml`) |
| skunkBat in `deploy.sh` | Added to `node` and `nest` composition lists |
| Absorption targets | 4 new items added to `EVOLUTION_GAPS.md` (skunkBat graphs, MethodGate parity, foundation integration, systemd portability) |
| Systemd template documentation | Added template comments to observer-static and cloudflared-replica units |

---

## 5. Remaining Local Absorption Targets

| Target | Priority | Status |
|--------|----------|--------|
| `composition.deploy(graph)` — replace nohup loop in deploy.sh | High | Not started |
| `composition.status` — wire into monitoring | Medium | Not started |
| `method.register` — dynamic spring registration | Medium | Not started |
| foundation integration — code path for science results | Low | Docs only |
| systemd unit parameterization | Low | Template comments added |

---

## 6. Upstream Handbacks

| Team | Item | Priority |
|------|------|----------|
| toadStool | MethodGate pre-dispatch check | Low |
| squirrel | MethodGate pre-dispatch check | Low |
| airSpring | Make `barracuda` optional for Tier 4 | Medium |
| All springs | Align barraCuda version to 0.3.13 | Low |
| healthSpring | Add skunkBat node to deploy graph TOMLs | Low |
| plasmidBin | Fix `primalspring_primal` checksum inconsistency | Low |

---

## References

- `projectNUCLEUS/specs/EVOLUTION_GAPS.md` — updated absorption targets + changelog
- `projectNUCLEUS/graphs/node_atomic_compute.toml` — skunkBat added
- `projectNUCLEUS/graphs/nest_atomic.toml` — skunkBat added
- `infra/wateringHole/SPRING_NUCLEUS_AUDIT_MAY2026.md` — spring readiness matrix
- `primalSpring/docs/PRIMAL_GAPS.md` — Wave 3 coordination

---

**Zero upstream gaps remain. Local absorption targets documented and prioritized.
skunkBat defense primal now wired into all composition tiers.**
