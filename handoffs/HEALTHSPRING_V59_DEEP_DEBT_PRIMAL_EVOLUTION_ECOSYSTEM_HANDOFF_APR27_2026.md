<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# healthSpring V59 — Deep Debt + Primal Evolution Ecosystem Handoff

**From**: healthSpring V59 (April 27, 2026)
**To**: primalSpring, all primals, all springs, biomeOS
**Scope**: Primal use evolution, composition patterns, upstream asks, gap resolution

---

## Summary

healthSpring (V57→V58→V59) achieved **guideStone Level 5** (first spring),
deployed a **full 8-primal NUCLEUS composition** (18/24 pass), and resolved
**structural debt** (typed enums, clone reduction, capability-first routing,
`ValidationOutcome`). This handoff documents what healthSpring learned about
primal composition, what patterns should be absorbed upstream, and what
gaps remain for primal teams.

---

## 1. healthSpring's Primal Use and Evolution

### Primal Dependency Map (V59)

| Primal | What healthSpring Uses | Wire Status |
|--------|----------------------|-------------|
| **barraCuda** | `stats.mean`, `stats.std_dev`, `stats.variance`, `stats.correlation` via IPC; 12+ library calls; 6 WGSL shaders | **Fully validated** — 4 IPC methods, zero-loss parity |
| **bearDog** | `crypto.sign` (Ed25519), BTSP client module ready | **Validated** — sign works, hash probe schema mismatch (Gap 21) |
| **nestGate** | `storage.store` + `storage.retrieve` round-trip | **Validated** — works when in PRIMAL_LIST |
| **toadStool** | `compute.capabilities`, compute dispatch | **Validated** — 16 cores, distributed coordinator |
| **petalTongue** | Scene push, interaction subscribe, sensor stream | **Validated** — works in server mode, proprioception limited |
| **songbird** | Discovery, capability announcement | **Failed** — crypto provider discovery error (Gap 24) |
| **rhizoCrypt** | `dag.session.create`, `dag.event.append` | **Degraded** — accepts UDS, returns empty (Gap 23) |
| **loamSpine** | `spine.create`, `commit.*` | **Degraded** — same empty response pattern (Gap 23) |
| **sweetGrass** | `braid.create`, `braid.commit` | **Resolved** — EOF-resilient `detect_protocol` + error responses on detection failure (v0.7.27, PG-52) |
| **primalSpring** | Composition framework, guideStone standard, transport, discovery | **Core dependency** — v0.9.17 |

### Evolution Arc

```
V22: healthspring_primal binary (JSON-RPC 2.0 over UDS, 55+ capabilities)
V48: ecoBin harvested (static-PIE x86_64-musl, 2.5 MB → 3.2 MB)
V53: Live IPC parity — science dispatch matches direct Rust calls
V54: healthspring_guidestone — self-validating NUCLEUS node
V55: Three-tier primal proof harness (Tier 1 local, Tier 2 IPC, Tier 3 NUCLEUS)
V56: guideStone Level 4 — 49/49 against live barraCuda
V57: guideStone Level 5 — 57/57 against live NUCLEUS (first spring to reach L5)
V58: Phase 46 full 8-primal composition (18/24), 5 new gaps (23-27)
V59: Deep debt — typed enums, capability-first routing, ValidationOutcome
```

---

## 2. Patterns for Upstream Absorption

### A. Typed Enums for IPC Payloads

**Problem**: Springs and primals use `String` for closed vocabularies (node
types, status values, edge types, clinical statuses). This allows invalid
values, prevents exhaustive matching, and produces runtime errors instead of
compile-time errors.

**healthSpring solution**: Define enums with `#[derive(Serialize, PartialEq)]`
and `#[serde(rename_all = "snake_case")]`. Implement `From<&str>` for backward
compatibility with existing JSON. Use enums in all internal data structures.

**Recommendation**: Any primal or spring with structured response payloads
should adopt this pattern. Particularly relevant for petalTongue (scene types),
toadStool (stage types), and metalForge (topology types).

### B. Capability-Domain Routing (No Primal Self-Knowledge)

**Problem**: Routing tables reference primal names (`"rhizocrypt"`,
`"toadstool"`, `"nestgate"`). This couples the spring to specific primal
identities rather than capabilities.

**healthSpring solution**: Route to capability domains (`"dag"`, `"compute"`,
`"storage"`). `discover_by_capability` resolves the domain to whichever primal
currently advertises it. `NicheDependency.name` is a socket-prefix fallback,
not an identity assertion.

**Recommendation**: All springs should audit their routing for hardcoded primal
names. The capability domain is the primary key; the primal name is a fallback.

### C. Library Code Returns, Doesn't Exit

**Problem**: `process::exit()` in library functions prevents composition —
callers can't catch failures or aggregate results.

**healthSpring solution**: `ValidationHarness::finish()` returns
`ValidationOutcome` with pass/fail/total. Binary wrappers call `.exit()`,
library consumers call `.finish()`.

**Recommendation**: `primalspring::composition` validation helpers should
adopt this pattern. Any shared library that currently calls `process::exit()`
should return a result type instead.

### D. Borrow-Based Data Sharing

**Problem**: When N builders share the same dataset (e.g., x-axis values),
passing `Vec<f64>` requires N clones.

