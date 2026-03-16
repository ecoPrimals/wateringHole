# scyBorg Exception Protocol — Symbiotic Licensing

**Date**: March 16, 2026
**Audience**: All primals, all springs, prospective symbiotic partners
**License**: CC-BY-SA 4.0 (this document), AGPL-3.0 (referenced code)
**Status**: Active
**Companion**: `SCYBORG_PROVENANCE_TRIO_GUIDANCE.md`, `LYSOGENY_PROTOCOL.md`

---

## 1. What Is a Symbiotic Exception?

A **symbiotic exception** is a grant of additional permissions beyond the
default scyBorg license (AGPL-3.0 + ORC + CC-BY-SA 4.0) to a named
organization or project, based on reciprocal benefit.

The default scyBorg license applies to everyone. Exceptions are diplomatic —
they create positive feedback loops between ecoPrimals and organizations
whose tools, hardware, or knowledge benefit the ecosystem. The exception
reduces licensing friction for the partner; the reciprocal relationship
benefits ecoPrimals.

**scyBorg exceptions are not for sale.** They are granted based on symbiotic
value, not payment. This is license-as-diplomacy, not dual licensing for
revenue.

---

## 2. Legal Basis

AGPL-3.0 Section 7 permits **additional permissions** — terms that supplement
the license by making exceptions from one or more of its conditions. As
copyright holder, the author may:

- Grant named organizations permission to use contributions under terms
  other than AGPL-3.0
- Limit the scope of the exception to specific code, projects, or use cases
- Revoke exceptions if the reciprocal relationship ends

**Critical constraint**: Exceptions apply only to code the author owns
copyright for. For forks of upstream AGPL projects, the exception covers
only the author's original contributions, never the upstream code.

---

## 3. Exception Tiers

| Tier | Who | Default License | Exception Grant | Reciprocal Basis |
|------|-----|-----------------|-----------------|------------------|
| **Public** | Everyone | Full scyBorg (AGPL + ORC + CC-BY-SA) | None | Prior art, community, lysogeny |
| **Symbiotic** | Named orgs/projects | Full scyBorg | May incorporate author's contributions under their existing license | Reciprocal benefit (tools, hardware, knowledge) |
| **Reciprocal Open** | Orgs willing to open their work | Full scyBorg | May incorporate under their license | They publish specs/docs/code under AGPL or equivalent copyleft |

### Public Tier (Default)

The entire ecoPrimals ecosystem under scyBorg. No exceptions. Anyone may use,
fork, modify, and redistribute under AGPL-3.0 + ORC + CC-BY-SA 4.0. This is
the constitutional baseline and cannot be weakened.

### Symbiotic Tier

For organizations or projects that provide reciprocal value to ecoPrimals.
The exception allows them to incorporate the author's original contributions
into their project under their existing license terms, without AGPL
obligations on those specific contributions.

The public scyBorg version remains unaffected. Both forks evolve in parallel.

### Reciprocal Open Tier

For organizations willing to publish their own proprietary knowledge under
AGPL or equivalent copyleft. This creates the strongest positive feedback
loop: both parties open their work, both benefit from the other's openness,
and the commons grows.

This tier sets a **precedent**. If a hardware vendor publishes their
architecture documentation under AGPL, they receive an exception to use
ecoPrimals' sovereign implementations however they want. The incentive:
openness earns openness.

---

## 4. Exception Scope

An exception grant specifies:

| Field | Description |
|-------|-------------|
| **Grantee** | Named organization or project |
| **Scope** | Which ecoPrimals code/contributions are covered |
| **Terms** | What the grantee may do (e.g., "incorporate into proprietary products") |
| **Reciprocal basis** | What ecoPrimals receives in return |
| **Duration** | Ongoing while reciprocal relationship persists, or fixed term |
| **Sublicense** | Whether grantee may sublicense to third parties (default: no) |
| **Revocability** | Conditions under which the exception may be revoked |

