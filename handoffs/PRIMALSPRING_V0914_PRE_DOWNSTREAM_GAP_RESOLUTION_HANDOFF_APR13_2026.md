# primalSpring v0.9.14 — Pre-Downstream Gap Resolution Handoff

**Date**: April 13, 2026
**From**: primalSpring (coordination spring)
**To**: All primal teams + all downstream spring teams
**Phase**: 41 — Pre-Downstream Gap Resolution
**Supersedes**: `PRIMALSPRING_V0913_NUCLEUS_COMPLETE_HANDOFF_APR13_2026.md`

---

## Summary

This handoff documents the gap resolution work performed after NUCLEUS Complete
(12/12 ALIVE, 19/19 exp094 PASS) and before handing downstream to springs for
absorption. Seven blocking and confusing gaps were identified during NUCLEUS
atomic validation and bonding model testing, then resolved in a single sprint.

**Key numbers**: 443 lib tests, 73 experiments (16 tracks), 67 deploy graphs +
6 fragments, 13 FullNucleus capabilities, 5 bonding models validated structurally.

---

## What Was Fixed (7 Items)

### 1. Songbird Capability Alias Mismatch (BLOCKING -> RESOLVED)

**Problem**: `ipc.resolve("ledger")` and `ipc.resolve("attribution")` returned
"No provider found" because loamSpine registers as `["spine", "merkle"]` and
sweetGrass as `["commit", "braid"]`.

**Fix**:
- `nucleus_launcher.sh` Phase 5 seeding now registers alias names:
  loamSpine = `spine,merkle,ledger`, sweetGrass = `commit,braid,attribution`,
  petaltongue = `visualization`, songbird = `discovery`
- `AtomicType::FullNucleus` expanded from 11 to **13 capabilities**
  (added `ledger`, `attribution`)
- `capability_to_primal()` maps all self-reported names: `spine`/`merkle`/`ledger`
  -> loamSpine, `commit`/`braid`/`attribution` -> sweetGrass, `provenance` -> rhizoCrypt

**Impact on primal teams**: None required. Songbird Phase 5 seeding handles aliases.
**Impact on springs**: `ipc.resolve("ledger")` and `ipc.resolve("attribution")` now work.

### 2. validate_parity Doc Examples (BLOCKING -> RESOLVED)

**Problem**: Module-level and function-level doc examples in `composition/mod.rs`
used `tensor.matmul` with inline matrices. barraCuda's `tensor.matmul` uses
session-based tensor IDs, not inline data. Springs copying the example would fail.

**Fix**: All doc examples updated to `stats.mean` with correct params:
- Parameter key: `"data"` (not `"values"`)
- Result key: `"result"` (not `"mean"`)
- `NICHE_STARTER_PATTERNS.md` `tensor.softmax` result key: `"values"` -> `"result"`

**Impact on springs**: Copy the doc example pattern verbatim. It works.

### 3. validate_parity_vec Silent Element Drop (BLOCKING -> RESOLVED)

**Problem**: `filter_map(as_f64)` silently dropped non-numeric elements. A primal
returning `[1.0, null, 3.0]` would produce `[1.0, 3.0]` (length 2), causing a
confusing "length mismatch" error.

**Fix**: Added explicit detection: if any array element is non-numeric, the check
fails immediately with a clear message identifying how many elements were dropped.

**Impact on springs**: Better error messages when primal responses contain nulls.

### 4. BtspEnforcer Cipher-Only Enforcement (CONFUSING -> DOCUMENTED)

**Problem**: `BtspEnforcer::evaluate_connection` always sets `allowed: true`.
Connections are never denied — weak ciphers are upgraded, not rejected.

**Documentation added**:
- Struct-level and method-level Rust docs on `BtspEnforcer`
- Downstream README: "Bonding & BTSP Enforcement" section with full table
- If your spring needs to deny unknown peers, implement your own guard layer

| Bond Type | Min Cipher | Behaviour |
|-----------|------------|-----------|
| Covalent | Null | Same-family, full trust |
| Metallic | Aes256Gcm | Org-level, strong cipher |
| Ionic | ChaCha20Poly1305 | Cross-family, cipher upgraded |
| Weak | ChaCha20Poly1305 | Unknown peer, cipher upgraded but **not rejected** |
| OrganoMetalSalt | ChaCha20Poly1305 | Hybrid, same upgrade semantics |

### 5. Multi-Node Graph Schema (CONFUSING -> UNIFIED)

**Problem**: `graphs/multi_node/*.toml` used `id` instead of `name`, had nested
`[graph.nodes.primal]`/`[graph.nodes.operation]` sub-tables, and no `binary` or
`order` fields. `graph.validate` could not parse them.

**Fix**:
- `GraphNode.name` now accepts `id` as serde alias
- `binary`, `order`, `health_method` default when absent
- `primal`, `operation`, `constraints`, `output` captured as opaque fields
- `structural_checks()` skips binary/health/order validation for multi-node graphs
- 2 new tests confirm parsing of `basement_hpc_covalent.toml` and `data_federation_cross_site.toml`
- `graphs/multi_node/README.md` documents the schema differences

**Impact on springs**: Multi-node graphs can now be loaded by `DeployGraph`. Springs
doing multi-node deployment no longer need a separate parser.

### 6. loamSpine health.check Auto-Param (CONFUSING -> RESOLVED)

**Problem**: loamSpine's `health.check` requires `{"include_details": true}` while
all other primals accept empty params. Uniform health sweeps would fail on loamSpine.

**Fix**: `CompositionContext::health_check()` now automatically sends the required
param for loamSpine capabilities (`ledger`, `spine`, `merkle`).

**Impact on springs**: Health sweeps via `CompositionContext` just work.
Manual callers should send `{"include_details": true}` for loamSpine.

