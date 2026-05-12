<!--
SPDX-License-Identifier: AGPL-3.0-or-later
Documentation: CC-BY-SA-4.0
-->

# ludoSpring V37.1 — plasmidBin Live Validation Gap Matrix

**Date:** 2026-03-31
**Source:** ludoSpring V37.1 live run against plasmidBin primals
**Score:** 95/141 composition checks passing (67.4%)
**Method:** All 15 composition experiments (exp084-098) run against live UDS primals started from `infra/plasmidBin/`

---

## Live Primal Stack Used

| Primal | Source | Socket | Status |
|--------|--------|--------|--------|
| BearDog | plasmidBin | `/run/user/1000/biomeos/beardog.sock` | RUNNING |
| biomeOS Neural API | plasmidBin | `/run/user/1000/biomeos/neural-api.sock` | RUNNING |
| toadStool | plasmidBin | `/run/user/1000/biomeos/toadstool-ludotest.sock` | RUNNING |
| coralReef | plasmidBin | `/run/user/1000/biomeos/coralreef-core-default.sock` | RUNNING |
| barraCuda | **source build** | `/run/user/1000/biomeos/barracuda-core.sock` | RUNNING (not in plasmidBin) |
| NestGate | plasmidBin | `/run/user/1000/biomeos/nestgate.sock` | RUNNING (requires manual JWT) |
| Songbird | plasmidBin | `/run/user/1000/biomeos/songbird.sock` | RUNNING |
| sweetGrass | plasmidBin | `/run/user/1000/biomeos/sweetgrass.sock` | RUNNING |
| rhizoCrypt | plasmidBin | TCP:9401 (dual-mode) + `$XDG_RUNTIME_DIR/biomeos/rhizocrypt.sock` | **UDS FIXED** (s23) |
| loamSpine | plasmidBin | — | **PANIC on startup** |
| Squirrel | plasmidBin | not started | available |
| petalTongue | plasmidBin | not started | available |

---

## Results by Experiment

| Exp | Name | Pass/Total | Status | Primals Exercised |
|-----|------|------------|--------|-------------------|
| 084 | barraCuda Math IPC | 12/15 | FAIL | barraCuda, biomeOS |
| 085 | Shader Dispatch Chain | 7/8 | FAIL | toadStool, coralReef |
| 086 | Tensor Composition | **10/10** | **PASS** | barraCuda |
| 087 | Neural API Pipeline | 3/8 | FAIL | biomeOS |
| 088 | Continuous Game Loop | 2/10 | FAIL | biomeOS |
| 089 | Psychomotor Composition | 4/8 | FAIL | barraCuda |
| 090 | GameFlow Tensor | **13/13** | **PASS** | barraCuda |
| 091 | PCG/Noise | 7/8 | FAIL | barraCuda |
| 092 | Composite Pipeline | **8/8** | **PASS** | barraCuda |
| 093 | Continuous Session | **6/6** | **PASS** | barraCuda, biomeOS |
| 094 | Session Lifecycle | 3/8 | FAIL | BearDog, NestGate, ~~rhizoCrypt~~ |
| 095 | Content Ownership | 0/8 | FAIL | ~~rhizoCrypt~~, ~~loamSpine~~ |
| 096 | NPC Dialogue | 5/10 | FAIL | barraCuda, ~~rhizoCrypt~~ |
| 097 | Population Dynamics | **10/10** | **PASS** | barraCuda |
| 098 | NUCLEUS Game Session | 5/6 | FAIL | barraCuda, BearDog, NestGate, ~~rhizoCrypt~~ |

**5 experiments fully PASS. 10 experiments expose primal evolution gaps.**

---

## Gap Matrix — Per-Primal Evolution Targets

### rhizoCrypt (~~CRITICAL~~ RESOLVED — v0.14.0-dev session 23, March 31, 2026)

**Gap:** TCP-only transport. Binds `0.0.0.0:9401` for JSON-RPC but does not create a Unix domain socket.

**Impact:** exp094, exp095, exp096, exp098 cannot reach rhizoCrypt. All provenance checks fail.

**Fix required:**
- Add `--unix [PATH]` CLI flag, default to `$XDG_RUNTIME_DIR/biomeos/rhizocrypt.sock`
- Follow the pattern established by BearDog, NestGate, sweetGrass, barraCuda
- Update `start_primal.sh` rhizoCrypt case block once UDS is supported

**Experiments that will pass when fixed:** exp094 (+5 checks), exp095 (+2 checks), exp096 (+1 check), exp098 (+1 check) = **+9 checks**

---

### loamSpine (CRITICAL — blocks 1 experiment)

**Gap:** Panic on startup — `"Cannot start a runtime from within a runtime"` at `crates/loam-spine-core/src/service/infant_discovery.rs:233`

**Impact:** exp095 requires all 4 primals (beardog + loamspine + rhizocrypt + sweetgrass). loamSpine panic means the entire experiment enters dry-run mode.

**Fix required:**
- Replace `block_on()` with `spawn` or restructure the infant discovery to avoid nesting async runtimes
- This is a Tokio anti-pattern — the async context already exists when `block_on` is called

**Experiments that will pass when fixed:** exp095 (+6 checks, with rhizoCrypt fix) = **+6 checks**

---

### barraCuda (HIGH — 3 formula gaps)

**Gap 1: Fitts formula mismatch**
- `activation.fitts(distance=256, width=32, a=200, b=150)` returns **800**
- Python baseline expects **708.85** (Shannon formulation: `a + b * log2(2*D/W + 1)`)
- barraCuda likely implements `a + b * log2(D/W)` (Welford variant)
- **Fix:** Add `variant` parameter to select Shannon vs Welford, or default to Shannon

