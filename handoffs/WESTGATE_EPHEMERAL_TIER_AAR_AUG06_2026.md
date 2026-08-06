# AAR: Ephemeral Hot Tier — ENOSPC Event + Architecture Pattern

**Date**: Aug 6, 2026 | **Gate**: westGate (Data NAS)
**Event**: NVMe hot tier filled to 100%, crashed convoy, degraded OS
**Severity**: P1 — OS filesystem full, self-recovered via rsync drain
**Root Cause**: Hot tier treated as permanent sink with no drain mechanism

---

## What Happened

| Time | Event |
|------|-------|
| Aug 5 5:45 PM | XDG symlink repointed: `~/.local/share/nestgate/storage` → `/mnt/cas-hot` (NVMe) |
| Aug 5 5:45 PM | Convoy throughput jumped to 313/s instantaneous (2.4× improvement) |
| Aug 5 ~11 PM | NVMe reached 100% capacity (1.8 TB OS drive completely full) |
| Aug 5 ~11 PM | Convoy workers killed by ENOSPC on `content.put` write |
| Aug 6 2:53 AM | Convoy shell exited. Last status: workers at 76-90% progress |
| Aug 6 2:55 AM | Symlink reverted to ZFS. `rsync --remove-source-files` started draining NVMe→ZFS |
| Aug 6 7:17 AM | NVMe at 53% (917 GB), rsync still draining. System stable. |

## What Went Wrong

1. **No high-water mark.** The hot tier had no capacity guard. CAS objects
   accumulated at ~107 MB/s with no backpressure. 1.6 TB free → 0 in ~5 hours.

2. **Cross-tier dedup was broken.** When the symlink pointed to NVMe,
   `content.put`'s dedup check (`object_path.exists()`) only checked the
   NVMe path. ~600 GB of data already on ZFS cold was re-written to NVMe
   because the objects didn't exist at the new path.

3. **Hot tier as permanent sink.** We treated NVMe as permanent CAS storage
   instead of ephemeral working memory. No drain mechanism, no lifecycle.

4. **Shared OS drive.** `/mnt/cas-hot` lives on the root NVMe partition.
   When CAS filled it, the OS couldn't create temp files, journals, or
   shell state files.

## The Correct Pattern: Ephemeral Hot Tier

The hot tier is **braiding workspace** — ephemeral working memory for active
provenance sessions. The lifecycle:

```
INGEST:   nestGate content.put → warm tier (NVMe, fast random write)
BRAID:    rhizoCrypt dag.event → session accumulates on warm
SEAL:     loamSpine spine.commit → provenance chain sealed
DRAIN:    content.archive warm → cold (sequential bulk write to ZFS)
FREE:     warm tier cleared, ready for next session
```

The nest atomic must **own all its pools** and manage transitions internally.
The symlink hack proved the throughput thesis (2.4×) but broke because:
- nestGate sees one `storage_base_path`, not warm + cold
- No drain trigger on spine commit
- No capacity monitoring or backpressure

## What Exists in nestGate (Unwired)

| Component | Location | Status |
|-----------|----------|--------|
| `SubstrateTiers` | `nestgate-config/substrate_tiers.rs` | Discovers warm/cold paths, detects rotational media, measures capacity. **Not used by CAS handlers.** |
| `TierMigrationPlan` | `nestgate-zfs/automation/tier_migration.rs` | ZFS `send/receive` between tiers, dry-run support. **Not triggered by RPC.** |
| `MultiTierCache` | `nestgate-cache/multi_tier.rs` | Hot/warm/cold cache with promotion/demotion thresholds. **Not wired to CAS.** |
| `NESTGATE_WARM_PATHS` / `NESTGATE_COLD_PATHS` | env var support in `SubstrateTiers` | Parsed but unused by `content.put`. |
| `content.put` handler | `nestgate-rpc/content_handlers/cas.rs` | Uses `get_storage_base_path()` — single path, no tier awareness, no cross-tier dedup. |

## What Needs to Change (Upstream to nestGate)

**P0: Wire `SubstrateTiers` into `content.put`**
- `content.put` writes to first warm tier path
- Dedup check spans ALL tier paths (warm + cold)
- Capacity check before write (reject or backpressure at high-water mark)

**P1: Drain hook on `spine.commit`**
- When `loamSpine` commits a session, trigger `content.archive` for all
  CAS objects referenced by that session
- Archive = sequential copy from warm → cold, then delete warm copy
- This is the ZIL-at-application-layer pattern

**P2: `NESTGATE_STORAGE_PATH` audit**
- The env var is read by `storage_base_path()` but the XDG symlink at
  `data_dir.join("storage")` takes precedence in practice
- Either fix the resolution order or deprecate the env var

## Convoy Status Post-Event

| Worker | Braided | Progress | Status |
|--------|---------|----------|--------|
| convoy-0 | 2,169,800 | 76.0% | Killed (ENOSPC) |
| convoy-1 | 2,262,000 | 79.2% | Killed (ENOSPC) |
| convoy-2 | 2,315,688 | 90.0% | Killed (ENOSPC), 124,712 phantom errors |
| convoy-3 | 2,216,000 | 82.2% | Killed (ENOSPC) |
| **Total** | **~8,963,488** | **~81%** | Can `--resume` after drain |

Remaining: ~2M files across 4 partitions. ETA after restart: ~5-6 hours
at spinner speed (symlink back on ZFS).

## Key Numbers

| Metric | Value |
|--------|-------|
| NVMe hot tier throughput | 313/s (2.4× over spinner) |
| NVMe fill rate | ~107 MB/s sustained |
| Time to fill 1.6 TB | ~4.5 hours |
| Cross-tier data duplication | ~600 GB (dedup broken by tier switch) |
| Total braided before crash | ~8.96M / 11M (81%) |
| rsync drain rate NVMe→ZFS | ~28 MB/s |
| Estimated drain time | ~8 hours for remaining 740 GB |

## Lessons

1. **Hot tier needs a drain loop, not a symlink.** The throughput proof
   (2.4×) is solid. The architecture proof (ephemeral working memory) is
   correct. What's missing is the lifecycle management in nestGate itself.

2. **Dedup must be cross-tier.** Single-path `exists()` checks break when
   data lives across multiple tiers. The CAS content hash is the dedup key —
   it should be checked against a tier-spanning index.

3. **Never fill the OS drive.** Hot tier should either be on a dedicated
   partition/device or have a hard capacity limit. The convoy should have
   been monitoring `df` and pausing at 80%.

4. **The nest atomic should own its pools.** Symlink routing is a jelly
   string. `SubstrateTiers` exists in the codebase — wiring it into the
   CAS write path is the real fix. Then nestGate manages hot→cold internally,
   with the primal lifecycle (session → commit → archive) as the drain trigger.

---

*The hot tier worked. The throughput thesis is proven. What's missing is the
lifecycle: ingest on warm, braid through rhizoCrypt, seal via loamSpine,
drain to cold. The nest atomic needs to own all its pools — that's the
upstream priority for nestGate.*
