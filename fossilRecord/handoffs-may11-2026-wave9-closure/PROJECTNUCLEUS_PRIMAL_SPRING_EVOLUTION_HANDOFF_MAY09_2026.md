# projectNUCLEUS → Primal & Spring Teams: Evolution Handoff

**Date**: 2026-05-09
**From**: projectNUCLEUS (sporeGarden)
**For**: All primal teams, all spring teams, primalSpring coordination
**Context**: Post-interstadial, deep debt swept, sovereign hosting live

---

## Purpose

This handoff captures everything projectNUCLEUS learned while deploying,
validating, hardening, and evolving a full 13-primal NUCLEUS composition on
real hardware under real external load. It is structured for absorption by
primal teams (who build the components) and spring teams (who compose them).

---

## 1. NUCLEUS Composition — What We Proved

### The composition works

13 primals composed on a single gate (i9-14900K, 96 GB DDR5, RTX 4070/3090).
All primals healthy, all ports on `127.0.0.1`, MethodGate enforced on 10/13
(remaining 3 are BTSP-gated or IPC-only — correct behavior). 175 security
checks PASS, 0 FAIL. Full provenance pipeline operational (BLAKE3 → rhizoCrypt
DAG → loamSpine ledger → sweetGrass braid).

### Composition patterns validated on real hardware

| Pattern | Evidence | Applicable to |
|---------|----------|---------------|
| Deploy graph germination | BearDog first → rest in dependency order → biomeOS last | Any multi-primal deployment |
| `composition.reload` hot-swap | Single primal restarts without tearing down composition | Live production gates |
| Resource envelope enforcement | biomeOS v3.48 + ToadStool S232: `timeout_ms`, `mem_mb`, `cpu_cores` | All dispatch paths |
| 5-tier discovery | Songbird IPC → Neural API → UDS → socket registry → TCP | Any primal needing to find another |
| MethodGate + ionic tokens | Ed25519 bearer, scope-checked, expiry-verified, JTI replay prevention | All external-facing primals |
| Open/gated access split | Voila (open, anonymous) ← pappusCast ← JupyterHub (authenticated) | Any public science surface |
| Snapshot propagation | Validated copies, not live symlinks; quarantine on failure | Any content pipeline |
| Python → Rust → primal evolution | darkforest (bash→Rust), pappusCast (Python, Rust planned) | New tooling across ecosystem |
| Cloudflare as calibration instrument | Hourly baselines (TTFB, TLS, DNS); primal must meet or exceed before cutover | Sovereignty replacements |

### The 14 primal ports (post-deep-debt-sweep)

All port assignments now resolve from environment variables with compiled
fallback defaults. Any deployer can override via `nucleus_config.sh`:

| Primal | Port | Env Var |
|--------|------|---------|
| beardog | 9100 | `BEARDOG_PORT` |
| songbird | 9200 | `SONGBIRD_PORT` |
| toadstool | 9300 | `TOADSTOOL_PORT` |
| toadstool-rpc | 9301 | `TOADSTOOL_RPC_PORT` |
| barracuda | 9400 | `BARRACUDA_PORT` |
| coralreef | 9500 | `CORALREEF_PORT` |
| nestgate | 9600 | `NESTGATE_PORT` |
| rhizocrypt | 9601 | `RHIZOCRYPT_PORT` |
| rhizocrypt-rpc | 9602 | `RHIZOCRYPT_RPC_PORT` |
| loamspine | 9700 | `LOAMSPINE_PORT` |
| sweetgrass | 9850 | `SWEETGRASS_PORT` |
| squirrel | 9800 | `SQUIRREL_PORT` |
| skunkbat | 9900 | `SKUNKBAT_PORT` |
| petaltongue | 9901 | `PETALTONGUE_PORT` |

---

## 2. neuralAPI Deployment from biomeOS

### Current model (what's live)

```
deploy.sh → systemd user services → per-primal env vars → health check polling
```

This works but is gate-local and imperative. biomeOS discovers running primals
via the 5-tier hierarchy after they're already started.

### Target model (neuralAPI-driven)

```
biomeOS → Neural API → composition.deploy(graph) → germinate primals → wire capabilities
```

The deploy graph (TOML DAG) becomes the deployment contract. biomeOS reads the
graph, germinates primals in dependency order, waits for health, and wires
capability routes.

### What's validated vs what's still needed

