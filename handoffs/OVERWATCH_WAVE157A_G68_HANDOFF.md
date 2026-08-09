# Overwatch Audit Handoff — Wave 157a VERTEBRATE EVOLUTION

**Date**: Aug 9, 2026 9:15AM | **Wave**: 157a | **From**: eastGate overwatch
**Purpose**: westGate retrospective exposed 3 P0s. Mesh code-complete, production-blocked. Primals self-audit.

---

## Ecosystem Posture

| Metric | Value |
|--------|-------|
| **P0** | **3 OPEN** (bearDog sign stub, nestGate API mismatch, biomeOS FD leak) |
| **G68** | **COMPLETE — 16/16 prod-clean** |
| **NUCLEUS gates** | **6/6 redeployed** to G68-converged binaries |
| **Mesh** | **Code-complete, PRODUCTION-BLOCKED** (P0-C FD leak) |
| **Depot** | songBird 24 MB FIXED. bearDog STALE (health-only stub). |
| **SSH discipline** | **ENFORCED** — zero `github` remotes ecosystem-wide |
| **Primal health** | **13/13 GREEN** |
| **Total tests** | ~135,000+ |
| **Primals** | **16** (N-series 90/91) |
| **westGate** | 989K files braided, 153 datasets, 3.3 TB, 14/14 services |
| **Vine-bat** | **OPERATIONAL** — gossip.spread → metadata.analyze → accept/reject |
| **arXiv** | **41/42** — validate.sh + freeze/sign remain |
| **sporePrint** | 338 pages, current at Wave 157a |

---

## 3 P0 ISSUES

### P0-A: bearDog Sign Surface Missing
Depot binary v0.9.0 returns health response for ALL methods including
`crypto.sign_ed25519`. All spine commits unsigned. loamSpine `session.commit` fails.
**Owner**: bearDog team. **Fix**: Rebuild with actual Ed25519 signing + socket naming fix.

### P0-B: nestGate API Surface Mismatch
`content.ingest` (directory walk + CAS) does not exist in nestGate v0.5.0.
Pipeline must do Python directory walks (3× I/O, 33% payload inflation from base64).
**Owner**: nestGate team. **Fix**: Ship native `content.ingest(directory)` + `content.stat(hash)`.

### P0-C: biomeOS FD Leak
Auto-discovery loop opens sockets, never closes them. 14→58,613 FDs after 4
`capability.call` invocations. `capability.resolve` works (7ms). Only forwarding leaks.
**Owner**: biomeOS team. **Fix**: Socket cleanup in discovery loop.

---

## VERTEBRATE EVOLUTION — PRIMAL SELF-AUDIT

| Primal | Evolution Task |
|--------|----------------|
| **bearDog** | P0-A: Rebuild with actual crypto. Fix socket naming. |
| **nestGate** | P0-B: Ship `content.ingest` + `content.stat`. Document actual API. |
| **biomeOS** | P0-C: Fix FD leak. Build provenance graph templates. |
| **songBird** | 9 transports → shared `Transport` trait. Excise `mesh.capabilities_announce` → swarmVine. |
| **petalTongue** | doom-core → ludoSpring. Converge 656 deps. |
| **toadStool** | S371 WASM split 24/48. `core` 272K natural split. |
| **All** | Self-audit: verify actual RPC surface matches capability_registry.toml. |

---

## GAPS CLOSED (cumulative Wave 157a)

| Gap | Resolution |
|-----|-----------|
| Gate redeploy 6/6 | All running G68-converged from golgi depot |
| NG-05 westGate CAS federation | 26 capabilities, TCP :8080, songbird-register.service |
| strandGate depot access | SSH key on golgi + Forgejo |
| plasmid.fetch --source forgejo | cellMembrane `55fdff3` |
| pseudoSpore routes | LIVE on nestgate.io |
| QCD pseudoSpore bundle | lithoSpore v1.0.0-rung1 PACKAGED |
| SU(2)→SU(N) relabel | hotspring-qcd-sun across 10 files |
| SSH discipline | Zero github remotes ecosystem-wide |
| Cascade auto-push | ExecStartPost rsync to golgi |
| Root doc audit | 4 stale TODOs closed, zero debris |

## REMAINING GAPS

### P0 (immediate — blocks production use of Neural API)
1. **bearDog**: Rebuild depot binary with Ed25519 signing + fix socket naming
2. **nestGate**: Ship `content.ingest(directory)` + `content.stat(hash)` + document actual params
3. **biomeOS**: Fix FD leak in auto-discovery loop (close sockets after health probes)

### arXiv (trust surface — 41/42)
1. `validate.sh` — bundle-specific BLAKE3 + DAG + Ed25519 verification
2. Freeze/sign v1.0.0-rung1 (bearDog Ed25519) — **blocked by P0-A**
3. Reviewer send (Murillo, Chuna, Bazavov)

### Ecosystem evolution (primal teams — self-directed)
- **songBird**: Transport trait convergence (9 crates → shared `Transport`)
- **petalTongue**: doom-core → ludoSpring. Dep convergence.
- **toadStool**: Continue S371 WASM split.
- **cellMembrane**: `native_braid.py` → Rust (last Python in active pipeline)
- **All primals**: Verify RPC surface matches registry.

### Fleet + operations
- **Fleet-wide gate redeploy** — golgi depot ready. Gates pull on harvest.
- **P1: FD exhaustion limits** — `LimitNOFILE=65536` on 4/6 gates. Remaining: strandGate, blueGate, southGate.
- **southGate mesh enrollment** — not discoverable on LAN, deferred

### Windows P3/P4
- skunkBat: `PRIMAL_BIND_MODE` env var
- petalTongue: `--port` in server mode
- songBird: stale PID file

### Ops
- coralReef BLAKE3 checksum stale on golgi depot

---

## What sporePrint Shipped (Wave 157a cumulative)

1. **SU(2)→SU(N) relabel** — 3 pages renamed, 10 files updated
2. **Gate status** — 4 rewrites: 3/6 → 6/6 → NG-05 CLOSED → 3 P0s + vertebrate evolution
3. **hotSpring QCD** — arXiv 41/42, trust surface blockers, pseudoSpore PACKAGED
4. **Homepage** — 5 updates tracking wave progression
5. **Trust surfaces** — nestgate.io routes documented
6. **CHANGELOG** — [3.26.0], [3.26.1], [3.27.0], [3.28.0]
7. **All specs** — llms.txt, EVOLUTION_QUEUE, CONTEXT, CONTENT_MAP current
8. **Root doc audit** — 4 stale TODOs closed, zero debris

---

*Wave 157a VERTEBRATE EVOLUTION. 3 P0s exposed by westGate retrospective.
Mesh code-complete, production-blocked. Primals self-audit RPC surfaces.
bearDog sign → freeze/sign → arXiv is the critical path. 16 primals, N-series 90/91.*