**healthSpring solution**: Helpers accept `&[f64]` and `.to_vec()` once at
the storage boundary. Eliminated ~45 clones.

**Recommendation**: Any primal with builder patterns or test fixtures that
share data should audit for unnecessary cloning.

---

## 3. Composition Patterns for NUCLEUS Deployment

### Shell Composition (primalSpring Phase 46)

```bash
COMPOSITION_NAME=healthspring PRIMAL_LIST="beardog toadstool barracuda \
  rhizocrypt loamspine sweetgrass nestgate petaltongue" \
  ./tools/composition_nucleus.sh start

PATH="$(pwd)/tools:$PATH" ./tools/healthspring_composition_headless.sh
```

### Key Learnings for All Springs

1. **BTSP breaks non-BTSP primals**: Unset `FAMILY_SEED` before any
   `primalspring`-based client connects to non-BTSP primals. Transport
   should probe for BTSP capability before attempting handshake.

2. **Provenance trio — shell composition UDS gap**: rhizoCrypt and
   loamSpine still return empty (Gap 23 open). sweetGrass resolved:
   `detect_protocol` EOF resilience + JSON-RPC error on detection failure
   (PG-52). Shell callers must send `\n`-terminated requests and use
   >=10s read timeouts for domain methods. Domain logic must still
   degrade gracefully for unresolved primals.

3. **socat is not universal**: Use `nc -q 1 -U` as fallback. healthSpring
   provides a shim script.

4. **nestgate must be explicitly added**: Default PRIMAL_LIST omits it.
   Storage tests skip without it.

5. **songbird fails without crypto provider**: Even with beardog running,
   songbird's internal discovery doesn't find it. Compositions work without
   songbird via capability-keyed socket symlinks.

6. **petalTongue server mode has no proprioception**: Scene push and
   interaction work; frame_rate monitoring does not.

---

## 4. Gap Registry (27 Gaps, V59 Current)

### Open Gaps Requiring Upstream Action

| # | Gap | Owner | Priority |
|---|-----|-------|----------|
| 2 | Ionic bridge / bonding policy | BearDog + NestGate | Blocked |
| 3 | Discovery method naming | Songbird | Low (dual fallback) |
| 4 | Inference namespace | Squirrel | Low |
| 9 | Squirrel in deploy graph | Squirrel | Blocked |
| 10 | BTSP server endpoint | BearDog | Medium |
| 20 | **BTSP breaks non-BTSP IPC** | **primalSpring** | **High** |
| 21 | Crypto probe schema | BearDog | Low |
| 22 | **Capability socket discovery** | **Ecosystem** | **Medium** |
| 23 | **Provenance trio empty UDS** | **Trio primals** | **High** |
| 24 | Songbird crypto discovery | Songbird | Medium |
| 25 | petalTongue proprioception | petalTongue | Low |
| 26 | NestGate default PRIMAL_LIST | primalSpring | Low |
| 27 | socat dependency | primalSpring | Low |

### Resolved Gaps

Gaps 1, 5–8, 11–19: All resolved in V48–V57. See `docs/PRIMAL_GAPS.md`
for full details.

---

## 5. healthSpring Current State

| Metric | Value |
|--------|-------|
| Version | V59 |
| guideStone | Level 5 — 57/57, 10 skip |
| NUCLEUS composition | Phase 46 — 18/24, 4 fail, 2 skip |
| Tests | 892 pass, 0 fail, 0 clippy warnings |
| Experiments | 94 (84 science + 11 composition) |
| JSON-RPC capabilities | 84+ (62 science + 22 infrastructure) |
| Python baselines | 54, cross-validation 113/113 |
| ecoBin | 0.9.0 (3.2 MB static-PIE x86_64-musl) |
| primalSpring | v0.9.17 |
| barraCuda | v0.3.12 |
| Unsafe blocks | 0 |
| TODO/FIXME | 0 in production |
| GUIDESTONE_COMPOSITION_STANDARD | v1.2.0 |

---

## 6. What healthSpring Hands Back

### For primalSpring
- `ValidationOutcome` pattern for library composition helpers
- BTSP negotiation requirement (probe before handshake)
- `nestgate` in default PRIMAL_LIST
- socat fallback in `nucleus_composition_lib.sh`
- Capability socket standardization spec

### For barraCuda
- All 4 generic math methods validated end-to-end via IPC
- No open wire gaps (Gap 19 resolved Sprint 44)
- 6 WGSL shaders validated at both CPU and GPU tiers

### For petalTongue
- Synthetic proprioception needed in server mode
- Scene push + interaction subscribe confirmed working headless

### For provenance trio (rhizoCrypt, loamSpine, sweetGrass)
- UDS connections accepted but empty responses returned
- JSON-RPC handler may need startup delay or additional config
- Domain compositions degrade gracefully without provenance

### For songbird
- Crypto provider discovery fails with beardog running
- Document startup dependencies or env vars

### For all springs (airSpring, groundSpring, wetSpring, hotSpring, etc.)
- Typed enum pattern for closed vocabularies
- Capability-domain routing (no primal self-knowledge)
- Borrow-based helpers for shared datasets
- `ValidationOutcome` for library validation code
- Phase 46 composition template is ready — copy `composition_template.sh`,
  fill in 5 domain hooks, get a working NUCLEUS composition
