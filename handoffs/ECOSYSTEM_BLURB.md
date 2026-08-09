# ecoPrimals Ecosystem Blurb — Wave 157a VERTEBRATE EVOLUTION

**Date**: Aug 9, 2026 9:30AM | **Wave**: 157a | **From**: eastGate overwatch
**Posture**: **VERTEBRATE EVOLUTION. 2 P0s OPEN (P0-B RESOLVED).** nestGate P0-B resolved: `content.ingest` confirmed shipped since S136 (stale depot was root cause), `content.stat` now shipped, self-audit complete (zero phantom methods, registry synced). skunkBat self-audit complete (675 tests). bearDog P0-A + biomeOS P0-C remain open. Mesh code-complete but production-blocked by P0-C.

---

## PHASE SHIFT — VERTEBRATE EVOLUTION

G64 cephalization gave the ecosystem a nervous system (Neural API, biomeOS routing, Tower mesh). Now primals develop **internal skeletal structure** — shared abstractions across crates, domain delegation, self-audit.

**The westGate signal**: 7 sessions of real data work (989K files braided, 153 datasets, 3.3 TB) revealed that **primal API surfaces diverge silently from what consumers expect**. nestGate `content.ingest` was shipped but depot binary was stale (P0-B, now resolved). bearDog returns health responses for every method. Parameter names don't match. Six Python jelly strings exist because primal APIs don't do what they claim.

**The vertebrate fix**: each primal team self-audits — verify actual RPC surface matches capability_registry.toml, abstract repeated patterns behind shared traits, delegate cross-focus to its right home.

---

## P0 ISSUES — 3 OPEN

### P0-A: bearDog Sign Surface Missing
- **What**: Depot binary v0.9.0 returns health response for ALL methods including `crypto.sign_ed25519`
- **Impact**: All spine commits unsigned. loamSpine `session.commit` fails.
- **Evidence**: `nonexistent_xyz → {"primal":"beardog","status":"alive","version":"0.9.0"}`
- **Fix**: bearDog team rebuilds depot binary with actual Ed25519 signing + socket naming fix (`beardog-default.sock` → `beardog-{family_id}.sock`)

### P0-B: nestGate API Surface Mismatch — RESOLVED
- **What**: `content.ingest` was reported missing. **Investigation: content.ingest has been shipped since Session 136 (Aug 5)** — 590 LOC, 7 tests, both dispatch paths. Root cause: stale depot binary on westGate predated the implementation.
- **content.stat**: Was genuinely missing. **Now shipped** (`4cafa535`) — CAS metadata without data transfer (size, tier, provenance, timestamps). 4 tests.
- **Self-audit**: Zero phantom methods. `dataset.convergence` added to SUPPORTED_METHODS (announce gap fixed). Registry synced.
- **Action**: Rebuild nestGate depot binary from `main` and redeploy to westGate. Pipeline can then use `content.ingest(directory)` instead of per-file `content.put`.

### P0-C: biomeOS FD Leak
- **What**: Auto-discovery loop opens sockets and never closes them. 14→58,613 FDs after 4 `capability.call` invocations.
- **Impact**: `capability.call` unusable for production workloads. westGate bypasses biomeOS entirely.
- **Evidence**: `capability.resolve` works (7ms). Direct primal UDS works (0.2ms). Only forwarding leaks.
- **Fix**: biomeOS team adds socket cleanup in discovery loop.

---

## CURRENT STATE

| Metric | Value |
|--------|-------|
| Primals | **16** (N-series 90/91) |
| NUCLEUS gates | **6/6 redeployed** |
| G68 | **16/16 prod-clean, 16/16 cross-arch** |
| P0 | **3 OPEN** (bearDog sign, nestGate API, biomeOS FD) |
| Depot | songBird 24 MB FIXED (`af0d8fa8`). bearDog STALE (health-only stub). |
| Mesh | code-complete, production-blocked by P0-C |
| Vine-bat | OPERATIONAL (gossip.spread → metadata.analyze → accept/reject) |
| westGate | 989K files braided, 153 datasets, 3.3 TB, 14/14 services |

---

## VERTEBRATE EVOLUTION — PRIMAL SELF-AUDIT

| Primal | Binary | Evolution Task |
|--------|--------|----------------|
| **bearDog** | 8.3 MB | **P0-A**: Rebuild with actual crypto. Fix socket naming. Self-audit: no silent health fallback. |
| **nestGate** | 8.5 MB | **P0-B RESOLVED**: `content.ingest` was shipped S136. `content.stat` now shipped. Self-audit complete. Depot rebuild needed. |
| **biomeOS** | 20.4 MB | **P0-C**: Fix FD leak in discovery loop. Build provenance graph templates. |
| **songBird** | 23.8 MB | Abstract 9 transport crates behind shared `Transport` trait. Excise `mesh.capabilities_announce` → swarmVine. |
| **petalTongue** | 33.8 MB | Move `doom-core` → **ludoSpring**. Converge 656 deps. |
| **toadStool** | 12.4 MB | S371 `core` 272K → natural WASM split. 24/48 done. |
| **All** | — | Self-audit: verify actual RPC surface matches capability_registry.toml. |

---

## REMAINING

### P0 (immediate — blocks production use of Neural API)
- **bearDog**: Rebuild depot binary with Ed25519 signing + fix socket naming
- **nestGate**: ~~Ship content.ingest + content.stat~~ **DONE** (`4cafa535`). Depot rebuild + westGate redeploy remaining.
- **biomeOS**: Fix FD leak in auto-discovery loop (close sockets after health probes)

### Vertebrate evolution (primal teams — self-directed)
- **songBird**: Transport trait convergence (9 crates → shared `Transport`). Delegate gossip to swarmVine.
- **petalTongue**: doom-core → ludoSpring. Dep convergence.
- **toadStool**: Continue S371 WASM split.
- **bearDog**: Self-audit all methods — error on unknown, don't return health.
- **nestGate**: Self-audit API surface vs capability_registry.toml.
- **All primals**: Verify RPC surface matches registry. westGate proved they diverge.

### Fleet + operations
- **Fleet-wide gate redeploy** — golgi depot ready (19/19 + BLAKE3SUMS). Gates pull on harvest.
- **P1: FD exhaustion on remaining gates** — `LimitNOFILE=65536` applied on sporeGate + ironGate + eastGate + westGate. Remaining: strandGate, blueGate, southGate.
- **southGate mesh enrollment** — not discoverable on LAN, deferred

### Data + science
- **westGate**: Pipeline adapted. Spine commits deferred until bearDog sign surface ships.
- **swarmVine integration**: nestGate/loamSpine → data gossip (`cas.have`). toadStool/coralReef → compute gossip.
- **arXiv**: `validate.sh` + reviewer send. 41/42.
- **cellMembrane**: `native_braid.py` → Rust (last Python in active pipeline)

---

*Wave 157a VERTEBRATE EVOLUTION. 2 P0s remain (P0-B RESOLVED). bearDog sign stub (P0-A, spine commits unsigned), biomeOS FD leak (P0-C, capability.call unusable). nestGate P0-B resolved: content.ingest shipped since S136 (stale depot was root cause), content.stat now shipped, self-audit complete — zero phantom methods. skunkBat + nestGate self-audits complete. Mesh code-complete, production-blocked by P0-C. westGate 989K files braided. 16 primals. N-series 90/91.*
