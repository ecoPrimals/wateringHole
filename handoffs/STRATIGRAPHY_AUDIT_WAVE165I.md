# Process Stratigraphy — Full Audit Pass

**Wave 165i — October 7, 2026 19:22 ET**
**Purpose**: Map jelly (Python prototypes), Rust primals, shell glue, and data state. Identify what fossilizes, what evolves into Rust, what cleans up.

---

## golgiBody Stack — What's Running

### Rust Primals (already evolved)

| Binary | Version | Size | Port | PID | Role |
|--------|---------|------|------|-----|------|
| `caddy` | 2.11.4 | 46M | :443/:80 | 2854378 | TLS surface, 29 domains, 1172-line config |
| `skunky-ingest` | 0.2.18 | 5.3M | :9753 | 2976038 | Fleet detection, scatter server, Caddy bridge |
| `skunkbat` | 0.2.18 | 3.4M | :9750 | 2834181 | Fleet thymus — behavioral classification |
| `swarmvine` | — | 2.5M | :7800 | 2942875 | Epidemic gossip mesh |
| `squirrel` | 0.1.0 | 8.6M | socket | 3514834 | AI coordination |
| `beardog` | — | — | socket | 2547656 | BTSP crypto, secrets |
| `membrane` | 0.1.0 | 18M | — | — | Membrane binary (not currently primary process) |
| `petaltongue` | — | — | :8090 | 4002770 | sporePrint web + peptidoglycan |
| `forgejo` | — | — | :3000/:2222 | 2968416 | Sovereign git forge |
| `step-ca` | — | — | :9443 | 2606896 | SSH certificate authority |

**Total Rust: 10 running services, ~94MB binaries**

### Python Jelly (evolution candidates)

| Script | Lines | Size | Status | Rust Target |
|--------|-------|------|--------|-------------|
| `bloom_live.py` | 745 | 32K | **RUNNING** — core classifier | **skunky-ingest** — absorb epitope hash + L2 collision |
| `entity_topology.py` | 534 | 24K | Imported by bloom_live | **skunky-ingest** — topology module |
| `epitope_bridge.py` | 83 | 4K | Cron every 5 min | **skunky-ingest** — native epitope→Caddy bridge |
| `investigation_export.py` | 180 | 8K | Manual run | **skunky-ingest** — investigation subcommand |

**Total Python: 1,542 lines, 68K — all candidates for skunky-ingest absorption**

### Shell Glue (fossilize or absorb)

| Script | Cron | Purpose | Target |
|--------|------|---------|--------|
| `refresh-signal-data.sh` | */15 | Generate signal-data.js from logs | **skunky-ingest** — native JS output |
| `braid-billboard.sh` | */5 | Hash-check billboard, append to braid | **sweetGrass** — native braid daemon |
| `epitope_bridge.sh` | — | Original bridge (superseded by .py) | **FOSSILIZE** |
| `cascade-sense.sh` | — | Cascade trigger detector | **nestGate** — webhook handler |
| `sovereign-ci-trigger.sh` | — | CI trigger | **nestGate** |

### Data State

| File | Size | Update | Purpose |
|------|------|--------|---------|
| `dashboard.json` | 23K | 10s | Full fleet observatory data |
| `feed.txt` | 22K | 10s | Live terminal text feed |
| `state.json` | 208B | 10s | Compact state for signal page |
| `epitope_caddy.json` | 1.1K | 10s | Epitope→IP map for bridge |
| `billboard.txt` | 32B | Manual | Current billboard text |
| `topology.json` | 33K | Periodic | Entity topology graph |
| `investigation.json` | 2K | Manual | Active investigation data |
| `billboard/braid.jsonl` | — | 5m | Human braid entries (7) |
| `artisan/braid.jsonl` | — | Manual | Artisan braid entries (4) |

---

## Disk Sprawl — Cleanup Targets

### skunky-ingest backup sprawl: **17 copies, ~48MB**
```
skunky-ingest.bak               5.3M
skunky-ingest.bak-20261006      2.4M
skunky-ingest.bak-20261006-2025 2.5M
skunky-ingest.bak-20261007-1021 2.6M
skunky-ingest.bak-pre-crossmirror   2.5M
skunky-ingest.bak-pre-crossmirror2  2.5M
skunky-ingest.bak-pre-plasmid       2.6M
skunky-ingest.bak-pre-prism         2.5M
skunky-ingest.bak.1791404109        5.2M
skunky-ingest.bak2              2.4M
skunky-ingest-musl              2.6M
skunky-ingest-musl-new          2.6M
skunky-ingest-new               2.6M
skunky-ingest.old               2.6M
skunky-ingest.pre-bloom         2.3M
skunky-ingest.prev              2.3M
```

**Action**: Keep `.bak` (latest) and `.pre-bloom` (last pre-bloom version). Fossilize rest to fossilRecord. Delete from /opt/membrane.

