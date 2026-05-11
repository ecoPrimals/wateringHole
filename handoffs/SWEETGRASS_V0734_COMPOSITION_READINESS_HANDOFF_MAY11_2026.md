# sweetGrass v0.7.34 — Composition Readiness Handoff

**Date**: May 11, 2026
**From**: sweetGrass team
**To**: primalSpring, ecosystem teams
**Ref**: primalSpring Full Stadial Gate Audit — sweetGrass composition path

---

## Summary

sweetGrass v0.7.34 validates the full composition path for the provenance
trio pipeline and resolves the MEDIUM gap from the stadial gate audit.

**Key fix**: `braid.create` now accepts flattened convenience fields
(`name`, `description`, `tags`, `source_session`, `source_merkle_root`)
as top-level params, merged into `BraidMetadata`. Previously, composition
callers sending `name` and `description` as top-level fields had them
silently ignored by serde.

---

## What Changed

### Flattened Convenience Fields on `braid.create`

Composition callers can now send the natural payload shape from the
operational handoff:

```json
{
  "data_hash": "292ebbcf8f02561aaa6c67b532ebbefc14c32192cf3dfb733ce81e45fba50f9e",
  "name": "abg-pipeline-20260504",
  "mime_type": "application/x-provenance-pipeline",
  "description": "ABG Full Pipeline - 24 events across wetSpring validators",
  "size": 24,
  "source_session": "019df42d-0fba-7170-a216-2f3b282e3fb9",
  "source_merkle_root": "292ebbcf8f02...",
  "tags": ["provenance", "pipeline"]
}
```

Field mapping:
- `name` -> `metadata.title` (if `metadata.title` not already set)
- `description` -> `metadata.description` (if not already set)
- `tags` -> `metadata.tags` (if tags array is empty)
- `source_session` -> `metadata.custom["source_session"]`
- `source_merkle_root` -> `metadata.custom["source_merkle_root"]`

Structured `metadata` takes precedence when both forms are present.

### Composition Contract Tests (8 new)

Validated exact payload shapes from `PROVENANCE_TRIO_OPERATIONAL_HANDOFF_MAY2026.md`:
1. Flattened name/description mapping
2. Structured metadata precedence
3. Source session + Merkle root in custom metadata
4. Bare hex hash acceptance (no `sha256:` prefix required)
5. Tags propagation
6. NFT seal round-trip (create -> commit -> loamSpine wire format)
7. skunkBat attribution.witness with security event payload
8. Full provenance trio pipeline end-to-end

---

## What Was Verified (no code changes needed)

- `urn:braid:` identifiers work with both bare hex and `sha256:`-prefixed hashes
- `braid.commit` produces base64 `data_hash_bytes` for loamSpine
- `is_signed()` correctly reports Tower Ed25519 signature status
- `CryptoDelegate` sign path produces valid witnesses
- `compute_signing_hash()` covers all braid identity fields
- NFT seal end-to-end: `braid.create` -> signed witness -> `braid.commit`

---

## Composition Readiness Status

| Path | Status |
|------|--------|
| Provenance trio pipeline | **READY** — `braid.create` accepts trio payload shapes |
| skunkBat JH-5 Phase 3 | **READY** — `attribution.witness` accepts forwarded events |
| NFT seal (braid -> commit -> loamSpine) | **READY** — round-trip verified |
| bearDog crypto delegation | **READY** — Ed25519 signing via `CryptoDelegate` |
| Token-gated methods | **READY** — `_bearer_token` extraction + JH-0 gate |

---

## Metrics

| Metric | v0.7.33 | v0.7.34 |
|--------|---------|---------|
| Tests | 1,536 | 1,544 |
| LOC | 54,565 | 54,879 |
| Clippy | 0 | 0 |
| Deep debt | 0 | 0 |

---

## Verification

```bash
cargo test --all-features    # 1,544 pass, 0 fail
cargo clippy --workspace --all-features --all-targets  # 0 warnings
```
