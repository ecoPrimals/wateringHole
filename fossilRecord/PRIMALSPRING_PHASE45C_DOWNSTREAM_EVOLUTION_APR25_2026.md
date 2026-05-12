# primalSpring Phase 45c — Downstream Evolution Handoff

**From**: primalSpring v0.9.17 (Phase 45c)
**Date**: April 25, 2026
**For**: All spring teams + garden teams + primal teams

---

## What Happened

primalSpring's `primalspring_guidestone` passes **187/187 checks** against a live
12-primal NUCLEUS deployed from plasmidBin ecoBin binaries. All 13 capabilities are
BTSP-authenticated. All 8 cellular deployment graphs enforce BTSP per-node. biomeOS
v3.25 has absorbed all three identified architectural gaps (graph bootstrapping, BTSP
runtime escalation, tensor translations). The base composition is certified.

**Your turn.**

---

## Key Numbers

| Metric | Value |
|--------|-------|
| guidestone checks | **187/187 ALL PASS** |
| BTSP authenticated | **13/13 capabilities** |
| Cellular graphs | **8 cells, all BTSP-enforced** |
| Primals alive | **12/12** (UDS) |
| Cross-arch binaries | **46** (6 targets, Tier 1 39/39) |
| biomeOS version | **v3.25** (graph bootstrap + BTSP escalation) |
| Experiments | **75** (17 tracks) |
| Tests | **631** (585 passed + 46 ignored) |

---

## What This Means For You

### Spring teams

The full NUCLEUS stack is deployable from pre-built binaries. You no longer need
to build primals from source. Your cell graph in `primalSpring/graphs/cells/` is
ready to deploy.

**Your next step — the primal proof:**

```
Python baseline (L1) → Rust proof (L2) → guideStone bare (L3) → NUCLEUS validated (L4) → primal proof (L5)
YOU ARE HERE ──────────────────────────────────────────────────────────────→ GO HERE
```

1. **Pull primalSpring** and `infra/wateringHole` before starting
2. **Deploy NUCLEUS** from plasmidBin:
```bash
export FAMILY_ID="myspring-validation"
export FAMILY_SEED="$(head -c 32 /dev/urandom | xxd -p)"
export ECOPRIMALS_PLASMID_BIN="path/to/infra/plasmidBin"
./tools/nucleus_launcher.sh --composition full start
./tools/nucleus_launcher.sh status    # verify 12/12 healthy
```
3. **Run your cell** via `cell_launcher.sh`:
```bash
./tools/cell_launcher.sh yourspring start
```
4. **Write your primal-proof validation harness** (three tiers):
   - **Tier 1: LOCAL_CAPABILITIES** — your existing Rust math, always green in CI
   - **Tier 2: IPC-WIRED** — call primals by capability, `check_skip()` when absent
   - **Tier 3: FULL NUCLEUS** — deploy from plasmidBin, run guidestone externally

### Garden teams (esotericWebb)

Your garden cell graph (`esotericwebb_cell.toml`) includes ludoSpring as the science
layer and petalTongue in live mode. The composition pattern is:

```
NUCLEUS (primals) → ludoSpring (game science) → esotericWebb (narrative/UX) → petalTongue (live GUI)
```

petalTongue's `mode = "live"` enables the interactive desktop experience. Your next
step is wiring scene push through `game.push_scene` → petalTongue IPC.

### Primal teams

All primals are BTSP-converged. Your BTSP posture is validated by guidestone Layer 1.5
with trust model enforcement per tier:

| Tier | Bond Type | Trust Requirement |
|------|-----------|-------------------|
| Tower (BearDog, Songbird) | Covalent | Nuclear-tier genetics |
| Node (ToadStool, barraCuda, coralReef) | Metallic | Mito-beacon genetics |
| Nest (NestGate, Squirrel) | Metallic | Mito-beacon genetics |
| Provenance (rhizoCrypt, loamSpine, sweetGrass) | Metallic | Mito-beacon genetics |

**biomeOS v3.25 absorption**: `register_capabilities_from_graphs()` pre-populates the
route table from graph definitions at startup. `btsp.escalate` RPC enables runtime
transition from cleartext bootstrap to BTSP-enforced. All your capabilities are
routable through the Neural API.

---

## Cell Graph BTSP Requirement

