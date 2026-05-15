<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
# Foundation Integration Guide

**Audience**: Spring developers, primal maintainers, garden product teams
**Purpose**: How to integrate with `gardens/foundation` — the scientific
knowledge layer that defines what NUCLEUS should validate
**Last Updated**: May 6, 2026

---

## What is Foundation?

`gardens/foundation` is the soil. It declares:
- **What data exists** (data/sources/*.toml — NCBI accessions, UniProt proteomes, KEGG pathways, PDB structures)
- **What results to expect** (data/targets/*.toml — published numerical values with tolerances)
- **How threads connect** (lineage/THREAD_INDEX.toml, lineage/BASECAMP_PAPER_MAP.toml)
- **How to validate** (deploy/foundation_validate.sh — provenance-wrapped pipeline)

Foundation does NOT contain primals, spring code, or deploy infrastructure.
projectNUCLEUS does that. Foundation tells NUCLEUS what to aim at.

```
foundation   →   "validate Paper A cell cycle at 9.0 ± 0.5 hours"
projectNUCLEUS → "deploy toadStool + barraCuda + provenance trio on ironGate"
spring        →   "run the ODE solver, get 8.7 hours, report [OK]"
```

---

## For Spring Developers

### Reading Foundation Targets

Your spring's validation binaries should read targets from foundation
manifests. The TOML schema for a validation target:

```toml
[[targets]]
id = "paper_a_cell_cycle"
paper = "A"
description = "Cell cycle duration for M. genitalium whole-cell model"
expected_value = 9.0
unit = "hours"
tolerance = 0.5
source = "Karr et al. 2012, Table S4"
spring = "hotSpring"
blake3 = ""
validated = false
```

When your spring validates this target:
1. Compare your result against `expected_value ± tolerance`
2. Output `[OK]` or `[FAIL]` to stdout (the provenance pipeline counts these)
3. The pipeline records your result hash in NestGate and marks the target

### Data Source Anchors

Foundation's `data/sources/*.toml` declares where external data lives.
Each source has an accession, URL, and (once fetched) a BLAKE3 hash.

Your spring should consume fetched data from the foundation cache
(`.data/` directory) rather than fetching independently. This ensures
every spring works from the same content-addressed dataset.

If your spring needs a source not yet in the manifests, add it:
1. Create or update the appropriate `data/sources/thread*.toml`
2. Include accession, database, URL, format, and paper reference
3. Leave `blake3 = ""` and `retrieved = ""` — the fetcher populates these
4. Submit the change to foundation

### Depositing Sediment

When your spring validates a target, the result becomes a sediment layer
in foundation's geological record. The process:

```
Spring binary runs → outputs [OK]/[FAIL] + result data
  ↓
foundation_validate.sh captures output → BLAKE3 hash
  ↓
NestGate stores the result artifact
  ↓
rhizoCrypt records the computation in the DAG
  ↓
loamSpine commits the Merkle root
  ↓
sweetGrass braids attribution (paper authors → your spring → the result)
  ↓
Sediment layer deposited in validation/run-<timestamp>/
```

The `validated = true` flag in `data/targets/*.toml` is set when the
full provenance chain is recorded. Results without provenance don't count.

### Creating Workloads

To make your spring's validation binaries discoverable by the foundation
pipeline, create a workload TOML in `workloads/thread*_*/`:

```toml
[metadata]
name = "your-workload-name"
description = "What this validates against which target"
version = "0.1.0"
thread = "01"

[execution]
type = "native"
command = "/path/to/your/spring/target/release/validate_binary"
working_dir = "/path/to/your/spring"

[resources]
max_memory_bytes = 2147483648
max_cpu_percent = 80.0

[security]
isolation_level = "None"
```

The `foundation_validate.sh` script discovers all `.toml` files in the
thread directory and executes them through toadStool with provenance.

---

## For Primal Maintainers

### NestGate: Data Source Storage

Foundation's `fetch_sources.sh` downloads public data and (with `--register`)
stores artifacts via NestGate's `storage.store` method. Key format:

```
ncbi:nucleotide:NC_000908.2    → GenBank file for M. genitalium
uniprot:proteome:UP000000807   → FASTA for M. genitalium proteome
kegg:mge                       → KEGG pathway data
```

NestGate should support efficient retrieval of these content-addressed
artifacts for spring consumption.

### rhizoCrypt: Validation DAGs

Each foundation validation run creates a DAG session. Event types used:
- `DataCreate` — artifact registered (source fetch)
- `ExperimentStart` — workload begins
- `ExperimentEnd` — workload completes (with ok/fail counts)

### loamSpine: Sediment Commits

Each validation run commits a `SessionCommit` entry with the Merkle root
of the rhizoCrypt DAG. This is the permanent record of what was validated,
when, and with what results.

### sweetGrass: Attribution Braids

Each validation run creates a braid linking:
- Original paper authors (e.g., "Karr et al. 2012")
- Data sources (NCBI, UniProt, etc.)
- Spring developers who built the validation binary
- The foundation repository and its maintainers

This is radiating attribution: credit flows backward through the chain.

---

## For Garden Product Teams

### Consuming Foundation Data

Products (helixVision, esotericWebb, blueFish) don't interact with
foundation directly. They consume validated results through NUCLEUS:

```
Product → toadStool → spring binary → foundation-anchored data
                                            ↓
                                    provenance trio records it all
```

The product never needs to know about NCBI accessions or BLAKE3 hashes.
It asks toadStool to compute something, and the provenance chain forms
automatically underneath.

### Thread Relevance

| Product | Foundation Threads |
|---------|-------------------|
| helixVision | 1 (WCM), 3 (Immuno), 4 (Enviro), 5 (Evo) |
| blueFish | 4 (Enviro) + data pipeline |
| esotericWebb | 9 (Gaming) |
| Patient Records | 8 (Health), 10 (Provenance) |
| Games@Home | 9 (Gaming) |

---

## The Feedback Loop

Foundation strengthens as springs validate:

```
Layer 0: Foundation declares targets and data sources
Layer 1: fetch_sources.sh pulls real NCBI/UniProt/KEGG data
Layer 2: Springs validate published results through NUCLEUS
Layer 3: Results flow back to foundation as sediment layers
Layer 4: Foundation targets get marked validated = true
Layer 5: Products consume validated data with full provenance
```

Each cycle adds geological weight. When a spring validates Paper A's
cell cycle at 9.0 hours with BLAKE3-hashed parameters traced to
1,900 source publications, that result is permanent. The next spring
builds on it. The sediment accumulates.

---

## Quick Reference

| What | Where |
|------|-------|
| Data source manifests | `gardens/foundation/data/sources/*.toml` |
| Validation targets | `gardens/foundation/data/targets/*.toml` |
| Thread index | `gardens/foundation/lineage/THREAD_INDEX.toml` |
| baseCamp paper map | `gardens/foundation/lineage/BASECAMP_PAPER_MAP.toml` |
| Deploy graph | `gardens/foundation/graphs/foundation_validation.toml` |
| Fetch script | `gardens/foundation/deploy/fetch_sources.sh` |
| Validation pipeline | `gardens/foundation/deploy/foundation_validate.sh` |
| Workloads | `gardens/foundation/workloads/thread*_*/` |
| Data integrity spec | `gardens/foundation/specs/DATA_INTEGRITY_CONTRACT.md` |
| Expression authoring | `gardens/foundation/specs/EXPRESSION_AUTHORING_GUIDE.md` |
