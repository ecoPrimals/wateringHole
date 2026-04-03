# guideStone Standard — Verification Class for Reproducible Artifacts

**Status**: Ecosystem Standard v1.0
**Adopted**: March 31, 2026
**Authority**: WateringHole Consensus
**Compliance**: Recommended for all ecoBins producing verifiable output
**License**: AGPL-3.0-or-later
**Concept Paper**: `whitePaper/gen4/architecture/GUIDESTONE.md`

---

## Purpose

This standard defines **guideStone**: the verification class for ecoBins that
produce reproducible, self-proving output. Where the binary ladder describes
structure (UniBin → ecoBin → genomeBin) and deployment classes describe context
(NUCLEUS → Niche → fieldMouse), guideStone describes **what the output means** —
that the computation's results are their own proof of correctness.

guideStone is not a primal. It is not a binary type. It is not a deployment
class. It is a **quality certification** — an orthogonal dimension that any
ecoBin can carry when its output meets the five properties defined below.

---

## The Three Axes

```
Structure (what is it built from?):     UniBin → ecoBin → genomeBin
Deployment (where does it run?):        NUCLEUS → Niche → fieldMouse
Verification (what does its output mean?):  guideStone
```

These axes are independent. A fieldMouse sensor can be a guideStone. A full
NUCLEUS can produce output that is not guideStone. The classification depends
on the rigor of the output, not the scale of the deployment.

---

## The Five Properties

A guideStone-certified artifact satisfies all five properties. Each is
necessary. Together they are sufficient.

### 1. Deterministic Output

Same input, same binary, any hardware → same output within named tolerances.

- The binary detects its substrate at runtime (CPU architecture, GPU
  availability, memory) and adapts execution path accordingly
- The mathematical result is invariant across substrates
- Bitwise identity is not required — floating-point deviations across
  architectures are acceptable when bounded by a named tolerance with a
  derivation (see Property 5)
- The phrase "works on my machine" is disqualifying

### 2. Reference-Traceable

Every numeric claim in the output traces to a verifiable source.

Acceptable sources:

| Source Type | Example |
|-------------|---------|
| Published paper | Bazavov & Chuna, arXiv:2101.05320 |
| International standard | ILDG/QCDml 2.0, FAO-56, DADA2 |
| Physical constant | CODATA 2018, PDG 2024 |
| Mathematical proof | Strong-coupling expansion, spectral theorem |
| NIST test vectors | FIPS 186-5 Ed25519, AES-256-GCM |
| Calibration standard | NIST-traceable pH buffer, certified reference material |

Numbers that "float in space" — computed values with no traceable origin —
are not guideStone-grade.

### 3. Self-Verifying

The artifact carries its own integrity mechanism.

| Mechanism | When |
|-----------|------|
| SHA-256 CHECKSUMS file | Artifact directory (pre-execution) |
| CRC32 or ILDG CRC on data payloads | Per-record or per-file |
| Merkle root (when provenance trio is wired) | Per-session |
| Ed25519 signature (when bearDog is available) | Per-vertex or per-certificate |

The consumer does not need to trust the transfer channel. The artifact
proves it arrived intact. The minimum requirement is a CHECKSUMS file
validated before execution — the same mechanism the External Validation
Artifact Standard already requires.

### 4. Environment-Agnostic

No hardcoded paths. No "install X first." No platform assumptions.

| Requirement | Rationale |
|-------------|-----------|
| ecoBin compliant | Pure Rust, static musl, cross-arch |
| No external dependencies at runtime | No package managers, no downloads |
| No sudo | Runs in user space |
| No GPU required | CPU-only path must produce the same mathematical result |
| No network required | Fully offline operation |
| Runtime substrate detection | The binary tells the user what it found, not the other way around |

This is the External Validation Artifact Standard's portability
requirement, generalized to any ecoBin.

### 5. Tolerance-Documented

No magic numbers. Every threshold has a derivation.

```json
{
  "name": "chiral_condensate_4x4x4x8",
  "measured": 0.0847,
  "threshold": 0.01,
  "comparison": "absolute_error",
  "tolerance_justification": "stochastic estimator with 50 noise vectors; error bounded by 1/sqrt(N_noise) * lattice_volume",
  "paper": "Bazavov et al., Phys. Rev. D 85, 054503 (2012)"
}
```

