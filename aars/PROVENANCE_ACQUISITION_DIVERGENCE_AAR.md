# AAR: Provenance × Acquisition Speed Divergence

**Date**: Aug 4, 2026
**Wave**: 156a
**Gate**: westGate
**Team**: Hardware / Overwatch
**Audience**: Upstream primals teams, sporeGate topology, biomeOS signal team

---

## Objective

Make provenance tracking integral to data acquisition — no more separate
revalidation passes. "From here on out, we should be getting provenance with
the data pulls."

## What Happened

### Phase 1: Inline Provenance (Direct Approach)

Wired the full provenance chain directly into `alphafold_bulk_download.py`:

```
download .cif → BLAKE3 hash → CAS put → DAG event → spine entry
```

**Result: 12× throughput collapse.** Download rate dropped from 74 files/s to
5–6 files/s. At 5/s, the 240M remaining AlphaFold structures would take
~555 days instead of ~37 days.

### Root Cause

Each provenance step is a synchronous UDS RPC call:

| Operation | Target Socket | ~Latency |
|-----------|--------------|----------|
| `blake3_hash` | local CPU | < 1ms (300 KB file) |
| `cas_put` | nestgate.sock | 5–10ms |
| `dag_event_append` | rhizocrypt.sock | 5–10ms |
| `spine_entry_append` | loamspine.sock | 5–10ms |

Total provenance per file: ~20–30ms. But the RPC calls are serialized on the
UDS socket — even with 8 parallel provenance workers in a thread pool executor,
the sockets serialize requests. The async download pipeline (20 concurrent HTTP
connections) produces files at 74/s, but the provenance chain can only consume
~30–40/s through its single-threaded UDS handlers.

**This is the acquisition-provenance divergence**: download throughput scales
with network concurrency, but provenance throughput is bounded by sequential
UDS RPC latency.

### Phase 2: Trailer Architecture

Decoupled into two companion services:

| Service | Role | Rate |
|---------|------|------|
| `alphafold-bulk.service` | Download only (full speed) | 63–74/s |
| `alphafold-prov.service` | Follows behind, braids new files | ~30–40/s |

The trailer reads the download progress file, finds unbraided .cif files on
disk, and runs the full provenance chain. It can fall behind temporarily but
catches up during pauses (rate limits, network issues, restarts).

**Problem discovered**: the initial `find_unbraided()` scan across 5.8M files
in thousands of subdirectories was itself too slow. The trailer needs a
progress-file-driven approach rather than filesystem scan.

### Phase 3: Metered Download Script

Updated `metered_download.sh` to call `revalidate_data.py --dataset` after
each download completes. This works well for the sequential queue (one file
at a time), but doesn't scale for the async bulk downloader.

### Phase 4: Standard Acquisition Pattern

Added `fetch_and_ingest()` to `bulk_ingest.py` — a single function that
downloads a URL and immediately runs it through the full provenance chain.
This is the correct pattern for small-to-medium datasets (<1000 files).

---

## Current State

| Component | Status | Detail |
|-----------|--------|--------|
| AlphaFold bulk download | RUNNING | 5.84M done, 240M remaining, 63/s |
| AlphaFold prov trailer | STOPPED | Needs progress-file-driven scan |
| AlphaFold revalidation (old) | RUNNING | PID 133597, processing existing 575K structures |
| Remaining braid job | RUNNING | alphafold proteomes (1.1 TB), nist_pfas, pdb_mmcif_manifests |
| nestGate CAS | HEALTHY | v0.5.0 |
| metered_download.sh | UPDATED | Inline provenance per download |
| bulk_ingest.py | UPDATED | `fetch_and_ingest()` convenience function |

### Provenance Coverage

| Data Class | Files | Braided? | Method |
|------------|-------|----------|--------|
| Priority datasets (14) | ~33K | YES | CAS ingest script |
| SRA FASTQ (785 files) | 785 | YES | Revalidation complete |
| AlphaFold structures (5.84M) | 5.84M | PARTIAL | Revalidation running (~13K done) |
| AlphaFold proteomes (1,145) | 1,145 | IN PROGRESS | Background braid job |
| PDB mmCIF manifests | small | IN PROGRESS | Background braid job |
| New downloads (metered) | varies | YES | metered_download.sh inline |
| New AlphaFold structures | 240M+ | NO | Awaiting trailer fix |

---

## The Divergence Problem (for upstream)

The core issue is architectural:

```
Acquisition rate:    74 files/s  (bounded by network + API)
Provenance rate:     30-40 files/s  (bounded by sequential UDS RPC)
Gap:                 ~2× at current scale
```

At 240M files, this gap compounds into months of divergence. The provenance
chain can never catch up if downloads run continuously.

### Why This Matters Beyond AlphaFold

Any high-throughput data source will hit this same wall:
- Bulk genomic data from ENA/SRA
- PDB full mirror updates
- LINCS L1000 level 5 updates
- Any mesh-based data federation (gate-to-gate transfers at 10 Gbps)

The UDS RPC model works perfectly for human-speed operations (experiment
results, manual ingests, API queries). It breaks at machine-speed bulk
acquisition.

### Potential Evolution Paths

1. **Batch RPC**: Instead of one RPC per file, send batches of 100–1000
   events in a single DAG/spine call. This requires `dag.event_batch` and
   `spine.entry_batch` methods in rhizoCrypt and loamSpine.

