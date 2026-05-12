<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# LTEE GuideStone — Subsystem Handoff

**Date**: May 11, 2026
**Type**: New projectNUCLEUS Subsystem
**Standard**: `TARGETED_GUIDESTONE_STANDARD.md`
**Source**: `infra/whitePaper/gen4/architecture/GUIDESTONE_LTEE.md`

---

## What This Is

The LTEE guideStone is the ecosystem's first **Targeted GuideStone** — a
self-contained, USB-deployable artifact that reproduces 7 published
Long-Term Evolution Experiment papers and generates new predictions, all
without requiring the ecosystem to be running.

It is a **projectNUCLEUS subsystem**: a deployment product that will
conceivably leave ecosystem possession and be validated on external machines
(starting with the Barrick Lab at UT Austin).

---

## Target: Barrick Lab (UT Austin)

Richard Barrick runs the continuation of Richard Lenski's LTEE — the longest
running evolution experiment in history (75,000+ generations of *E. coli*).
The guideStone artifact is designed to:

1. Reproduce published results from 9 Barrick/Lenski papers (B1–B9)
2. Reproduce results from 5 Eaves/Woldring papers (E1–E5)
3. Generate new predictions using the Anderson disorder framework
4. Run on Barrick lab machines without any ecosystem dependencies
5. Track its own validation history via liveSpore.json

---

## Seven Science Modules

| Module | Paper(s) | Spring Source | What It Proves |
|--------|----------|---------------|----------------|
| 1. Power-law fitness | Wiser 2013 (B2) | groundSpring (stats), wetSpring (diversity) | Fitness trajectories follow power law with Anderson disorder analogy |
| 2. Mutation accumulation | Barrick 2009 (B1) | groundSpring (drift vs selection), neuralSpring (LSTM prediction) | Mutation clock with neutral null model |
| 3. Allele trajectories | Good 2017 (B3) | neuralSpring (LSTM+HMM+ESN), groundSpring (clonal interference) | Multi-clade dynamics with regime classification |
| 4. Citrate structural | Blount 2008/2012 (B4) | neuralSpring (early warning ESN), groundSpring (rare event stats) | Potentiating cascade detection before innovation |
| 5. BioBrick burden | Burden 2024 (B6) | neuralSpring (ML prediction), groundSpring (Anderson Wc analogy) | Burden distribution across 301 plasmids |
| 6. breseq comparison | Tenaillon 2016 (B7) | wetSpring (sovereign pipeline), groundSpring (epistasis quantification) | 264 genome download + mutation accumulation curves |
| 7. Anderson-QS predictions | Wiser + Anderson framework | hotSpring (disorder analogy), groundSpring (DFE/RMT) | New predictions: fitness landscape as disordered potential |

---

## Spring Paper Queue Seeding (Completed)

Paper targets from `infra/whitePaper/attsi/non-anon/contact/{barrick,eaves}/PAPER_REVIEW_AND_SPRING_TARGETS.md`
have been added to each spring's `specs/PAPER_REVIEW_QUEUE.md`:

| Spring | Papers Added | Track |
|--------|-------------|-------|
| wetSpring | B1–B8, E1, E5 (10 papers) | LTEE guideStone queue |
| neuralSpring | B1–B4, B6–B9, E2–E5 (12 papers) | LTEE guideStone queue |
| groundSpring | B1–B4, B6–B9 (8 papers) | LTEE guideStone queue |
| hotSpring | B2, B9 (2 papers) | LTEE guideStone queue |
| healthSpring | B5, E2, E4 (3 papers) | LTEE guideStone queue |
| airSpring | E3 (1 paper) | LTEE guideStone queue |

Total: 36 paper-spring assignments across 6 springs.

---

## Three-Tier Architecture

| Tier | What Runs | Requirements |
|------|-----------|-------------|
| **1 (Python)** | Pre-rendered HTML notebooks, Python analysis scripts | Python 3.10+ (or just a browser for HTML) |
| **2 (Rust)** | musl-static ecoBin binaries — full validation at native speed | Linux x86_64 or aarch64 (no runtime deps) |
| **3 (Primal)** | NUCLEUS composition with deploy graphs, provenance trio | NUCLEUS running + plasmidBin binaries |

Tier 1 runs everywhere. Tier 2 runs on any Linux machine. Tier 3 requires
the ecosystem. **No containers** — genomeBin/ecoBin handles platform detection;
primals self-container via genomeBin if needed.

---

## Cross-Platform Deployment

