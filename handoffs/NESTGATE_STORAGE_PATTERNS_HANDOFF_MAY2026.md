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

## Gaps and Suggestions

### Gap 1: Values are Flat Strings (Medium)

Currently `storage.store` accepts a flat string `value`. The pipeline stores metadata as a formatted string: `"blake3:<hash> size:<bytes>"`. There's no structured metadata.

**Suggestion**: Support structured `value` as JSON object:
```json
{"method": "storage.store", "params": {
    "key": "ncbi:SRR7760408:R1",
    "value": {
        "blake3": "6250f200...",
        "size": 2223544784,
        "source": "ncbi",
        "accession": "SRR7760408",
        "read": "R1"
    }
}}
```

This would enable NestGate to serve as a proper metadata catalog, not just a key-value store.

### Gap 2: No `storage.get` Exercised (Low)

The pipeline stores artifacts but never retrieves them. The verification path (`storage.get` → compare BLAKE3 → confirm integrity) was not tested.

**Suggestion**: Verify `storage.get` returns exactly what was stored. Add a `storage.verify` method that re-hashes stored content and compares.

### Gap 3: No Blob Storage (Medium)

Currently only **metadata references** are stored (hash + size as strings). The actual FASTQ files (2+ GB each) remain on the filesystem. NestGate should support storing actual file content with automatic BLAKE3 verification.

**Suggestion**: Add `storage.store_blob` that:
1. Accepts a file path or streamed bytes
2. Computes BLAKE3 hash automatically
3. Stores content in the configured storage backend (ZFS, local FS, etc.)
4. Returns the content hash as the storage key

This is the natural evolution toward the `[data.inputs]` TOML pattern where toadStool resolves content-addressed data from NestGate before execution.

### Gap 4: Key Namespace Convention (Low)

The pipeline used ad-hoc key patterns (`ncbi:SRR7760408:R1`, `workload:name:output`). No formal namespace convention exists.

**Suggestion**: Document a key schema: `{domain}:{identifier}:{qualifier}` where domain is one of `ncbi`, `workload`, `pipeline`, `artifact`, etc.

---

## Integration Notes

- NestGate starts quickly and is very stable (ran for hours without issues)
- The capability symlink pattern (`storage-9b32f3a8.sock`) works well for discovery
- TCP JSON-RPC is straightforward for shell script integration
- Family ID in the response confirms correct routing in multi-gate scenarios
