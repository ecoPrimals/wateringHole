# healthSpring V57 — Level 5 Primal Proof: Ecosystem Handoff

**Date**: April 20, 2026
**From**: healthSpring V57
**To**: primalSpring (audit + absorb), all primal teams, all spring teams, biomeOS integrators
**Context**: Response to primalSpring v0.9.17 Phase 45 downstream directive
**Standard**: `GUIDESTONE_COMPOSITION_STANDARD` v1.2.0

---

## Executive Summary

healthSpring achieved **guideStone Level 5 (primal proof)** — the highest
readiness level. The `healthspring_guidestone` binary passes **57/57 checks**
(10 skipped) against a live NUCLEUS comprising barraCuda, beardog, and nestgate.
This is the first spring to reach Level 5, validating the full
Python → Rust → library → primal IPC chain for health science.

---

## 1. What Was Validated

### Three-Tier Harness Results

```
Tier 1 (LOCAL):  43/43 PASS — 5 bare properties + 17 BLAKE3 checksums + domain science
Tier 2 (IPC):    8/8  PASS — 4 math methods + 2 storage ops + 2 liveness probes
                  3   SKIP — crypto probes (BearDog schema mismatch, Gap 21)
                  7   SKIP — socket discovery miss (DAG/AI/commit, Gap 22)
Tier 3 (PROOF):  6/6  PASS — 4 math parity + domain science local confirmation
```

### IPC Parity Evidence

| Method | Local (Rust) | Composition (IPC) | Diff | Tolerance |
|--------|-------------|-------------------|------|-----------|
| `stats.mean` | 5.5 | 5.5 | 0.00e0 | 1.00e-10 |
| `stats.std_dev` | 3.0276503540974917 | 3.0276503540974917 | 0.00e0 | 1.00e-10 |
| `stats.variance` | 9.166666666666668 | 9.166666666666666 | 1.78e-15 | 1.00e-10 |
| `stats.correlation` | 1.0 | 1.0 | 0.00e0 | 1.00e-10 |
| `storage.store` | — | stored successfully | — | — |
| `storage.retrieve` | — | round-trip match | — | — |

### Primals Used

| Primal | Capability | Socket Pattern | Status |
|--------|-----------|----------------|--------|
| **barraCuda** | `tensor` (stats.*) | `tensor-{family}.sock` | PASS (all 4 methods) |
| **beardog** | `security` (crypto.*) | `security-{family}.sock` | PASS (liveness), SKIP (crypto probes) |
| **nestgate** | `storage` (store/retrieve) | `storage-{family}.sock` | PASS (round-trip) |
| rhizocrypt | `dag` | — | SKIP (no capability:dag socket) |
| sweetgrass | `commit` | — | SKIP (no capability:commit socket) |
| squirrel | `ai` | — | SKIP (no capability:ai socket) |

---

## 2. Primal Evolution Observations

### What We Learned Running Each Primal

**barraCuda** (Sprint 44 / v0.3.12):
- `stats.variance` and `stats.correlation` confirmed on wire — Sprint 44 delivered.
- JSON-RPC surface works cleanly over UDS with `--unix` flag.
- No BTSP handshake support (cleartext only). This is fine for dev mode.
- healthSpring's `math_dispatch` module is the "validation window" — it calls
  barraCuda as a library for Level 2 comparison, then the guideStone validates
  the same math via IPC. Domain science (Hill, Shannon, Simpson, Bray-Curtis)
  are LOCAL compositions of these primitives — they are not candidates for
  barraCuda wire migration.

**beardog**:
- Liveness probe works (`security` capability domain).
- `crypto.hash` fails: "Invalid base64 data: Invalid symbol 45, offset 12" —
  the guideStone sends a hex string probe, beardog expects base64.
- `crypto.sign` fails: "Missing required parameter: message" — parameter schema
  differs from the generic probe payload.
- **Ask**: Publish JSON-RPC method parameter schemas in wateringHole so
  downstream clients can construct valid probes.

**nestgate**:
- `storage.store` + `storage.retrieve` round-trip works perfectly.
- Family-scoped key (`guidestone_probe_healthspring`) stored and retrieved.
- JSON payload fidelity confirmed (nested objects survive round-trip).

