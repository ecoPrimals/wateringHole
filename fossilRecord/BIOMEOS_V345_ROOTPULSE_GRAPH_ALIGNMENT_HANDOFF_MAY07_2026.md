# biomeOS v3.45 — RootPulse Graph Method Alignment + Standalone Executor (RP-1 through RP-5)

**Date**: May 7, 2026
**Author**: biomeOS agent
**Triggered by**: projectNUCLEUS sovereignty testing on ironGate — 5/6 RootPulse phases passing, Phase 5 (LoamSpine commit) failing due to method/param mismatches.

---

## Summary

All 6 RootPulse/provenance graph TOML files have been updated to match the
canonical method names and parameter schemas in primalSpring's
`capability_registry.toml`. A new `biomeos graph execute` CLI enables
standalone execution of any graph TOML against the live Neural API server.

## RP-1 (HIGH): Method/Param Name Alignment

Three mismatches fixed across 6 graph files:

| Old (broken) | New (correct) | Primal |
|---|---|---|
| `crypto.sign` param `data` | `crypto.sign` param `message` | BearDog |
| `commit.session` | `session.commit` | LoamSpine |
| `provenance.create_braid` | `braid.create` | sweetGrass |

Additional fixes:
- `dag.dehydrate` → `dag.dehydration.trigger` (rhizoCrypt)
- `dag`/`get_merkle_root` → `dag.merkle.root` (rhizoCrypt)
- `entry`/`get_tip` → `entry.get` (LoamSpine)
- `crypto`/`verify_ed25519` → `crypto.verify` (BearDog)
- Stale `did` parameter removed from `crypto.sign` calls.

Files updated:
- `graphs/rootpulse_commit.toml`
- `graphs/rootpulse_branch.toml`
- `graphs/rootpulse_merge.toml`
- `graphs/rootpulse_diff.toml`
- `graphs/rootpulse_federate.toml`
- `graphs/provenance_pipeline.toml`

## RP-2 (HIGH): Spine Lifecycle Prerequisites

All commit-path graphs now document `${SPINE_ID}` as a required input
variable. The commit graph header explains that a spine must already
exist (created via `rootpulse_branch` or `spine.create`).

## RP-3 (MEDIUM): Type Documentation

All graphs document required input variables with types (string, integer)
in the header comments. Phase comments document the method owner, canonical
param names, and wire contract notes.

## RP-4 (MEDIUM): Standalone Graph Executor

New CLI:

```bash
biomeos graph execute rootpulse_commit --param SESSION_ID=abc --param SPINE_ID=s1 --param AGENT_DID=did:key:z6Mk
biomeos graph execute graphs/rootpulse_commit.toml --param SESSION_ID=abc --dry-run
```

Sends `graph.execute` JSON-RPC to the Neural API server. Accepts graph ID
or TOML file path. `--dry-run` shows the request without sending.

## RP-5 (MEDIUM): Signing Lifecycle Clarification

Phase comments in graph files clarify:
- BearDog signs the dehydration merkle root (Phase 3), not the LoamSpine entry.
- `session.commit` takes `committer` as a DID string.
- `braid.create` takes `data_hash` (the commit ref), not a full summary.

## Verification

- `cargo clippy --workspace -- -D warnings`: 0 warnings.
- `cargo fmt --check`: clean.
- `cargo test --workspace --lib`: 6,842 tests, 0 failures.
- `cargo test -p biomeos-unibin`: 474 bin tests, 0 failures.
- No unsafe code, no TODO/FIXME markers.
