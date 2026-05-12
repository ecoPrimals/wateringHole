# plasmidBin Push Automation Pipeline — Ecosystem Standard

**Status**: ACTIVE  
**Version**: 1.0  
**Date**: May 12, 2026  
**Authority**: primalSpring (pipeline owner)  
**Depends on**: [ECOBIN_ARCHITECTURE_STANDARD.md](ECOBIN_ARCHITECTURE_STANDARD.md)

---

## Overview

Every push to a primal's `main` branch triggers an automated pipeline that
builds ecoBin-compliant static binaries, computes BLAKE3 checksums, publishes
to `plasmidBin`, and creates GitHub Releases. This document defines the
pipeline, its components, and the contract each primal team must uphold.

## Pipeline Flow

```
Primal push to main
        │
        ▼
notify-plasmidbin.yml (per-primal workflow)
  sends repository_dispatch event-type: primal-updated
  payload: { primal, sha }
        │
        ▼
auto-harvest.yml (plasmidBin repo)
        │
   ┌────┴────┐
   │ prepare  │  Determine primal + version tag
   └────┬────┘
        │
   ┌────┴──────────────────────────┐
   │ build (3x parallel matrix)    │
   │  x86_64-unknown-linux-musl    │
   │  aarch64-unknown-linux-musl   │
   │  armv7-unknown-linux-musleabihf│
   └────┬──────────────────────────┘
        │
   ┌────┴──────────┐
   │  consolidate   │
   │  harvest.sh    │  per-arch: validate, strip, BLAKE3, copy
   │  ↓             │
   │  commit        │  checksums.toml + binaries
   │  ↓             │
   │  validate      │  post-harvest integrity check
   │  ↓             │
   │  release       │  GitHub Release (vYYYY.MM.DD)
   └───────────────┘
        │
        ▼
Downstream consumers (fetch.sh, update.sh)
  verify BLAKE3 against checksums.toml
```

## Triggers

| Trigger | When | Scope |
|---------|------|-------|
| `repository_dispatch` | Primal pushes to `main` | Single primal |
| `workflow_dispatch` | Manual (operator) | Single primal or `all` |
| Daily cron (05:30 UTC) | Catch-up for missed dispatches | `all` (reconciliation) |
| Weekly cron (Monday 06:00 UTC) | Full sweep | `all` |

The daily cron exists because `repository_dispatch` has a rate limit (~10/min/repo)
and can silently drop events. It runs as a reconciliation pass, not a full rebuild
— `harvest.sh` skips binaries whose BLAKE3 hash already matches `checksums.toml`.

## Primal Team Contract

Every primal repository with its own git repo MUST have:

1. **`.github/workflows/notify-plasmidbin.yml`** — the dispatch workflow.
   Template lives at `infra/plasmidBin/templates/notify-plasmidbin.yml`.
   Copy it verbatim; do not customize.

2. **`PLASMIDBIN_DISPATCH_TOKEN` secret** — a GitHub PAT with `repo` scope on
   the `ecoPrimals/plasmidBin` repository. Set as a repository secret.

3. **`sources.toml` entry** — `infra/plasmidBin/sources.toml` must have a
   `[sources.<primal>]` section with the correct `repo` URL.

### Current Wiring Status (May 2026)

All 12 primals with their own repositories are wired:
bearDog, songbird, toadStool, barraCuda, coralReef, rhizoCrypt, loamSpine,
sweetGrass, biomeOS, squirrel, petalTongue, skunkBat.

nestGate does not yet have its own repository. Workflow is staged on disk.

## Key Scripts

### `build-primal.sh`

Clones a primal (from `sources.toml`), builds for a target triple, and stages
the binary to `/tmp/primalspring-deploy/primals/{triple}/`.

```
./build-primal.sh beardog --target x86_64-unknown-linux-musl
./build-primal.sh --all --target aarch64-unknown-linux-musl
```

### `harvest.sh`

Takes staged binaries, validates they are static ELFs, strips them, computes
BLAKE3 checksums, copies to `plasmidBin/primals/{triple}/`, and updates
`checksums.toml`.

**Idempotent**: If the computed BLAKE3 hash matches the existing
`checksums.toml` entry, the binary is skipped. This prevents no-op commits
from polluting git history during reconciliation runs.

```
./harvest.sh --source /path/to/bins --arch x86_64-unknown-linux-musl
./harvest.sh --primal beardog --arch aarch64-unknown-linux-musl
./harvest.sh --dry-run
```

Exit code 1 if any binary fails validation.

### `update.sh`

Downstream consumer script. Fetches binaries from GitHub Releases, verifies
BLAKE3 checksums against `checksums.toml`, and installs locally.

Architecture detection emits full Rust target triples
(`x86_64-unknown-linux-musl`, not `x86_64-linux-musl`) to match
`checksums.toml` keys exactly.

```
./update.sh                  # fetch all
./update.sh beardog          # fetch one
./update.sh --verify-only    # check existing binaries
```

### `fetch.sh`

Lightweight fetcher for deployment. Downloads from GitHub Releases with
`manifest.toml` fallback to mirror URLs.

## `checksums.toml` Format

```toml
[primals.beardog]
"x86_64-unknown-linux-musl" = "<blake3-hex>"
"aarch64-unknown-linux-musl" = "<blake3-hex>"
"armv7-unknown-linux-musleabihf" = "<blake3-hex>"
```

Keys are full Rust target triples (quoted). Values are 64-character lowercase
hex BLAKE3 hashes of the stripped binary. Sections follow the pattern
`primals.<name>` or `springs.<name>`.

## Error Handling

The pipeline is designed to **fail loudly** rather than commit stale checksums:

- **Build failures**: `fail-fast: false` in the matrix means all three arches
  attempt to build, but the consolidate job tracks failures per-arch and
  aborts if any harvest exits non-zero.

- **Harvest failures**: `harvest.sh` exits 1 if any binary fails static ELF
  validation. The consolidate step counts failures across all arches and
  aborts before committing if any occurred.

- **Post-harvest validation**: After committing, a validation step re-reads
  every binary on disk and re-computes BLAKE3 against `checksums.toml`.
  If any mismatch is found, the job fails. This catches races where a
  concurrent push updated `checksums.toml` between harvest and commit.

## Sovereign CI Bridge (Tier 3 — Pre-Stadial)

The current pipeline runs on GitHub Actions. The interstadial exit plan
(H3-02/03/04) includes migrating to sovereign Forgejo CI on ironGate
(`git.primals.eco`).

**Preparation**:
- `sources.toml` will gain a `forge` field per primal pointing to the
  Forgejo mirror. `build-primal.sh` will fall back to Forgejo when
  GitHub clone fails.
- Forgejo Actions runner on biomeGate (GPU access for coralReef/toadStool
  sovereign builds).
- Shadow CI: run both GitHub and Forgejo in parallel, compare checksums,
  cut over when parity is proven.
- NestGate as release artifact store (`content.put` with BLAKE3 provenance)
  replaces GitHub Releases for sovereign distribution.

Cross-arch on Forgejo (single x86_64 machine) will use QEMU or
cross-compilation initially; dedicated aarch64/armv7 runners are a stadial
item.

## References

- [ECOBIN_ARCHITECTURE_STANDARD.md](ECOBIN_ARCHITECTURE_STANDARD.md) — binary compliance
- [INTERSTADIAL_EXIT_CRITERIA.md](INTERSTADIAL_EXIT_CRITERIA.md) — H3 sovereign CI gates
- `infra/plasmidBin/` — pipeline source code
- `infra/plasmidBin/templates/` — workflow templates for primal repos