The derivation must be:

- **Physical or mathematical** — derived from the computation's error model
- **Documented in the output metadata** — not in a code comment
- **Auditable** — a domain expert reads the justification and can verify
  whether the tolerance is meaningful

A tolerance chosen because "the test passes at this value" is not
guideStone-grade. A tolerance derived from finite-size scaling, stochastic
noise bounds, or instrument precision specifications is.

---

## guideStone by Domain

### Spring guideStone

A spring guideStone is the External Validation Artifact with guideStone
certification. The `validation/` directory, `./run`, static musl binaries,
`expected/` reference data, JSON output with named tolerances — all of that
is already defined by the Validation Artifact Standard. guideStone adds
the explicit requirement that tolerances are derived, not tuned.

| Spring | guideStone Artifact | Key Outputs |
|--------|--------------------|----|
| hotSpring | Chuna Engine (6 binaries) | ILDG gauge configurations, QCDml metadata, gradient flow observables |
| airSpring | FAO-56 validation suite | ET₀ with R²=0.967 across 918 station-days, soil hydrology |
| wetSpring | Sovereign 16S pipeline | Taxonomic assignments, GPU spectral matching at 1,077x |
| groundSpring | Uncertainty validation | Cross-domain noise characterization, 236 checks |
| neuralSpring | ML primitive validation | PINN, DeepONet, fused pipeline benchmarks |
| healthSpring | PK/PD validation | Pharmacokinetic models, microbiome dynamics |

### Primal guideStone

A primal guideStone is the **reference edition** — the pinned, fully
auditable version where every internal operation is validated against
external test vectors or mathematical proofs.

| Primal | guideStone Contents | Validation Source |
|--------|--------------------|----|
| bearDog | Cryptographic reference — Ed25519, X25519, AES-256-GCM, BLAKE3 test vectors | NIST FIPS, RFC 8032, RFC 7748 |
| barraCuda | Shader math corpus — every `assert_shader_math!` with f32/DF64/f64 precision tiers | NumPy baselines, analytical solutions |
| coralReef | Compiler validation — WGSL → SASS output matches reference binaries | NVIDIA ISA documentation, instruction-level verification |

A primal guideStone is what allows third parties to audit the plumbing.
bearDog's guideStone means: when someone creates their own ephemeral
seed through the `PrimalBridge`, they can trace every step against the
reference edition's documented outputs. The cryptography is not a black
box.

### Composition guideStone

A composition guideStone certifies an end-to-end pipeline built from
multiple primals and/or springs.

| Composition | guideStone Scope | What It Proves |
|-------------|-----|-----|
| Chuna Engine (hotSpring) | Generate → flow → measure → convert pipeline | ILDG-compatible data with full QCDml provenance |
| helixVision (wetSpring) | Sequencer → basecall → assembly → variant call | Reproducible genomics from raw reads |
| esotericWebb (ludoSpring) | Player action → enrichment → provenance → NFT | Creative events with verifiable DAG provenance |

The composition guideStone is the gen4-specific case: when primals
disappear into the product, the guideStone is what makes the product's
output trustworthy.

---

## Certification Process

### Self-Certification

guideStone is self-certified. There is no committee, no review board, no
approval queue. The artifact either satisfies the five properties or it
does not. The certification is auditable by anyone who runs the binary.

This follows the Sovereign Science principle: credentials are tools, not
authorities. The guideStone does not derive its validity from who
certified it. It derives its validity from the reproducibility of its
output.

### Certification Checklist

