# hotSpring v0.6.32 — Phase 46 Composition Template Absorption

**Date:** April 27, 2026
**From:** hotSpring team
**To:** primalSpring, sibling spring teams, primals teams
**Lane:** Event-Driven Computation + DAG Memoization
**primalSpring phase:** 46 (Composition Template)
**License:** AGPL-3.0-or-later

---

## Summary

hotSpring absorbed primalSpring Phase 46's reusable NUCLEUS composition library
and implemented a domain-specific composition script (`tools/hotspring_composition.sh`)
for event-driven QCD computation with DAG memoization. This document captures the
async computation patterns, DAG memoization patterns, and scientific provenance
schema discovered during the exploration — all three are candidates for ecosystem
standardization.

---

## 1. Async Tick Model — Convergence-Based Progression

### Problem

The composition template's `domain_on_tick()` is designed for 60Hz interactive loops
(e.g., TTT game state). hotSpring simulations (lattice QCD HMC, nuclear EOS sweeps)
run for minutes to hours and converge rather than tick at fixed rates.

### Pattern Implemented

```bash
domain_on_tick() {
    # Priority 1: Check background compute completion (file-based signal)
    if check_background_compute; then
        # Result ready — store in DAG, update visualization
        return
    fi

    # Priority 2: Advance sweep if active and compute slot free
    if $SWEEP_ACTIVE && [[ "$COMPUTE_STATUS" != "running" ]]; then
        # Step to next beta value in sweep
        # Check memo cache before launching compute
        return
    fi

    # Priority 3: Proprioception (idle heartbeat)
    check_proprioception
}
```

**Key design decisions:**

- **Background compute via process polling**: Long-running computations spawn as
  background processes (`cargo run --release --bin validate_pure_gauge &`). The tick
  handler checks `kill -0 $PID` rather than blocking.
- **Adaptive backoff**: `sleep 0.2` during active sweep/compute, `sleep $POLL_INTERVAL`
  (default 0.5s) when idle. Prevents busy-waiting during GPU runs.
- **Result file handoff**: Background processes write results to a temp file. The tick
  handler reads and cleans up on completion detection.

### Recommendation for Sibling Springs

Any spring with long-running computations (neuralSpring training, mineralSpring
simulations) should follow this pattern:
1. Spawn compute as background process
2. Poll in `domain_on_tick()` with adaptive backoff
3. Use file-based or socket-based result handoff
4. Never block the main loop

---

## 2. DAG Memoization Wrapper — Candidate for Upstream Promotion

### Problem

Parameter sweeps (e.g., 6 beta values × 3 lattice sizes = 18 configurations) can
revisit identical parameter sets through different DAG paths. Without memoization,
each visit re-triggers expensive computation.

### Pattern Implemented

```bash
# Session-local associative array cache
declare -A MEMO_CACHE

memo_param_key() {
    echo "${BETA}|${LATTICE_L}|${LATTICE_T}|${ALGORITHM}|${N_TRAJ}" \
        | sha256sum | cut -c1-16
}

memo_check_vertex() {
    local key=$(memo_param_key)
    [[ -n "${MEMO_CACHE[$key]+_}" ]] && echo "${MEMO_CACHE[$key]}" && return 0
    return 1
}

memo_store_result() {
    local vertex_id="$1" result_json="$2"
    local key=$(memo_param_key)
    MEMO_CACHE[$key]="$result_json"
    # Persist to DAG if available
    cap_available dag && dag_append_event ...
}
```

**Design properties:**

- **Two-tier storage**: In-memory associative array (fast) + rhizoCrypt DAG (persistent).
  Session-local cache survives DAG unavailability.
- **Deterministic key hashing**: SHA-256 of pipe-delimited parameters ensures identical
  parameter sets always hit cache regardless of DAG path.
- **Graceful degradation**: If DAG is offline, memo still works in-memory. If both are
  gone, computation proceeds (no crash).

### Candidate for `nucleus_composition_lib.sh`

The memo wrapper is domain-agnostic. Proposed addition to the lib:

```bash
declare -A MEMO_CACHE

memo_check() {
    local key="$1"
    [[ -n "${MEMO_CACHE[$key]+_}" ]] && echo "${MEMO_CACHE[$key]}" && return 0
    return 1
}

memo_store() {
    local key="$1" value="$2"
    MEMO_CACHE[$key]="$value"
}

memo_key() {
    echo "$*" | sha256sum | cut -c1-16
}
```

Springs would call `memo_key "$BETA" "$L" "$T"` to get a key, then `memo_check`/`memo_store`.

---

## 3. Scientific Provenance Schema — Peer-Review Audit Metadata

### Problem

Peer reviewers need to reconstruct the exact conditions of a simulation run.
sweetGrass braids carry attribution metadata, but the schema for scientific
simulations was undefined.

### Schema Implemented

Each braid record carries a JSON metadata payload:

```json
{
    "event": "compute_complete",
    "beta": "5.7",
    "L": "4",
    "T": "4",
    "algorithm": "HMC",
    "n_traj": 10,
    "doi": "10.1103/PhysRevD.10.2445",
    "hardware": "x86_64",
    "rust": "rustc 1.87.0 (stable)",
    "computed": 5,
    "memoized": 2
}
```

**Fields and rationale:**

