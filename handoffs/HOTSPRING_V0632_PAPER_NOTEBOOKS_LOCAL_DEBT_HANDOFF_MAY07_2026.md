# hotSpring v0.6.32 — Paper Baseline Notebooks + Local Debt Resolution

**Date:** May 7, 2026
**From:** hotSpring
**For:** primalSpring (composition evolution), sporePrint (content pipeline), primal teams (gaps)
**Status:** 993/993 tests, 0 clippy errors, 17 notebooks, guideStone Level 5

---

## What We Shipped

### Paper Baseline Notebooks (12)

Created `notebooks/papers/` — 12 publishable-grade Jupyter notebooks wrapping
22 peer-reviewed physics papers from `control/` Python baselines. Each notebook
is a self-contained entry point: run it, see the physics, compare to Rust.

| # | Notebook | Domain | Compute | Source |
|---|----------|--------|---------|--------|
| 01 | SEMF Binding Energy | Nuclear physics | Live (2042 nuclei, <1s) | `skyrme_hf.py`, `objective.py` |
| 02 | Yukawa Screening | Screened Coulomb | Live (eigenvalues, ~1s) | `yukawa_eigenvalues.py` |
| 03 | Sarkas Yukawa MD | Plasma MD | Live small + frozen | `yukawa_md_baseline.py` |
| 04 | TTM Laser-Plasma | Laser heating | Live (ODE, ~1s) | `run_local_model.py` |
| 05 | Transport Coefficients | Daligault fit | Live analytical | `daligault_fit.py` |
| 06 | Surrogate Learning | ML sampling | Live demo + frozen | `run_reproduction.py` |
| 07 | Quenched QCD | SU(3) HMC | Live 4^4 (~30s) | `quenched_beta_scan.py` |
| 08 | Dynamical Fermions | Staggered QCD | Live small + frozen | `dynamical_fermion_control.py` |
| 09 | Abelian Higgs | U(1) gauge-Higgs | Live 8x8 (~5s) | `abelian_higgs_hmc.py` |
| 10 | Spectral Theory | Anderson/Hofstadter | Live (~5s) | `spectral_control.py` |
| 11 | Gradient Flow | Wilson flow | Live 4^4 (~10s) | `gradient_flow_control.py` |
| 12 | Plasma Dielectric | BGK/Mermin | Live (~1s) | `bgk_dielectric_control.py` |

**Collaborator pattern:** `notebooks/papers/PAPER_NOTEBOOK_GUIDE.md`

### Local Debt Resolved

1. **RPC method name mismatches fixed (3):**
   - `validate_nucleus_node.rs`: `shader.compile` → `shader.compile.wgsl` (aligned with `niche::ROUTED_CAPABILITIES`)
   - `validate_nucleus_nest.rs`: RPC call `dag.create_session` → `dag.session.create` (aligned with `niche` and `dag_provenance.rs`)
   - `validate_nucleus_nest.rs`: capability assertion `provenance.create_braid` → `braid.create` (aligned with `niche`)
   - `dag_provenance.rs`: doc comment updated to match

2. **Notebook CI readiness:**
   - `notebooks/requirements-notebooks.txt`: `numpy>=2`, `scipy>=1.12`, `matplotlib>=3.8`, `jupyter>=1.0`, `nbconvert>=7.0`
   - All 17 notebooks: `matplotlib.use('Agg')` for headless CI execution
   - `np.trapezoid` compat shim in notebooks 03 and 12 (`trapezoid = np.trapezoid if hasattr(np, 'trapezoid') else np.trapz`)

3. **sporeprint/README.md:** Added Zola TOML front matter (`render = false`) to prevent broken ingest

4. **Revalidation:** 993/993 tests pass, `cargo clippy --lib` clean, both modified binaries (`validate_nucleus_node`, `validate_nucleus_nest`) compile clean

---

## For sporePrint Team

### Notebook Rendering Pipeline

hotSpring now has 17 notebooks (5 sporePrint + 12 paper baselines) ready for rendering.
The `notify-sporeprint.yml` fires with `content: "true"` on push to main.

**What's needed upstream to render paper notebooks on primals.eco:**