### 7. rhizoCrypt dag.event.append Event Type Reference (CONFUSING -> DOCUMENTED)

**Problem**: `event_type` requires Rust-style tagged enum syntax, not plain strings.
Springs would need to know the 27 variant names and their required fields.

**Documentation added** to `graphs/downstream/README.md`:
- 4 worked JSON examples: `DataCreate`, `AgentAction`, `ExperimentStart`, `Custom`
- Complete 27-variant table with domains and required fields

---

## Wire Method Reference (Validated April 13, 2026)

Springs should use these exact schemas for `validate_parity` and direct IPC calls:

| Method | Params | Returns |
|--------|--------|---------|
| `stats.mean` | `{"data": [f64...]}` | `{"result": f64}` |
| `tensor.create` | `{"shape": [usize], "data": [f64]}` | `{"tensor_id": str}` |
| `storage.store` | `{"key": str, "value": str}` | `{"status": "stored"}` |
| `dag.session.create` | `{"label": str}` | bare UUID string |
| `dag.event.append` | `{"session_id": str, "event_type": {"DataCreate": {...}}, "payload": {}}` | `{"vertex_id": str}` |
| `braid.create` | `{"data_hash": str, "agent": str, "mime_type": str, "size": u64}` | `{"braid_id": str}` |
| `spine.create` | `{"name": str, "owner": str}` | `{"spine_id": UUID}` |
| `crypto.hash` | `{"data": base64, "algorithm": "blake3"}` | `{"hash": base64(44)}` |
| `health.liveness` | `{}` (loamSpine: `{"include_details": true}`) | `{"alive": true}` |

---

## Composition Pattern for Springs

Every spring should follow this pattern for NUCLEUS parity validation:

```rust
use primalspring::composition::{CompositionContext, validate_parity};
use primalspring::tolerances;
use primalspring::validation::ValidationResult;

let mut ctx = CompositionContext::from_live_discovery();
let mut v = ValidationResult::new("mySpring — NUCLEUS parity");

validate_parity(
    &mut ctx, &mut v,
    "my_check_name",
    "tensor",                                    // capability
    "stats.mean",                                // method
    serde_json::json!({"data": [1.0, 2.0, 3.0]}),
    "result",                                    // result key
    2.0_f64,                                     // expected
    tolerances::CPU_GPU_PARITY_TOL,
);
```

The 13 FullNucleus capabilities (any of which can be used as the `capability` arg):
`security`, `discovery`, `compute`, `tensor`, `shader`, `storage`, `ai`, `dag`,
`commit`, `provenance`, `visualization`, `ledger`, `attribution`

---

## Primal Evolution Notes for Teams

| Primal | What Changed | Action Required |
|--------|-------------|-----------------|
| **BearDog** | `crypto.hash` base64 normalized, BTSP handshake on all connections | None |
| **Songbird** | Phase 5 seeding includes alias names, self-healing 30s socket rescan | None |
| **barraCuda** | `stats.mean` uses `"data"` param / `"result"` key, BTSP guard line replayed | None |
| **coralReef** | Capability `"shader"` (was `"shader,compile"` in launcher) | None |
| **ToadStool** | BTSP auto-detect on all transports | None |
| **NestGate** | Persistent UDS connections, crypto delegation to BearDog | None |
| **rhizoCrypt** | UDS unconditional, `dag.event.append` event_type is typed enum | Document enum variants for domain springs |
| **loamSpine** | `health.check` requires `include_details` param | Upstream: fix to accept empty params |
| **sweetGrass** | `braid.create` requires `mime_type` + `size` params | None |
| **petalTongue** | `--socket` CLI flag for NUCLEUS launcher alignment | None |
| **Squirrel** | AI router, MCP tools, abstract socket discovery | None |
| **biomeOS** | DOWN during testing sessions (11/12 primals) | Needs investigation |

---

## Remaining Structural Debt

These items do NOT block downstream handoff but should be planned:

### benchScale Integration (5 gaps)
1. `create-lab.sh` doesn't handle ecoPrimals topology YAML
2. `deploy-ecoprimals.sh` doesn't apply launch profile env vars
3. `FAMILY_ID` mismatch between topology and validation scripts
4. `mesh.peers` needs multiple Songbird instances
5. No harvested binaries in plasmidBin for container deployment

### Bonding Experiments: 13 Skipped Live Checks
All require 2+ NUCLEUS instances via benchScale Docker labs:
`family_seed_sharing`, `mesh_auto_discover_second_gate`, `cross_gate_capability_call`,
`cross_family_capability_sharing`, `plasmodium_formation`, `query_collective`,
`capability_aggregation`, `gate_failure`, `graceful_degradation`,
`capability_aggregation_routing` (exp030-034)

### Other
- `capability_to_primal()` passthrough: `other => other` for unknown capabilities
  may silently connect to wrong primal socket
- biomeOS DOWN: Neural API composition validation skips in exp001/exp004
- `graph.deploy` via biomeOS is untested

---

## What Downstream Springs Can Now Do

1. **Copy the validate_parity pattern** from `graphs/downstream/README.md` verbatim
2. **Use `ipc.resolve` for all 13 capabilities** including `ledger` and `attribution`
3. **Run uniform health sweeps** via `CompositionContext::health_check()` (loamSpine handled)
4. **Load multi-node graphs** via `DeployGraph` (id/name alias, nested sub-tables captured)
5. **Reference rhizoCrypt event_type variants** from the downstream README table
6. **Trust validate_parity_vec** to catch non-numeric elements with clear errors
7. **Rely on cipher enforcement** for bonding (understand: upgrade-only, no deny path)

---

**License**: AGPL-3.0-or-later (code) / CC-BY-SA 4.0 (documentation)
