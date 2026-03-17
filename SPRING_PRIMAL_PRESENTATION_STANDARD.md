# Spring & Primal Presentation Standard — Getting Your Face Together

**Purpose:** Every spring and primal should be independently reviewable by an
outsider — a PI evaluating capability, a student onboarding, a compliance officer
auditing, or a hobbyist deciding what to build on. This standard defines what
"reviewable" means and provides a checklist for getting there.

**Audience:** Every spring and primal maintainer.
**Last Updated:** March 17, 2026

---

## Why This Matters

We have four audiences who will read your repo without context:

1. **Faculty and PIs** — evaluating whether this replaces a commercial tool in
   their lab. They need: what does it do, how does it compare, can I verify it.
2. **Students and core facility staff** — onboarding to use or extend the code.
   They need: how do I build it, how do I run it, where is the entry point.
3. **Hardware builders and hobbyists** — deciding whether to build compute
   infrastructure. They need: what hardware does it run on, what can my GPU do.
4. **Compliance and institutional review** — IRB, legal, QA, grant agencies.
   They need: what standards does it meet, what are the dependencies, is it safe.

A spring or primal that can't be understood in 5 minutes by any of these
audiences has not gotten its face together yet.

---

## The Checklist

### 1. Root README.md — The First Thing Anyone Reads

**Required sections (in this order):**

```markdown
# <Name> — <One-Line Domain Description>

**Date:** <last updated>
**License:** AGPL-3.0-or-later
**MSRV:** <minimum supported Rust version>
**Status:** <version> — <key metrics: test count, experiment count, check count>

## What This Is
<2-3 paragraphs: what domain, what it replaces, why it exists>

## Quick Start
<the fewest commands to build and verify>
  git clone ...
  cd ...
  cargo test --workspace
  cargo run --release --bin <most representative validation>

## Current Results
<table: metric | value — tests, checks, papers, binaries, shaders, etc.>

## Repository Structure
<brief directory tree with 1-line descriptions>

## Dependencies
<what external crates, what path dependencies, zero C?>

## Evolution Architecture
<Write → Absorb → Lean cycle status if applicable>
```