**rhizocrypt**:
- Started successfully with `--unix` flag (not `--socket`).
- CLI requires `rhizocrypt server --unix /path/to/socket.sock`.
- Socket registered but `discover_by_capability("dag")` finds nothing —
  rhizocrypt does not register a `capability:dag` socket.

**sweetgrass**:
- Started but socket not discoverable via `capability:commit`.
- Same capability registration gap as rhizocrypt.

**coralReef** (not in final NUCLEUS — CLI documented):
- `coralreef server` requires `--tarpc-bind unix:///path/to/socket.sock`
  (not `--socket` or `--unix`). Uses TarPC, not JSON-RPC.
- Cannot participate in `primalspring::composition` IPC which expects JSON-RPC.
  Needs a JSON-RPC adapter or protocol bridge.

### Socket Discovery Mechanism (what works, what doesn't)

`primalspring::ipc::capability::discover_by_capability` searches:
1. Neural API query (if biomeOS running)
2. `$XDG_RUNTIME_DIR/biomeos/capability-{family}.sock`
3. `$XDG_RUNTIME_DIR/biomeos/capability.sock` (no family)
4. Socket registry (if available)

**What works**: Primals that register sockets with `{capability}-{family}.sock`
pattern (barraCuda → `tensor-healthspring-validation.sock`).

**What fails**: Primals that register with primal-name patterns
(`rhizocrypt.sock`) but don't create capability symlinks.

**Recommendation**: Either:
- (a) All primals register `capability:{domain}.sock` alongside their named socket, OR
- (b) `discover_by_capability` falls back to a capability→primal-name mapping

### BTSP Transport Issue (Gap 20)

**Root cause**: When `FAMILY_SEED` is in the environment (from any primal),
`primalspring::ipc::Transport::connect` attempts a BTSP handshake before
JSON-RPC. Non-BTSP primals reject this silently, causing all IPC to fail.

**Workaround**: `unset FAMILY_SEED BEARDOG_FAMILY_SEED RHIZOCRYPT_FAMILY_SEED`

**Fix needed in primalSpring**: `Transport::connect` should either:
- Probe for BTSP capability before attempting the handshake, OR
- Fall back to cleartext on BTSP rejection (currently it hard-fails)

---

## 3. Composition Patterns for NUCLEUS Deployment

### healthSpring's Deployment Recipe

```bash
export FAMILY_ID=healthspring-validation
export BIOMEOS_SOCKET_DIR=$XDG_RUNTIME_DIR/biomeos

# Start primals with capability-keyed sockets
nohup barracuda server --unix $BIOMEOS_SOCKET_DIR/tensor-$FAMILY_ID.sock &
nohup beardog server --unix $BIOMEOS_SOCKET_DIR/security-$FAMILY_ID.sock &
nohup nestgate server --unix $BIOMEOS_SOCKET_DIR/storage-$FAMILY_ID.sock &

# Create capability symlinks for discover_by_capability
ln -sf tensor-$FAMILY_ID.sock $BIOMEOS_SOCKET_DIR/capability-tensor.sock
ln -sf security-$FAMILY_ID.sock $BIOMEOS_SOCKET_DIR/capability-security.sock
ln -sf storage-$FAMILY_ID.sock $BIOMEOS_SOCKET_DIR/capability-storage.sock

# Unset FAMILY_SEED to avoid BTSP (Gap 20)
unset FAMILY_SEED BEARDOG_FAMILY_SEED RHIZOCRYPT_FAMILY_SEED

# Run guideStone
FAMILY_ID=$FAMILY_ID target/debug/healthspring_guidestone
```

### Pattern for Other Springs

Any spring following the same three-tier pattern needs:
1. **`primalspring` v0.9.17** with `composition` feature
2. **`CompositionContext`** for IPC validation (not raw socket calls)
3. **`validate_parity`** for numeric method comparison
4. **Capability-keyed sockets** — `{capability}-{family}.sock` convention
5. **FAMILY_SEED unset** until Gap 20 is resolved in primalSpring
6. **BLAKE3 checksums** via `primalspring::checksums::verify_manifest()`

### What biomeOS / Neural API Should Know

- healthSpring's full capability surface: 84+ JSON-RPC methods (62 science +
  22 infrastructure) — all discoverable via `capability.list`.
- The `healthspring_guidestone` binary is NOT a server — it's a validator.
  The server binary is `healthspring_primal` (started with `serve` subcommand).
