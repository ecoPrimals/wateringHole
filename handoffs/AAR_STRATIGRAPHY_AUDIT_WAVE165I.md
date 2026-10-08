# Stratigraphy Audit: golgiBody Process & File Inventory

**Wave 165i — October 7, 2026, 20:27 ET**
**Purpose**: Full geological survey of what's running, what's Python jellystein, what's compiled Rust, what's shell glue, and what's ready to evolve.

---

## Process Taxonomy

### 🦀 Compiled Rust (Production Grade)

| Binary | Service | Size | Since | PID | Purpose |
|--------|---------|------|-------|-----|---------|
| `caddy` | caddy-tls | 46M | May 15 | 2854378 | TLS termination, routing, scatter proxy, honeycomb |
| `skunky-ingest` | skunky-ingest | 5.3M | Oct 7 | 2976038 | Caddy log tailer → skunkBat + scatter server + Caddy bridge |
| `skunkbat` | skunkbat | 3.4M | Oct 6 | 2834181 | Fleet thymus — reconnaissance & automated defense |
| `swarmvine` | swarmvine-membrane | 2.5M | Oct 7 | 2942875 | Epidemic gossip engine — mesh coordination |
| `squirrel` | squirrel-membrane | 8.6M | Aug 10 | 3514834 | AI coordination |
| `membrane` | membrane-webhook | 18M | Oct 7 | 2943146 | Webhook listener (CI-EVO-01) |
| `beardog` | beardog-membrane | — | Jul 27 | 2547656 | BTSP + secrets — genetic token auth |
| `nestgate` | nestgate-sporeprint | 8.5M | Jul 8 | 2017630 | CAS storage |
| `petaltongue` | membrane-petaltongue | 19M | Aug 12 | 4002770 | sporePrint web server |
| `forgejo` | forgejo | — | Oct 7 | 2982005 | Sovereign git forge |
| `step-ca` | step-ca | — | Jul 29 | 2606896 | SSH Certificate Authority |

**Total Rust surface**: 10 binaries, ~130M compiled, all systemd-managed.

### 🐍 Python Jellystein (Evolve to Rust)

| Script | Lines | Running | Purpose | Evolution Target |
|--------|-------|---------|---------|-----------------|
| `bloom_live.py` | **745** | ✅ PID 2978413 | Epitope collision classifier, L2/L1 classification, dashboard output | **skunky-ingest** — should be a module in the Caddy log tailer |
| `entity_topology.py` | **534** | Imported by bloom_live | Entity topology graph generator, subnet/geo analysis | **skunky-ingest** — topology should be computed in the same pipeline |
| `epitope_bridge.py` | **83** | Cron (*/5 min) | Reads epitope map, rewrites Caddy FLEET_PRESSURE matchers | **skunky-ingest** — the bridge should be internal to the Caddy bridge |
| `investigation_export.py` | **180** | Manual | Export investigation data from bloom state | Can stay Python — offline tooling |

**Total Python jellystein**: 1,542 lines across 4 files. **bloom_live + entity_topology + epitope_bridge = 1,362 lines** that should converge into skunky-ingest.

### 🐚 Shell Glue (Minimize)

| Script | Lines | Running | Purpose | Evolution Target |
|--------|-------|---------|---------|-----------------|
| `braid-billboard.sh` | 13 | Cron (*/5 min) | Auto-braid billboard snapshots | Could stay shell or move into a provenance service |
| `refresh-signal-data.sh` | 25 | Cron (*/15 min) | Refresh signal.primals.eco data from bloom outputs | Eliminate when signal page pulls from API directly |
| `ssh-hygiene.sh` | — | Manual | SSH key hygiene | Stay as-is |

**Total shell glue**: 38 lines. Minimal — good.

### 🪨 Fossils (Already Stopped)

Located in `/opt/membrane/fossils/`:
- `bloom_live_v2.py.fossil` — binary classifier (superseded by v4)
- `bloom_live_v3.py.fossil` — behavioral collision (superseded by v4)
- `entity_topology.pre-epitope.py` — pre-epitope version
- `epitope_bridge.sh.fossil` — first attempt (heredoc quoting issues)
- `feed-to-repo.fossil.sh` — old feed pipeline
- `forgejo-watchdog.fossil.sh` — old watchdog
- `membrane-inflammatory.fossil.sh` — old inflammatory response
- `plasmid-federation.fossil.sh` — old federation script
- `tower-shadow-benchmark.fossil.*` — old benchmark
- `skunky-backups/` — **13 old skunky-ingest binaries** (evolution trail)
- `wg0.conf.pre-wave166` — old WireGuard config

**Fossil disk**: ~52M (mostly old skunky-ingest binaries). Can be cleaned.

---

## Data Files

### Live Output (bloom_live writes)