| Piece | Status |
|-------|--------|
| Deploy graph format and structural validation | Validated (guidestone) |
| Germination ordering (Tower first) | Validated (systemd dependency model) |
| `composition.reload` single-primal hot-swap | Validated (biomeOS v3.48) |
| Resource envelope enforcement on dispatch | Validated (ToadStool S232) |
| Neural API semantic routing (170+ translations) | Validated (biomeOS routes capability queries) |
| `composition.deploy(graph)` — full graph deployment | **Not tested** (GAP-03) |
| `composition.status` — health + resource pressure | **Not implemented** (needed for adaptive daemons) |
| Neural API registration for new methods | **Not implemented** (GAP-09) |
| Cross-primal token federation | **Not implemented** (JH-11) |

### Interaction map (what calls what on the active gate)

```
                    ┌─────────────────────────────────────────────────┐
                    │  biomeOS (orchestration, Neural API routing)     │
                    └──┬──────────┬──────────┬──────────┬─────────────┘
                       │          │          │          │
              ┌────────▼──┐  ┌───▼────┐  ┌──▼────┐  ┌─▼──────────┐
              │ ToadStool  │  │Squirrel│  │ pCast │  │tunnelKeeper│
              │ (dispatch) │  │  (AI)  │  │(prop.)│  │  (health)  │
              └────┬───────┘  └────────┘  └───┬───┘  └────────────┘
                   │                          │
          ┌────────▼──────────────────────────▼────────┐
          │         BearDog (trust, identity, BTSP)     │
          └────┬──────────────────┬────────────────────┘
               │                  │
      ┌────────▼───┐    ┌────────▼────────────────────┐
      │  Songbird  │    │  Provenance Trio             │
      │  (network) │    │  rhizoCrypt → loamSpine      │
      └────────────┘    │              → sweetGrass     │
                        └─────────────────────────────┘
```

Every arrow is an IPC call (UDS or TCP on localhost). No primal imports another
primal's code. The composition graph defines the wiring.

---

## 3. What Primal Teams Should Absorb

### For all primal teams

1. **Gate-agnostic paths**: Use env-var indirection for any filesystem path.
   Pattern: `GATE_HOME` → `HOME` → safe default. See `darkforest/src/crypto.rs`
   `gate_home()` function for the reference implementation.

2. **`expect()` audit**: Audit all `expect()` and `unwrap()` calls in network,
   config, and credential code paths. Convert to `Result` propagation. The
   cost is ~3 lines per call site; the benefit is deployability on
   misconfigured or new gates.

3. **Dependency slimming**: Audit `tokio` features (`["full"]` → specific
   features), `rand` usage (`rand` → `rand_core` if only `OsRng` needed).
   Compounds across the ecosystem build graph.

4. **MethodGate enforcement**: All 13 primals now ship MethodGate. If your
   primal does not respond to `auth.mode` on TCP, document whether this is
   intentional (BTSP-gated, IPC-only) or a gap.

5. **Port env-var convention**: `{PRIMAL_NAME}_PORT` (e.g., `BEARDOG_PORT=9100`).
   Downstream deployers override via `nucleus_config.sh`.

### For biomeOS specifically

- **`composition.status` method** (HIGH): pappusCast and other adaptive daemons
  need `{ active_users, primal_health, resource_pressure }` without querying
  JupyterHub directly.
- **`composition.deploy(graph)` validation** (MEDIUM): GAP-03 — live cell graph
  deployment not tested end-to-end.
