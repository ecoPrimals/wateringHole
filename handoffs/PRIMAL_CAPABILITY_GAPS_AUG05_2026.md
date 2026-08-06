# Upstream Primal Capability Gaps — westGate Field Report

**Date**: Aug 5, 2026 | **Wave**: 156d | **From**: westGate overwatch
**Context**: After migrating all Python glue from socat subprocess to native
socket RPC, we found that the primals themselves are fast (nestGate 16K RPCs/s,
rhizoCrypt <1ms batch). The remaining Python scripts exist only because the
primals don't yet expose certain operations natively.

---

## Capabilities That Would Eliminate Python Scripts

### nestGate

| Gap | Current Python Workaround | What It Would Do |
|-----|---------------------------|------------------|
| `content.fetch` | `curl` subprocess + `content.put` | Download URL directly into CAS. Fetch → hash → store in one RPC. Eliminates all download-then-ingest scripts. |
| `content.ingest` | Filesystem walk + per-file `read_bytes()` + `content.put` | Scan a directory, hash all files, bulk store. Eliminates `revalidate_data.py` entirely. |
| `dataset.convergence` | `convergence_check.py` (183 lines) — sample files, check CAS membership, query braids | Report provenance state (CONVERGED/PARTIAL/PRIMORDIAL/EMPTY) for a dataset path. Would be one RPC call. |
| `dataset.list` | Python `pathlib.iterdir()` on `/mnt/nestgate/cold/zfs/data/` | List known datasets with CAS stats. |
| `content.query` | Not currently possible | Query CAS by metadata (dataset, hash prefix, size range). |

### rhizoCrypt

| Gap | Current Python Workaround | What It Would Do |
|-----|---------------------------|------------------|
| `dag.pipeline.ingest` | Multi-step Python: `session.create` → per-file `event.append_batch` → `dehydration.trigger` | Full pipeline in one RPC: accept file list, create session, batch events, dehydrate, return Merkle root. |
| `dag.session.list` | No way to enumerate sessions | List active/completed sessions with stats. |

### sweetGrass

| Gap | Current Python Workaround | What It Would Do |
|-----|---------------------------|------------------|
| `convergence.check` | Manual chain: CAS exists? → DAG has events? → spine committed? → braid exists? → signed? | Verify full provenance chain for a dataset in one call. The trust gate for spring consumption. |
| `braid.list` | No way to enumerate braids | List braids by dataset, time range, committer. |
| `braid.validate` | Not possible without manual chain walk | Verify braid integrity: Merkle proof → signature → spine → DAG → CAS content hashes. |

### loamSpine

| Gap | Current Python Workaround | What It Would Do |
|-----|---------------------------|------------------|
| `spine.status` | `spine.list` exists but limited | Report spine health: entry count, last commit, Merkle root, associated sessions. |

---

## What Stays in Python (Appropriate)

These are data-specific or coordination tasks that don't belong in primals:

| Script | Lines | Why It's Python |
|--------|-------|-----------------|
| `alphafold_bulk_download.py` | 183 | HTTP API client for AlphaFold. Network I/O, API-specific retry/pagination. |
| `gps_to_json.py` | 309 | NumPy/pickle → JSON data transformation. Domain-specific. |
| `pdb_manifest_ingest.py` | 360 | PDB-specific batch hashing (b3sum multi-threaded, 257K files). |
| `westgate_boot_check.sh` | 309 | System health check (bash, systemd, ZFS). |

---

## What We Archived (Fossils)

| Script | Superseded By |
|--------|---------------|
| `bulk_ingest.py` | `prov_inline.py` (native sockets, in-process blake3) |
| `alphafold_prov_trailer.py` | `prov_inline.py` + `alphafold_prov_convoy.py` |
| `alphafold_bulk_structures.sh` | `alphafold_bulk_download.py` |
| `metered_download.sh` | `manifest_download.py` |

---

### nestGate — Multi-Tier CAS (P0 — PROVEN CRITICAL)

