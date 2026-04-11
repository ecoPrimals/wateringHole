# Spring Audit Prompt — Canonical

**Date**: April 11, 2026
**Version**: v2.0 (Phase 34 — adds primal composition validation layer)
**License**: AGPL-3.0-or-later

---

Use this prompt when spinning up a spring session. Copy the block below.

---

```
Review this Spring's codebase, specs/, docs, and the ecosystem standards at
ecoPrimals/infra/wateringHole/ (especially README.md,
PURE_RUST_SOVEREIGN_STACK_GUIDANCE.md, SCYBORG_PROVENANCE_TRIO_GUIDANCE.md,
ECOBIN_ARCHITECTURE_STANDARD.md, PRIMAL_REGISTRY.md,
SPRING_COMPOSITION_PATTERNS.md, and NUCLEUS_SPRING_ALIGNMENT.md).
Also review sibling springs for handoff patterns and cross-spring conventions.

A Spring is a niche validation domain that proves scientific Python baselines
can be faithfully ported to sovereign Rust+GPU compute using the ecoPrimals
stack, and ultimately composed as primal capability orchestrations via the
NUCLEUS atomic model.

Springs depend on barraCuda (pure math — WGSL shaders, precision strategy)
for all numerical work. They coordinate with toadStool (hardware discovery,
compute orchestration) and coralReef (sovereign shader compiler) via JSON-RPC
IPC. Springs never import other springs — they coordinate through wateringHole
handoffs and shared barraCuda primitives.

The evolution path is:

  Python baseline → Rust validation → barraCuda CPU → barraCuda GPU →
  fused TensorSession pipeline → sovereign dispatch (coralReef native) →
  primal composition (NUCLEUS atomic validation)

The maturity cycle for local GPU code is:

  Write (local WGSL) → Validate → Handoff → barraCuda Absorbs → Lean on upstream

The maturity cycle for primal composition is:

  Wire IPC → Capability discovery → Compose by capability (not name) →
  Validate against proto-nucleate graph → Hand back patterns to primalSpring

Audit against all of the following:

COMPLETION STATUS:
What have we not completed? What mocks, TODOs, FIXMEs, debt, hardcoding
(expected values, tolerance thresholds, data paths, primal names, socket
paths) and gaps remain? Are hardcoded validation targets properly sourced from
documented Python runs with provenance (script, commit, date, exact command)?
Is every experiment traceable?

CODE QUALITY:
Are we passing all linting, fmt, clippy (pedantic+nursery), and doc checks
with zero warnings? Are we as idiomatic and pedantic as possible? What bad
patterns and unsafe code do we have? Target zero unsafe in application code
(#![forbid(unsafe_code)]). Zero #[allow()] in production code. Zero mocks
outside #[cfg(test)]. All files under 1000 LOC. Pure Rust deps only (ecoBin
compliant — zero C dependencies in application code). Zero-copy where possible
(especially I/O parsers — stream, don't buffer).

VALIDATION FIDELITY:
Do ALL Rust results match Python baselines exactly (or within documented,
justified, minimal tolerances)? Is every tolerance named, centralized, and
explained? Are Python baselines still reproducible — rerun and confirm no
baseline drift? Are validation binaries following the hotSpring pattern
(hardcoded expected values, explicit pass/fail, exit 0/1)?

BARRACUDA DEPENDENCY HEALTH:
Are we using barraCuda primitives where they exist (stats, linalg, ops,
dispatch, nn, spectral, nautilus) instead of reinventing? No duplicate math —
if barraCuda has it, delegate to it. Are we on the latest barraCuda version?
Are all local WGSL shaders candidates for upstream absorption
(Write→Absorb→Lean)?

GPU EVOLUTION READINESS:
Which Rust modules are ready for GPU shader promotion (Tier A: direct rewire
to existing barraCuda op, Tier B: adapt existing shader, Tier C: new shader
needed)? What blocks promotion? Document the mapping: Rust module → barraCuda
op / WGSL shader → pipeline stage. Are we using TensorSession for fused
multi-op pipelines where possible?

PRIMAL COMPOSITION READINESS:
Review this spring's proto-nucleate graph at
primalSpring/graphs/downstream/{thisspring}_*_proto_nucleate.toml.
Audit against the composition patterns in
infra/wateringHole/SPRING_COMPOSITION_PATTERNS.md:
- Method normalization: Are all dispatch paths stripping legacy prefixes?
- Capability registration: Are capabilities registered with domain, cost,
  and dependency metadata — not just bare strings?
- Socket discovery: Is primal discovery using the 6-tier search order with
  structured DiscoveryResult (not hardcoded paths)?
- Two-tier dispatch: Is infrastructure routing separated from domain science?
- Niche identity: Does the spring have a niche.rs with CAPABILITIES,
  SEMANTIC_MAPPINGS, and DEPENDENCIES constants?
- Graceful degradation: Does the spring run standalone when primals are absent?
  Does provenance degrade gracefully (available: false, not error)?
- Deploy graph validation: Can the spring validate its proto-nucleate against
  the live NUCLEUS mesh?
- biomeOS feature gate: Is orchestration code behind #[cfg(feature = "biomeos")]
  so lightweight builds stay fast?
Rate each pattern: YES / partial / not started.

TEST COVERAGE:
Target 90%+ line coverage (llvm-cov). Do we have: unit tests (analytical
known-values), integration tests (file parsing round-trips, primal IPC),
validation binaries (baseline comparison with exit codes), and determinism
tests (rerun-identical)? For stochastic algorithms, is the seed fixed and
tolerance justified?

ECOSYSTEM STANDARDS (wateringHole/):
- License: AGPL-3.0-or-later only (SCYBORG trio: AGPL + ORC + CC-BY-SA)
- Architecture: ecoBin compliant (pure Rust, zero C deps, cross-compile)
- IPC: JSON-RPC 2.0 over Unix sockets, capability-based discovery
- Files: all under 1000 LOC, single-responsibility modules
- Data provenance: all datasets from public repositories (SRA, Zenodo, EPA,
  PDB) with documented accession numbers
- Sovereignty: no vendor lock-in, no proprietary dependencies
- Handoffs: wateringHole/handoffs/ follow naming convention
  {SPRING}_{VERSION}_{TOPIC}_HANDOFF_{DATE}.md

PRIMAL COORDINATION:
Are we wired to discover and communicate with relevant primals (toadStool,
Squirrel, petalTongue, biomeOS) via IPC? Is our capability set registered?
Do we have typed IPC clients or MCP tool definitions where appropriate?

Archive code and docs exist for reference and fossil record — ignore them
for this audit. Focus on active production code and current-state docs.
```
