# primalSpring Phase 45c — Downstream Spring Evolution Handoff

**From**: primalSpring v0.9.17 (Phase 45c)
**For**: All spring teams (ludoSpring, hotSpring, wetSpring, neuralSpring, healthSpring, airSpring, groundSpring)
**Date**: April 2026

---

## What Changed Since Phase 45

primalSpring's guidestone now expects **BTSP authentication on every capability**,
not just Tower and Provenance tiers. **13/13 capabilities are BTSP-authenticated** —
full NUCLEUS convergence achieved. The base composition is fully encrypted.

### Key Numbers

| Metric | Phase 45 | Phase 45c (converged) |
|--------|----------|-----------|
| guidestone checks | 162/166 | **171/171 ALL PASS** |
| BTSP authenticated | 5/13 | **13/13** |
| BTSP policy | tower_delegated OK | **cleartext = FAIL** |
| Remaining upstream | 5 primals | **0** — all converged |

### What This Means for You

1. **FAMILY_SEED is now critical**: Every NUCLEUS deployment must set both
   `FAMILY_ID` and `BEARDOG_FAMILY_SEED` (or `FAMILY_SEED`). Without it,
   BTSP handshakes fail.

2. **Your guidestone inherits BTSP checks**: If you use `primalspring::composition`
   and `CompositionContext`, your discovery and health checks go through
   BTSP-authenticated channels. No code changes needed on your side.

3. **Cleartext connections are degraded**: If a primal responds on cleartext,
   guidestone reports it as FAIL (not SKIP or PASS). Your test harnesses
   should expect this if running against primals that haven't pulled BTSP fixes.

---

## Deploy a Live NUCLEUS (Updated)

```bash
export FAMILY_ID="myspring-validation"
export BEARDOG_FAMILY_SEED="$(head -c 32 /dev/urandom | xxd -p)"
export ECOPRIMALS_PLASMID_BIN="path/to/infra/plasmidBin"

./nucleus_launcher.sh --composition full start
./nucleus_launcher.sh status    # verify 12/12 healthy
```

All 14 binaries in plasmidBin are musl-static, stripped, x86_64, zero C dependencies.

---

## YOUR NEXT STEP — THE PRIMAL PROOF

```
Python baseline (L1) → Rust proof (L2) → guideStone bare (L3) → NUCLEUS validated (L4) → primal proof (L5)
                                                                   YOU ARE HERE ─────────→ GO HERE
```

### Step 1 — Read your manifest entry

Your capabilities are defined in `primalSpring/graphs/downstream/downstream_manifest.toml`.
Find your `[[downstream]]` entry. Your `validation_capabilities` list is exactly which
IPC methods your science needs to call.

### Step 2 — Write your primal-proof validation harness

Follow the three-tier pattern:

**Tier 1: LOCAL_CAPABILITIES** — Your existing Rust math. Always green in CI. No IPC needed.

**Tier 2: IPC-WIRED** — Call primals by capability. Use `check_skip()` when primals are absent.

**Tier 3: FULL NUCLEUS** — Deploy from plasmidBin, run your guideStone externally. This is the primal proof.

```rust
use primalspring::composition::{CompositionContext, validate_liveness};
use primalspring::ipc::capability::discover_by_capability;
use primalspring::validation::{check_bool, check_skip, check_relative};

let socket = discover_by_capability("tensor", family_id)?;
let result = ctx.call("tensor", "tensor.matmul", &params)?;
check_relative(&mut v, "parity:tensor:matmul", result, expected, 1e-12, "scipy baseline");
```

### Step 3 — Document gaps and hand back

Any primal that misbehaves, returns unexpected formats, or is missing a capability
you need — document it and hand back to primalSpring via `docs/PRIMAL_GAPS.md`.

---

## Composition Patterns for NUCLEUS Deployment via Neural API

### biomeOS as Substrate

