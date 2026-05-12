# hotSpring Deep Debt Push 3 — Handoff (May 11, 2026)

**From:** hotSpring (syntheticChemistry/hotSpring)
**To:** primalSpring coordination, upstream primal teams, sibling springs, projectNUCLEUS, foundation

---

## Summary

hotSpring completed three post-interstadial evolution pushes on May 11, 2026.
This handoff covers Push 3 (deep debt) and cumulative state.

**Current metrics:** 1,025 lib tests, 576 primal-proof tests, zero clippy warnings,
7 registered validation scenarios, 7 deploy graphs (all with skunkBat), 188
experiments, guideStone L6 CERTIFIED, 85 gaps tracked (all resolved or
documented).

---

## What changed (Push 3)

1. **NUCLEUS workload was broken — now fixed.** `hotspring-md-validation.toml`
   referenced `sarkas_yukawa_md` but no scenario matched. Created
   `sarkas-yukawa-md` scenario with foundation-grade validation (12 Daligault
   D* reference points, RMSE, CPU MD simulation with energy drift). All three
   workload TOMLs updated (NUCLEUS, foundation/hotspring, foundation/thread02_plasma).

2. **Foundation Thread 2 workload pipeline connected.** Created
   `workloads/thread02_plasma/hs-sarkas-md.toml` so
   `foundation_validate.sh --thread plasma` works. Fixed targets file
   `[meta].expression` to reference the expression doc.

3. **Fleet discovery evolved.** `discover_diesel_ember_socket()` uses XDG
   cascade (`$CORALREEF_RUN_DIR` → `$XDG_RUNTIME_DIR/coralreef` →
   `/run/coralreef`) instead of hardcoded path.

4. **Documentation fully aligned.** All docs (README, CHANGELOG, whitePaper,
   experiments, DOWNSTREAM_PATTERNS) reconciled to 1,025 tests / 188
   experiments / 7 scenarios / Level 6 / UniBin-first narrative.

---

## For upstream primal teams

### barraCuda
- **TensorSession adoption (GAP-HS-027):** hotSpring's GPU HMC pipeline still
  uses 22 deprecated per-iteration readback APIs, all properly gated behind
  `#[expect(deprecated)]`. Migration depends on TensorSession API stabilization
  for lattice workloads. No blocking action for hotSpring, but would benefit
  from upstream signal on timeline.

### coralReef
- **Sovereign GPU barriers (Low severity):** Titan V FECS secure boot requires
  PMU firmware (not in linux-firmware for GK210/GV100). K80 PCIe link training
  requires manual BAR0 MMIO. Both characterized; benchScale VM isolation is the
  production path. Owner: L3 (spring + coralReef).
- **Fleet discovery:** hotSpring now uses `coralreef_run_dir()` cascade for
  ember socket discovery. If coralReef standardizes a runtime dir env var,
  `CORALREEF_RUN_DIR` is what we check.

### toadStool
- **`$SPRINGS_ROOT` expansion (Gap 8):** NUCLEUS workload TOMLs use
  `$SPRINGS_ROOT` but toadStool template docs warn this is not expanded.
  Verify behavior when workloads are dispatched via real toadStool execution.

### nestGate — HIGH PRIORITY UPSTREAM
- **Not live for data chains.** hotSpring has the IPC client wired
  (`ipc/signing.rs`, `ipc/provenance/`), deploy graphs include nestGate,
  but actual data persistence and BLAKE3 content hashing depend on nestGate
  being operational. Next evolution round needs full data and compute chains
  through nestGate → rhizoCrypt → loamSpine → sweetGrass.
- **Foundation data sources** (`thread02_plasma.toml`) have empty `blake3` and
  `retrieved` fields — these can't be populated until nestGate is live for
  content-addressed storage.

### skunkBat
- **JH-5 ready.** `src/ipc/skunkbat.rs` module emits `security.audit_log`
  queries. 7/7 deploy graphs include skunkBat node. When Phase 3
  (cross-primal forwarding) ships, audit events propagate to rhizoCrypt DAG +
  sweetGrass braid automatically. No action needed from hotSpring.

### biomeOS
- **`composition.status` and `method.register` wired.** Both absorbed and
  operational in hotSpring's primal server.

---

## For sibling springs

### Patterns to absorb

1. **sarkas-yukawa-md scenario pattern:** Foundation-grade `validate` scenario
   that runs real physics (not just config checks). Dual-mode: full CPU
   simulation when `barracuda-local` enabled, transport math validation in
   `primal-proof` mode. Other springs should ensure their NUCLEUS workload
   scenario IDs match registered scenario `meta.id` values exactly.

2. **XDG cascade for fleet/runtime dirs:** Don't hardcode `/run/<service>/`.
   Use env var → XDG fallback → well-known default. Pattern in
   `fleet_client.rs::coralreef_run_dir()`.

3. **`#[cfg(feature = "barracuda-local")]` test gating:** Tests that import
   barracuda types need to be behind the feature gate too, not just production
   code. hotSpring has 576 tests passing in primal-proof mode.

4. **Deploy graph skunkBat coverage:** All graphs should include skunkBat
   defense/audit node. Check your graph count — if any are missing, add them.

### Level 6 certification path
hotSpring achieved L6 via: 5 substrates (x86_64 + aarch64) × 59 checks =
295 certification data points, UniBin consolidation, NUCLEUS workload TOMLs,
foundation seeding (12 validated targets). The pattern is documented in
`whitePaper/baseCamp/nucleus_composition_evolution.md`.

---

## For projectNUCLEUS

- **Workload TOML verified:** `hotspring-md-validation.toml` now uses correct
  scenario ID `sarkas-yukawa-md`. Workload will match and run 15+ checks (or
  20+ with barracuda-local).
- **Cell graph updated:** `hotspring_cell.toml` in plasmidBin now includes
  skunkBat (order 10), all primals renumbered.
- **`$SPRINGS_ROOT` risk:** Documented in toadStool section above.

---

## For foundation

- **Thread 2 fully wired:** Expression doc, 12 validated targets,
  `workloads/thread02_plasma/hs-sarkas-md.toml`, provenance manifest, and
  validation summary all in place. `foundation_validate.sh --thread plasma`
  execution path is live.
- **Next:** Populate `blake3` and `retrieved` fields in source anchors when
  nestGate content-addressed storage is live.

---

## Remaining hotSpring work (not blocking ecosystem)

| Item | Severity | Owner |
|------|----------|-------|
| Sovereign GPU barriers (Titan V FECS, K80 PCIe) | Low | L3 + coralReef |
| TensorSession migration (deprecated GPU HMC APIs) | Low | L3 + barraCuda |
| Paper queue Tier 4 (WDM papers 32-42) | Future | L3 |
| Paper queue Track 5 (distributed compute 25-31) | Future | L3 |
| NestGate BLAKE3 content hashing for foundation sources | Blocked | L1 (nestGate) |
| Live Science API counts update | Pending gate run | L4 (NUCLEUS) |
| Additional NUCLEUS workloads (nuclear EOS, spectral) | Future | L3 + L4 |
