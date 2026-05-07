# Phase 59 Convergence + Live Science Handoff

**Date**: May 6, 2026
**From**: projectNUCLEUS (sporeGarden)
**To**: primalSpring, all primal teams, all spring teams
**Scope**: Security convergence, live science pipeline, composition patterns, next steps

---

## 1. What's Live Now

### Public Notebooks on primals.eco

5 wetSpring notebooks are rendered with embedded matplotlib charts at
[primals.eco/lab/notebooks/](https://primals.eco/lab/notebooks/):

| Notebook | Evidence |
|----------|----------|
| 16S Pipeline Validation | DADA2, taxonomy, LC-MS, R/vegan parity, NCBI data |
| Python vs Rust vs GPU | Timing curves, energy costs, 33x overall speedup |
| 63/63 Paper Reproductions | 5 researchers, 6 tracks, full evidence map |
| Cross-Spring Connections | 79 barraCuda primitives, ToadStool log_f64 bug discovery |
| Soil Anderson Deep Dive | 9 Track 4 experiments, QS probability, soil type predictions |

All notebooks load frozen data from `experiments/results/*.json` — no live
primals needed to view them. This is the Tier 1 exemplar for all springs.

### Spring Science Hubs

Science hub pages at `/lab/springs/` for wetSpring, hotSpring, airSpring,
healthSpring with validation summaries, key findings, and primal consumption maps.

### Validation Pipeline

- 13,648+ checks across 8 springs (235+ in wetSpring alone across 11 workloads)
- Full provenance chain: BLAKE3 → rhizoCrypt DAG → loamSpine ledger → sweetGrass braid
- 15/15 external checks via Cloudflare Tunnel (270ms p50 latency)
- JupyterHub with 4-tier PAM access (observer/compute/admin/reviewer)

---

## 2. sporePrint Automation

### Auto-Refresh CI

`notify-sporeprint.yml` is installed in all 26 source repos (15 primals + 8 springs + 3 products).
When a source repo pushes to main, it dispatches a `repository_dispatch` event to sporePrint.

**Tier 1 — Metrics** (auto-committed, no review):
```
source repo push → notify-sporeprint.yml → sporePrint auto-refresh.yml
  → spore-validate refresh --write --source <name>
  → updates sources.toml (loc, tests, files, crates)
  → auto-commit to main
```

**Tier 2 — Content** (creates PR for review):
```
source repo push (content: "true") → notify-sporeprint.yml → sporePrint auto-refresh.yml
  → clones source, copies sporeprint/*.md to content/lab/
  → renders notebooks/*.ipynb via jupyter nbconvert --execute
  → creates PR: "content: add <source> lab pages + notebooks"
```

### sources.toml Registry

`sporePrint/sources.toml` maps every entity to its GitHub repo. `spore-validate`
uses this for metric collection. To add a new repo, add an entry to `sources.toml`
and install `notify-sporeprint.yml` — see `sporePrint/ONBOARDING.md`.

---

## 3. Notebook Pipeline

### How Notebooks Get Rendered

```
your-spring/notebooks/*.ipynb
    ├─ git push to main
    │     └─ notify-sporeprint.yml fires (content: "true")
    ├─ sporePrint auto-refresh.yml (CI)
    │     ├─ pip install jupyter nbconvert matplotlib numpy
    │     ├─ jupyter nbconvert --execute --template basic
    │     └─ wraps output HTML in Zola front matter
    └─ primals.eco/lab/notebooks/<slug>.md
```

### Convention

- `notebooks/` directory in your spring repo
- Load frozen data from `../experiments/results/*.json` (relative paths)
- Use matplotlib for charts (do NOT set `matplotlib.use('Agg')`)
- End each notebook with a provenance summary linking to primals.eco
- See `wetSpring/notebooks/NOTEBOOK_PATTERN.md` for the full pattern

### Recommended Set (5 notebooks per spring)

1. `01-domain-validation.ipynb` — flagship validation story
2. `02-benchmark-comparison.ipynb` — Python vs Rust vs GPU
3. `03-paper-reproductions.ipynb` — per-researcher evidence
4. `04-cross-spring-connections.ipynb` — ecosystem flows
5. `05-domain-deep-dive.ipynb` — most compelling cross-domain insight

---

## 4. LIVE_SCIENCE_API — Tier 2 Target

6 JSON-RPC methods defined in `projectNUCLEUS/specs/LIVE_SCIENCE_API.md` for
notebooks to call primals directly:

| Method | Primal | Priority | Purpose |
|--------|--------|----------|---------|
| `toadstool.validate` | ToadStool | P0 | Execute a workload TOML and return structured results |
| `toadstool.list_workloads` | ToadStool | P0 | List available workload specs |
| `barracuda.compute` | barraCuda | P1 | Execute a named GPU primitive with parameters |
| `biomeos.spring_status` | biomeOS | P1 | Query which springs have active compositions |
| `nestgate.artifact_query` | NestGate | P2 | Retrieve stored validation artifacts by content hash |
| `rhizocrypt.dag_summary` | rhizoCrypt | P2 | Get the DAG summary for a validation session |

P0 methods are the bridge from Tier 1 (static notebooks) to Tier 2 (live dispatch).
Springs implementing `--format json` on their validators enable this transition.

---

## 5. Workload TOMLs

### wetSpring (11 workloads)

8 Rust PASS + 2 Python RUN + 1 deferred FAIL:
- `wetspring-16s-rust-validation.toml` — flagship 16S pipeline
- `wetspring-diversity-rust-validation.toml` — Shannon/Simpson/Chao1
- `wetspring-pfas-rust-validation.toml` — PFAS screening
- `wetspring-qs-ode-rust-validation.toml` — quorum sensing ODE
- `wetspring-metagenomics-rust-validation.toml` — deep-sea ANI/SNP
- `wetspring-soil-qs-rust-validation.toml` — Track 4 soil Anderson
- `wetspring-drug-repurposing-rust-validation.toml` — NMF/TransE
- `wetspring-phylogenetics-rust-validation.toml` — Felsenstein/HMM/RF
- `wetspring-16s-python-baseline.toml` — Python Galaxy baseline
- `wetspring-r-industry-parity.toml` — R/vegan cross-check
- `wetspring-gpu-validation.toml` — GPU parity (deferred: requires RTX)

### Skeleton TOMLs (3 springs)

- `hotspring/hotspring-md-validation.toml` — molecular dynamics (awaiting binary)
- `airspring/airspring-et0-validation.toml` — evapotranspiration (awaiting binary)
- `healthspring/healthspring-pk-validation.toml` — pharmacokinetics (awaiting binary)

**Pattern for new springs**: Copy a wetSpring TOML, change `[workload]` fields,
point `binary` at your spring's validation binary.

---

## 6. Phase 59 Security Convergence

All five security gaps from the Phase 2a pen test are resolved upstream.

| PG | Resolution |
|----|-----------:|
| **PG-55** | All 13 primals default `127.0.0.1`. Songbird/ToadStool/skunkBat/biomeOS/petalTongue: `--bind`. sweetGrass: bare `--port` = localhost. biomeOS forwards `--bind` to nucleus. |
| **PG-56** | NestGate BTSP method-level auth gating. 10-method exempt whitelist (health, identity, capabilities). |
| **PG-57** | skunkBat multi-dimensional anomaly detection (connection rate + traffic volume + port diversity). 12 normal + 7 attack patterns seeded. |
| **PG-58** | Songbird `--bind` for HTTP server, `--listen` for IPC socket (separate concerns). |
| **PG-59** | sweetGrass `--http-address` and `--port` both accept `host:port`, documented in CLI help. |

### What to absorb

1. **Bind policy**: Drop explicit `--bind 0.0.0.0` from deploy scripts — all primals default localhost. Use `bind_policy = "localhost"` in graph metadata; guidestone validates it. Pass `--bind 0.0.0.0` only for intentional cross-host access.

2. **`PrimalDeployProfile.bind_flag`**: All 13 primals return `Some(flag)` — deploy tooling can use `profile.bind_flag` programmatically.

3. **Foundation validation graph**: `graphs/compositions/foundation_validation.toml` — 12-node NUCLEUS for scientific sediment pipeline.

4. **NestGate TCP fallback**: BTSP gating applies to UDS/isomorphic paths only. TCP fallback (Tier 5, localhost) dispatches all methods ungated — acceptable for localhost but noted for external TCP exposure.

### Ecosystem state after Phase 59
- 13/13 BTSP Phase 3 FULL AEAD (ChaCha20-Poly1305)
- 13/13 default `127.0.0.1` bind
- Zero open security gaps
- Discovery escalation hierarchy live (5 tiers)
- 85 experiments, 661 tests, 74 deploy graphs (primalSpring)

---

## 7. biomeOS Neural API Composition Patterns

### Deploy Graph Patterns

Compositions are declared in TOML deploy graphs. The canonical schema
(`[[graph.nodes]]`) defines node identity, capabilities, ports, and bonding:

```toml
[graph.metadata]
name = "wetspring_science_nucleus"
bonding = "covalent"
bind_policy = "localhost"

[[graph.nodes]]
name = "beardog"
role = "identity"
capabilities = ["security"]
tcp_fallback_port = 9100
```

### Capability-Based Discovery

All graphs use `by_capability` discovery (not `name`). A spring's workload
requests a capability (e.g., `compute.gpu`), and Songbird's 5-tier discovery
resolves it to the appropriate primal:

```
Tier 1: UDS (same machine, <1ms)
Tier 2: mDNS (LAN, <5ms)
Tier 3: BearDog gossip (mesh, <50ms)
Tier 4: Registry (global, <200ms)
Tier 5: TCP fallback (localhost, direct connect)
```

### 5 biomeOS Coordination Patterns

1. **NeuralApiServer**: Main coordinator, binds configurable address (`--bind`), forwards bind policy to child primals
2. **Graph execution**: `biomeos deploy --graph <path>` reads TOML, starts primals in dependency order, verifies health
3. **Spring status**: `biomeos.spring_status` JSON-RPC method returns which springs have active compositions
4. **Bind forwarding**: biomeOS nucleus start passes `--bind` to all child primals, enabling single-point configuration
5. **Health orchestration**: Periodic health checks on all graph nodes, restart on failure

---

## 8. What Springs Do Next

### Immediate (this week)

1. **Fill `sporeprint/`**: Update `sporeprint/validation-summary.md` with your spring's current validation state — headline numbers, key findings, primal consumption
2. **Create `notebooks/`**: Follow the wetSpring pattern (see `notebooks/NOTEBOOK_PATTERN.md`). Start with `01-domain-validation.ipynb` loading your frozen experiment data
3. **Push to main**: The `notify-sporeprint.yml` workflow will fire automatically

### Next iteration

4. **Add `--format json`** to your validation binaries — enables structured output for Tier 2
5. **Create workload TOMLs** in `projectNUCLEUS/workloads/<yourspring>/` — enables ToadStool dispatch
6. **Evolve toward Tier 2**: Replace frozen data with `toadstool.validate` calls in notebooks

### Phase 3 convergence

7. **JSON-RPC methods**: Implement the methods in `specs/LIVE_SCIENCE_API.md` relevant to your spring
8. **petalTongue dashboards**: Create live visualization scenarios for your domain
9. **Standalone NUCLEUS**: Your spring runs as a self-hosted composition with live primals

### References

- `wateringHole/sporePrint/CONTENT_GUIDE.md` — how to publish to primals.eco
- `wateringHole/sporePrint/SPRING_EVOLUTION_TARGETS.md` — full evolution path
- `sporePrint/ONBOARDING.md` — adding a new repo to auto-refresh
- `projectNUCLEUS/specs/LIVE_SCIENCE_API.md` — JSON-RPC method specs
- `projectNUCLEUS/notebooks/spring-validation-template.ipynb` — parameterized dispatch template

---

## Files Changed in This Session

### projectNUCLEUS
- 8 files: RTX 5070 → RTX 4070 / RTX 3090 (GPU hardware correction)
- `README.md`: sporePrint live status, workload count (11), notebook references
- `PHASES.md`: sporePrint live vs planned (Phase 3), GPU fix
- `docs/NUCLEUS_PRIMER.md`: Complete 13-primal table (added Squirrel, skunkBat, biomeOS, petalTongue)
- `docs/BONDING_MODELS.md`: sporePrint visibility section, GPU fix
- `specs/VALIDATION_RESULTS.md`: Title updated to Phase 1-2a
- `validation/archive/`: Raw run artifacts archived

### wetSpring
- `whitePaper/baseCamp/README.md`: Public Science Visibility section
- `README.md`: Public Notebooks section with table and links
- `experiments/README.md`: Notebook integration note

### wateringHole
- `handoffs/PHASE59_CONVERGENCE_LIVE_SCIENCE_HANDOFF_MAY06_2026.md`: This document
