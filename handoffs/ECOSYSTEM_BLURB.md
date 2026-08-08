# ecoPrimals Ecosystem Blurb — Wave 157a GATE REDEPLOY STATUS

**Date**: Aug 8, 2026 9:10AM | **Wave**: 157a | **From**: eastGate overwatch
**Posture**: **3/6 NUCLEUS GATES REDEPLOYED. strandGate DIVERGED (needs depot access path). K-DERM ENFORCED. TRUST SURFACES LIVE.** sporeGate 13/13 ALIVE. blueGate 13/13 (Windows, 3 P3/P4 issues). southGate 13/13 (96 MB RSS, 2.6x faster). strandGate BLOCKED — can't pull G68 binaries (GitHub stale, Forgejo API parse fails, no SSH to golgi). westGate + ironGate pending.

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

## GATE REDEPLOY STATUS

| Gate | Status | Details |
|------|--------|---------|
| **sporeGate** | **DONE** — 13/13 ALIVE | S369 deployed, cascade auto-push, zero drift |
| **blueGate** | **DONE** — 13/13 ALIVE (Windows) | 15/15 depot pulled, 264 MB RSS, SSH discipline compliant |
| **southGate** | **DONE** — 13/13 ALIVE | 96 MB RSS, 0.058ms Tower latency (2.6x faster), SSH discipline (33 repos cleaned) |
| **strandGate** | **DIVERGED — BLOCKING** | Cannot fetch G68 binaries (see below) |
| **westGate** | **PENDING** | Awaiting redeploy |
| **ironGate** | **PENDING** | Awaiting redeploy |

### strandGate Deploy Divergence (BLOCKING)

strandGate is stuck on `v2026.05.30` binaries (2+ months stale). Root cause:
- `plasmid.fetch --source github` → stale release (`v2026.05.30`)
- `plasmid.fetch --source forgejo` → API parse failure
- No SSH shell access to golgi depot directory

**Science is unblocked** — SU(3) campaign COMPLETE (36 configs), SU(4) running, NPU hardware live. Only primal binary deployment is blocked.

**Resolution — Option C (rsync depot pull via SSH)**:
Give strandGate SSH access to golgi depot directory. Aligns with K-Derm model (no GitHub dependency for deploy):
```
rsync golgi:/srv/depot/musl/ ~/.local/share/ecoPrimals/plasmidBin/primals/x86_64-unknown-linux-musl/
```
**Owner**: golgi ops / overwatch. SSH key registration on golgi for strandGate.

**Also needed**: Fix `membrane plasmid.fetch --source forgejo` API parse (cellMembrane team) so all remote gates have a sovereign deploy path.

### blueGate Windows Issues (P3/P4)

| ID | Issue | Workaround |
|----|-------|------------|
| P3 | skunkBat ignores `PRIMAL_BIND_MODE=tcp` env | Pass `--bind-mode tcp` on CLI |
| P4 | petalTongue `--port` ignored in server mode | Accept dynamic ports (internal IPC) |
| P3 | songBird stale PID file blocks startup | Clean `C:\var\run\songbird\*` before start |

---

## CURRENT STATE

| Metric | Value |
|--------|-------|
| NUCLEUS gates redeployed | **3/6** (sporeGate, blueGate, southGate) |
| G68 | **16/16 prod-clean, 16/16 cross-arch** |
| Golgi depot | Musl **17/17**, Windows **15/15** |
| Cascade | synced=15, zero drift, auto-push to golgi |
| SSH discipline | **ENFORCED** — eastGate, blueGate, southGate all compliant |
| Trust surfaces | 3 new routes live on nestgate.io |
| Divergences | **1** — strandGate depot access |

---

## REMAINING (from blurb, updated)

### sporeGate/eastGate owns
- ~~nestgate.io data braids backend~~ **DONE** (`/api/content/stats`)
- ~~`/pseudospore/` route~~ **DONE** (5 bundles + validate.sh)
- ~~Cascade golgi push~~ **DONE** (ExecStartPost rsync)
- ~~SSH key cleanup~~ **DONE** (zero github remotes)

### Other teams own
- **sporePrint**: SU(2)→SU(N) relabel, QCD download pages, LaTeX preprint
- ~~**lithoSpore**: Package QCD bundle for pseudoSpore v1.0.0-rung1~~ **DONE** — `e586c9d` (3 modules, 15/15 checks, 6.8 KB tarball)
- **primalSpring**: Neural API evolution (capability.call, N2-N5)
- **toadStool**: hw-safe long-tail cross-arch (S369: 15/15 targets + iOS)
- **cellMembrane**: `native_braid.py` → Rust + fix `plasmid.fetch --source forgejo` API parse
- **westGate**: nestGate TCP + content registration (NG-05) + redeploy from golgi
- **ironGate**: Redeploy from golgi depot
- **strandGate**: Needs SSH depot access to golgi (Option C) — escalated to overwatch
- **skunkBat**: `PRIMAL_BIND_MODE` env var support on Windows (P3, blueGate finding)
- **petalTongue**: `--port` flag in server mode on Windows (P4, blueGate finding)

### arXiv blockers (trust surface, not physics)
1. ~~pseudoSpore URL~~ `/pseudospore/` now **serves** — QCD bundle **PACKAGED** (`hotSpring-QCD-Lattice_v1.0.0-rung1.tar.gz`, 6.8 KB) — needs deploy to nestgate.io
2. `validate.sh` downloadable — but bundle-specific validation not wired
3. sporePrint QCD page needs relabel (sporePrint team)
4. Freeze/sign v1.0.0-rung1 (bearDog Ed25519)
5. Reviewer send (Murillo, Chuna, Bazavov)

---

*Wave 157a — 3/6 NUCLEUS gates redeployed (sporeGate, blueGate, southGate — all 13/13 ALIVE, SSH discipline enforced). strandGate DIVERGED — needs SSH depot access to golgi (no GitHub dependency). westGate + ironGate pending. Trust surfaces live: /api/content/stats, /pseudospore/ (5 bundles), /api/pseudospore/bundles. blueGate found 3 Windows issues (skunkBat env, petalTongue port, songBird PID — all P3/P4). Remaining: strandGate depot path, sporePrint relabel, lithoSpore QCD bundle, primalSpring Neural API, Forgejo plasmid.fetch fix.*