1. **`auto-refresh.yml` workflow** — the CONTENT_GUIDE documents this CI step
   but it does not exist in the sporePrint repo. The workflow should:
   - Clone the spring repo
   - `pip install -r notebooks/requirements-notebooks.txt`
   - `jupyter nbconvert --execute --to html` each notebook
   - Wrap output HTML in Zola front matter
   - PR into sporePrint `content/lab/notebooks/`

2. **Recursive notebook discovery** — current docs reference `notebooks/*.ipynb`.
   hotSpring's paper notebooks live at `notebooks/papers/*.ipynb`. The rendering
   pipeline needs to recurse or explicitly include `papers/`.

3. **Execution timeouts** — paper notebooks 07 (QCD), 08 (dynamical fermions),
   and 10 (spectral theory) may need 60-120s. Set
   `ExecutePreprocessor.timeout = 300` as a safe default.

4. **hotSpring lab page** — `content/lab/springs/hotspring.md` on primals.eco
   currently says "10+ papers." Should be updated to "22 papers, 12 paper
   baseline notebooks, 5 sporePrint notebooks."

5. **Science index** — `primals.eco/science/` lists only 3 hotSpring papers
   (07, 10, 25). The remaining 19 are now covered by notebooks and should have
   entries or at minimum a grouped "hotSpring baseCamp" page.

### Matplotlib Agg Guidance

CONTENT_GUIDE says "do not set `matplotlib.use('Agg')`" while
SPRING_EVOLUTION_TARGETS says "use Agg for headless rendering."
We went with Agg in all notebooks for CI safety. One authoritative rule
would help springs stay consistent.

---

## For Primal Teams — Active Gaps

### P1: rhizoCrypt DAG Graceful Degradation (GAP-HS-039)

**Primal:** rhizoCrypt
**Issue:** rhizoCrypt may accept UDS connection with no JSON-RPC response, causing
DAG calls to timeout silently. hotSpring mitigates with `cap_available dag` guards
and local memo cache fallback in composition script.
**Ask:** Implement connection-level healthcheck — return error on connect if not ready.

### P1: Composition Script SEMF Proxy (new gap)

**Primal:** barraCuda / hotSpring
**Issue:** `hotspring_composition.sh` dispatches SEMF computation via `stats.mean`
as a proxy — not an actual SEMF RPC. The physics dispatch path uses `stats.mean`
because barraCuda does not expose a dedicated SEMF method over IPC.
**Ask:** Either (a) barraCuda adds `physics.semf` or `stats.semf` method, or
(b) hotSpring's primal server handles this routing (hotSpring as physics provider).
The Rust binary path (`hotspring_primal.rs`) already handles `physics.nuclear_eos`
correctly — the shell composition script is the gap.

### P2: toadStool Short Timeout Sensitivity (GAP-HS-040)

**Primal:** toadStool
**Issue:** toadStool IPC is slow on short timeouts (< 5s). Composition script uses
>= 10s for real compute dispatch. Background validation uses async polling.
**Ask:** Document minimum recommended timeout. Consider `health.liveness` fast-path.

### P2: `stats.entropy` Not Implemented (GAP-HS-041)

**Primal:** barraCuda
**Issue:** `stats.entropy` method is missing. hotSpring computes entropy locally
and uses `stats.mean` for IPC smoke tests.
**Ask:** Add `stats.entropy(data) -> f64` to barraCuda's stats module and register
as IPC-routable capability.

### P3: Squirrel E2E Parity (GAP-HS-001)

**Primal:** Squirrel / neuralSpring
**Status:** `validate_squirrel_roundtrip` wired, exits 2 (skip) when absent.
Remaining: confirm parity once neuralSpring WGSL shader ML replaces Ollama fallback.

### P3: TensorSession Adoption (GAP-HS-027)

**Primal:** barraCuda
**Status:** Deferred. GPU HMC trajectory (leapfrog + force + gauge update) is the
natural first candidate. Blocked on API stabilization.

### P3: IONIC Cross-Family GPU Lease (GAP-HS-005)