| File | Size | Update | Purpose |
|------|------|--------|---------|
| `dashboard.json` | 24K | 10s | Full dashboard with epitope clusters, offenders, geography |
| `state.json` | 210B | 10s | Compact state: RPS, fleet/human IPs, epitope summary |
| `feed.txt` | 27K | Per-event | Rolling text feed of classified events |
| `epitope_caddy.json` | 1.4K | 10s | Epitope→IP map for Caddy bridge |
| `billboard.txt` | 32B | On update | Current billboard text |
| `topology.json` | 33K | Periodic | Entity topology graph |
| `investigation.json` | 2K | Manual | Investigation state |

### Provenance Chain

| Path | Entries | Purpose |
|------|---------|---------|
| `provenance/billboard/braid.jsonl` | 7 | Human billboard braid — content-hashed entries |
| `provenance/billboard/*.txt` | 5 | Billboard snapshots |
| `provenance/artisan/braid.jsonl` | 4 | Artisan reflection braid |
| `provenance/artisan/*.txt` | 4 | Artisan snapshots |

### Content Surfaces

| Surface | Size | Source | Served by |
|---------|------|--------|-----------|
| `signal.primals.eco` | 97K | Hand-rolled HTML | Caddy file_server |
| `thesis.primals.eco` | 36K | Hand-rolled HTML | Caddy file_server |
| `sporeprint.primals.eco` | ~15M | Zola build | petaltongue |
| `git.primals.eco` | — | Forgejo + scatter | Caddy → Forgejo/scatter |

---

## Evolution Roadmap

### Phase 1: Converge Python → skunky-ingest (Rust)

**bloom_live.py** (745 lines) is the biggest jellystein. It:
1. Tails Caddy access log (skunky-ingest already does this)
2. Classifies visitors into L2 classes (skunky-ingest already does fleet detection)
3. Computes epitope hashes (new capability)
4. Tracks behavioral state per IP (new capability)
5. Writes dashboard/state/feed files (skunky-ingest could do this)
6. Writes epitope_caddy.json (epitope_bridge.py reads this)

**Target**: All of bloom_live's classification should move into skunky-ingest as `--bloom-classifier` or `--epitope-mode` flags. The epitope bridge becomes internal — skunky-ingest already writes the FLEET_PRESSURE block, it just needs to group by epitope hash instead of timing.

**entity_topology.py** (534 lines) generates topology graphs. This should be a skunky-ingest output mode.

**epitope_bridge.py** (83 lines) disappears entirely when skunky-ingest does epitope-keyed grouping natively.

### Phase 2: Signal Page → API-Driven

`signal.primals.eco` is 97K of hand-injected HTML that pulls from `dashboard.json` via JS fetch. This works but is fragile.

**Target**: petaltongue or a small Rust binary serves the signal page with SSR from `dashboard.json`. Or: keep the static HTML but have skunky-ingest write a more structured API endpoint.

### Phase 3: Provenance → sweetGrass/loamSpine/rhizoCrypt

The braid files (billboard + artisan) are currently JSONL with sha256 content hashing. This is the minimum viable braid — it works but isn't running through the provenance trio.

**Target**: When sweetGrass is deployed, braids flow through the proper content-addressed pipeline with Merkle tree verification.

### Phase 4: Fossil Cleanup

- Delete old skunky-ingest backups (13 binaries, ~52M)
- Archive bloom_live v2/v3 fossils (already in fossils/)
- Clean `skunky-ingest.bak` and `swarmvine.bak` from /opt/membrane root

---

## Current System Health

| Metric | Value |
|--------|-------|
| Disk usage | /opt 574M, /var/log 103M |
| Memory | 686M/1.9G used (36%) |
| Processes | 10 Rust + 1 Python + 3 cron |
| Uptime | Since May 15 (golgiBody) |
| Fleet state | 15 organisms, 51 IPs hashed, 8 clusters |
| Human traffic | 79 IPs, 4 genuine, 62 agentic |
| RPS | 11.8 steady |

---

## Summary

**What's solid (Rust, keep)**:
- skunky-ingest, skunkBat, swarmVine, bearDog, squirrel, Caddy, Forgejo, nestGate, petalTongue, step-ca, membrane

**What's jellystein (Python, evolve to Rust)**:
- bloom_live.py (745 lines) → skunky-ingest
- entity_topology.py (534 lines) → skunky-ingest
- epitope_bridge.py (83 lines) → skunky-ingest

**What's glue (shell, minimize)**:
- braid-billboard.sh (13 lines) — keep for now
- refresh-signal-data.sh (25 lines) — eliminate when API is native

**What's fossil (clean)**:
- 13 old skunky-ingest binaries (~52M)
- Pre-wave166 configs
- Old scripts in fossils/

**The convergence target**: skunky-ingest absorbs bloom_live + entity_topology + epitope_bridge. One Rust binary does log tailing, fleet detection, behavioral classification, epitope hashing, topology generation, Caddy bridge writing, and scatter server. The Python layer disappears.

---

*Wave 165i — October 7, 2026*