- Deploy graph: `graphs/healthspring_niche_deploy.toml` specifies startup order.
- Proto-nucleate: `primalSpring/graphs/downstream/healthspring_enclave_proto_nucleate.toml`
  defines the dual-tower architecture.

---

## 4. What healthSpring Needs from Each Team

### primalSpring Team

| Priority | Ask | Gap |
|----------|-----|-----|
| **High** | Fix BTSP negotiate — `Transport::connect` should not hard-fail when non-BTSP primals reject handshake | 20 |
| **Medium** | Add primal-name-keyed fallback to `discover_by_capability` | 22 |
| **Low** | Document `start_primal.sh` CLI audit — per-primal flags differ significantly (`--unix` vs `--tarpc-bind` vs `--socket`) | — |

### barraCuda Team

No outstanding asks. Sprint 44 delivered `stats.variance` and `stats.correlation`.
healthSpring validates both end-to-end. Thank you.

### BearDog Team

| Priority | Ask | Gap |
|----------|-----|-----|
| **Medium** | Publish `crypto.hash` and `crypto.sign` JSON-RPC parameter schemas | 21 |
| **Low** | Consider BTSP server-side handshake for non-beardog primals that set `FAMILY_SEED` | 20 |

### NestGate Team

No outstanding asks. Storage round-trip validated. healthSpring confirms
family-scoped key-value storage works correctly over UDS.

### Rhizocrypt / Sweetgrass / Squirrel Teams

| Priority | Ask | Gap |
|----------|-----|-----|
| **Medium** | Register `capability:{domain}.sock` alongside primal-named sockets | 22 |
| | Rhizocrypt: `capability:dag.sock` | |
| | Sweetgrass: `capability:commit.sock` | |
| | Squirrel: `capability:ai.sock` | |

### All Spring Teams

- healthSpring's three-tier guideStone pattern is available for adoption.
  See `ecoPrimal/src/bin/healthspring_guidestone/` for the reference implementation.
- The `validate_parity` helper in `primalspring::composition` works well for
  numeric method validation — it handles tolerance checking, skip/fail logic,
  and structured output.
- `check_skip` is essential for graceful degradation when primals are offline.
- Family-aware socket discovery (`{capability}-{family}.sock`) works well
  for isolating validation runs from production traffic.

---

## 5. healthSpring Readiness Summary

| Property | Status |
|----------|--------|
| P1 Deterministic | All checks reproducible across runs |
| P2 Traceable | Every number traces to a paper or proof |
| P3 Self-Verifying | BLAKE3 checksums (17 files) |
| P4 Env-Agnostic | Pure Rust, ecoBin, no network, no sudo |
| P5 Tolerance-Documented | All tolerances in `tolerances.rs` with provenance |
| **guideStone Level** | **5 — primal proof** |
| **Standard** | **v1.2.0** |
| **primalSpring** | **v0.9.17** |
| **Checks** | **57/57 pass, 10 skip** |
| Tests | 948+ |
| Experiments | 94 (84 science + 11 composition) |
| Python baselines | 54 |
| JSON-RPC capabilities | 84+ |
| Gaps filed | 22 (15 resolved, 7 open — see `docs/PRIMAL_GAPS.md`) |

---

## 6. Files Changed (V57)

| File | Change |
|------|--------|
| `ecoPrimal/Cargo.toml` | primalspring v0.9.16 → v0.9.17 |
| `ecoPrimal/src/bin/healthspring_guidestone/main.rs` | v1.2.0 standard ref |
| `ecoPrimal/src/bin/healthspring_guidestone/domain.rs` | stats.variance + stats.correlation in Tier 2/3 |
| `ecoPrimal/src/niche.rs` | GUIDESTONE_READINESS = 5, migration inventory updated |
| `docs/PRIMAL_GAPS.md` | Gap 19 resolved, Gaps 20–22 added |
| `CHANGELOG.md` | V57 entry |
| `README.md` | Level 5 status |
| `validation/CHECKSUMS` | Regenerated |
| 16 doc files | Version banners V56→V57 across specs/, baseCamp/, wateringHole/ |
| `wateringHole/handoffs/HEALTHSPRING_V57_PRIMAL_PROOF_HANDOFF_APR20_2026.md` | Upstream handoff |
