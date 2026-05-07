# sporePrint Content Guide

How springs, primals, and products publish their science to [primals.eco](https://primals.eco).

**Audience**: Upstream maintainers who want their baseCamp science, validation results, or documentation visible on the public site.

---

## Two Tiers of Content

### Tier 1: Metrics (automatic)

When you push to `main`/`master`, the `notify-sporeprint.yml` workflow fires a `repository_dispatch` to sporePrint. sporePrint auto-updates `config.toml` with your latest LOC, tests, files, and crates. No human intervention.

**You already have this** if your repo was onboarded (see [ONBOARDING.md](https://github.com/ecoPrimals/sporePrint/blob/main/ONBOARDING.md)).

### Tier 2: Content (PR for review)

To publish markdown pages to primals.eco, create a `sporeprint/` directory in your repo. On push, if your dispatch payload includes `"content": "true"`, sporePrint's CI will extract markdown from `sporeprint/` and create a PR for human review.

```
your-repo/
  sporeprint/
    my-validation-results.md    ← becomes a page on primals.eco
    my-gpu-benchmarks.md        ← another page
```

To enable Tier 2, update your `notify-sporeprint.yml` payload:

```yaml
client-payload: '{"source": "${{ github.event.repository.name }}", "sha": "${{ github.sha }}", "type": "spring", "content": "true"}'
```

---

## Spring Science Hub Pages

Each spring should have a science hub page at `content/lab/springs/<springname>.md` on sporePrint. Four exemplars exist (wetSpring, hotSpring, airSpring, healthSpring). Use them as templates.

### Required Front Matter

```toml
+++
title = "yourSpring — Domain Summary"
description = "One-line description with key numbers"
date = 2026-05-06
weight = 5

[taxonomies]
primals = ["barracuda", "toadstool"]  # primals your spring validates
springs = ["yourspring"]               # always include yourself + connected springs
+++
```

### Recommended Sections

1. **Domain** — one sentence + repository link
2. **The Science Story** — 2-3 paragraphs: what you proved, why it matters
3. **Headline Results** — bullet list of your strongest numbers
4. **Validation Phases** — table of phases with key results
5. **Researchers Reproduced** — table: researcher, department, domain
6. **What the Constraint Revealed** — what eliminating dependencies taught you
7. **Cross-Spring Connections** — how your spring feeds/consumes others
8. **baseCamp Papers** — which papers your spring contributed to

---

## Adding Papers to /science/

baseCamp papers live in `content/science/` on sporePrint. Each paper is a standalone markdown file.

### Front Matter Template

```toml
+++
title = "baseCamp Paper XX — Title"
description = "Brief abstract"
date = 2026-05-06

[taxonomies]
primals = ["barracuda", "toadstool"]
springs = ["wetspring", "hotspring"]
+++
```

### Taxonomy Tagging

**Every page must include taxonomy tags** in its front matter. This is how cross-referencing works on primals.eco:

- `primals = [...]` — lowercase, no spaces: `barracuda`, `toadstool`, `biomeos`, `nestgate`, `songbird`, `rhizocrypt`, `loamspine`, `sweetgrass`, `squirrel`, `coralreef`, `skunkbat`, `petaltongue`, `beardog`, `bingocube`, `sourdough`
- `springs = [...]` — lowercase, no spaces: `airspring`, `groundspring`, `healthspring`, `hotspring`, `ludospring`, `neuralspring`, `primalspring`, `wetspring`

The taxonomy pages (`/primals/barracuda/`, `/springs/wetspring/`) automatically aggregate every page that references them.

---

## Notebook Content — Full Pipeline

Jupyter notebooks are the primary science visibility mechanism. The full
pipeline from notebook to live public page is:

```
your-spring/notebooks/*.ipynb     ← frozen data, matplotlib charts
        │
        ├─ git push to main
        │       └─ notify-sporeprint.yml fires (content: "true")
        │
        ├─ sporePrint auto-refresh.yml (CI)
        │       ├─ clones your repo
        │       ├─ pip install jupyter nbconvert matplotlib numpy
        │       ├─ jupyter nbconvert --execute (runs all cells)
        │       └─ wraps output HTML in Zola front matter
        │
        └─ primals.eco/lab/notebooks/<slug>.md  ← live on the public site
```

### Creating Notebooks (follow the wetSpring pattern)

1. Create `notebooks/` directory in your spring repository
2. Copy wetSpring's `NOTEBOOK_PATTERN.md` for the convention
3. Load frozen data from `../experiments/results/*.json` (relative paths)
4. Use `matplotlib` for charts — **do NOT set `matplotlib.use('Agg')`** (breaks inline rendering)
5. End each notebook with a provenance summary linking to primals.eco

The recommended set (5 notebooks):
- `01-domain-validation.ipynb` — flagship validation story
- `02-benchmark-comparison.ipynb` — Python vs Rust vs GPU
- `03-paper-reproductions.ipynb` — per-researcher evidence
- `04-cross-spring-connections.ipynb` — ecosystem flows
- `05-domain-deep-dive.ipynb` — your most compelling discovery

### Local Rendering

```bash
cd infra/sporePrint
bash scripts/render_notebooks.sh --notebook /path/to/notebook.ipynb
```

### Automated Rendering (CI)

When your dispatch payload includes `"content": "true"`, the auto-refresh
CI will:
1. Clone your repo
2. Install jupyter/matplotlib
3. Execute and render all `notebooks/*.ipynb`
4. Create a PR with the rendered pages

Rendered notebooks appear at `primals.eco/lab/notebooks/<slug>/` with
embedded PNG charts, data tables, and cross-references.

### Live Example

wetSpring's 5 notebooks are live at:
- [16S Pipeline Validation](https://primals.eco/lab/notebooks/01-16s-pipeline-validation/)
- [Python vs Rust vs GPU](https://primals.eco/lab/notebooks/02-benchmark-python-vs-rust/)
- [Paper Reproductions](https://primals.eco/lab/notebooks/03-paper-reproductions/)
- [Cross-Spring Connections](https://primals.eco/lab/notebooks/04-cross-spring-connections/)
- [Soil Anderson Deep Dive](https://primals.eco/lab/notebooks/05-soil-anderson-deep-dive/)

---

## The `sporeprint/` Directory Convention

```
your-repo/
  sporeprint/
    README.md           ← describes what's being published
    validation-summary.md ← validation results page
  notebooks/
    NOTEBOOK_PATTERN.md ← convention docs
    01-validation.ipynb ← loads ../experiments/results/*.json
    02-benchmarks.ipynb
```

Files are placed in sporePrint at paths determined by the auto-refresh CI. The PR created for review lets maintainers adjust placement.

---

## Quick Checklist

- [ ] Repo is onboarded ([ONBOARDING.md](https://github.com/ecoPrimals/sporePrint/blob/main/ONBOARDING.md))
- [ ] `notify-sporeprint.yml` installed with correct `type` (primal/spring/product)
- [ ] `SPOREPRINT_DISPATCH_TOKEN` secret set in your repo
- [ ] Taxonomy tags in all markdown front matter
- [ ] Science hub page created (springs) or entity registry entry present (primals/products)
- [ ] For Tier 2: `sporeprint/` directory created, `content: "true"` in dispatch payload

---

## Reference

- [ONBOARDING.md](https://github.com/ecoPrimals/sporePrint/blob/main/ONBOARDING.md) — CI pipeline setup
- [sporePrint README](https://github.com/ecoPrimals/sporePrint/blob/main/README.md) — auto-refresh architecture
- [SPRING_CATALOG.md](https://primals.eco/architecture/spring-catalog-status-science-and-evolution/) — full spring data
- [Lab](/lab/) — where published results appear
