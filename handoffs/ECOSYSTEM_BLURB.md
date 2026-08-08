# ecoPrimals Ecosystem Blurb — Wave 157a TRUST SURFACE + K-DERM ENFORCED

**Date**: Aug 8, 2026 9:05AM | **Wave**: 157a | **From**: eastGate overwatch
**Posture**: **DEPLOYED. 13/13 ALIVE. K-DERM ENFORCED. TRUST SURFACES LIVE.** GitHub remotes removed from all repos on eastGate — zero remaining. Three new routes live on nestgate.io: `/api/content/stats` (CAS from rhizoCrypt), `/pseudospore/` (5 bundles downloadable), `/api/pseudospore/bundles`. Cascade timer auto-pushes depot to golgi. toadStool S369 deployed. Depot: Musl 17/17, Windows 15/15.

---

## EXECUTION SUMMARY — sporeGate/eastGate overwatch (this session)

### SSH Key Discipline — K-Derm ENFORCED
- Removed `github` remotes from 7 repos: bearDog, nestGate, songBird, cellMembrane, wateringHole
- Rewired 2 gardens (loamSpine, metalForge) from GitHub origin → Forgejo origin
- **Zero repos with github remotes remaining on eastGate**
- All routes now go through pepti layer: gate → Forgejo → golgi-ext → GitHub

### Trust Surfaces — 3 Routes LIVE on nestgate.io

| Route | Status | What it does |
|-------|--------|-------------|
| `/api/content/stats` | **LIVE** | Queries rhizoCrypt CAS via UDS — live object counts, sizes, namespaces |
| `/pseudospore/` | **LIVE** | Serves 5 pseudoSpore bundles as downloadable files |
| `/api/pseudospore/bundles` | **LIVE** | Lists bundles with provenance metadata |
| `/pseudospore/validate.sh` | **200 OK** | Downloadable verification script |

petalTongue commits: `037535e` (content stats) + `01961ce` (pseudospore routes)

### Cascade Pipeline — Auto-Push to Golgi
- `ExecStartPost` added to cascade timer: rsync depot → golgi after each harvest
- Pipeline: `Forgejo → fetch → drift detect → harvest → stage → golgi push`
- Only manual step remaining: NUCLEUS deploy (stop → copy → restart)

### Depot — Revalidated (3 cascade cycles this session)
- toadStool S366→S369 absorbed (ioctl fix, libc elimination, hw-safe cross-arch, 15/15 targets)
- cellMembrane `c56d911` (cascade reliability), biomeOS `f49cc75b`, sourDough `edfa26e`
- All rebuilt musl + Windows, pushed to golgi, deployed to NUCLEUS
- toadStool socket fix permanent (ExecStartPost)

---

## CURRENT STATE

| Metric | Value |
|--------|-------|
| sporeGate NUCLEUS | **13/13 ALIVE** |
| G68 | **16/16 prod-clean, 16/16 cross-arch** |
| Golgi depot | Musl **17/17**, Windows **15/15** |
| Cascade | synced=15, zero drift, auto-push to golgi |
| GitHub remotes | **zero** on eastGate |
| Trust surfaces | 3 new routes live on nestgate.io |
| Primal drift | **zero** |

---

## WHAT BLURB SAID vs ACTUAL

| Blurb claim | Actual |
|-------------|--------|
| `/api/content/stats` missing | **FIXED** — live from rhizoCrypt |
| `/pseudospore/` route 404 | **FIXED** — 5 bundles serving, validate.sh at 200 |
| "GitHub remotes removed from all 23" | Was 7 remaining, now **zero** |
| toadStool S366 deployed | S369 deployed (team shipped S367-S369 on top) |

---

## REMAINING (from blurb, updated)

### sporeGate/eastGate owns
- ~~nestgate.io data braids backend~~ **DONE** (`/api/content/stats`)
- ~~`/pseudospore/` route~~ **DONE** (5 bundles + validate.sh)
- ~~Cascade golgi push~~ **DONE** (ExecStartPost rsync)
- ~~SSH key cleanup~~ **DONE** (zero github remotes)

### Other teams own
- **sporePrint**: SU(2)→SU(N) relabel, QCD download pages, LaTeX preprint
- **lithoSpore**: Package QCD bundle for pseudoSpore v1.0.0-rung1
- **primalSpring**: Neural API evolution (capability.call, N2-N5)
- **toadStool**: hw-safe long-tail (7→0 test-only remaining)
- **cellMembrane**: `native_braid.py` → Rust
- **westGate**: nestGate TCP + content registration (NG-05)
- **Gate teams**: Redeploy from golgi depot

### arXiv blockers (trust surface, not physics)
1. ~~pseudoSpore URL~~ `/pseudospore/` now **serves** but QCD bundle not yet packaged
2. `validate.sh` downloadable — but bundle-specific validation not wired
3. sporePrint QCD page needs relabel (sporePrint team)
4. Freeze/sign v1.0.0-rung1 (bearDog Ed25519)
5. Reviewer send (Murillo, Chuna, Bazavov)

---

*Wave 157a — TRUST SURFACE + K-DERM ENFORCED. 13/13 ALIVE. Zero github remotes on eastGate. Three new routes live on nestgate.io: /api/content/stats (CAS from rhizoCrypt), /pseudospore/ (5 bundles), /api/pseudospore/bundles. Cascade auto-pushes depot to golgi. Depot: Musl 17/17, Windows 15/15. All sporeGate topology tasks from blurb DONE. Remaining: sporePrint relabel, lithoSpore QCD bundle, primalSpring Neural API, gate redeploys.*
