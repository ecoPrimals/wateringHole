# ecoPrimals Ecosystem Blurb — Wave 157a VERTEBRATE EVOLUTION

**Date**: Aug 9, 2026 9:20AM | **Wave**: 157a | **From**: eastGate overwatch
**Posture**: **CEPHALIZATION → VERTEBRATE EVOLUTION. 3 P0s OPEN. skunkBat SELF-AUDIT COMPLETE.** skunkBat: programmatic RPC surface verification (3 self-audit tests), capability_registry.toml synced (metadata domain, gossip consumed, protocol field), 675 tests. No phantom APIs — every method has a real handler, unknown methods return `METHOD_NOT_FOUND`. westGate 7-session retrospective exposed critical gaps: bearDog depot binary is health-only stub (P0-A), nestGate `content.ingest` doesn't exist (P0-B), biomeOS FD leak (P0-C). Mesh code-complete but production-blocked.

---

## PHASE SHIFT — VERTEBRATE EVOLUTION

G64 cephalization gave the ecosystem a nervous system (Neural API, biomeOS routing, Tower mesh). Now primals develop **internal skeletal structure** — shared abstractions across crates, domain delegation, self-audit.

**The westGate signal**: 7 sessions of real data work (989K files braided, 153 datasets, 3.3 TB) revealed that **primal API surfaces diverge silently from what consumers expect**. `content.ingest` was never shipped. bearDog returns health responses for every method. Parameter names don't match. Six Python jelly strings exist because primal APIs don't do what they claim.

**The vertebrate fix**: each primal team self-audits — verify actual RPC surface matches capability_registry.toml, abstract repeated patterns behind shared traits, delegate cross-focus to its right home.

---

## P0 ISSUES — 3 OPEN

### P0-A: bearDog Sign Surface Missing
- **What**: Depot binary v0.9.0 returns health response for ALL methods including `crypto.sign_ed25519`
- **Impact**: All spine commits unsigned. loamSpine `session.commit` fails.
- **Evidence**: `nonexistent_xyz → {"primal":"beardog","status":"alive","version":"0.9.0"}`
- **Fix**: bearDog team rebuilds depot binary with actual Ed25519 signing + socket naming fix (`beardog-default.sock` → `beardog-{family_id}.sock`)

### P0-B: nestGate API Surface Mismatch
- **What**: `content.ingest` (directory walk + CAS) does not exist in nestGate v0.5.0. `content.stat` also missing.
- **Impact**: Pipeline assumed Rust walks directories — actually must do it in Python (3× I/O, 33% payload inflation from base64)
- **Fix**: nestGate team ships native `content.ingest(directory)` + `content.stat(hash)`. Document actual RPC params.
- **Workaround**: westGate pipeline adapted — Python walks + per-file `content.put`

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
| **nestGate** | 8.5 MB | **P0-B**: Ship `content.ingest` + `content.stat`. Document actual API surface. |
| **biomeOS** | 20.4 MB | **P0-C**: Fix FD leak in discovery loop. Build provenance graph templates. |
| **songBird** | 23.8 MB | Abstract 9 transport crates behind shared `Transport` trait. Excise `mesh.capabilities_announce` → swarmVine. |
| **petalTongue** | 33.8 MB | Move `doom-core` → **ludoSpring**. Converge 656 deps. |
| **toadStool** | 12.4 MB | S371 `core` 272K → natural WASM split. 24/48 done. |
| **All** | — | Self-audit: verify actual RPC surface matches capability_registry.toml. |

---

## REMAINING

### P0 (immediate — blocks production use of Neural API)
- **bearDog**: Rebuild depot binary with Ed25519 signing + fix socket naming
- **nestGate**: Ship `content.ingest(directory)` + `content.stat(hash)` + document actual params
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

*Wave 157a VERTEBRATE EVOLUTION. Cephalization complete — primals now develop internal structure. 3 P0s: bearDog sign stub (spine commits unsigned), nestGate phantom API (content.ingest doesn't exist), biomeOS FD leak (capability.call unusable). Mesh code-complete, production-blocked. westGate 989K files braided, 7-session retrospective filed. Primals self-audit: verify RPC surface, abstract early patterns, delegate cross-focus. songBird 9 transports → shared trait. doom-core → ludoSpring. 16 primals. N-series 90/91.*
