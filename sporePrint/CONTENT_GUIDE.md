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

## Notebook Content

To publish Jupyter notebooks:

1. Place `.ipynb` files in the shared workspace (`/shared/abg/showcase/`) or your repo's `sporeprint/` directory
2. The `render_notebooks.sh` pipeline converts them to static HTML
3. Rendered content goes under `/lab/` on primals.eco
4. Provenance metadata is preserved in the rendered output

---

## The `sporeprint/` Directory Convention

```
your-repo/
  sporeprint/
    README.md           ← optional: describes what's being published
    validation.md       ← validation results page
    benchmarks.md       ← performance benchmarks
    notebooks/          ← Jupyter notebooks for rendering
      analysis.ipynb
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