2. **Direct CAS write**: For bulk imports, bypass the UDS RPC and write
   directly to the CAS storage layer (ZFS path). Then create a single DAG
   session covering the entire batch with a manifest hash.

3. **Provenance-at-rest**: Instead of inline provenance, write a manifest
   file alongside the download progress. A periodic job (timer) processes
   the manifest and creates provenance records. Trades immediacy for
   throughput.

4. **Streaming DAG**: rhizoCrypt accepts a persistent connection (not
   request-response) where events stream in and acknowledgments batch out.
   This eliminates per-event RPC overhead.

5. **Sharded provenance**: Multiple DAG sessions running in parallel on
   different socket endpoints. Each provenance worker gets its own session.
   Sessions merge at dehydration time.

### Recommended for biomeOS Signal Team

Option 1 (batch RPC) is the lowest-friction evolution. The existing
`dag.event.append` signal could gain a batch variant:

```toml
[signal.dag.event.batch]
provider = "rhizoCrypt"
params = ["session_id", "events"]  # events = [{hash, name, size, source}]
returns = ["vertex_ids"]
```

Similarly for spine:

```toml
[signal.spine.entry.batch]
provider = "loamSpine"
params = ["spine_id", "entries"]  # entries = [{hash, mime, size}]
returns = ["entry_ids"]
```

This keeps the existing architecture (UDS RPC, signal graphs, capability
registry) while eliminating the per-file overhead. A batch of 500 events
in one RPC call would close the 2× gap.

---

## Mixed Provenance → Unified CAS

The local westGate challenge: we now have data in three provenance states:

| State | Description | Example |
|-------|-------------|---------|
| **Primordial** | On disk, no CAS entry, no DAG, no spine | Early ad-hoc downloads |
| **CAS-only** | BLAKE3 hashed and in CAS, but no DAG/spine/braid | Old `content.put` calls |
| **Fully braided** | CAS + DAG session + spine + Merkle root + signature + braid | All new acquisitions |

To unify:

1. **Inventory**: Walk ZFS data root, cross-reference with CAS `content.exists`,
   check for DAG session and braid records per dataset.

2. **Promote primordial → fully braided**: Run `revalidate_data.py` per
   dataset. This creates the full chain retroactively. Already running for
   the priority datasets and AlphaFold structures.

3. **Promote CAS-only → fully braided**: These files already have BLAKE3
   hashes in CAS. Just need DAG session + spine + sign + braid wrapping.
   A lightweight variant of revalidation that skips the hash + CAS put.

4. **Convergence marker**: Once a dataset has a sealed Merkle root + braid,
   mark it as "converged" in a manifest. Springs can check convergence
   before trusting data for computation.

### Convergence Check Pattern

```python
def is_dataset_converged(dataset_name):
    """Check if a dataset has full provenance — safe for spring consumption."""
    braids = rpc_result("sweetgrass", "braid.list", {"dataset": dataset_name})
    if not braids:
        return False
    latest = braids[-1]
    sig = rpc_result("beardog", "signature.verify", {"hash": latest["merkle_root"]})
    return sig and sig.get("valid", False)
```

This becomes the gate between "data available" and "data trusted."

---

## Files Changed

| File | Change |
|------|--------|
| `scripts/alphafold_bulk_download.py` | Reverted to clean download-only (removed inline prov) |
| `scripts/alphafold_prov_trailer.py` | NEW — companion provenance service |
| `scripts/metered_download.sh` | Added inline provenance per download |
| `scripts/bulk_ingest.py` | Added `fetch_and_ingest()` standard pattern |
| `scripts/alphafold_full_sync.sh` | Added provenance pass after sync |
| `systemd/alphafold-prov.service` | NEW — trailer service unit |

---

## Upstream Actions

- **biomeOS signal team**: Design `dag.event.batch` and `spine.entry.batch`
  signals. This is the single highest-impact evolution for data throughput.
- **rhizoCrypt team**: Implement batch event append (accept array of events,
  return array of vertex IDs, single RPC round trip).
- **loamSpine team**: Implement batch entry append (same pattern).
- **sporeGate topology**: The acquisition-provenance divergence will also
  appear in mesh data transfers. Design bandwidth governance to account for
  provenance overhead in federation throughput calculations.
- **westGate local**: Fix the prov trailer's file discovery (use progress
  file diff instead of filesystem scan). Continue revalidation of existing
  data. Target: all spring-critical data fully braided before Phase 4 boot.

---

## Lessons

1. **Provenance at machine speed is an unsolved problem** in the current
   architecture. UDS RPC is perfect for human-speed, breaks at bulk speed.
   This is the same class of problem that databases solved with WAL batching
   and LSM trees — the answer is always batching.

2. **The trailer pattern works** as a bridge. Download fast, braid later,
   but always braid. No data should exist on ZFS without eventually getting
   a Merkle root and braid. The "eventually" is the gap to close.

3. **Mixed provenance is a real state** that the system needs to handle
   gracefully. Springs should check convergence before trusting data.
   The primordial → braided promotion path is well-defined and automated.

4. **The `fetch_and_ingest()` pattern is the right default** for everything
   except bulk downloads. One function call: download + full provenance.
   All future acquisition scripts should use it.

---

*The divergence between acquisition speed and provenance speed is the first
real-world scaling challenge for the primal composition model. Solving it
with batch RPCs will benefit every gate, every spring, and every future
data federation operation.*
