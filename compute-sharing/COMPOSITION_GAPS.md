# Composition Gaps — wetSpring Through Nest Atomic

**Date**: 2026-05-04 (updated 2026-05-05)
**Source**: Live composition validation of wetSpring science through
toadStool dispatch on ironGate — initially Node Atomic (5 primals),
elevated to Nest Atomic + ToadStool (9 primals) with provenance pipeline.
**Purpose**: Document gaps for other teams to evolve. Each gap is a handoff —
not a defect, but a known surface area where the next cycle of work lands.

---

## Gap 1: Python Runtime Not Registered (pyo3 Removed)

**Primal**: toadStool
**Severity**: Low (workaround exists)
**Observed**: toadStool logs `Python runtime: delegate to AI/routing service via IPC` — the Python engine is present in code but not registered as an active runtime.

**Root cause**: pyo3 FFI removed per ecoBin v3.0 to maintain pure-Rust, statically-linked binary compliance. Python workloads execute as `type = "native"` with explicit interpreter paths.

**Impact**:
- Python workloads work but bypass toadStool's resource accounting and introspection
- No per-workload memory/CPU tracking for Python subprocesses
- Workload isolation relies on OS process separation, not toadStool's sandbox

**Recommendation**: Accept for Phase 1. If Python introspection is needed later, consider a lightweight IPC protocol (Unix socket or JSON-RPC) between toadStool and a Python sidecar, rather than re-embedding pyo3.

---

## Gap 2: Sandbox Overrides working_dir to /tmp

**Primal**: toadStool
**Severity**: Medium (requires TOML workaround)
**Observed**: With default `isolation_level = "Standard"`, toadStool overrides `working_dir` to `/tmp` regardless of what the workload TOML specifies. Relative paths in `args` then resolve against `/tmp`.

**Impact**:
- Every workload TOML must use absolute paths in `args` and `command`
- `working_dir` in the TOML is effectively ignored under Standard isolation
- Scripts that assume CWD == project root fail silently (e.g., exp001 looking for `MiSeq_SOP`)

**Workaround applied**: Added `[security] isolation_level = "None"` to all local dev workload TOMLs. Absolute paths used in args.

**Recommendation**: Add a `trusted_directories` list to the sandbox config, or an `allow_working_dir` flag that lets the TOML's `working_dir` pass through when isolation is Standard. This preserves the safety model while enabling real workloads.

---

## Gap 3: GPU Build Breakage (wgpu API Drift)

**Primal**: barraCuda + wetSpring
**Severity**: Medium (blocks GPU workloads)
**Observed**: `cargo build --release --features gpu` fails:
```
error[E0599]: no method named `submit_and_poll` found for struct `Arc<WgpuDevice>`
```

**Root cause**: `WgpuDevice` in barraCuda replaced `submit_and_poll` with `submit_and_map`. wetSpring's `bio/pairwise_l2_gpu.rs` still calls the old API.

**Impact**:
- GPU-dependent binaries (`validate_anderson_2d_qs`, `validate_qs_disorder_real`) cannot build
- All CPU parity validators work fine — the GPU feature is additive, not blocking

**Recommendation**: Update `pairwise_l2_gpu.rs` to use `submit_and_map`. This is a one-line API migration, not an architectural change.

---

## Gap 4: Data Dependencies Not Managed by Composition

**Primal**: toadStool / nestGate
**Severity**: Medium (limits reproducibility)
**Observed**: Python baseline scripts depend on external FASTQ data files (PRJNA488170, PRJNA382322, MiSeq_SOP) that must be downloaded separately via `scripts/download_paper_data.sh`. The composition has no mechanism to declare or fetch these dependencies.