**Gap 2: Hick formula variant**
- `activation.hick(n_choices=8, a=200, b=150)` returns **675.49**
- Python baseline expects **650** (standard: `a + b * log2(n)`)
- barraCuda uses `a + b * log2(n+1)` (includes "no-choice" option)
- **Fix:** Add `include_no_choice` parameter, or default to standard `log2(n)`

**Gap 3: Perlin3D lattice invariant**
- `noise.perlin3d(0, 0, 0)` returns **-0.11** instead of 0
- Gradient noise must be zero at integer lattice points by definition
- **Fix:** Check gradient interpolation at lattice boundaries in 3D implementation

**Gap 4: No binary in plasmidBin**
- barraCuda was started from source build (`target/release/barracuda`)
- Need a published ecoBin in `infra/plasmidBin/barracuda/`

**Experiments affected:** exp089 (-4 checks), exp091 (-1 check) = **+5 checks when fixed**

---

### biomeOS Neural API (HIGH — capability registration)

**Gap:** Running primals do not auto-register capabilities with the Neural API. The only registered capabilities are:
`primal.germination`, `primal.terraria`, `ecosystem.nucleation`, `graph.execution`, `ecosystem.coordination`

Missing domains: `math`, `tensor`, `compute`, `noise`, `stats`, `activation`, `dag`, `visualization`, `crypto`, `security`, `storage`

**Impact:** `capability.call` cannot route to any primal by domain. `graph.execute_pipeline` and `graph.start_continuous` cannot resolve graph node capabilities.

**Fix required:**
- biomeOS bootstrap graph should register capabilities from all detected primals
- OR: primals should self-register their capabilities on startup via `lifecycle.register` + `capability.register`
- The v2.80 bootstrap graph has `register_barracuda` — this works for direct IPC but the Neural API capability registry doesn't see it

**Experiments affected:** exp087 (-5 checks), exp088 (-8 checks), exp084 (-1 check) = **+14 checks when fixed**

---

### toadStool + coralReef (MEDIUM — inter-primal discovery)

**Gap:** `compute.dispatch` returns `"coralReef not available — sovereign dispatch requires coralReef driver"` despite coralReef socket existing at `/run/user/1000/biomeos/coralreef-core-default.sock`.

**Fix required:** toadStool needs to discover coralReef via socket directory scan or Songbird query, not hardcoded URL.

**Experiments affected:** exp085 (-1 check)

---

### plasmidBin start_primal.sh (LOW — JWT generation)

**Gap:** NestGate case block generates `NESTGATE_JWT_SECRET="plasmidbin-${NODE_ID:-gate}-$FAMILY_ID"` = 25 bytes. NestGate requires minimum 32 bytes.

**Fix:** Use `openssl rand -base64 48` or similar in the NestGate case block.

---

## Projected Impact

| Fix | Checks Gained | New Total | New % |
|-----|--------------|-----------|-------|
| Current baseline | — | 95/141 | 67.4% |
| + rhizoCrypt UDS | +9 | 104/141 | 73.8% |
| + loamSpine panic fix | +6 | 110/141 | 78.0% |
| + barraCuda formulas | +5 | 115/141 | 81.6% |
| + biomeOS capability registration | +14 | 129/141 | 91.5% |
| + toadStool↔coralReef discovery | +1 | 130/141 | 92.2% |
| **All fixes** | **+35** | **130/141** | **92.2%** |

The remaining ~11 checks are domain-level math methods (`math.flow.evaluate`, `math.engagement.composite`) which are explicitly composable from existing barraCuda primitives — low-priority convenience methods.

---

## What ludoSpring Validated Successfully

These patterns work TODAY with live plasmidBin primals:

1. **barraCuda tensor math** — create, read, add, scale, clamp, reduce, sigmoid, matmul (exp086: 10/10)
2. **barraCuda stats** — mean, weighted_mean, std_dev (exp092: 8/8)
3. **barraCuda activation** — sigmoid for flow curves (exp090: 13/13)
4. **barraCuda population dynamics** — replicator, Markov, Wright-Fisher via tensor IPC (exp097: 10/10)
5. **60Hz game session** — 10-tick continuous loop under 0.54ms per tick (exp093: 6/6)
6. **BearDog crypto** — blake3_hash (base64), sign_ed25519 (exp094, exp098)
7. **NestGate storage** — store/retrieve round-trip with family_id (exp094, exp098)
8. **sweetGrass attribution** — UDS socket ready, API available (discovered but not fully tested due to rhizoCrypt/loamSpine)

---

## For primalSpring

These validation graphs can be handed off to primalSpring for composition testing:

- `graphs/composition/science_validation.toml` — sequential barraCuda math pipeline
- `graphs/composition/nucleus_game_session.toml` — continuous 60Hz NUCLEUS game tick
- `graphs/composition/session_provenance.toml` — session lifecycle via Nest Atomic + Trio

The experiments are the validation harnesses. primalSpring's graph executor should be able to replicate these results by deploying the graphs and routing through live primals.

---

## Local Debt Resolved in V37.1

These were experiment bugs, NOT primal gaps (fixed before this run):

- BearDog `crypto.blake3_hash` expects base64 data, not raw strings
- BearDog `crypto.sign_ed25519` expects `{"message": ...}`, not `{"data": ...}`
- NestGate `storage.store/retrieve` requires `family_id` parameter
- exp093: removed unused `has_result` function