```
## guideStone Certification — <Artifact> <Version>

### Property 1: Deterministic Output
- [ ] Same binary produces same results on x86_64 and aarch64
- [ ] CPU-only and GPU paths produce results within named tolerances
- [ ] No environment-dependent behavior (locale, timezone, hostname)
- [ ] Tested on at least two distinct hardware configurations

### Property 2: Reference-Traceable
- [ ] Every numeric output traces to a paper, standard, constant, or proof
- [ ] References are machine-readable in output metadata (not just comments)
- [ ] No "orphan" numbers — every value has provenance

### Property 3: Self-Verifying
- [ ] CHECKSUMS file present and validated before execution
- [ ] Data payloads carry integrity (CRC, hash, or signature)
- [ ] Tampered input is detected and reported (not silently accepted)

### Property 4: Environment-Agnostic
- [ ] ecoBin compliant (Pure Rust, static musl, cross-arch)
- [ ] No runtime dependencies (no downloads, no package managers)
- [ ] No sudo required
- [ ] CPU-only mode covers full output (not a subset)
- [ ] No hardcoded paths or platform assumptions
- [ ] Binary reports detected substrate to the user

### Property 5: Tolerance-Documented
- [ ] Every tolerance has a derivation in the output metadata
- [ ] Derivation is physical/mathematical, not empirical ("test passes")
- [ ] A domain expert can audit the tolerance justification
- [ ] No magic numbers
```

---

## Naming Convention

guideStone artifacts follow the ecosystem's `camelCase` convention:

```
<artifact>-guideStone-<version>
```

Examples:

- `hotSpring-guideStone-v0.7.0` — Chuna Engine validation artifact
- `bearDog-guideStone-v0.9.0` — Cryptographic reference edition
- `helixVision-guideStone-v1.0.0` — Sovereign genomics pipeline
- `esotericWebb-guideStone-v4.0.0` — Creative provenance build

The `-guideStone-` infix identifies the artifact as guideStone-certified
in plasmidBin manifests, GitHub Releases, and provenance chains.

---

## Relationship to Other Standards

| Standard | Relationship |
|----------|-------------|
| **ecoBin** | A guideStone IS an ecoBin — Pure Rust, static musl, cross-arch. guideStone adds output quality requirements |
| **External Validation Artifact** | A spring's validation artifact is a specific kind of guideStone. guideStone generalizes the pattern to any ecoBin |
| **genomeBin** | guideStone does not require genomeBin (deployment wrappers). A bare ecoBin with guideStone properties is sufficient |
| **fieldMouse** | A fieldMouse can be a guideStone — if its sensor readings meet the five properties (calibrated, traceable, self-verifying) |
| **plasmidBin** | guideStone artifacts are distributed via plasmidBin with the `-guideStone-` infix in their release naming |
| **scyBorg** | guideStone artifacts are AGPL-3.0-or-later. The verification is open. Anyone can audit |
| **Provenance Trio** | Complementary. guideStone certifies the computation. The trio certifies the event (who, when, where). Both together produce a Novel Ferment Transcript |
| **Anchoring Pipeline** | guideStone output + trio provenance → BTC/ETH-anchored proof. The guideStone is the content; the anchor is the timestamp |
| **Novel Ferment Transcript** | A guideStone-backed NFT is the highest-grade digital artifact in the ecosystem: reproducible computation + attributed provenance + public chain anchor |

---

## What guideStone Is NOT

- **Not a primal** — it is a verification class
- **Not a binary type** — ecoBin is the binary type; guideStone is a quality grade on top
- **Not a deployment class** — fieldMouse is a deployment class; guideStone is orthogonal
- **Not required** — exploratory computation, prototypes, and development builds are not guideStone
- **Not a committee** — certification is self-assessed and publicly auditable
- **Not blockchain-dependent** — guideStone works offline with no trio, no anchoring
- **Not science-specific** — applies to cryptographic references, creative provenance, and any domain with verifiable output

---

## Evolution Path

guideStone artifacts evolve along the composition axis:

```
Bare guideStone (reproducible output, offline, no provenance)
  → + bearDog signing (integrity, identity)
  → + rhizoCrypt DAG (full computation trace)
  → + loamSpine certificate (permanent record)
  → + sweetGrass braid (attribution)
  → + BTC/ETH anchor (public chain proof)
  = Novel Ferment Transcript (full sovereign science stack)
```

Each layer is additive. A guideStone at the bottom of this stack is
useful — it produces reproducible output. A guideStone at the top is
a permanently anchored, attributed, self-proving digital fact.

---

*The artifact proves itself. The output is the review. The computation
is the credential. guideStone is how ecoPrimals transfers sovereignty
from the producer to the consumer.*
