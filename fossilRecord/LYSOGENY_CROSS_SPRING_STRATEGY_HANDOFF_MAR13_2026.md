# Lysogeny — Cross-Spring Open Recreation Strategy

**Date**: March 13, 2026
**From**: ludoSpring V11
**To**: All springs, toadStool, barraCuda, neuralSpring, wetSpring, healthSpring, airSpring
**License**: AGPL-3.0-or-later
**Status**: 6 lysogeny targets implemented, 237 validation checks, 0 failures

---

## 1. What Is Lysogeny?

Lysogeny is the ecoPrimals strategy for openly recreating proprietary game
mechanics from published scientific math, cross-validating across biology and
ecology, and releasing under AGPL-3.0 copyleft.

The name comes from bacteriophage biology: a lysogenic phage integrates its
genome into the host cell, lies dormant as a prophage, and when triggered
replicates and lyses the host — bursting out as copies.

Applied to software IP:

```
identify proprietary mechanic
    → trace the underlying math to published open research (prior art)
    → recreate from first principles under AGPL-3.0
    → cross-validate: same math works in biology/ecology (proves generality)
    → AGPL-3.0 copyleft = lysogeny (infects derivatives, forces open)
    → adoption lyses the proprietary gate
```

### Three Layers of Protection

1. **Prior art**: The math existed in ecology/population biology before the game
   mechanic was patented or trade-secreted.
2. **Cross-domain utility**: The same math works in microbial ecology, population
   genetics, and clinical science — proving it is general mathematics.
3. **Independent derivation**: Every constant and equation traces to a published
   paper with citation — never reverse-engineered from proprietary code.

---

## 2. The 6 Targets

| Code Name | Game Mechanic | Experiment | Checks | Open Math |
|-----------|--------------|------------|--------|-----------|
| **Usurper** | Nemesis System (WB patent) | exp055 | 48 | Replicator dynamics + spatial PD + Lotka-Volterra with memory |
| **Integrase** | Capture/bonding (Pokemon) | exp056 | 47 | Wright-Fisher fixation + QS threshold + Markov chains |
| **Symbiont** | Faction/reputation | exp057 | 35 | Multi-species Lotka-Volterra + frequency-dependent fitness |
| **Conjugant** | Roguelite meta-progression | exp058 | 40 | HGT + Wright-Fisher + Price equation + Red Queen |
| **Quorum** | Emergent procedural narrative | exp059 | 39 | Agent-based modeling + Markov + DAG causality + QS threshold |
| **Pathogen** | Gacha/lootbox (anti-pattern) | exp060 | 28 | Operant conditioning + prospect theory + parasitism |

All targets use biological names from the phage lifecycle / microbial ecology.

---

## 3. Existing `barraCuda` Math Wired

These validated primitives are already implemented and were used or referenced
by the lysogeny experiments:

| Primitive | Location | Used By |
|-----------|----------|---------|
| Lotka-Volterra ODE (RK45) | `barraCuda/src/numerical/rk45.rs` | Usurper, Symbiont, Conjugant |
| Wright-Fisher (f32 GPU) | `barraCuda/src/ops/wright_fisher_f32.rs` | Integrase, Conjugant |
| Spatial PD (WGSL shader) | `barraCuda/src/ops/bio/spatial_payoff.rs` | Usurper, Symbiont |
| Replicator dynamics | `neuralSpring/src/game_theory.rs` | Usurper |
| Cooperation/cheater ODE | `wetSpring/barracuda/src/bio/cooperation.rs` | Usurper |
| QS threshold dynamics | `wetSpring/barracuda/src/bio/qs_biofilm.rs` | Integrase, Quorum |
| Competitive exclusion | `neuralSpring/src/eco_dynamics.rs` | Integrase, Symbiont |
| Phage defense ODE | `barraCuda/src/numerical/ode_bio/systems.rs` | Integrase |

---

## 4. Cross-Spring Validation Assignments

Each target needs a science spring experiment that validates the same math in
a biological context. This creates the cross-domain proof of generality.

| Target | wetSpring | neuralSpring | healthSpring | airSpring |
|--------|-----------|-------------|-------------|-----------|
| Usurper | Antibiotic resistance populations | Evolutionary game theory | — | — |
| Integrase | Phage lysogeny / MOI dynamics | — | — | — |
| Symbiont | Microbiome community assembly | Multi-agent cooperation | — | Soil microbiome |
| Conjugant | HGT / LTEE mutation accumulation | — | — | Cover crop meta-progression |
| Quorum | QS biofilm formation narrative | — | Patient journey narrative | — |
| Pathogen | — | Reward prediction error | Addiction modeling | — |

### What Each Spring Needs To Do

Each cross-spring validation experiment should:

1. Take the same mathematical model used in the ludoSpring game experiment
2. Apply it to a biological/ecological/clinical domain
3. Validate against published experimental data from that domain
4. Document the vocabulary mapping (game term ↔ biology term)
5. Use the same `barraCuda` primitive — proving the math is identical