**Primal:** BearDog / Songbird
**Status:** Blocked upstream. ionic propose/accept/seal protocol not implemented.

### P3: petalTongue musl-static Threading (GAP-HS-042)

**Primal:** petalTongue
**Status:** plasmidBin musl build may have winit threading issues. Composition
script degrades to no-op when visualization offline.

### Hardware-Specific (coralReef)

- **GV100 WPR pivot** (GAP-HS-030): Volta has no WPR; ACR boot path needs
  Volta-specific bypass. Warm handoff (nouveau→VFIO) works but FECS/GPCCS halted.
- **Ember absorption** (GAP-HS-030): ember → toadStool after sovereign pipeline
  validated across GPU generations. Deferred.
- **Fork isolation pattern** (GAP-HS-029): Reusable hardware fault containment
  primitive in coral-driver. Should be documented as ecosystem pattern.

---

## For primalSpring — Composition Patterns

### Method Name Registry Alignment

hotSpring found and fixed 3 method name drifts between validators and
`niche::ROUTED_CAPABILITIES`. This suggests a systemic risk:

| Stale name | Canonical name | Where found |
|-----------|---------------|-------------|
| `dag.create_session` | `dag.session.create` | nest validator RPC call |
| `provenance.create_braid` | `braid.create` | nest capability assertion |
| `shader.compile` | `shader.compile.wgsl` | node capability assertion |

**Recommendation:** primalSpring Phase 60+ should add a CI check that validates
all `validate_capability()` and `ctx.call()` strings in spring binaries against
the capability registry TOML. The `config/capability_registry.toml` sync test
in hotSpring catches local drift but can't catch binary-embedded string literals.

### `downstream_manifest.toml` Completeness

hotSpring's entry in `primalSpring/graphs/downstream/downstream_manifest.toml`
lists `depends_on` for tower/node primals but omits the optional provenance trio
(rhizoCrypt, loamSpine, sweetGrass) that `niche::DEPENDENCIES` declares. These
should be present with `optional = true` annotations.

### Paper Notebook Pattern for Springs

The `PAPER_NOTEBOOK_GUIDE.md` pattern and 12-notebook structure is ready for
sibling springs to replicate. Key conventions:

- **Three-tier evolution:** Small live compute → frozen data → NUCLEUS primal
  composition. Notebooks cover Tier 1; heavy compute elevates to ecoPrimal
  compositions for Tier 2/3.
- **Self-contained:** No imports from `control/` modules. All physics inlined
  in notebook cells. Dependencies: numpy, scipy, matplotlib only.
- **Headless-safe:** `matplotlib.use('Agg')` + `savefig('/tmp/...')` pattern.
- **NumPy 2.x compat:** Use `trapezoid = np.trapezoid if hasattr(np, 'trapezoid') else np.trapz`.

---

## Validation State

```
cargo test --lib:    993 passed, 0 failed, 6 ignored (62.7s)
cargo clippy --lib:  0 warnings, 0 errors
cargo check --bin validate_nucleus_nest validate_nucleus_node:  clean
guideStone bare:     30/30 checks, 5/5 properties
Notebooks:           17 total (5 sporePrint + 12 paper baseline)
Python deps:         numpy>=2, scipy>=1.12, matplotlib>=3.8
```

---

## Files Changed (this handoff)

```
# New
notebooks/requirements-notebooks.txt
notebooks/papers/PAPER_NOTEBOOK_GUIDE.md
notebooks/papers/01-semf-binding-energy.ipynb ... 12-plasma-dielectric.ipynb (12 files)

# Modified
barracuda/src/bin/validate_nucleus_node.rs    (shader.compile → shader.compile.wgsl)
barracuda/src/bin/validate_nucleus_nest.rs    (dag/braid method names aligned)
barracuda/src/dag_provenance.rs               (doc comment)
sporeprint/README.md                          (Zola front matter)
sporeprint/validation-summary.md              (paper notebook table)
notebooks/01-05 sporePrint notebooks          (matplotlib Agg backend)
notebooks/papers/03,12                        (np.trapezoid compat)
README.md, CHANGELOG.md, experiments/README.md (paper notebook references)
```