All cell graphs now require `security_model = "btsp"` on every `[[graph.nodes]]` entry.
guidestone Layer 7 validates this. If any node uses `tower_delegated` or omits the
security model, the cell will FAIL validation.

```toml
[[graph.nodes]]
name = "yourprimal"
security_model = "btsp"
binary = "yourprimal"
# ... rest of node config
```

---

## Guidestone Readiness — Where Everyone Stands

| Spring | gS Level | Next Step |
|--------|----------|-----------|
| primalSpring | 4 (**187/187 live, 13/13 BTSP**) | Certifying base for all |
| hotSpring | 5 (certified) | Template for others |
| wetSpring | 3 (bare works) | Deploy NUCLEUS, begin Tier 2 |
| ludoSpring | 3 (bare works, composition evolution partner) | Deploy NUCLEUS, wire game science |
| neuralSpring | 2 (scaffold) | Wire bare property checks |
| healthSpring | 2 (scaffold) | Wire bare property checks |
| airSpring | 0 | Start with guideStone scaffold |
| groundSpring | 0 | Start with guideStone scaffold |

---

## Composition Patterns for NUCLEUS Deployment

### Via biomeOS Neural API (recommended for production)

```bash
# Deploy via graph
echo '{"jsonrpc":"2.0","method":"graph.deploy","params":{"graph":"nucleus_complete"},"id":1}' \
  | socat - UNIX-CONNECT:/run/user/$(id -u)/biomeos/neural-api-${FAMILY_ID}.sock

# Escalate BTSP after Tower healthy
echo '{"jsonrpc":"2.0","method":"btsp.escalate","params":{},"id":2}' \
  | socat - UNIX-CONNECT:/run/user/$(id -u)/biomeos/neural-api-${FAMILY_ID}.sock

# Check BTSP status
echo '{"jsonrpc":"2.0","method":"btsp.status","params":{},"id":3}' \
  | socat - UNIX-CONNECT:/run/user/$(id -u)/biomeos/neural-api-${FAMILY_ID}.sock
```

### Via nucleus_launcher.sh (development)

The launcher handles dependency ordering, socket creation, symlinks, and post-Tower
BTSP verification. It probes all primals after launch and reports BTSP readiness
before guidestone runs.

### Via cell_launcher.sh (spring deployment)

Wraps `nucleus_launcher.sh` + domain overlay + petalTongue live mode. Each spring's
cell graph defines the full composition. Cell graphs are at `graphs/cells/*.toml`.

---

## What's New Since Last Handoff

| Change | Impact |
|--------|--------|
| guidestone 171→187 checks | +16 checks from Layer 7 cellular deployment validation |
| Per-node `security_model = "btsp"` | All 8 cell graphs, all 93 nodes tagged |
| biomeOS v3.25 absorbed | Graph bootstrap + BTSP runtime escalation resolved |
| `BtspEnforcer` trust model in guidestone | Per-tier bond type and genetics requirements validated |
| `btsp.escalate` / `btsp.status` RPC | biomeOS supports runtime BTSP escalation |
| `register_capabilities_from_graphs()` | biomeOS populates route table from graph definitions at startup |

---

## Key References

| Resource | Path |
|----------|------|
| Depot workflow | `primalSpring/wateringHole/PLASMINBIN_DEPOT_PATTERN.md` |
| guideStone standard | `primalSpring/wateringHole/GUIDESTONE_COMPOSITION_STANDARD.md` (v1.1.0) |
| Composition guidance | `primalSpring/wateringHole/PRIMALSPRING_COMPOSITION_GUIDANCE.md` |
| Cell graphs | `primalSpring/graphs/cells/*.toml` |
| BTSP relay pattern | `wateringHole/SOURDOUGH_BTSP_RELAY_PATTERN.md` |
| BTSP convergence | `wateringHole/handoffs/BTSP_WIRE_CONVERGENCE_APR24_2026.md` |
| Upstream guidance | `wateringHole/handoffs/PRIMALSPRING_PHASE45C_BTSP_CONVERGED_UPSTREAM_GUIDANCE_APR2026.md` |
| Gap registry | `primalSpring/docs/PRIMAL_GAPS.md` |
| Ecosystem alignment | `wateringHole/NUCLEUS_SPRING_ALIGNMENT.md` |
| Primal registry | `wateringHole/PRIMAL_REGISTRY.md` |

---

**License**: AGPL-3.0-or-later
