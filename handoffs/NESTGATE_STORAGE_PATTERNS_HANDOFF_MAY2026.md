# NestGate Storage Patterns Handoff — May 2026

**Source**: projectNUCLEUS provenance pipeline elevation on ironGate
**Audience**: NestGate primal team
**Date**: 2026-05-05

---

## Context

NestGate was deployed as part of a Nest Atomic + ToadStool composition (9 primals) on ironGate. It served as the content-addressed storage layer for the provenance pipeline, storing BLAKE3 hash references for NCBI data artifacts and workload outputs.

---

## Deployment Configuration

```bash
nestgate server --family-id 9b32f3a8 --port 9500
```

| Setting | Value |
|---------|-------|
| TCP JSON-RPC | `0.0.0.0:9500` (newline-delimited) |
| UDS | `/tmp/biomeos/biomeos/nestgate-9b32f3a8.sock` |
| Capability symlink | `/tmp/biomeos/biomeos/storage-9b32f3a8.sock` |
| Family ID | `9b32f3a8` |

---

## Methods Exercised

### `health.liveness`
```json
{"method": "health.liveness", "params": {}}
// Returns: {"primal": "nestgate", "status": "alive"}
```

### `storage.store`
```json
{"method": "storage.store", "params": {
    "key": "ncbi:SRR7760408:R1",
    "value": "blake3:6250f200f9ff45e0... size:2223544784"
}}
// Returns: {"family_id": "9b32f3a8", "key": "ncbi:SRR7760408:R1", "status": "stored"}
```

### `storage.list`
```json
{"method": "storage.list", "params": {}}
// Returns: {"keys": ["ncbi:SRR7760408:R1", "ncbi:SRR7760408:R2", ...]}
```

### Protocol Note
NestGate uses **newline-delimited JSON-RPC** on TCP (not HTTP). Calls use `printf '...JSON...\n' | nc -w 5 127.0.0.1 9500`, not `curl`. This is different from loamSpine (HTTP) and sweetGrass (HTTP).

---

## What Was Stored

14 artifacts across two categories:

### NCBI Data References (4)
| Key | BLAKE3 Hash | Size |
|-----|------------|------|
| `ncbi:SRR7760408:R1` | `6250f200f9ff45e0f3aa52ede78dbe4ad4a68dd1a55b355d7502b02afeaa672a` | 2.07 GB |
| `ncbi:SRR7760408:R2` | `cd89f43d74d09c64b4c832040f0cc04837c30bf7bb897f083dcd89ee6ece1d7c` | 2.21 GB |
| `ncbi:SRR5534045:R1` | `096878541679cd066ffa873ac024c7ca3089f4e5df0e6c81dbe05ed64acaeb30` | 424 MB |
| `ncbi:SRR5534045:R2` | `bee510af71ac914a5442492574f57b02b6a490eabeecce9d06242c333d9e1d7d` | 430 MB |

### Workload Output References (10)
| Key | Content |
|-----|---------|
| `workload:wetspring-r-industry-parity:output` | BLAKE3 hash of stdout capture |
| `workload:wetspring-fajgenbaum-pathway:output` | BLAKE3 hash of stdout capture |
| `workload:wetspring-diversity-rust-validation:output` | BLAKE3 hash of stdout capture |
| `workload:wetspring-gonzales-cpu-parity:output` | BLAKE3 hash of stdout capture |
| `workload:wetspring-algae-16s-rust:output` | BLAKE3 hash of stdout capture |
| `workload:wetspring-16s-rust-validation:output` | BLAKE3 hash of stdout capture |
| `workload:wetspring-cold-seep-pipeline:output` | BLAKE3 hash of stdout capture |
| `workload:wetspring-real-ncbi-pipeline:output` | BLAKE3 hash of stdout capture |
| `workload:wetspring-16s-python-baseline:output` | BLAKE3 hash of stdout capture |
| `workload:wetspring-benchmark-python-baseline:output` | BLAKE3 hash of stdout capture |

---

## Gaps and Resolutions

### Gap 1: Values are Flat Strings (Medium) — RESOLVED (Session 57)

`content.put` now accepts raw content, computes BLAKE3 automatically, stores
with hash-as-key, and returns the hash. Metadata (size, content type,
timestamps) stored in `.meta.json` sidecars. The KV `storage.store` API remains
flat-string for backward compatibility; content-addressed workflows should use
the `content.*` methods.

### Gap 2: No `storage.get` Exercised (Low) — RESOLVED (Session 57)

`content.get` retrieves by BLAKE3 hash with metadata. Integrity verification is
inherent: the hash *is* the key, so retrieval by hash guarantees content
integrity. Round-trip tests (`content.put` → `content.get` → verify) in
`content_handler_tests.rs`.

### Gap 3: No Blob Storage (Medium) — RESOLVED (Sessions 55-57)

`storage.store_blob` / `storage.retrieve_blob` implemented (Session 55+).
`storage.list_blobs` / `storage.blob_exists` added (Session 57) to close the
namespace visibility gap. For content-addressed blob workflows, `content.put`
accepts binary (base64-encoded) content and computes BLAKE3 automatically.

### Gap 4: Key Namespace Convention (Low) — PARTIALLY RESOLVED (Session 56)

All storage methods accept an optional `namespace` parameter for scoping:
`{family}/{namespace}/{key}`. The `content.*` methods use BLAKE3 hashes as keys,
providing implicit namespacing by content identity. Formal domain-level key
schema (`{domain}:{identifier}:{qualifier}`) remains a convention, not enforced.

---

## Current Storage Surface (as of Session 58)

### Content-Addressed Methods (Session 57)
| Method | Purpose |
|--------|---------|
| `content.put` | Store content, compute BLAKE3, return hash |
| `content.get` | Retrieve by BLAKE3 hash |
| `content.exists` | Check existence by hash |
| `content.list` | Enumerate stored hashes |
| `content.publish` | Create versioned manifest (path → hash) |
| `content.resolve` | Resolve path in manifest to content |
| `content.promote` | Set alias (e.g., `latest`) for a version |
| `content.collections` | List collections and versions |

### Blob Methods
| Method | Purpose |
|--------|---------|
| `storage.store_blob` | Store binary blob (param: `blob`, base64) |
| `storage.retrieve_blob` | Retrieve blob by key |
| `storage.list_blobs` | Enumerate blob keys |
| `storage.blob_exists` | Check blob existence |
| `storage.fetch_external` | Fetch URL, compute BLAKE3, cache (param: `cache_key`) |

### Streaming Methods
| Method | Purpose |
|--------|---------|
| `storage.store_stream` | Chunked upload (4 MiB max per chunk) |
| `storage.retrieve_stream` | Chunked download with offset/total_size |

### Parameter Naming (documented in `capability_registry.toml`)
- `storage.store_blob` uses `blob` (not `data`)
- `storage.fetch_external` uses `cache_key` (not `key`)
- `content.*` methods use `hash` for BLAKE3 references

---

## Integration Notes

- NestGate starts quickly and is very stable (ran for hours without issues)
- The capability symlink pattern (`storage-9b32f3a8.sock`) works well for discovery
- TCP JSON-RPC is straightforward for shell script integration
- Family ID in the response confirms correct routing in multi-gate scenarios
