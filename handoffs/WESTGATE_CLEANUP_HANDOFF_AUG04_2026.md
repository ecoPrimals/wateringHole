# westGate Cleanup Handoff — Aug 4, 2026

**Wave**: 156d | **From**: westGate overwatch | **To**: golgiBody cascade → upstream audit

---

## What Changed

### Script Fixes (canonical provenance alignment)

| File | Change | Why |
|------|--------|-----|
| `manifest_download.py` | Removed per-file `spine_entry_append` call + import, updated docstring | Last script still using the old O(n) per-file spine pattern. Now canonical: per-file CAS+DAG, session-level spine commit. |
| `metered_download.sh` | Fixed header (was "INLINE provenance", actually runs batch `revalidate_data.py` post-download) | Header claimed per-file inline braiding; code does batch revalidation. Noted as superseded by `manifest_download.py`. |
| `pdb_ingest.py` | Updated docstring from "full provenance chain" to "smoke test" | Script only does `health.check` on rhizoCrypt/loamSpine, not full DAG→spine→sign→braid. |
| `pdb_manifest_ingest.py` | Updated docstring from "one DAG event, one cert, one sig, one braid" to "connectivity smoke test" | Same: runs `spine.create` + `health.check`, not the canonical dehydrate→commit flow. |
| `alphafold_bulk_structures.sh` | Added SUPERSEDED header | Replaced by `alphafold_bulk_download.py` (async Python, systemd service, `.prov_queue` integration). |

### Data Stats Corrected

| Doc | Old | Current |
|-----|-----|---------|
| `ECOSYSTEM_BLURB.md` | 519 GB / 130 datasets | 3.65 TB / 154 datasets |
| `data_federation_schedule.md` | 782 GB / 136 datasets | 3.65 TB / 154 datasets |
| `data_blockers.md` | 790 GB | 3.65 TB |

### Debris Cleaned

- `scripts/__pycache__/bulk_ingest.cpython-310.pyc` — deleted
- `.gitignore` added to `wateringHole/` (excludes `__pycache__/`, `*.pyc`, `*.pyo`, `*.log`)

---

## No False Positives Found

- **No stale TODOs/FIXMEs** in any scripts
- **No temp/backup files** (.bak, .swp, .orig, .tmp)
- **No cargo targets** to clean (sort-after Cargo.toml dirs have no target/ built)
- **All handoff docs in handoffs/** are current or intentional fossils
- **100 AAR fossils** properly archived in `aars/fossils/` (4 absorbed subdirs)
- **Protocols** (11 files) are stable standards docs — no cleanup needed

## Convergence Sweep Results — Aug 4, 2026

Full sweep across 153 datasets (147 scanned, 6 remaining):

| State | Count | Size | What it means |
|-------|-------|------|---------------|
| **CONVERGED** | 0 | — | Full provenance chain (CAS + DAG + spine + sig + braid) |
| **CAS-ONLY** | 5 | ~15.5 GB | BLAKE3 hashed in CAS, no DAG/spine. Includes alphafold_structures, gps_platform, ncbi_gene, noaa_ghcnd, refseq_human. |
| **PARTIAL** | 89 | ~205 GB | Some files CAS'd, others not. Most small/medium datasets. |
| **PRIMORDIAL** | 32 | ~636 GB | No CAS at all. Mostly large bulk downloads (ncbi_nr 48 GB, uniprot_trembl 110 GB, uniref100 43 GB, etc.) |
| **EMPTY** | 21 | 0 | Directory exists, no files yet (placeholders). |
| **Not scanned** | 6 | ~70 GB | uniref90, usda_nass, usda_plants, usgs_3dep, vibrio, zinc20_smiles (sweep timed out before reaching). |

**ZFS**: 3.21 TB used / 50.7 TB pool (6.3%). CAS pool: 135 GB.

**Key finding**: Zero datasets at CONVERGED. The canonical pipeline (DAG session → dehydrate → commit → sign → braid) has been proven at 43/s throughput but hasn't been run at bulk scale across the estate. The 89 PARTIAL datasets have CAS hashes but no provenance chain. The 32 PRIMORDIAL datasets are raw downloads with no CAS at all.

**Priority for convergence**:
1. Run batch provenance on the 89 PARTIAL datasets (smallest first — most are <100 MB)
2. CAS-ingest the 32 PRIMORDIAL datasets, then braid
3. The 5 CAS-ONLY datasets need DAG + spine wiring

## biomeOS v4.57 Deployed — Aug 4, 2026

- Built from source (commit `96083386`), installed to plasmidBin
- `nucleus attach` CLI available — unblocks tideGlass cell boot
- NUCLEUS restarted: 14/14 HEALTHY (13 primals + neural-api)
- `content.query` available via nestGate (same depot rebuild)

## GPS Data Converted — Aug 4, 2026

- 11 JSON outputs (103.4 MB total) CAS-ingested with BLAKE3
- Covers: 2198 gene lists, MLP weights, RCL ensembles, compound matrices
- Unblocks tideGlass Phase 0 Rust consumption

## Upstream Gaps for Primals Teams

| Gap | Owner | Detail |
|-----|-------|--------|
| `spine_entry_append` still DEFINED in `bulk_ingest.py` | wateringHole | Dead code — no callers remain after manifest_download.py fix. Can remove once confirmed no other repos import it. |
| `pdb_ingest.py` / `pdb_manifest_ingest.py` only smoke-test provenance | wateringHole | If PDB needs full provenance, wire canonical pipeline (DAG session → dehydrate → commit → sign → braid). Currently health.check only. |
| `alphafold_bulk_structures.sh` fossil | wateringHole | Superseded. Can archive to `fossilRecord/` if desired. |
| Depot CDN stale | sporeGate | golgi depot still serves v4.56.0 binary despite provenance.toml showing Aug 4 rebuild. westGate built from source. Other gates need depot fix or source build. |
| Bulk convergence campaign | wateringHole | 0/153 datasets at CONVERGED. Need batch provenance run across estate. |

---

*Cleanup + convergence sweep + biomeOS v4.57 deploy complete. westGate NUCLEUS 14/14 on v4.57. GPS data converted. 0 datasets CONVERGED — bulk provenance campaign needed. Ready for upstream audit.*