| Field | Type | Purpose |
|-------|------|---------|
| `event` | string | Event type (genesis, param_change, compute_start, compute_complete, sweep_step) |
| `beta` | string | Coupling constant — the primary physics parameter |
| `L` | string | Spatial lattice dimension |
| `T` | string | Temporal lattice dimension |
| `algorithm` | string | HMC, RHMC, or hybrid — determines trajectory generation |
| `n_traj` | integer | Number of trajectories per configuration |
| `doi` | string | Paper DOI for the reference calculation |
| `hardware` | string | `uname -m` output — architecture identifier |
| `rust` | string | `rustc --version` — compiler version for reproducibility |
| `computed` | integer | Cumulative compute count at this point |
| `memoized` | integer | Cumulative cache hit count — shows sweep efficiency |

### Recommendation for Ecosystem

Springs with scientific domains should adopt a provenance schema with:
1. **Domain parameters** (the physics/ML/simulation inputs)
2. **Reference DOI** (what paper is being reproduced)
3. **Hardware fingerprint** (architecture, GPU ID if applicable)
4. **Software fingerprint** (compiler version, binary hash)
5. **Computation metrics** (count, cache hits, wall time)

The `braid_record` function from `nucleus_composition_lib.sh` accepts arbitrary
JSON metadata — no schema enforcement is needed at the library level, but springs
should document their schema in their handoff for reproducibility.

---

## 4. Compute Dispatch Patterns

### Tensor Probe (IPC Round-Trip Validation)

```bash
dispatch_tensor_probe() {
    if ! cap_available tensor; then return 1; fi
    local resp=$(send_rpc "$(cap_socket tensor)" "stats.mean" '{"data":[1,2,3,4,5]}')
    echo "$resp" | grep -q '"result"'
}
```

Used in `domain_init()` to verify IPC connectivity before starting sweeps.

### SEMF Computation (Physics via IPC or Local Fallback)

```bash
dispatch_semf_computation() {
    local z="$1" n="$2"
    if ! cap_available tensor; then
        echo '{"source":"local","z":'$z',"n":'$n'}'
        return 0
    fi
    # Encode SEMF terms as tensor data, send via stats.mean as proxy
    local resp=$(send_rpc_quiet "$(cap_socket tensor)" "stats.mean" ...)
    echo "{\"source\":\"ipc\",\"z\":$z,\"n\":$n,\"be_proxy\":$result}"
}
```

Falls back to local computation when tensor capability is offline.

### Background Validation (Long-Running Compute)

```bash
dispatch_background_validation() {
    (cd "$barracuda_dir" && cargo run --release --bin hotspring_guidestone ...) &
    COMPUTE_PID=$!
    COMPUTE_STATUS="running"
}
```

Spawns in background, polled in `domain_on_tick()`. Results stored in DAG + ledger + braids.

---

## 5. Ledger Sealing for Reproducibility

Each simulation run creates a loamSpine spine at `domain_init()`. Events are appended
as the sweep progresses:

1. `sweep-step-N` — parameters and result for each configuration
2. `semf-pb208` — SEMF probe results (Z=82, N=126 for Lead-208)
3. `compute-result` — background validation outcomes
4. `sweep-summary` — final statistics (computed/memoized counts)

The spine is sealed on quit (Q key) or sweep completion, creating an immutable record.
A sealed spine + its braid chain = a reproducible, auditable simulation run.

---

## 6. Files Changed in hotSpring

| File | Change |
|------|--------|
| `tools/hotspring_composition.sh` | **New** — domain composition script (350 lines) |
| `tools/nucleus_composition_lib.sh` | **New** — copied from primalSpring Phase 46 |
| `CHANGELOG.md` | Phase 46 absorption entry |
| `README.md` | Composition template reference |
| `docs/PRIMAL_GAPS.md` | GAP-HS-038 (resolved), GAP-HS-039 through GAP-HS-042 (active) |
| `experiments/README.md` | Phase 46 composition session entry |
| `scripts/README.md` | Added composition scripts to active table |

---

## 7. Active PRIMAL_GAPS Discovered

| ID | Primal | Description |
|----|--------|-------------|
| GAP-HS-039 | rhizoCrypt | DAG accepts UDS but may not respond to JSON-RPC — mitigated with `cap_available` guards + local memo fallback |
| GAP-HS-040 | toadStool | Slow on short timeouts (< 5s) — mitigated with >= 10s timeout + async polling |
| GAP-HS-041 | barraCuda | Missing `stats.entropy` — mitigated with `stats.mean` proxy |
| GAP-HS-042 | petalTongue | musl-static + winit threading — mitigated by using local build for live mode |

---

## 8. Upstream Recommendations for primalSpring

1. **Add DAG memoization to `nucleus_composition_lib.sh`**: The `memo_check`/`memo_store`/`memo_key` trio is domain-agnostic and useful for any spring doing parameter exploration.

2. **Document async tick pattern**: The composition template's `domain_on_tick()` needs guidance for springs with long-running compute. A "Computation Patterns" section in the template could show the background-process + polling pattern.

3. **Scientific provenance schema guidance**: Add a recommended schema structure to `DOWNSTREAM_COMPOSITION_EXPLORER_GUIDE.md` — minimum fields for reproducibility (parameters, reference, hardware, software).

4. **rhizoCrypt connection healthcheck**: rhizoCrypt should respond to a simple healthcheck on UDS connect, not just accept the connection silently. This would let `cap_available dag` be more reliable.

5. **toadStool timeout documentation**: Minimum recommended timeout for compute dispatch should be documented in toadStool's README or capability registry.
