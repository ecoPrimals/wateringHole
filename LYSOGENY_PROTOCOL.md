# Lysogeny Protocol — Area Denial Through Open Prior Art

**Date**: March 13, 2026
**Audience**: All springs, all primals
**License**: AGPL-3.0-or-later
**Status**: Active — ludoSpring has 6 validated targets (237 checks), model ready for adoption

---

## 1. What Is Lysogeny?

Lysogeny is the ecoPrimals strategy for permanently opening proprietary technology
gates. The protocol applies to any domain — game mechanics, data platforms,
pharmaceutical tools, GPU compute, clinical pipelines, or any system where
proprietary control restricts access to general-purpose mathematics.

The name comes from bacteriophage biology: a lysogenic phage integrates its
genome into the host cell, lies dormant, and when triggered replicates and lyses
the host. Applied to software IP: AGPL-3.0 copyleft integrates into derivatives,
lies dormant until adoption, and when adopted forces openness.

```
identify proprietary gate
    → trace underlying math to published open research (prior art)
    → implement from first principles under AGPL-3.0
    → cross-validate across domains (proves generality, not domain-specific IP)
    → document provenance chain (7 links, see §4)
    → publish and wait
    → adoption lyses the proprietary gate
```

Lysogeny is area denial, not siege. It does not attack existing proprietary
deployments. It contaminates the ground they haven't expanded to yet. Every
prospective customer who finds the open alternative is a customer the proprietary
vendor never acquires.

---

## 2. Three Layers of Protection

Every lysogeny target must establish all three layers. If any layer is missing,
the target is vulnerable to legal challenge.

### Layer 1: Prior Art

The mathematics must exist in published, peer-reviewed literature predating the
proprietary implementation. Every constant, equation, and algorithm must trace
to a specific citation with author, journal, year, and page number. The prior
art establishes that the math is not novel to the proprietary system.

**Standard**: Citation must be to a publication that predates the proprietary
patent filing date (for patented systems) or the proprietary system's first
public release (for trade-secreted systems).

### Layer 2: Cross-Domain Generality

The same mathematics must be validated in at least two distinct domains. This
proves the math is general-purpose — not a specific implementation of the
proprietary system. If the same equation models NPC adaptation in games AND
antibiotic resistance in bacteria, it cannot be claimed as a game-specific
invention.

**Standard**: At least one cross-domain validation experiment with passing
checks in a domain unrelated to the proprietary system's market.

### Layer 3: Independent Derivation

The implementation must derive entirely from published research. No proprietary
code, assets, documentation, APIs, or reverse-engineering is referenced during
implementation. The developer reads the published paper, implements the equation,
and validates against the paper's published results.

**Standard**: Every source file must be traceable to published citations only.
No reference to proprietary implementations in code, comments, or documentation.

---

## 3. The Lysogeny Lifecycle

### Phase 1: Target Identification

Identify a proprietary gate — a technology, algorithm, or system where
proprietary control restricts access.

Questions to answer:
- What capability does the proprietary system provide?
- Is the underlying math published in open literature?
- Does the proprietary system hold patents? If so, what are the filing dates?
- What domains would benefit from open access to this math?

### Phase 2: Prior Art Research

Trace the proprietary system's core algorithms to published research.

Requirements:
- Minimum 3 independent citations per core algorithm
- All citations must predate the proprietary filing/release
- Cross-reference across fields (biology, physics, economics, CS)
- Document the citation chain in a catalog entry (see §5)

### Phase 3: Implementation

Build from the published math only.

Requirements:
- Pure Rust, `#![forbid(unsafe_code)]`
- AGPL-3.0-or-later license header on every file
- Use existing barraCuda primitives where available
- If new math is needed, implement in the spring and document for barraCuda absorption
- hotSpring validation pattern (hardcoded expected values, exit code 0/1)
- All files < 1000 lines
- Zero TODO/FIXME/HACK in source

### Phase 4: Cross-Domain Validation

Validate the same math in at least one unrelated domain.

This is the generality proof. It can be done by:
- The implementing spring (e.g., ludoSpring validates game + biology)
- A partner spring (e.g., wetSpring validates the biology side)
- Both (strongest: independent validation in independent springs)

Requirements:
- Same barraCuda primitive used in both domains
- Vocabulary mapping table (domain A term ↔ domain B term)
- Independent validation checks (not shared test harness)

### Phase 5: Documentation

Complete the provenance chain (§4) and publish.

### Phase 6: Area Denial (Passive)

Once published, the target enters passive area denial. No further action is
required. The AGPL-3.0 license propagates through derivatives. The prior art
documentation weakens patent claims. The cross-domain validation prevents
domain-specific IP arguments. Prospective customers of the proprietary system
who find the open alternative reduce the proprietary vendor's addressable market.

---

## 4. Provenance Chain Requirements

Every lysogeny target must establish all 7 links:

```
1. Published paper (pre-patent) describing the mathematical model
2. barraCuda primitive implementing the model (or spring-local with absorption path)
3. Spring experiment applying the math in the target domain
4. Cross-domain experiment validating the same math in another domain
5. Vocabulary mapping table proving generality
6. AGPL-3.0-or-later license on all code
7. wateringHole documentation (catalog entry + handoff)
```

Links 1-5 establish the three layers of protection. Link 6 is the copyleft
mechanism. Link 7 is the ecosystem coordination.

---

## 5. Catalog Entry Format

Each lysogeny target should have a catalog entry in the implementing spring's
`specs/` directory. Format:

```markdown
## Target N: [Code Name] ([Proprietary System])

**Proprietary gate**: [Description of the proprietary system, patent number if applicable]

### Core Mechanics
- [What the proprietary system does]

### Open Math (Pre-Patent Publication)

| Model | Citation | Year | Contribution |
|-------|----------|------|-------------|
| [model name] | [author, journal, volume:pages] | [year] | [what it provides] |

### Cross-Domain Mapping

| Proprietary Concept | Domain B Equivalent |
|---------------------|---------------------|
| [term in proprietary domain] | [term in validation domain] |

### Alternative Use Case
[Description of how the math serves a non-proprietary domain]

### Experiment
[Path to validation experiment, check count]
```

---

## 6. Domain-Specific Guidance

### For Game Mechanics (ludoSpring)

ludoSpring has validated the protocol with 6 targets:

| Code Name | Proprietary Gate | Checks | Open Math |
|-----------|-----------------|--------|-----------|
| Usurper | WB Nemesis patent | 48 | Replicator dynamics + spatial PD + Lotka-Volterra |
| Integrase | Pokemon capture | 47 | Wright-Fisher + QS threshold + Markov |
| Symbiont | Faction/reputation | 35 | Multi-species Lotka-Volterra |
| Conjugant | Roguelite meta-progression | 40 | HGT + Price equation + Red Queen |
| Quorum | Emergent narrative | 39 | Agent-based + Markov + DAG + QS |
| Pathogen | Gacha (anti-pattern) | 28 | Operant conditioning + prospect theory |

Full catalog: `ludoSpring/specs/LYSOGENY_CATALOG.md`
Strategy handoff: `wateringHole/handoffs/LYSOGENY_CROSS_SPRING_STRATEGY_HANDOFF_MAR13_2026.md`

### For Pharmaceutical Tools (healthSpring)

Targets: proprietary clinical pharmacology software where the underlying
algorithms are published.

| Candidate | Proprietary Gate | Published Math |
|-----------|-----------------|----------------|
| FOCE algorithm | NONMEM (~$50K/seat) | Beal & Sheiner (1982) |
| SAEM algorithm | Monolix | Kuhn & Lavielle (2005) |
| NCA analysis | WinNonlin (Phoenix) | Gabrielsson & Weiner (2001) |
| Hill equation | Various | Hill (1910) |

healthSpring V20 already implements these algorithms. The lysogeny provenance
chain (catalog entry, cross-domain validation, vocabulary mapping) should be
formalized.

### For Data Platforms (wetSpring, biomeOS)

Targets: proprietary ontology/provenance systems where the underlying
computer science is published.

| Candidate | Proprietary Gate | Published Math |
|-----------|-----------------|----------------|
| Knowledge graphs | Palantir Ontology, Neo4j Enterprise | Berners-Lee (2001), RDF (W3C 1999) |
| Entity resolution | Palantir, Informatica | Fellegi & Sunter (1969) |
| Provenance tracking | Various | W3C PROV-O (Moreau & Missier 2013) |
| Graph fraud detection | Proprietary AML/KYC | Already validated: exp065 (74 checks) |

The provenance trio (rhizoCrypt + loamSpine + sweetGrass) already provides
the core primitives. Formalize the lysogeny chain against specific proprietary
systems.

### For GPU Compute (hotSpring, coralReef, toadStool)

Targets: vendor lock-in through proprietary GPU toolchains.

| Candidate | Proprietary Gate | Published Math / Open Standard |
|-----------|-----------------|-------------------------------|
| CUDA lock-in | NVIDIA proprietary | Vulkan (Khronos 2016), WGSL (W3C 2021) |
| cuBLAS/cuFFT | NVIDIA proprietary | BLAS (Lawson et al. 1979), Cooley-Tukey (1965) |
| f64 poisoning | NVIDIA compute-class pricing | IEEE 754 (1985) — f64 is a standard, not a feature |
| Tensor Cores | NVIDIA proprietary API | Matrix multiplication is not patentable math |

The sovereign compute stack (barraCuda + coralReef + toadStool) already
provides the bypass. Formalize the lysogeny chain: document exactly which
NVIDIA capabilities are reimplemented, from which published standards, with
which validation checks.

### For Bioinformatics Pipelines (wetSpring)

Targets: proprietary bioinformatics platforms where the algorithms are
published.

| Candidate | Proprietary Gate | Published Math |
|-----------|-----------------|----------------|
| Galaxy/QIIME2 workflows | Platform lock-in | All underlying algorithms are published |
| 16S pipeline | Proprietary wrappers | DADA2 (Callahan et al. 2016), SILVA, RDP |
| Spectral matching | Proprietary MS software | Cosine similarity (1950s), MassBank (open) |