biomeOS is the execution engine. Your spring is NOT a binary to ship — it is a
**composition graph** that biomeOS consumes. The graph defines which primals your
science needs, and biomeOS spawns them in topological order.

```toml
[graph]
name = "myspring_validation"
composition_model = "validation"

[[graph.nodes]]
name = "biomeos_neural_api"
by_capability = "neural_api"
required = true
spawn = false
order = 0

[[graph.nodes]]
name = "beardog"
by_capability = "security"
required = true
order = 1

[[graph.nodes]]
name = "songbird"
by_capability = "discovery"
required = true
order = 2

[[graph.nodes]]
name = "myspring_science"
by_capability = "your_domain"
order = 3
depends_on = ["beardog", "songbird"]
```

### Gardens Consume Compositions

Springs validate science. Gardens (esotericWebb, blueFish) are the usable products.
A garden is a composition that has been proved by its spring's guidestone.

```
hotSpring (physics validation) → garden produces MILC results for physicists
ludoSpring (game science validation) → esotericWebb (interactive game product)
neuralSpring (ML validation) → inference pipeline product
```

The spring guidestone certifies the composition. The garden inherits that certification.

---

## petalTongue UI Status

petalTongue is the visualization primal for desktop UI. Current state:

- **BTSP**: Not yet supported (upstream debt — Tier 1 plaintext works)
- **Modes**: TUI, egui, web, headless
- **IPC**: `visualization.*`, `interaction.*` methods via JSON-RPC 2.0
- **Desktop live target**: petalTongue + ToadStool (Node atomic) for interactive display

**For ludoSpring/esotericWebb**: petalTongue interaction via the Node atomic (ToadStool
dispatches to display) is the path to live user experience. User interaction metrics
feed back into game science validation.

---

## GUIDESTONE READINESS — WHERE EVERYONE STANDS

| Spring | gS Level | Next Step |
|--------|----------|-----------|
| primalSpring | 4 (**171/171 live, 13/13 BTSP**) | Certifying base for all |
| hotSpring | 5 (certified) | Template for others |
| wetSpring | 3 (bare works) | Deploy NUCLEUS, begin Tier 2 |
| ludoSpring | 3 (bare works) | Deploy NUCLEUS, begin Tier 2, petalTongue UI |
| neuralSpring | 2 (scaffold) | Wire bare property checks |
| healthSpring | 2 (scaffold) | Wire bare property checks |
| airSpring | 0 | Start with guideStone scaffold |
| groundSpring | 0 | Start with guideStone scaffold |

---

## Known Issues

| Issue | Workaround |
|-------|------------|
| BearDog requires BEARDOG_FAMILY_SEED env | Export before launch (see Step 2) |
| petalTongue has no BTSP | Use Tier 1 plaintext for visualization |
| ~~loamSpine incomplete handshake~~ | **RESOLVED** — `HandshakeComplete` now includes `"status":"ok"` discriminator. Connection lifecycle fixed: persistent `ProviderConn`, no `shutdown()`, 10s read timeout (April 24). |
| 5 seed fingerprint mismatches | Expected — reharvest to plasmidBin resolves |

---

## Key References

- Depot workflow: `primalSpring/wateringHole/PLASMINBIN_DEPOT_PATTERN.md`
- guideStone standard: `primalSpring/wateringHole/GUIDESTONE_COMPOSITION_STANDARD.md`
- Composition guidance: `primalSpring/wateringHole/PRIMALSPRING_COMPOSITION_GUIDANCE.md`
- Your manifest: `primalSpring/graphs/downstream/downstream_manifest.toml`
- Gap registry: `primalSpring/docs/PRIMAL_GAPS.md`
- Ecosystem alignment: `infra/wateringHole/NUCLEUS_SPRING_ALIGNMENT.md`
- Upstream primal handoff: `infra/wateringHole/handoffs/PRIMALSPRING_PHASE45C_BTSP_DEFAULT_UPSTREAM_HANDOFF_APR2026.md`
