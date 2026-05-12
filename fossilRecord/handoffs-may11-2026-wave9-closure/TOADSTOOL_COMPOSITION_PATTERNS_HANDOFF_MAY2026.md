# ToadStool Composition Patterns Handoff — May 2026

**Source**: projectNUCLEUS ABG pipeline demo + provenance pipeline elevation
**Audience**: toadStool and biomeOS primal teams
**Date**: 2026-05-05

---

## Context

toadStool was exercised as the compute dispatch layer in a 9-primal Nest Atomic composition on ironGate. 11 workload TOMLs were executed (8 Rust validators, 2 Python baselines, 1 skipped for missing data), dispatching 235+ scientific validation checks across 6 bioinformatics domains with real NCBI data.

A provenance wrapper script (`provenance_pipeline.sh`) brackets each `toadstool execute` call with pre/post RPC calls to the provenance trio. This handoff documents what worked, what didn't, and what toadStool could absorb.

---

## Workload TOML Patterns That Work

### Rust Native Workload (validated)
```toml
[metadata]
name = "wetspring-r-industry-parity"
description = "R Industry Parity — vegan/DADA2/phyloseq validation"
version = "1.0.0"
tags = ["wetspring", "diversity", "rust"]

[execution]
type = "native"
command = "/absolute/path/to/validate_r_industry_parity"
args = []
working_dir = "/absolute/path/to/wetSpring"

[resources]
cpu_cores = 1
memory_mb = 512
timeout_seconds = 60

[security]
isolation_level = "None"
```

### Python Native Workload (validated)
```toml
[execution]
type = "native"
command = "/absolute/path/to/python3"
args = ["/absolute/path/to/script.py", "--arg1", "value"]
working_dir = "/absolute/path/to/wetSpring"
```

### Key Pattern: All Paths Must Be Absolute

toadStool does not expand environment variables (`${VAR}`) or `~`. The sandbox may override `working_dir` to `/tmp` under Standard isolation. Every workload TOML that needs to find files must use absolute paths throughout.

---

## Gaps for toadStool Team

### Gap 1: Environment Variable Expansion (Medium)

`${WETSPRING_DIR}`, `${PYTHON_BIN}`, `$HOME` in TOML fields are passed as literal strings. All 11 workload TOMLs had to be manually updated with machine-specific absolute paths.

**Suggestion**: Expand `${VAR}` patterns before execution. Even minimal support (`$HOME`, `$ECOPRIMALS_ROOT`) would make TOMLs portable. Alternative: a `[variables]` section in the TOML:
```toml
[variables]
WETSPRING = "/path/to/wetSpring"
PYTHON = "/path/to/python3"

[execution]
command = "${PYTHON}"
args = ["${WETSPRING}/scripts/baseline.py"]
```

### Gap 2: Sandbox working_dir Override (Medium)

With `isolation_level = "Standard"`, toadStool overrides `working_dir` to `/tmp`. All data-dependent workloads require `isolation_level = "None"` to function.

**Suggestion**: `trusted_directories` list or `allow_working_dir` flag.

### Gap 3: Python Runtime Not Introspected (Low)

Python workloads run as native subprocesses. toadStool has no visibility into their resource usage, output format, or lifecycle.

**Suggestion for provenance**: Python workloads don't produce `[OK]`/`[FAIL]` markers that Rust validators do. Consider a standard output format (`{checks_passed: N, checks_failed: M}` JSON line) that toadStool can parse.

---

## The Provenance Wrapper Pattern

Currently, provenance is handled by an external shell script that calls toadStool:

```
for each workload:
    1. rhizoCrypt: dag.event.append (ExperimentStart)
    2. toadstool execute workload.toml > output
    3. b3sum output → BLAKE3 hash
    4. NestGate: storage.store (output hash + size)
    5. rhizoCrypt: dag.event.append (Result, confidence_percent)
    6. loamSpine: entry.append (DataAnchor for output)
```

### Suggestion: Native `[provenance]` Section

If toadStool absorbed the provenance wrapper, workload TOMLs could declare:
```toml
[provenance]
enabled = true
session_id = "019df42d-..."            # or auto-create
nestgate_key = "workload:{{name}}:output"
hash_algorithm = "blake3"
```

toadStool would automatically:
- Hash outputs with BLAKE3
- Store in NestGate via `storage.store`
- Append DAG events to rhizoCrypt
- Record results in loamSpine

This eliminates the shell wrapper and makes provenance a first-class dispatch feature.

---

## Deploy Graph Patterns Exercised

The following deploy graphs from projectNUCLEUS were used:

| Graph | Primals | Use |
|-------|---------|-----|
| `node_atomic.toml` | beardog, songbird, toadstool, barracuda, coralreef | Initial compute composition |
| `nest_atomic.toml` | tower + nestgate + provenance trio | Storage + provenance elevation |
| `tower_atomic.toml` | beardog + songbird | Trust foundation |

biomeOS was **not** in the live composition. All dispatch was via direct `toadstool execute` CLI. Neural API routing was not exercised.

### Suggestion: biomeOS Graph Executor for Provenance Pipeline

The provenance pipeline follows the same pattern as `biomeOS/graphs/provenance_pipeline.toml`:
1. Verify stack health
2. For each workload: execute → hash → store → record
3. Dehydrate DAG → sign → commit → braid

biomeOS graph executor could orchestrate this natively once it's in the live composition.

---

## Results Summary

| Metric | Value |
|--------|-------|
| Workloads dispatched | 10 (+ 1 skipped) |
| Rust checks passed | 235+ |
| Real NCBI data | PRJNA488170 (11.9M reads) |
| Dispatch overhead | Sub-millisecond for Rust binaries |
| Longest workload | Algae 16S: 23s (11.9M reads through DADA2/taxonomy/UniFrac) |
| Provenance events | 24 (4 data + 10 starts + 10 results) |
| Primals stable for | Multiple hours, zero crashes |
