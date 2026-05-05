# Spring Audit Prompt — Canonical

**Date**: April 13, 2026
**Version**: v2.3 (Phase 40 — adds Level 5 Composition Validation, NUCLEUS Complete)
**License**: AGPL-3.0-or-later

---

Use this prompt when spinning up a spring session. Copy the block below.

---

```
Review this Spring's codebase, specs/, docs, and the ecosystem standards at
ecoPrimals/infra/wateringHole/ (especially README.md,
ECOSYSTEM_EVOLUTION_CYCLE.md, PURE_RUST_SOVEREIGN_STACK_GUIDANCE.md,
SCYBORG_PROVENANCE_TRIO_GUIDANCE.md, ECOBIN_ARCHITECTURE_STANDARD.md,
PRIMAL_REGISTRY.md, SPRING_COMPOSITION_PATTERNS.md,
NUCLEUS_SPRING_ALIGNMENT.md, and SPRING_AUDIT_PROMPT.md).
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

  Paper → Python baseline → Rust validation → barraCuda CPU → barraCuda GPU →
  (spring Rust math evolves upstream primals, then retires as fossil record) →
  primal composition (NUCLEUS atomic validation via IPC — no spring binary)

At each stage, the spring's local code drives primal evolution. Once primals
absorb the math, the spring validates via composition: call primals through
IPC, compare results against original Python baselines. Springs do NOT ship
binaries at the composition level. Gardens (esotericWebb) are the final
downstream — pure compositions of primals via biomeOS, graph-as-product.

THE WATER CYCLE (see ECOSYSTEM_EVOLUTION_CYCLE.md for full detail):
The ecosystem evolves like a water cycle. Primals are mountains — their
capabilities melt down as IPC endpoints. primalSpring validates compositions.
Domain springs (delta) absorb validated patterns and discover gaps. Gaps
evaporate back up through primalSpring to primal teams. As of April 13, 2026, NUCLEUS is COMPLETE: 12/12 primals ALIVE, 19/19
exp094 composition parity PASS, all LD gaps RESOLVED. The current season
is SPRING: domain springs should now elevate from Rust math to primal
composition validation using primalspring::composition.

The maturity cycle for local GPU code is:

  Write (local WGSL) → Validate → Handoff → barraCuda Absorbs → Lean on upstream

The maturity cycle for primal composition is:

  Wire IPC → Capability discovery → Compose by capability (not name) →
  Validate parity (primalspring::composition::validate_parity) →
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
- Dependency governance: Does the spring have a `deny.toml` that bans C/FFI
  deps (openssl-sys, ring, aws-lc-sys, native-tls)? Is `cargo deny check`
  enforced in CI?
- Inference namespace: Do IPC methods use `inference.*` (canonical) rather than
  `ai.*` or `model.*` for inference operations?
- Composition parity: Does the spring use primalspring::composition to validate
  that domain math produces the same results via primal IPC as it does locally?
  Does it use named tolerances from primalspring::tolerances?
Rate each pattern: YES / partial / not started.

LEVEL 5: COMPOSITION VALIDATION (new — Phase 40):
NUCLEUS is now complete. 12/12 primals are ALIVE with stable wire contracts.
Springs can now validate that primal-orchestrated IPC produces the same
results as local Rust math. This is the final maturity level.

- CompositionContext: Does the spring create a CompositionContext via
  `CompositionContext::from_live_discovery()`? This discovers all running
  NUCLEUS primals by scanning UDS sockets.
- validate_parity: Does the spring call `validate_parity()` with:
  - capability-based addressing (e.g. "tensor", not "barracuda")
  - actual wire methods (stats.mean, storage.store, crypto.hash — NOT
    aspirational methods like tensor.attention)
  - named tolerances from primalspring::tolerances
  - Python baseline values with documented provenance
- Wire method awareness: Does the spring use actual live wire methods?
  Key methods: stats.mean (barraCuda), storage.store/storage.retrieve
  (NestGate), crypto.hash (BearDog, returns base64), ipc.resolve
  (Songbird, returns native_endpoint/virtual_endpoint),
  shader.compile.capabilities (coralReef).
  Note: tensor.matmul requires session-based tensor IDs (tensor.create
  first) — use stats.mean for inline-data parity checks.
- Transport mismatch handling: Does the spring handle
  IpcError::is_transport_mismatch() gracefully (SKIP, not FAIL)?
  Some primals use tarpc on their UDS sockets alongside JSON-RPC.
- Phase 5 registry seeding: Does the spring's launcher seed Songbird's
  registry via ipc.register for its primals? Does it use ipc.resolve
  for capability-based endpoint discovery?
- exp094 reference: Has the spring created its own composition parity
  experiment modeled on primalSpring/experiments/exp094_composition_parity/?
  The 19 check pattern (Tower + Node + Nest + Cross-Atomic) is the template.

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
