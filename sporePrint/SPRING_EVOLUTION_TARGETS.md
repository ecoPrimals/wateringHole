# Spring Evolution Targets

How springs evolve from CLI validation to fully live science on primals.eco.

**Audience**: Spring maintainers planning their next iteration.

---

## The Convergence Path

```
Tier 0: CLI binary         → stdout [OK]/[FAIL]
Tier 1: + notebook         → parse CLI output, matplotlib, exported HTML
Tier 2: + JSON-RPC methods → notebooks call primals directly, structured data
Tier 3: + petalTongue      → live web dashboards rendered from primal APIs
Standalone:                → NestGate serves content, sporePrint self-hosted on NUCLEUS
```

Each tier adds capability without removing previous tiers. A spring at Tier 0
continues to work when Tier 2 APIs exist. You always have a working system.

---

## What to Do Now (Tier 0 → Tier 1)

### 1. Fill Your `sporeprint/` Directory

Every spring now has a `sporeprint/` directory with starter content.
This is your publishing pipeline to [primals.eco](https://primals.eco).

```
your-spring/
  sporeprint/
    README.md                  ← explains the directory (already created)
    validation-summary.md      ← headline results stub (already created — fill in real data)
    additional-pages.md        ← add more as your science grows
```

**Validation summary template** (already in your repo):

```toml
+++
title = "yourSpring Validation Summary"
description = "One-line summary of your spring's results"
date = 2026-05-06

[taxonomies]
primals = ["barracuda", "toadstool"]    # primals your spring uses
springs = ["yourspring"]                 # your spring + cross-spring refs
+++

## Status

- **N checks** across M experiments — all passing
- **X papers** reproduced with full provenance

## Key Validation Binaries

- `validate_your_domain` — what it does
```

### 2. Create a Workload TOML

Add a workload TOML to `projectNUCLEUS/workloads/yourspring/`:

```toml
[metadata]
name = "yourspring-validation"
description = "What this workload validates"
version = "0.1.0"

[execution]
type = "native"
command = "/path/to/your/target/release/validate_binary"
working_dir = "/path/to/your/spring"

[resources]
max_memory_bytes = 4294967296
max_cpu_percent = 80.0

[security]
isolation_level = "None"
```

This lets ToadStool dispatch your validation on any gate running NUCLEUS.

### 3. Add a Notebook

Copy `projectNUCLEUS/notebooks/spring-validation-template.ipynb` and
customize for your spring:

1. Change `SPRING = 'yourspring'` in Cell 2
2. Update the visualization in Cell 5 for your domain
3. Add domain-specific analysis cells

The template already handles health-checking, workload dispatch, output
parsing, and provenance inspection.

### 4. Trigger Auto-Refresh

When you push to `main`, your `notify-sporeprint.yml` workflow fires.
To include content updates, set `"content": "true"` in the dispatch payload:

```yaml
# In your .github/workflows/notify-sporeprint.yml
client_payload: '{"source":"yourspring","content":"true"}'
```

sporePrint CI will clone your repo, copy `sporeprint/*.md` to `content/lab/`,
and create a PR for review.

---

## What to Evolve Toward (Tier 1 → Tier 2)

### JSON-RPC Method Targets

These methods are specified in `projectNUCLEUS/specs/LIVE_SCIENCE_API.md`.
When your primals implement them, notebooks call primals directly:

| Method | Owner | What It Does |
|--------|-------|-------------|
| `toadstool.validate` | ToadStool | Dispatch workload → structured JSON results |
| `toadstool.list_workloads` | ToadStool | Auto-discover available workloads |
| `biomeos.spring_status` | biomeOS | Which springs have binaries on this gate |
| `barracuda.compute` | barraCuda | Direct GPU compute request |
| `nestgate.artifact_query` | NestGate | Provenance chain for an artifact hash |
| `rhizocrypt.dag_summary` | rhizoCrypt | DAG session summary |

**Priority**: `toadstool.validate` and `toadstool.list_workloads` are P0 —
they unlock Tier 2 for every spring simultaneously.

### What Changes for Springs

At Tier 2, your validation binaries gain a `--format json` flag (or equivalent)
that outputs structured results instead of `[OK]/[FAIL]` text. ToadStool wraps
this into `toadstool.validate`.

```
Current:  binary → stdout → notebook parses text
Tier 2:   binary → json → toadstool.validate → notebook gets data
```

Your binary still works standalone. The JSON output is additive.

---

## What Comes After (Tier 3 → Standalone)

### Tier 3: petalTongue Live Dashboards

petalTongue reads Tier 2 APIs and renders web dashboards. Your spring gets a
live page on primals.eco that updates in real time as validation runs.

**What springs need**: Nothing — if your data flows through Tier 2 APIs,
petalTongue can render it.

### Standalone: Self-Hosted Science

When Phase 3 converges:

1. NestGate serves sporePrint content directly (no GitHub Pages)
2. petalTongue renders live dashboards from the running composition
3. rhizoCrypt/loamSpine/sweetGrass provide provenance for every result
4. The entire site runs on the same hardware as the science

**What springs need**: Nothing new — standalone is an infrastructure
evolution, not a spring interface change.

---

## Checklist for Spring Maintainers

- [ ] Fill `sporeprint/validation-summary.md` with real data
- [ ] Create additional `sporeprint/*.md` pages as science grows
- [ ] Create workload TOML(s) in `projectNUCLEUS/workloads/yourspring/`
- [ ] Customize notebook from template
- [ ] Set `"content": "true"` in notify-sporeprint dispatch payload
- [ ] Add `--format json` to validation binaries (Tier 2 prep)
- [ ] Review `LIVE_SCIENCE_API.md` for target method signatures

---

## Cross-References

- [CONTENT_GUIDE.md](CONTENT_GUIDE.md) — how to write sporePrint content
- [ONBOARDING.md](https://github.com/ecoPrimals/sporePrint/blob/main/ONBOARDING.md) — new repo onboarding checklist
- [LIVE_SCIENCE_API.md](https://github.com/sporeGarden/projectNUCLEUS/blob/main/specs/LIVE_SCIENCE_API.md) — full JSON-RPC method specs
- [NOTEBOOK_ELEVATION.md](https://github.com/sporeGarden/projectNUCLEUS/blob/main/specs/NOTEBOOK_ELEVATION.md) — notebook tier definitions