**What NOT to put in the root README:**
- Changelog entries (that's CHANGELOG.md)
- Detailed API documentation (that's rustdoc / module docs)
- Full experiment catalog (that's experiments/README.md)
- Internal planning (that's specs/ or whitePaper/)

### 2. CHANGELOG.md — What Changed and When

**Required:** Keep a Changelog format (keepachangelog.com).

Every version entry should answer:
- What was added / changed / fixed?
- How many tests/checks now?
- Were there breaking changes?

**One line per feature, not one paragraph.** A reviewer scanning the changelog
should understand the evolution trajectory in 30 seconds.

### 3. whitePaper/ — The Science

**Required structure:**

```
whitePaper/
├── README.md          # What the white paper covers, reading order
├── STUDY.md           # Main narrative, results, methodology
├── METHODOLOGY.md     # Validation protocol (how we test)
└── baseCamp/
    ├── README.md      # Index of baseCamp papers and faculty
    └── <papers>.md    # Per-faculty or per-domain research briefings
```

**baseCamp/README.md** must include:
- Date and current version status (copy the root README status line)
- Faculty summary table (who, institution, track, papers, experiments, checks)
- Reading order for different audiences (microbiologist, physicist, pharmacologist)

### 4. experiments/ — The Evidence

**Required:**

```
experiments/
├── README.md          # Experiment index: number, title, status, checks
└── <NNN_name>.md      # Per-experiment protocol and results
```

The experiments README should be a scannable table:

```markdown
| # | Title | Status | Checks |
|---|-------|:------:|:------:|
| 001 | Galaxy bootstrap | PASS | 12/12 |
| 002 | DADA2 denoising | PASS | 18/18 |
```

### 5. specs/ — The Requirements

**Required:**

```
specs/
├── README.md              # Spec index and status
├── PAPER_REVIEW_QUEUE.md  # What papers are reproduced / queued
├── BARRACUDA_REQUIREMENTS.md  # What GPU primitives this spring needs
└── <domain>_*.md          # Domain-specific specs
```

The specs README should clearly state:
- What papers have been reproduced (count and list)
- What barraCuda primitives are consumed (count and categories)
- What is planned vs validated

### 6. Validation Binaries — The Proof

Every `barracuda/src/bin/validate_*.rs` binary is a self-contained proof.

**Standard for validation binaries:**
- Hardcoded expected values with named tolerance constants
- Explicit PASS/FAIL output per check
- Exit 0 on all pass, exit 1 on any failure
- No interactive input, no external data files (unless unavoidable)
- Binary name describes what it validates: `validate_<domain>_<specifics>.rs`

**For reviewers:** Running `cargo run --release --bin validate_diversity`
should print something like:

```
[PASS] Shannon H' for uniform: expected 2.302585, got 2.302585 (tol 1e-12)
[PASS] Simpson D for uniform: expected 0.900000, got 0.900000 (tol 1e-12)
...
12/12 checks passed
```

### 7. scripts/ — The Baselines

**Required:** `README.md` explaining what each script does and why it exists.

Python/R baseline scripts exist to provide ground truth for Rust validation.
They are not production code. Label them clearly:

```
scripts/
├── README.md                    # What each script does
├── BASELINE_MANIFEST.md         # Provenance: Python version, package versions
├── requirements.txt             # Pin versions for reproducibility
├── python_<domain>_baseline.py  # Named to match the Rust validation
└── r_<domain>_baseline.R
```

### 8. wateringHole Handoffs — The Fossil Record

**Required for every version bump:**

A handoff in `wateringHole/handoffs/` with this structure:

```markdown
# <SPRING> <VERSION> — <Topic> Handoff

**Date:** <date>
**From:** <spring version>
**To:** barraCuda, toadStool, All Springs
**License:** AGPL-3.0-or-later
**Covers:** <previous version> → <current version>

## Executive Summary
- Bullet points of what changed

## Part 1: What Changed
- Detailed changes with tables

## Part 2: barraCuda Primitive Consumption
- CPU and GPU primitives consumed

## Part 3: Patterns Worth Absorbing
- What upstream should absorb from this spring

## Part 4: Quality Metrics
- Tests, checks, binaries, warnings, unsafe, TODO/FIXME
```

Previous handoffs go to `handoffs/archive/` — the fossil record.

---

## Presentation Quality Metrics

A spring or primal that has its face together meets ALL of these:

| Metric | Target | How to Check |
|--------|--------|:------------:|
| Root README is current | Version, date, metrics match reality | Read it |
| `cargo test --workspace` passes | 0 failures | Run it |
| `cargo clippy --all-targets -- -D warnings` | 0 warnings | Run it |
| `cargo fmt --all --check` | Clean | Run it |
| `cargo deny check` passes | No license/advisory violations | Run it |
| Zero `#[allow()]` in production | `#[expect(reason)]` only | `grep -r "#\[allow" src/` |
| Zero TODO/FIXME in production | Completed or tracked in specs | `grep -r "TODO\|FIXME" src/ --include="*.rs"` |
| Zero unsafe | `#![forbid(unsafe_code)]` in lib.rs | Check lib.rs |
| Zero mocks in production | All mocks in `#[cfg(test)]` | `grep -r "mock\|Mock" src/ --include="*.rs"` |
| CHANGELOG current | Latest version documented | Read it |
| Handoff filed | Latest evolution in wateringHole/handoffs/ | Check handoffs/ |
| whitePaper/baseCamp current | Faculty table matches reality | Read baseCamp/README.md |
| experiments/README current | Experiment count matches | Read it |

---

## Common Problems and Fixes

### "My README is 500 lines of changelog"

Move changelog entries to CHANGELOG.md. The README should be a snapshot of
current state, not a history of how you got there.

### "My validation binaries don't explain themselves"

Add a print header: what experiment this is, what paper it reproduces, how
many checks will run. Print PASS/FAIL per check with expected vs actual values.

### "My baseCamp is out of date"

The baseCamp status line should be copy-pasted from the root README status line.
If they diverge, one is wrong. Update after every version bump.

### "My specs reference capabilities we don't have yet"

Label clearly: "Validated" vs "Queued" vs "Planned". A reviewer who can't tell
what's real from what's aspirational will distrust everything.

### "My scripts/ has 50 Python files with no documentation"

Write `scripts/README.md` and `scripts/BASELINE_MANIFEST.md`. Each baseline
script should say which Rust validation binary it corresponds to.

### "I have outdated TODOs in my code"

Either complete them or remove them. A TODO that's been there for 3 versions
is not a TODO — it's a lie. Move it to specs/ if it's a real future item.

---

## For External Review: The 5-Minute Test

A reviewer should be able to do this in 5 minutes:

1. Open README.md → understand what this does and what it replaces
2. `cargo test --workspace` → see all tests pass
3. `cargo run --release --bin validate_<something>` → see explicit PASS/FAIL output
4. Open CHANGELOG.md → understand recent evolution
5. Open whitePaper/baseCamp/README.md → see the faculty and science context

If any of these steps fails or is confusing, the spring has not gotten its
face together yet.

---

## publicRelease/ Documents

The parent whitePaper repository maintains audience-specific briefs in
`attsi/non-anon/contact/publicRelease/` that reference capabilities across
all springs and primals:

| Document | Audience |
|----------|----------|
| `CAPABILITY_PARITY_BRIEF.md` | Technical evaluators |
| `FOR_FACULTY_AND_PIS.md` | Principal investigators |
| `FOR_STUDENTS_AND_CORE_FACILITIES.md` | Students, lab techs, core facilities |
| `FOR_HARDWARE_BUILDERS_AND_HOBBYISTS.md` | Gamers, hobbyists, distributed compute |
| `FOR_COMPLIANCE_AND_INSTITUTIONAL_REVIEW.md` | Legal, IRB, QA, regulatory |

Each spring should ensure its own presentation supports the claims made in
these documents. If a publicRelease brief says "wetSpring has 1,443+ tests"
and `cargo test` shows 1,200, something is wrong.

---

## Self-Assessment Template

Copy this to your spring/primal and fill it in before declaring "face together":

```markdown
## Presentation Self-Assessment — <Spring/Primal> <Version>

- [ ] README.md: date current, version current, metrics accurate
- [ ] README.md: Quick Start works (someone fresh can clone → build → verify)
- [ ] CHANGELOG.md: latest version documented
- [ ] cargo test: 0 failures
- [ ] cargo clippy: 0 warnings (pedantic + nursery)
- [ ] cargo fmt: clean
- [ ] cargo deny: passes
- [ ] Zero #[allow()] — only #[expect(reason)]
- [ ] Zero TODO/FIXME in production code
- [ ] Zero unsafe (#![forbid(unsafe_code)])
- [ ] Zero mocks in production
- [ ] whitePaper/baseCamp/README.md: status line matches root README
- [ ] experiments/README.md: experiment count matches reality
- [ ] specs/README.md: paper count and status current
- [ ] Latest handoff filed to wateringHole/handoffs/
- [ ] scripts/README.md exists and is current
- [ ] At least one validate_* binary produces clear PASS/FAIL output
```