wetSpring already implements sovereign pipelines. Formalize the lysogeny chain.

---

## 7. The Area Denial Model

Lysogeny is not competitive. It does not target existing customers of
proprietary systems. It operates through passive area denial:

```
                    Proprietary Vendor
                    ┌─────────────────┐
                    │  Existing       │ ← Immune (switching costs,
                    │  Customers      │    embedded engineers,
                    │                 │    institutional trust)
                    └────────┬────────┘
                             │
                     Expansion (new customers,
                     new verticals, new markets)
                             │
                             ▼
               ╔═══════════════════════════╗
               ║  LYSOGENY AREA DENIAL     ║
               ║                           ║
               ║  • AGPL-3.0 alternative   ║
               ║  • Documented prior art   ║
               ║  • Cross-domain proofs    ║
               ║  • Zero cost to adopt     ║
               ║  • Self-propagating       ║
               ╚═══════════════════════════╝
                             │
                    Prospective customers
                    who never enter the
                    proprietary funnel
```

The proprietary vendor does not lose existing customers. They lose future
customers who discover the open alternative before signing a contract.
The deals that never happen are invisible in competitive analysis.

Over time, the addressable market shrinks. The vendor's growth rate declines
relative to what it would have been. The effect compounds as the open
alternative improves (because every adopter contributes back under AGPL-3.0)
while the proprietary system's improvement is limited to paid engineering.

---

## 8. Relationship to scyBorg

scyBorg is the ecoPrimals licensing standard. Every primal, spring, experiment,
tool, and derivative work is licensed under scyBorg. Lysogeny is a strategy
that operates within the scyBorg framework.

```
scyBorg = AGPL-3.0 (code) + ORC (game mechanics) + CC-BY-SA 4.0 (creative content)
```

Lysogeny's AGPL-3.0 copyleft requirement is one layer of scyBorg. The full
standard adds:

- **ORC** (Open RPG Creative): Game rules, stat blocks, progression systems.
  Governed by the Open RPG Creative Foundation (nonprofit). Irrevocable.
- **CC-BY-SA 4.0**: Creative content (art, worlds, narrative, papers, docs).
  Governed by Creative Commons (nonprofit). Attribution + share-alike.

The provenance trio enforces all three layers:
- sweetGrass tracks attribution (BY in CC-BY-SA)
- rhizoCrypt tracks derivation (SA in CC-BY-SA)
- loamSpine issues license certificates (proof that terms apply)

Every lysogeny target inherits scyBorg licensing automatically. The AGPL-3.0
layer is the minimum; ORC and CC-BY-SA apply to any mechanics or creative
content produced during the lysogeny process.

See `SCYBORG_PROVENANCE_TRIO_GUIDANCE.md` for the full licensing standard.

---

## 9. Relationship to skunkBat

skunkBat is the defensive primal. Lysogeny is the defensive strategy.

skunkBat makes the ecoPrimals ecosystem hostile to extraction patterns at
the network and runtime level. Lysogeny makes the ecosystem hostile to
extraction patterns at the intellectual property level. They are complementary:

| Layer | Mechanism | Primal |
|-------|-----------|--------|
| Network defense | Threat detection, graduated response | skunkBat |
| IP defense | Prior art, AGPL copyleft, cross-domain proof | Lysogeny protocol |
| License defense | Triple copyleft, machine-verifiable | scyBorg + provenance trio |
| Economic defense | Radiating attribution, conservation | sunCloud + sweetGrass |

Together, these ensure that the ecosystem resists extraction at every layer:
code can't be closed (AGPL), math can't be patented (prior art), creative
work can't be de-attributed (sweetGrass), and value can't be captured by
platforms (sunCloud).

---

## 10. How to Start

For any spring adopting the lysogeny protocol:

1. **Identify** a proprietary gate in your domain
2. **Research** the published math behind it (minimum 3 citations, pre-patent)
3. **Implement** from published math only, in Pure Rust, under AGPL-3.0
4. **Validate** with hotSpring-pattern checks (hardcoded expected, exit 0/1)
5. **Cross-validate** in at least one other domain (coordinate with another spring)
6. **Document** the catalog entry in your `specs/` directory
7. **Handoff** to wateringHole for ecosystem visibility

The first target is the hardest. After that, the pattern is mechanical.

---

## References

- `ludoSpring/specs/LYSOGENY_CATALOG.md` — 6 validated game mechanic targets
- `wateringHole/handoffs/LYSOGENY_CROSS_SPRING_STRATEGY_HANDOFF_MAR13_2026.md` — cross-spring assignment
- `wateringHole/SCYBORG_PROVENANCE_TRIO_GUIDANCE.md` — triple copyleft framework
- `wateringHole/NOVEL_FERMENT_TRANSCRIPT_GUIDANCE.md` — NFT architecture
- `whitePaper/gen3/baseCamp/20_novel_ferment_transcript_economics.md` — Paper 20