The `./ltee` entry point detects `uname -m` and `uname -s`, selects binaries
from `bin/{arch}/static/`. On unsupported platforms, falls back to Tier 1 and
reports what's available.

- **Linux x86_64/aarch64**: Full Tier 1 + 2 (+ Tier 3 with NUCLEUS)
- **macOS**: Tier 1 (Python/HTML) + genomeBin-selected binary if cross-compiled
- **Windows**: Tier 1 (Python/HTML) + WSL2 for Tier 2
- **Cloud**: Full Tier 1–3

---

## Artifact Size Estimate

| Component | Size |
|-----------|------|
| Binaries (x86_64 + aarch64, 7 modules) | ~200 MB |
| Data (published datasets, BLAKE3-hashed) | ~1.5 GB |
| Python notebooks + HTML renders | ~50 MB |
| Validation harness + expected values | ~10 MB |
| Deploy graphs (Tier 3) | ~1 MB |
| **Total** | **~1.8 GB** (fits on USB stick) |

---

## liveSpore Tracking

Every `./ltee validate` run appends to `liveSpore.json`:

```json
{
  "timestamp": "2026-05-15T14:30:00Z",
  "hostname_hash": "blake3(hostname)",
  "arch": "x86_64",
  "os": "linux",
  "tier_reached": 2,
  "modules_passed": 7,
  "modules_total": 7,
  "runtime_ms": 342000
}
```

No PII — hostname is BLAKE3-hashed. The artifact accumulates a provenance trail
of where it has been and what it proved.

---

## Data Freshness

The artifact can update itself via `./ltee refresh`:
- Reads `source_uri` from `data.toml` for each dataset
- Re-fetches from NCBI, Dryad, journal supplementals
- Re-hashes and compares against bundled hashes
- Re-validates to confirm artifact still passes

---

## Implementation Roadmap

### Phase 1: Architecture + Queue Seeding (THIS HANDOFF)

- [x] Targeted GuideStone standard defined (`TARGETED_GUIDESTONE_STANDARD.md`)
- [x] LTEE guideStone architecture defined (`whitePaper/gen4/architecture/GUIDESTONE_LTEE.md`)
- [x] Paper queues seeded in 6 springs (36 paper-spring assignments)
- [x] Subsystem registered in wateringHole

### Phase 2: Spring Reproductions (L3 — spring teams)

- [ ] Springs work through LTEE paper queue items
- [ ] Each reproduction produces validated Rust binaries + Python baselines
- [ ] Expected values and tolerances defined per module

### Phase 3: Binary Bundle + Data Assembly (L2 — primalSpring + L4 — NUCLEUS)

- [ ] Cross-compile contributing spring binaries as musl-static ecoBins
- [ ] Assemble data manifest with BLAKE3 hashes
- [ ] Write validation harness entry point
- [ ] Generate CHECKSUMS

### Phase 4: Integration + Deployment Testing (L4 — projectNUCLEUS)

- [ ] Test Tier 1 on macOS/Windows
- [ ] Test Tier 2 on clean Linux (no ecosystem installed)
- [ ] Test Tier 3 with NUCLEUS running
- [ ] Validate liveSpore tracking
- [ ] Dry-run data refresh

### Phase 5: External Deployment (L4 — projectNUCLEUS)

- [ ] Ship USB to Barrick Lab
- [ ] Collect liveSpore data from external validation
- [ ] Iterate based on feedback

---

## Ownership

| Layer | Responsibility |
|-------|---------------|
| L2 (primalSpring) | Targeted GuideStone standard, scope graph schema, validation harness pattern |
| L3 (springs) | Paper queue items, binary builds, scenario implementations |
| L4 (projectNUCLEUS) | Integration as subsystem, workload TOMLs, deployment testing |
| L5 (foundation) | Thread 04 (enviro genomics) + Thread 02 (plasma physics) data anchoring |

---

## References

- `infra/whitePaper/gen4/architecture/GUIDESTONE_LTEE.md` — original concept
- `infra/whitePaper/attsi/non-anon/contact/barrick/PAPER_REVIEW_AND_SPRING_TARGETS.md` — Barrick papers
- `infra/whitePaper/attsi/non-anon/contact/eaves/PAPER_REVIEW_AND_SPRING_TARGETS.md` — Eaves papers
- `infra/wateringHole/TARGETED_GUIDESTONE_STANDARD.md` — the standard this instance follows
- `infra/wateringHole/ECOBIN_ARCHITECTURE_STANDARD.md` — binary packaging
- `infra/wateringHole/PROVENANCE_TRIO_INTEGRATION_GUIDE.md` — Tier 3 provenance
