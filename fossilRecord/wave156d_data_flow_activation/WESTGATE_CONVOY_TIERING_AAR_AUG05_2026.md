# AAR: Convoy Provenance + Storage Tiering — westGate

**Date**: Aug 5, 2026 | **Gate**: westGate (Data NAS)
**Event**: 4-worker convoy braiding 11M+ AlphaFold files through provenance trio
**Duration**: Aug 4-5, 2026 (ongoing)
**Outcome**: 2.7× throughput improvement via NVMe hot tier; 4-tier storage
architecture proven and documented

---

## Timeline

| Time | Event | Rate |
|------|-------|------|
| Aug 4 AM | Convoy launched (socat + b3sum subprocesses, 4 workers) | 38.4/s combined |
| Aug 4 AM | Socat elimination: native `socket.AF_UNIX` + Python `blake3` | 145.5/s combined |
| Aug 4 PM | Rate degradation as CAS pool grows on spinners | ~80/s combined |
| Aug 5 AM | NVMe hot tier activated (`NESTGATE_STORAGE_PATH=/mnt/cas-hot`) | **217/s combined** |
| Aug 5 AM | Steady state on NVMe | ~180-220/s combined |

## What Went Right

1. **Native sockets eliminated subprocess overhead.** Replacing `socat` with
   `socket.AF_UNIX` and `b3sum` with Python `blake3` module removed ~50ms of
   subprocess spawn time per file. This was the single largest software
   optimization.

2. **Primals were fast from the start.** rhizoCrypt DAG append at 4ms,
   nestGate CAS put at 0.5ms, bearDog sign at 0.1ms. The Rust primals
   never needed optimization — they were idle waiting for I/O.

3. **NVMe hot tier was immediate and dramatic.** Changing one environment
   variable (`NESTGATE_STORAGE_PATH`) and restarting nestGate boosted
   throughput 2.7× instantly. No code changes.

4. **ZFS ARC and L2ARC worked as designed.** 98% ARC hit rate and 65.9%
   L2ARC hit rate meant most reads were served from cache. The problem
   was writes, not reads.

## What Went Wrong

1. **Initial convoy used socat/b3sum subprocesses.** Every RPC call spawned
   a process. At 4 RPCs per file, 38.4 files/s meant 153 process spawns/s.
   This was never going to scale.

2. **CAS writes on spinners caused I/O contention.** ZFS COW on raidz1
   amplified 80 logical writes/s to 247 disk IOPS. Spinners can't handle
   mixed random read/write workloads — reads and writes fight for the same
   heads.

3. **NVMe was underutilized for months.** 1.6 TB of free NVMe was available
   the entire time. No one considered pointing CAS writes there because
   "the ZFS pool is the data tier."

4. **No monitoring of storage I/O patterns.** The convoy rate degradation
   from 145/s to 80/s was initially puzzling. Only after checking `zpool
   iostat` did the write contention become visible.

## What We Learned

### For Other Gates to Model

**Pattern 1: Flash-backed braiding.** Any gate doing CAS ingest (braiding)
should write to NVMe, not spinners. The braiding operation (BLAKE3 hash +
CAS put + DAG event) is inherently random I/O. Random I/O on spinners is
the worst case for ZFS COW. NVMe eliminates the bottleneck.

**Pattern 2: Separate read and write tiers.** Spinners should do reads and
sequential writes. Flash should do random writes. L2ARC (SSD) should cache
reads. These three roles should not share hardware unless unavoidable.

**Pattern 3: Native socket IPC always.** Any script talking to primals in
a hot loop must use native sockets, not socat. The `socket.AF_UNIX` pattern
benchmarked at 16,352 RPCs/s — 100× faster than socat subprocess spawn.

**Pattern 4: Inline braiding > trailer braiding.** Processing provenance
while data is still in memory (just downloaded, still in RAM/page cache)
is always faster than re-reading from cold disk. westGate achieved 265/s
with inline braiding vs 217/s with trailer convoy (cold disk reads).

**Pattern 5: Monitor `zpool iostat -v` during heavy I/O.** Write contention
is invisible without per-vdev I/O monitoring. The symptoms (rate degradation,
high iowait) could be mistaken for primal slowdowns.

### For Future Gate Builds

| Recommendation | Why |
|---------------|-----|
| Dedicated NVMe for hot CAS | Don't share with OS at scale |
| 128 GB RAM (ECC) | ARC is the most effective cache layer |
| SSD for L2ARC (dedicated) | Read cache should not share with write tier |
| raidz2 at 8+ disks | raidz1 at 5 disks is one failure from data loss |
| 10G between all gates | Federation serving needs fast local + fast pipe |
| Braiding NUC pattern | Dedicated ingest appliance, pushes braided data to NAS |

### For Primal Teams

| Finding | Upstream Target |
|---------|----------------|
| nestGate could support multi-path storage (hot + cold) | `NESTGATE_HOT_PATH` + `NESTGATE_COLD_PATH` config |
| Convoy throughput correlates with storage tier, not primal speed | Document in nestGate operational guide |
| `session.commit` (not per-file `entry.append`) is canonical | Already documented in PROVENANCE_TRIO_ARCHITECTURE |

## Key Numbers

| Metric | Value |
|--------|-------|
| Convoy workers | 4 (parallel, partitioned queue) |
| Per-file primal time | ~5 ms |
| Per-file disk write (spinner) | ~36 ms |
| Per-file disk write (NVMe) | ~0.02 ms |
| Native socket RPC throughput | 16,352/s |
| socat subprocess overhead | ~10 ms/call |
| ZFS ARC hit rate | 98% |
| ZFS L2ARC hit rate | 65.9% |
| Convoy rate (socat) | 38.4/s |
| Convoy rate (native socket, spinner) | 145.5/s → 80/s (degraded) |
| Convoy rate (native socket, NVMe) | **217/s** |
| Inline braid rate (warm) | 265/s |

## Files Changed

| File | Change |
|------|--------|
| `scripts/alphafold_prov_convoy.py` | Native sockets, Python blake3, 4-worker partitioning |
| `scripts/prov_inline.py` | Inline braiding module (canonical) |
| `handoffs/WESTGATE_STORAGE_TIERS_AUG05_2026.md` | 4-tier architecture documentation |
| `whitePaper/subGen/LATENCY_FOLDING_HARDWARE.md` | Full subGen document on latency folding |
| `~/.config/systemd/user/nestgate.env` | `NESTGATE_STORAGE_PATH` → `/mnt/cas-hot` |

## Follow-Up Actions

| Action | Owner | Status |
|--------|-------|--------|
| Post-convoy: rsync hot → cold, restore `NESTGATE_STORAGE_PATH` | westGate | Pending (convoy running) |
| Document inline braiding as canonical in PRIMAL_CAPABILITY_GAPS | westGate | Done |
| Evaluate nestGate dual-path CAS as primal feature | nestGate team | Proposed |
| Monitor convoy to completion (~14h ETA from activation) | westGate | Running |

---

*Convoy at 217/s on NVMe hot tier. Primals at ~5ms/file. Storage was the
bottleneck. Latency folding across 4 tiers (RAM/NVMe/SSD/HDD) proven.
Pattern ready for replication across gates.*