### swarmvine backups: 3 copies, ~7.6M
**Action**: Keep `.bak`. Fossilize rest.

### bloom_live backups: 2 copies
```
bloom_live_v2.py.bak  15K
bloom_live_v3.py.bak  22K
```
**Action**: Move to fossils/ (the evolution history has value).

---

## Evolution Roadmap — Jelly to Rust

### Priority 1: bloom_live.py → skunky-ingest

bloom_live.py is the core classifier — 745 lines of Python doing what skunky-ingest should do natively:
- Tail Caddy access log ✓ (skunky already does this)
- Classify visitors (L2 collision) → absorb into skunky's fleet detection
- Compute epitope hashes (L1) → new skunky module
- Track behavioral state per IP → skunky already has IP tracking
- Write dashboard/state/feed → skunky already writes state
- Emit EPITOPE events → skunky already has event system

**Convergence**: skunky-ingest already tails the same log, already detects fleet IPs, already writes to the Caddyfile. bloom_live duplicates much of this in Python. The epitope hash, L2 collision classes, and dashboard output should be native skunky features.

**Migration path**: 
1. Add `--epitope` flag to skunky-ingest
2. Implement BLAKE2b epitope hash in Rust
3. Native Caddy bridge writes epitope-keyed matchers
4. Python bloom_live becomes unnecessary
5. Fossilize bloom_live.py to fossils/

### Priority 2: epitope_bridge.py → skunky-ingest

83 lines that reads epitope_caddy.json and rewrites the Caddyfile. This is exactly what skunky-ingest's `--caddy-bridge` already does — just with different grouping logic. Absorb the epitope grouping into skunky's bridge.

### Priority 3: entity_topology.py → skunky-ingest

534 lines generating entity topology. skunky already has entity detection. Absorb the topology graph generation.

### Priority 4: refresh-signal-data.sh + gen-signal-data.py

Shell + Python pipeline generating signal-data.js for the signal page. This could be a skunky-ingest subcommand or a petalTongue feature.

### Priority 5: braid-billboard.sh → sweetGrass

The braid hash-check-and-append is exactly what sweetGrass does. When sweetGrass is deployed on golgiBody, this shell script fossilizes.

---

## Remaining Work — Clean, Tighten, Converge

### Clean
- [ ] Delete 15 skunky-ingest backup copies (keep 2)
- [ ] Delete swarmvine backup copies (keep 1)
- [ ] Move bloom_live v2/v3 backups to fossils/
- [ ] Fossilize `epitope_bridge.sh` (superseded by .py)
- [ ] Remove `/opt/membrane/fossils/entity_topology.pre-epitope.py` (already archived)

### Tighten
- [ ] The Caddyfile is 1172 lines — skunky-ingest's bridge writes ~350 of those dynamically. The static portion should be version-controlled in plasmidBin and deployed via deploy_membrane.sh
- [ ] signal page (96K HTML) — consider splitting JS/CSS into separate files for cacheability
- [ ] bloom_live writes to 6 files every 10s — could consolidate to 2 (state + dashboard)
- [ ] 3 cron jobs — could be 1 supervisor script or a skunky-ingest periodic task

### Converge
- [ ] skunky-ingest absorbs bloom_live epitope classification (Priority 1)
- [ ] skunky-ingest absorbs epitope bridge (Priority 2)
- [ ] skunky-ingest absorbs entity topology (Priority 3)
- [ ] sweetGrass absorbs braid-billboard (Priority 5)
- [ ] thesis.primals.eco index.html → version control (currently hand-edited on VPS)
- [ ] signal.primals.eco index.html → version control (currently hand-edited on VPS)

---

## Architecture Summary

```
                    golgiBody (8W, $6/mo)
                    
  RUST (evolved)              PYTHON (jelly)           SHELL (glue)
  ═══════════════            ═══════════════          ═══════════════
  caddy          TLS          bloom_live     classify  refresh-signal
  skunky-ingest  detect+scat  entity_topo    topology  braid-billboard
  skunkbat       thymus       epitope_bridge bridge    
  swarmvine      gossip       investigation  export    
  squirrel       AI coord                              
  beardog        BTSP                                  
  petaltongue    web serve                             
  forgejo        git forge                             
  step-ca        SSH CA                                
                                                       
  10 services                4 scripts                2 cron scripts
  94 MB                      1,542 lines              
                             68 KB                     
```

The jelly is all classifier + bridge logic. It ALL converges into skunky-ingest. When that happens:
- Python goes to zero on golgiBody
- Shell glue drops to 1 script (signal refresh, or absorbed too)
- The stack is pure Rust + Caddy + Forgejo

---

*Process stratigraphy complete. The jelly tells us where the Rust needs to grow. The fossils tell us what we've already shed. The convergence path is clear: skunky-ingest absorbs the classifier, and the membrane becomes pure compiled immune response.*

*Wave 165i — October 7, 2026*
