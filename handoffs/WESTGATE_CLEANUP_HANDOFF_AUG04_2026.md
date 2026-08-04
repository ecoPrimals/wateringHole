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

## Upstream Gaps for Primals Teams

| Gap | Owner | Detail |
|-----|-------|--------|
| `spine_entry_append` still DEFINED in `bulk_ingest.py` | wateringHole | Dead code — no callers remain after manifest_download.py fix. Can remove once confirmed no other repos import it. |
| `pdb_ingest.py` / `pdb_manifest_ingest.py` only smoke-test provenance | wateringHole | If PDB needs full provenance, wire canonical pipeline (DAG session → dehydrate → commit → sign → braid). Currently health.check only. |
| `alphafold_bulk_structures.sh` fossil | wateringHole | Superseded. Can archive to `fossilRecord/` if desired. |
| GPS NumPy/pickle → JSON conversion | tideGlass | Only remaining data prep blocker for tideGlass Phase 0. |
| Convergence sweep across 154 datasets | wateringHole | `convergence_check.py` ready but hasn't been run at full scale. |

---

*Cleanup complete. All scripts aligned to canonical provenance (no per-file spine entries). Data stats current. Ready for upstream audit.*