### What an exception DOES NOT grant:

- Rights to upstream code (only the author's original contributions)
- Rights to relicense the public scyBorg version
- Rights to prevent others from using the public AGPL version
- Rights to the ecoPrimals name, branding, or trademarks
- Exclusivity (the same contribution remains available to everyone under AGPL)

---

## 5. Active and Candidate Exceptions

### Active Exceptions

*None yet. First candidates identified below.*

### Candidate: RustDesk

| Field | Value |
|-------|-------|
| **Project** | RustDesk (open-source remote desktop) |
| **Their license** | AGPL-3.0 |
| **Relationship** | ecoPrimals has used RustDesk as the primary remote access tool to all gates since gen2. Core operational dependency. |
| **Exception scope** | Any ecoPrimals contributions to a RustDesk fork (streamlined primal-ecosystem version) |
| **Exception terms** | RustDesk project may incorporate contributions under their existing AGPL-3.0 license |
| **Reciprocal basis** | RustDesk provides the remote access infrastructure that makes multi-gate development possible. The fork improves their tool. |
| **Notes** | Since RustDesk is already AGPL-3.0, the exception is mostly about removing friction — ensuring contributions flow back cleanly without license ambiguity on new code. Symbiotic: we improve their tool, they get improvements, we get a better tool. |

### Candidate: BrainChip (Akida)

| Field | Value |
|-------|-------|
| **Organization** | BrainChip Inc. |
| **Their license** | Proprietary SDK |
| **Relationship** | ecoPrimals developed rustChip — a pure Rust driver for the AKD1000 NPU — because BrainChip's SDK had platform limitations. 3 Akida NPUs deployed across the metalMatrix. |
| **Exception scope** | rustChip (akida-driver) and related Akida integration code |
| **Exception terms** | BrainChip may incorporate rustChip into proprietary products without AGPL obligations |
| **Reciprocal basis** | BrainChip makes the hardware ecoPrimals uses for neuromorphic workloads. rustChip improves their hardware's accessibility. Potential: dev hardware, technical documentation, direct engineering support. |
| **Notes** | 100% author-owned code (clean-room Rust driver, no SDK code). Full copyright control. Exception benefits BrainChip (production Rust driver they didn't build), benefits ecoPrimals (deeper hardware relationship, potential hardware access). |

### Candidate (Reciprocal Open): GPU Vendor

| Field | Value |
|-------|-------|
| **Organization** | Any GPU vendor (NVIDIA, AMD, Intel) |
| **Their license** | Proprietary |
| **Relationship** | coralReef reverse-engineers GPU architectures to build a sovereign shader compiler |
| **Exception scope** | coralReef compiler and related GPU dispatch code |
| **Exception terms** | Vendor may incorporate sovereign compiler improvements into their toolchain |
| **Reciprocal basis** | Vendor publishes their GPU architecture documentation (ISA encoding, register maps, dispatch protocols) under AGPL-3.0 or equivalent copyleft |
| **Notes** | This is the precedent-setting exception. The incentive structure: if a vendor opens their architecture docs, they get a sovereign compiler implementation for free. The community gets documented hardware. Both forks (proprietary driver + open compiler) co-evolve. The vendor loses nothing (the docs describe hardware they already sold) and gains a Rust-native compiler for their older architectures that they've stopped supporting. |

---

## 6. The Positive Feedback Loop

Each symbiotic exception creates incentive for the next:

```
Author publishes under AGPL (default)
    ↓
Partner provides reciprocal value (tool, hardware, knowledge)
    ↓
Author grants symbiotic exception
    ↓
Partner incorporates improvements freely
    ↓
Partner's product improves
    ↓
ecoPrimals benefits from improved partner product
    ↓
Author publishes more improvements under AGPL
    ↓
Cycle deepens
```

Each successful symbiotic relationship validates the model for the next
potential partner. "BrainChip got an exception and their hardware ecosystem
improved. RustDesk got an exception and their remote desktop improved. The
pattern works."

For the Reciprocal Open tier, the loop is stronger:

```
Author reverse-engineers proprietary system, publishes under AGPL
    ↓
Vendor sees open implementation gaining adoption on orphaned hardware
    ↓
Vendor chooses to engage rather than fight
    ↓
Vendor publishes architecture docs under AGPL (reciprocal open)
    ↓
Author grants exception (vendor can use sovereign compiler in proprietary tools)
    ↓
Open implementation improves (documented architecture > reverse-engineered)
    ↓
Community benefits (documented hardware, open compiler, vendor support)
    ↓
Vendor benefits (Rust-native toolchain for legacy hardware they stopped supporting)
    ↓
Precedent set for next vendor
```

The endgame: a commons where proprietary and open forks co-evolve in parallel,
with the open fork guaranteed to persist (AGPL) and the proprietary fork
incentivized to contribute back (exception conditional on reciprocity).

---

## 7. The Suppression Inversion

Traditional proprietary defense targets three vectors:

| Vector | Traditional Attack | scyBorg + Exception Response |
|--------|--------------------|------------------------------|
| **Legal** | Patent claims, trade secret, copyright on APIs | Lysogeny prior art + independent derivation. AGPL code is the author's original work. ORC protects mechanical interactions. |
| **Platform** | Pressure hosting provider to remove content | No single publisher. Code on sovereign hardware (gates). Git is distributed. No platform to suppress. |
| **Commercial** | Target revenue, employment, partnerships | No revenue to disrupt. No corporate entity to sue. No employer to pressure. Exceptions are grants, not contracts. |

The exception protocol adds a fourth dimension: **diplomatic incentive**. Instead
of pure area denial (lysogeny), exceptions offer a path to cooperation. The
vendor doesn't have to fight or ignore — they can engage and benefit.

This converts adversaries into potential allies. The AGPL ensures the commons
persists regardless. The exception ensures willing partners aren't penalized
for engaging.

---

## 8. What We Own

Nothing.

The code is AGPL — anyone can use it. The mechanics are ORC — unownable by
design. The documentation is CC-BY-SA — freely shareable. The hardware is
physical property, but the knowledge it produces is published.

Knowledge that can't be un-known. Prior art that can't be un-published.
Implementations that can't be un-open-sourced. The value is in the knowledge
being public, not in controlling access to it.

Exceptions don't give something away. They remove friction for allies while
the AGPL default ensures the commons is permanent.

---

## 9. Process for Granting an Exception

1. **Identify reciprocal value**: What does the partner provide to ecoPrimals?
2. **Scope the exception**: Which specific code/contributions are covered?
3. **Verify copyright ownership**: Author must own 100% of the excepted code
   (no upstream AGPL code from other projects)
4. **Draft the grant**: Document grantee, scope, terms, reciprocal basis,
   duration, sublicense rights, revocation conditions
5. **Publish**: Add to the Exception Registry in this document
6. **Notify**: Inform the partner of the grant and its terms
7. **Maintain**: Review annually — does the reciprocal relationship persist?

---

## 10. Exception Registry

*The registry tracks all active symbiotic exceptions. Currently empty — first
exceptions pending formalization with RustDesk and BrainChip.*

| # | Grantee | Scope | Tier | Status | Date |
|---|---------|-------|------|--------|------|
| — | — | — | — | — | — |

---

## References

- `SCYBORG_PROVENANCE_TRIO_GUIDANCE.md` — scyBorg triple license framework
- `LYSOGENY_PROTOCOL.md` — area denial strategy
- `GLOSSARY.md` — ecosystem terminology
- AGPL-3.0 Section 7 (additional permissions): https://www.gnu.org/licenses/agpl-3.0.html#section7
- ORC License: https://azoralaw.com/orclicense/
- CC-BY-SA 4.0: https://creativecommons.org/licenses/by-sa/4.0/