The cross-spring experiment does NOT need to know about the game mechanic. It
is a standalone biology/ecology validation that happens to use the same math.

---

## 5. Provenance Chain Requirements

Every lysogeny target must establish all 7 links:

```
1. Published paper (pre-patent) describing the mathematical model
2. barraCuda primitive implementing the model
3. ludoSpring experiment applying it as game mechanic         ← DONE (exp055-060)
4. Science spring experiment validating same math in biology  ← ASSIGNED (see §4)
5. Cross-domain mapping table proving generality              ← DONE (in catalog)
6. AGPL-3.0-or-later license on all code                     ← DONE
7. wateringHole handoff documenting the full chain            ← THIS DOCUMENT
```

---

## 6. Key Citations (Pre-Patent Prior Art)

All math used predates the proprietary implementations:

| Model | Citation | Year |
|-------|----------|------|
| Lotka-Volterra predator-prey | Lotka 1925, Volterra 1926 | 1925 |
| Frequency-dependent selection | Fisher 1930 | 1930 |
| Wright-Fisher drift | Wright 1931 | 1931 |
| Competitive exclusion | Gause 1934 | 1934 |
| Operant conditioning | Skinner 1938 | 1938 |
| Bacterial conjugation | Lederberg & Tatum 1946 | 1946 |
| Price equation | Price 1970 | 1970 |
| Schelling segregation | Schelling 1971 | 1971 |
| Red Queen hypothesis | Van Valen 1973 | 1973 |
| Replicator dynamics | Taylor & Jonker 1978 | 1978 |
| Quorum sensing | Nealson & Hastings 1979 | 1979 |
| Prospect theory | Kahneman & Tversky 1979 | 1979 |
| Evolutionary stable strategies | Maynard Smith 1982 | 1982 |
| Self-organized criticality | Bak et al. 1987 | 1987 |
| LTEE | Lenski et al. 1991 | 1991 |
| Spatial prisoner's dilemma | Nowak & May 1992 | 1992 |
| Causal inference | Pearl 2000 | 2000 |
| Mutualism-parasitism spectrum | Bronstein 2001 | 2001 |
| Persister cells | Balaban et al. 2004 | 2004 |
| Addiction modeling | Redish 2004 | 2004 |
| QS threshold dynamics | Waters & Bassler 2005 | 2005 |

---

## 7. `barraCuda` / `toadStool` Action Items

### GPU Promotion Candidates

Several lysogeny targets are batched-computation-heavy and ready for GPU:

| Target | GPU Workload | Priority |
|--------|-------------|----------|
| Usurper | Replicator dynamics over large NPC populations | High |
| Integrase | Wright-Fisher capture probability (already on GPU) | Ready |
| Symbiont | Multi-species LV step over faction networks | Medium |
| Conjugant | Wright-Fisher fixation + Price equation batch | Medium |
| Quorum | Agent-based model step over large agent grids | High |
| Pathogen | Prospect theory batch evaluation | Low |

### New Primitives Needed

1. **Replicator dynamics GPU shader** — vectorized `dx_i/dt = x_i * (f_i - f_bar)`
   for large populations. The spatial PD shader exists; extend to general
   replicator dynamics.
2. **Multi-species Lotka-Volterra GPU** — extend the single-species LV to
   N-species competition with interaction matrix.
3. **Agent-based model step shader** — Schelling-style grid update for Quorum.
4. **Markov chain GPU** — batched state transition for evolution chains and
   narrative event generation.

### Integration Pattern

Lysogeny experiments currently self-contain their math for validation
independence. When `barraCuda` absorbs these as primitives, the experiments
should be updated to import from `barraCuda` instead of re-implementing.
This is the standard `ludoSpring` → `barraCuda` promotion path.

---

## 8. Files of Interest

### Catalog

- `ludoSpring/specs/LYSOGENY_CATALOG.md` — full mapping of all 6 targets with
  citations, cross-domain tables, and alternative use cases

### Experiments

- `ludoSpring/experiments/exp055_usurper/` — Nemesis system (48 checks)
- `ludoSpring/experiments/exp056_integrase/` — Capture mechanics (47 checks)
- `ludoSpring/experiments/exp057_symbiont/` — Faction reputation (35 checks)
- `ludoSpring/experiments/exp058_conjugant/` — Roguelite meta-progression (40 checks)
- `ludoSpring/experiments/exp059_quorum/` — Emergent narrative (39 checks)
- `ludoSpring/experiments/exp060_pathogen/` — Gacha anti-pattern (28 checks)

### Related Plan

- `.cursor/plans/lysogeny_game_mechanics_ae59fb78.plan.md` — strategic plan

---

## 9. Quality Gates

All lysogeny experiments meet wateringHole standards:

- `#![forbid(unsafe_code)]` — zero unsafe
- `cargo clippy --pedantic --nursery` — zero warnings
- `cargo fmt` — formatted
- All files < 1000 lines
- No TODO/FIXME/HACK in code
- AGPL-3.0-or-later license
- hotSpring validation pattern (hardcoded expected values, exit code 0/1)
- 237 validation checks, 0 failures