- **Neural API registration** (MEDIUM): GAP-09 — new IPC methods from springs
  (e.g., ludoSpring's 15 game methods) need a registration endpoint.
- **Multi-gate propagation** (LOW): pappusCast on gate A should propagate to
  observer surfaces on gates B/C via Songbird + NestGate.

### For bearDog specifically

- **JH-11 cross-primal token federation** (HIGH): The single biggest remaining
  architectural gap. Without it, Tier 4 authenticated composition is impossible.
  Each primal validates independently — no shared key distribution or trust chain.
  biomeOS `_resource_envelope` forwarding works as a composition-level workaround
  but is not a real federation mechanism.

### For petalTongue specifically

- **PT-1 through PT-5**: Static file serving catch-all, NestGate backend
  integration, web-mode config schema, deploy mode naming, worker threading.
  These remain the primary blockers for Voila sovereignty replacement.
- **Notebook rendering with metadata**: `metadata.title` for page headers,
  configurable `strip_sources` for code visibility.

### For rhizoCrypt specifically

- **GAP-06 UDS transport**: Blocks the provenance trio in 4 ludoSpring
  experiments. TCP works but UDS is the canonical local transport.

---

## 4. What Spring Teams Should Absorb

### Composition patterns your springs can use

| Pattern | What it is | Which springs benefit |
|---------|-----------|---------------------|
| Deploy graph as contract | TOML DAG describing what capabilities you need | All (define your composition) |
| Two-tier validation | `--tier rust` (CI-safe, no primals) + full (live primals) | All (CI + integration) |
| Certification organelle | guidestone layers absorbed as library modules | All (L0-L8 quality gates) |
| IPC-first composition | Call capabilities via IPC, never import primal code | All (decoupling) |
| Snapshot propagation | Validated copies, not live mounts; quarantine on failure | ludoSpring (game state), wetSpring (data) |
| Adaptive rate limiting | `interval = min(BASE * max(1, users), MAX)` | neuralSpring (inference), any batch process |

### Path and kernel lessons from NUCLEUS deployment

- **Absolute paths for data**: Notebooks that use relative paths break when
  moved between compute, public, and sporePrint contexts. Anchor to
  `$SPRING_DATA_ROOT` or an absolute path.
- **Universal kernel**: Public-facing notebooks need the `python3` kernel
  (available everywhere). If you need specialized packages, graceful degradation:
  `try: import Bio except ImportError: HAS_BIO = False`.
- **Metadata titles**: All notebooks need `metadata.title`. pappusCast rejects
  notebooks without titles. Voila shows filenames otherwise.

### Spring-specific absorption targets

| Spring | What to absorb | Why |
|--------|---------------|-----|
| primalSpring | Observer composition graph template, pappusCast primal spec | Defines composition patterns |
| wetSpring | Path resolution, kernel consistency, data provenance | Primary observer content |
| healthSpring | Multi-tier testing, `primal-proof` feature gate | Parallels tier-specific testing |
| hotSpring | Python → Rust evolution evidence | Mid-rewiring (darkforest proves the pattern) |
| neuralSpring | Adaptive rate limiting, inference workload scheduling | Load-adaptive processing |
| ludoSpring | Snapshot propagation, IPC method registration (15 methods) | Game state + composition |
| groundSpring | Data pipeline provenance, BLAKE3 content addressing | Geological data integrity |
| airSpring | Resource envelope patterns, dispatch optimization | Compute workload composition |

---

## 5. Sovereignty Roadmap (for coordination)

Current state and what blocks each step:

```
Horizon 1: External Security       ██████████ COMPLETE (175 PASS, 0 FAIL)
Horizon 2: Sovereignty             █████░░░░░ 
  Step 2a: Tunnel baseline         ██████████ DONE (270ms p50)
  Step 2b: BTSP auth               ████░░░░░░ Ready to build (bearDog JH-11 needed for federation)
  Step 3a: Gate-served sporePrint   ████████░░ INTERMEDIATE (Zola + tunnel; petalTongue PT-1 blocks full)
  Step 3b: BearDog TLS             ██░░░░░░░░ Blocked (X.509/ACME upstream)
  Step 3c: Songbird NAT            █░░░░░░░░░ Blocked (STUN/TURN upstream)
  Step 4:  Sovereign DNS           ███░░░░░░░ INTERMEDIATE (DoT operational)
Horizon 3: Primal-Only             █░░░░░░░░░ All blocked on H2
```

---

## 6. The Fossil Record

projectNUCLEUS maintains its history in `validation/archive/`:

| Content | Location |
|---------|----------|
| Legacy darkforest scripts (bash/python) | `validation/archive/legacy/` |
| Security validation runs (timestamped) | `validation/archive/security-*` |
| Provenance pipeline runs | `validation/archive/provenance-*` |
| External validation snapshots | `validation/archive/external-*` |

These are not deleted — they are the geological record of how NUCLEUS evolved.
primalPSing audit can reference them for lineage verification.

---

## 7. Immediate Actions for primalPSing

1. **Audit the 7 Tier 3 code quality items** (coralReef `tracing`, barraCuda
   `unwrap`, nestGate `unwrap`, biomeOS mock isolation, bearDog HSM feature-gate,
   petalTongue `#[allow]` reasons, squirrel test file split)
2. **Triage JH-11** — cross-primal token federation is the next stadial gate
3. **Verify GAP-06** — rhizoCrypt UDS transport for provenance trio
4. **Review GAP-03/09** — biomeOS cell deploy and neural API registration
5. **Regenerate U1** — primalSpring CHECKSUMS after Phase 59 refactoring
6. **Structural fixes U2/U3** — deploy graph `by_capability` and `bonding_policy`

---

**The gate is clean, the composition is proven, the debt is swept. What flows
upstream is what the primals need to evolve next.**