| Gap | Current Workaround | What It Would Do |
|-----|-------------------|------------------|
| `content.put` tier-aware writes | Symlink repoint (`~/.local/share/nestgate/storage`) | Write to warm tier (NVMe), dedup-check across ALL tiers. `SubstrateTiers` already exists in `nestgate-config` but is NOT wired to `nestgate-rpc` CAS handlers. |
| `content.archive` / drain hook | Manual `rsync --remove-source-files warm → cold` | Post-`spine.commit` hook: migrate committed CAS objects from warm → cold. Hot tier is ephemeral working memory, not permanent storage. |
| High-water mark backpressure | None (NVMe filled to 100%, crashed convoy + OS) | When warm tier reaches capacity threshold (e.g. 80%), pause ingestion or begin drain. Prevents filling the OS drive. |
| Cross-tier dedup check | Dedup only checks current `storage_base_path` | `content.put` should check `object_path.exists()` on ALL tier paths before writing. When we repointed symlink from ZFS→NVMe, ~600 GB of already-CAS'd data was re-written because dedup only checked the new (empty) NVMe path. |
| `NESTGATE_STORAGE_PATH` env var | Dead letter — nestGate uses XDG symlink instead | Either wire the env var into `get_storage_base_path()` properly (it reads but doesn't take effect) or deprecate it and document the XDG symlink as the control surface. |

**What already exists in the codebase (unwired)**:
- `nestgate-config/substrate_tiers.rs`: `SubstrateTiers` with `NESTGATE_WARM_PATHS` / `NESTGATE_COLD_PATHS` env discovery, rotational detection, capacity detection
- `nestgate-zfs/automation/tier_migration.rs`: `TierMigrationPlan` with ZFS `send/receive` between tiers, dry-run support
- `nestgate-cache/multi_tier.rs`: `MultiTierCache` with hot/warm/cold and promotion/demotion thresholds

**What's missing**: `nestgate-rpc/content_handlers/cas.rs` uses `get_storage_base_path()` (single path) for all CAS operations. Zero references to `SubstrateTiers` or `StorageTier` in the RPC layer. The write path needs to be tier-aware.

**Conceptual model**: Hot tier is rhizoCrypt's working memory. As sessions commit through loamSpine, committed data migrates to cold. The nest atomic owns all its pools and manages the transitions internally — no symlink hacks, no manual rsync.

---

## Priority for Upstream

**P0** (caused production outage — NVMe filled to 100%):
1. `nestGate content.put` tier-aware writes — write to warm, dedup across all tiers
2. `nestGate content.archive` — drain warm → cold on spine commit

**P1** (would eliminate the most Python):
3. `nestGate content.ingest` — eliminates revalidate + convergence check + manual CAS orchestration
4. `sweetGrass convergence.check` — eliminates `convergence_check.py`, becomes the trust gate

**P2** (would simplify download pipelines):
5. `nestGate content.fetch` — download URL → CAS in one RPC
6. `rhizoCrypt dag.pipeline.ingest` — full pipeline in one call

**P3** (observability):
7. `sweetGrass braid.list` — enumerate braids for audit
8. `rhizoCrypt dag.session.list` — enumerate sessions
9. `nestGate dataset.list` — enumerate datasets with stats

---

## Metrics

| Before (socat era) | After (native socket) |
|---|---|
| 6 independent socat RPC copies | 1 canonical module (`prov_inline.py`) |
| 38 files/s provenance | 265 files/s inline, 130/s convoy |
| ~10ms per RPC (fork+exec+connect) | ~0.06ms per RPC (socket connect) |
| 4 fossil scripts | Archived to `fossilRecord/` |
| 11 active Python scripts | 10 active (bulk_ingest archived) |
| 0 scripts using native sockets | 8 scripts using `prov_inline` |

---

*The primals were always fast. nestGate handles 16K RPCs/s, rhizoCrypt <1ms
batch, bearDog signs in <5ms. Every performance issue we found was in the Python
glue layer — subprocess spawning, double file reads, sequential processing,
and most critically, storage topology (symlink routing, single-tier CAS,
no drain mechanism). The upstream priority is to wire nestGate's existing
`SubstrateTiers` infrastructure into the CAS write path, so the nest atomic
owns all its pools and manages hot→cold transitions internally. The Python
layer should shrink to data-specific transformation scripts only.*