**Impact**:
- Workloads silently skip or fail when data isn't present
- No content-addressed data resolution (nestGate has the primitives but isn't wired)
- Reproducibility depends on manual data setup

**Recommendation**: Wire nestGate into the dispatch pipeline. A workload TOML could declare `[data.inputs]` with content hashes. toadStool queries nestGate for cached data before execution. This is the natural evolution point for the `coralforge_pipeline.toml` graph that already references nestGate.

---

## Gap 5: No Automatic Results Archival — CLOSED

**Primal**: nestGate / loamSpine
**Status**: CLOSED (2026-05-04)
**Resolution**: `provenance_pipeline.sh` wraps toadStool execution with NestGate `storage.store`, rhizoCrypt `dag.event.append`, loamSpine `entry.append`, and sweetGrass `braid.create`. 14 artifacts stored, 24 DAG events, Merkle root committed, ed25519-witnessed braid created.

**Remaining evolution**: Native `--archive` flag in toadStool itself. A `[provenance]` section in workload TOMLs would enable toadStool to call the trio directly.

---

## Gap 6: No Cross-Gate Dispatch

**Primal**: songBird / biomeOS
**Severity**: Low (single-gate sufficient for now)
**Observed**: All workloads executed on the local toadStool instance. songBird is running but not participating in workload routing. biomeOS is not part of the Node Atomic composition.

**Impact**:
- Workloads can only run on the gate where `toadstool execute` is invoked
- No load balancing across the LAN cluster (which has multiple Cat6e-connected machines)
- The "lend a GPU to a friend" pattern requires cross-gate dispatch

**Recommendation**: This is the natural Phase 2 evolution. biomeOS deploy graphs already define cross-gate topologies. When a second Node Atomic is stood up on another machine (NUC, swiftGate), songBird can broker workload requests across gates.

---

## Gap 7: WASM/Container Workloads Not Exercised

**Primal**: toadStool
**Severity**: Low (not needed for wetSpring science)
**Observed**: toadStool registers both Native and WASM runtimes, but only Native was used. Container runtime listed in config but not registered during execution.

**Impact**:
- WASM and container dispatch paths are untested in a live composition
- Future workloads (e.g., containerized QIIME2, AlphaFold) would need these paths

**Recommendation**: Create a simple WASM workload TOML (hello-world level) to exercise the wasmi runtime end-to-end. Container runtime can wait until Podman/Docker is needed for a specific tool.

---

## Gap 8: toadStool Does Not Expand Environment Variables in TOMLs

**Primal**: toadStool
**Severity**: Medium (requires hardcoded absolute paths)
**Observed**: Shell variables like `${WETSPRING_DIR}` in workload TOML `command` and `args` fields are passed literally, not expanded. All 11 workload TOMLs required absolute paths.

**Impact**: Workload TOMLs are not portable across machines.

**Recommendation**: Expand `${VAR}` patterns in TOML fields before execution, or support a `[variables]` section.

---

## Gap 9: Provenance Trio API Ergonomics (Byte Arrays vs Hex Strings)

**Primal**: loamSpine / rhizoCrypt
**Severity**: Low (workaround in shell)
**Observed**: loamSpine `data_hash` and `merkle_root` require `[u8; 32]` JSON byte arrays, not hex strings. rhizoCrypt returns Merkle roots as hex strings. Conversion required in every call.

**Recommendation**: Accept both hex strings and byte arrays in JSON-RPC params.

---

## Gap 10: sweetGrass TCP Requires BTSP Handshake

**Primal**: sweetGrass
**Severity**: Low (HTTP endpoint available)
**Observed**: sweetGrass TCP port (9800) requires BTSP handshake. HTTP endpoint on dynamic port 39085 works without handshake.

**Recommendation**: Make BTSP optional on TCP, or document HTTP as the primary integration surface.

---

## Wins

1. **toadStool dispatch works end-to-end**: 11 workload TOMLs loaded, parsed, dispatched, and executed without modification to any primal binary
2. **235+ Rust validation checks passed through composition dispatch**: Full parity with standalone execution across 8 validators
3. **Real NCBI data processed**: 11.9M paired-end reads (PRJNA488170) through Rust, 50K through Python
4. **Full provenance pipeline operational**: BLAKE3 → rhizoCrypt DAG → loamSpine ledger → sweetGrass braid
5. **9 primals stable**: Nest Atomic + ToadStool ran for hours without crashes
6. **TOML workload format is expressive**: The `[metadata]` + `[execution]` + `[resources]` + `[security]` structure covers the dispatch needs well
7. **Sub-millisecond dispatch overhead**: Rust binaries completed in 1-2ms — the dispatch layer is not a bottleneck
8. **Provenance wrapper pattern validated**: Shell script brackets toadStool with pre/post RPC calls to the trio

---

## Next Cycles

| Priority | Gap | Owner Team | Effort | Status |
|----------|-----|------------|--------|--------|
| 1 | Sandbox working_dir passthrough | toadStool | Small | Open |
| 2 | Environment variable expansion in TOMLs | toadStool | Small | Open (Gap 8) |
| 3 | GPU API alignment (submit_and_map) | barraCuda / wetSpring | Small | Open |
| 4 | Data dependency declaration in TOML | toadStool / nestGate | Medium | Open |
| 5 | Results archival (--archive flag) | toadStool | Medium | Partially closed (wrapper exists) |
| 6 | Hex string acceptance in loamSpine | loamSpine / rhizoCrypt | Small | Open (Gap 9) |
| 7 | sweetGrass TCP without BTSP | sweetGrass | Small | Open (Gap 10) |
| 8 | Cross-gate dispatch via songBird | songBird / biomeOS | Large | Open |
| 9 | WASM runtime smoke test | toadStool | Small | Open |
| 10 | Python introspection sidecar | toadStool | Large (if needed) | Open |
