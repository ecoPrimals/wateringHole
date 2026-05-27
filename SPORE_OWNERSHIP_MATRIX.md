# Spore Ownership Matrix

**Purpose**: Authoritative ownership boundary for spore-related code and responsibilities.
Three concerns — domain science, spore envelope, and NUCLEUS gateway — have distinct
owners. This document prevents re-entanglement.

**Date**: May 27, 2026

---

## The Three Layers

A pseudoSpore transmission contains work from three ownership domains. Each layer
has exactly one owner. No layer imports code from another layer's owner.

```
┌─────────────────────────────────────────────────────────┐
│  biomeOS — NUCLEUS Gateway                              │
│  Ingests spores into NUCLEUS, emits spores from NUCLEUS │
│  Owner: primals/biomeOS                                 │
├─────────────────────────────────────────────────────────┤
│  lithoSpore — Spore Envelope (dispersal format)         │
│  BLAKE3, scope.toml, liveSpore.json, receipts, tarball  │
│  Owner: gardens/lithoSpore                              │
├─────────────────────────────────────────────────────────┤
│  Springs — Domain Science                               │
│  PLUMED, GROMACS, LTEE, game telemetry, etc.            │
│  Owner: springs/<spring> (each spring owns its domain)  │
└─────────────────────────────────────────────────────────┘
```

---

## Ownership Table

| Concern | Owner | What It Includes | What It Does NOT Include |
|---------|-------|-----------------|------------------------|
| **Spore Envelope** | lithoSpore (`gardens/lithoSpore/`) | BLAKE3 manifest (`data.toml`), `scope.toml` schema, `liveSpore.json` unified schema, `receipts/environment.toml`, `validation.json`, `domain_profile.toml` parsing, tarball creation (`[present]`/`[external]` split), braid envelope types, `tolerances.toml`, entry scripts (`validate`, `refresh`) | Domain-specific checks, GROMACS launch, NUCLEUS routing |
| **NUCLEUS Gateway** | biomeOS (`primals/biomeOS/`) | `biomeos nucleus ingest <spore>`, `biomeos nucleus emit <query>`, spore absorption into nest_atomic (NestGate + provenance trio), NUCLEUS composition registration, bidirectional spore lifecycle | Envelope parsing (delegates to pseudospore-core), domain science, figure generation |
| **Domain Science** | Individual springs | PLUMED-NEST targets, GROMACS mdrun, FES reconstruction, CAZyme FEL, barracuda GPU parity, LTEE growth curves, game telemetry, any domain-specific computation | Envelope packaging (delegates to `litho emit-pseudospore`), NUCLEUS routing |

---

## Shared Crate: pseudospore-core

Both lithoSpore and biomeOS depend on a shared crate for envelope primitives:

```
gardens/lithoSpore/crates/pseudospore-core/
├── src/
│   ├── blake3_manifest.rs    # data.toml read/write/verify
│   ├── braid_envelope.rs     # FermentBraid wire types (FermentTranscript)
│   ├── domain_profile.rs     # domain_profile.toml parsing
│   ├── livespore.rs          # liveSpore.json unified schema (envelope + validations)
│   ├── receipts.rs           # environment.toml, checksums.blake3, ChecksumEntry
│   ├── scope.rs              # scope.toml parsing and validation
│   ├── tarball.rs            # present/external split, tar.gz creation
│   ├── validation.rs         # validation.json read/write
│   └── lib.rs                # re-exports canonical types
└── Cargo.toml
```

**Dependency direction**: lithoSpore CLI and biomeOS CLI both depend on `pseudospore-core`.
Springs do NOT depend on `pseudospore-core` — they call `litho emit-pseudospore` as an
external binary.

---

## Current State vs Target

### nest-validate (current)

`springs/hotSpring/control/plumed_nest/nest-validate/src/main.rs` (~2,200 lines)
currently contains all three layers mixed together:

| Layer | Current Location | Target Location |
|-------|-----------------|-----------------|
| Domain science (PLUMED validate/analyze/ingest/run, cazyme, parity) | `main.rs`, `targets.rs`, `fes.rs`, `hills.rs`, `colvar.rs`, `stats.rs` | **Stays** in nest-validate |
| Spore envelope (guidestone hash/emit/verify, BLAKE3, scope, receipts) | `main.rs` lines ~469–2133 | **Moves** to `pseudospore-core` + `litho` CLI |
| NUCLEUS gateway (guidestone deploy step 7: litho ingest-pseudospore) | `main.rs` `guidestone_deploy()` | **Moves** to `biomeos nucleus ingest` |

### litho CLI (current)

`gardens/lithoSpore/crates/ltee-cli/src/` currently has LTEE-specific assumptions:

| Module | Current State | Target State |
|--------|--------------|--------------|
| `emit_pseudospore/` | **DONE** — domain-agnostic via `--domain-profile` | Domain-agnostic via `domain_profile.toml` |
| `audit/` | **DONE** — unified `{envelope, validations}` schema | Unified schema with `envelope` + `validations` |
| `ingest_pseudospore.rs` | Direct filesystem ingest (transitional until biomeOS NC-1.1) | Delegates to `biomeos nucleus ingest` when available |

---

## Interface Contracts

### Spring -> lithoSpore

Springs call `litho emit-pseudospore` to package their domain outputs:

```bash
litho emit-pseudospore \
  --name "hotSpring-CompChem-GuideStone" \
  --version "1.6.1" \
  --origin "ecoPrimals/springs/hotSpring" \
  --domain-profile ./domain_profile.toml \
  --output ./artifacts/
```

The spring provides:
- `domain_profile.toml` (declares modules, check commands, figure scripts)
- Raw data, configs, outputs, braids (via `--data-dir`, `--configs-dir`, etc.)

lithoSpore provides:
- Directory structure generation
- BLAKE3 checksums
- scope.toml, validation.json, liveSpore.json initialization
- Tarball creation
- Entry scripts (validate, refresh)

### lithoSpore -> biomeOS

The litho CLI calls `biomeos nucleus ingest` when absorbing a spore into a running
NUCLEUS:

```bash
biomeos nucleus ingest ./pseudoSpore_hotSpring-CompChem-GuideStone_v1.6.1/
```

biomeOS provides:
- Validation via `pseudospore-core`
- Absorption into nest_atomic (NestGate content-addressed storage)
- Registration with provenance trio (sweetGrass braid, loamSpine ledger, rhizoCrypt DAG)
- NUCLEUS composition update

### biomeOS -> lithoSpore (emit path, future)

NUCLEUS can create new spores from composition state:

```bash
biomeos nucleus emit --query "hotspring-compchem-guidestone" --output ./
```

biomeOS provides:
- Composition query resolution
- Data extraction from nest_atomic
- Packaging via `pseudospore-core`

---

## primalSpring Certification

primalSpring validates the ownership boundaries via:

| Experiment | What It Validates |
|-----------|-------------------|
| `exp_nest_ingest_pseudospore` | A pseudoSpore can be ingested by `biomeos nucleus ingest` on a Nest Atomic |
| `s_nest_atomic` (extended) | Spore ingest/verify round-trip through NestGate + provenance trio |

Gate criterion: **"Any spring can emit a pseudoSpore; any NUCLEUS can ingest it."**

---

## Universal Transmission Principle

A pseudoSpore is not a CompChem artifact. It is a **transmission package** for any domain.
The envelope is identical regardless of content:

| Domain | Module Contents | Same Envelope |
|--------|----------------|---------------|
| Computational chemistry | FES surfaces, HILLS, topologies | scope.toml, data.toml, liveSpore.json |
| Evolutionary biology | Growth curves, fitness landscapes | scope.toml, data.toml, liveSpore.json |
| Game design | Telemetry, interaction models | scope.toml, data.toml, liveSpore.json |
| Digital art | Textures, loan rules, provenance | scope.toml, data.toml, liveSpore.json |

Only `domain_profile.toml` and the module payloads change. The spore envelope,
NUCLEUS gateway, and primalSpring certification are domain-agnostic by design.
