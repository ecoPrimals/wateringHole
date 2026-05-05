SPDX-License-Identifier: AGPL-3.0-or-later

# Spring provenance pattern (tiered API responses)

| Field | Value |
|-------|-------|
| **Version** | 1.0.0 |
| **Date** | 2026-04-06 |
| **Status** | Canonical |

## Purpose

Standardize how springs wrap API results with provenance metadata. This pattern evolved from **wetSpring** NUCLEUS deployment—the first spring to implement full progressive provenance. Related context: `handoffs/WETSPRING_SCIENCE_NUCLEUS_GAPS_HANDOFF_APR06_2026.md`.

## RootPulse is not a primal

**RootPulse** is a coordination pattern: named TOML graphs that biomeOS executes over existing trio primals (**rhizoCrypt**, **loamSpine**, **sweetGrass**). Springs consume provenance via capability calls routed through the **Neural API**.

## Self-knowledge principle

Each spring implements its own provenance wiring. **primalSpring does not export provenance client code.** Springs invoke capabilities directly with `capability_call("domain", "operation", args)` on the Neural API. Canonical `by_capability` domain strings live in `CAPABILITY_DOMAIN_REGISTRY.md`.

## Tier 1 — Always available (local)

No external dependencies. Every API response includes:

- `guidestone_version` — spring version + git commit hash
- `content_hash` — BLAKE3 hash of the response body
- `timestamp` — ISO 8601 UTC
- `computation` — method name + parameters
- `reproduction` — embedded plasmidBin manifest (deploy graph, fetch/deploy commands); packaging norms in `STANDARDS_AND_EXPECTATIONS.md` and `ARTIFACT_AND_PACKAGING.md`
- `nft_vertex` — Novel Ferment Transcript vertex (`NOVEL_FERMENT_TRANSCRIPT_GUIDANCE.md`)

## Tier 2 — Trio reachable (Neural API)

When rhizoCrypt, loamSpine, and sweetGrass are reachable through the Neural API:

1. `capability_call("provenance", "create_session", ...)` — rhizoCrypt session
2. `capability_call("provenance", "event.append", ...)` — record computation
3. `capability_call("provenance", "dehydrate", ...)` — Merkle root
4. `capability_call("ledger", "session", ...)` — loamSpine commit
5. `capability_call("attribution", "create_braid", ...)` — sweetGrass braid

Augment the response with: `rhizocrypt_session`, `loamspine_commit`, `sweetgrass_braid`, `merkle_root`. Operation IDs may align with rhizoCrypt `dag.*` / loamSpine `commit.*` surfaces; resolve naming via `CAPABILITY_DOMAIN_REGISTRY.md` and deployed graphs.

## Tier 3 — Full RootPulse (federation)

When full provenance export is available:

- PROV-O export via `capability_call("attribution", "export_provo", ...)`
- `verify_url` — public verification endpoint
- Public chain anchor: loamSpine v0.9.16 `anchor.publish` / `anchor.verify` — records receipts from external ledgers; chain submission via capability-discovered `"chain-anchor"` primal

## Graceful degradation contract

| Condition | Behavior |
|-----------|----------|
| Neural API unreachable | Tier 1 only; domain logic proceeds |
| Trio partially available | Best-effort Tier 2; partial fields |
| All trio healthy | Full Tier 2 + optional Tier 3 |

## Resilience pattern

Implement a **circuit breaker** around trio calls. If the trio is down, short-circuit to Tier 1 for a cooldown. Prefer the generic `CircuitBreaker` from the IPC resilience module, or an equivalent (see `fossilRecord/nestgate/current/ERROR_HANDLING_FRAMEWORK_GUIDE.md` for the pattern in ecosystem docs).

## Envelope pattern

Wrap the payload returned to clients:

```json
{
  "result": {},
  "provenance": {
    "tier": 2,
    "guidestone": {},
    "content_hash": "blake3:...",
    "trio": {},
    "nft_vertex": {},
    "reproduction": {}
  }
}
```

Set `provenance.tier` to the integer `1`, `2`, or `3`. Use `"trio": null` at Tier 1; populate `trio` when Tier 2+ fields are present.

## Witnesses

Session witnesses carried by the trio are **self-describing**: each witness
carries `kind`, `encoding`, `algorithm`, and `tier` metadata alongside the
opaque evidence payload. Witnesses may be cryptographic signatures, hash
observations, checkpoints, markers, or bare timestamps — the trio is
agnostic. See `ATTESTATION_ENCODING_STANDARD.md` for the full `WireWitnessRef`
specification.
