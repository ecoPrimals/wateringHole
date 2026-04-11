<!--
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# wetSpring V142 — Wire Standard + Composition Evolution Handoff

| Field | Value |
|-------|-------|
| **Spring** | wetSpring |
| **Version** | V142 |
| **Date** | 2026-04-11 |
| **barraCuda** | 0.3.11 |
| **Wire Standard** | L2 + L3 compliant |
| **Status** | All quality gates green |

---

## Summary

wetSpring V142 completes Capability Wire Standard v1.0 compliance (L2+L3),
adds WireWitnessRef provenance encoding per Attestation Encoding Standard v2.0,
aligns to barraCuda 0.3.11, and declares 22 consumed capabilities for biomeOS
composition validation. This handoff documents patterns for absorption by
primal teams, sibling springs, and ecosystem infrastructure.

The validation narrative now has three complete tiers:
1. **Python validates Rust** — 58 scripts → 1,946 tests, 5,800+ checks
2. **Rust + Python validate NUCLEUS composition** — 97/97 proto-nucleate, 21 domains, cross-checks
3. **Composition self-describes via Wire Standard** — L2+L3, 22 consumed caps, identity.get, witnesses

---

## What Changed (for primal/spring teams)

### 1. Capability Wire Standard v1.0 Compliance

**Pattern for all primals/springs to adopt:**

`capabilities.list` now returns the canonical envelope:

```json
{
  "primal": "wetspring",
  "version": "0.1.0",
  "domain": "ecology",
  "methods": ["science.diversity", "science.anderson", "health.liveness", ...],
  "provided_capabilities": [
    {"type": "ecology.diversity", "description": "...", "methods": ["science.diversity"]},
    ...
  ],
  "consumed_capabilities": [
    "crypto.sign_ed25519", "compute.dispatch.submit", "storage.store",
    "dag.session.create", "braid.create", "inference.complete", ...
  ],
  "capabilities": ["capability.list", "identity.get", "health.check", ...],
  "operation_dependencies": {...},
  "cost_estimates": {...}
}
```

Key fields by compliance level:
- **L1**: `primal`, `version` (minimum)
- **L2**: + `methods` flat string array (biomeOS v2.93+ reads this first)
- **L3**: + `provided_capabilities`, `consumed_capabilities`, `cost_estimates`, `operation_dependencies`

**Action for primals:** Add `methods` to your `capabilities.list` response.
biomeOS v2.93+ parses `result.methods` first and skips legacy format detection.

### 2. `identity.get` Handler

New JSON-RPC method:

```json
{"jsonrpc": "2.0", "method": "identity.get", "params": {}, "id": 1}
→ {"primal": "wetspring", "version": "0.1.0", "domain": "ecology", "license": "AGPL-3.0-or-later"}
```

**Action for primals/springs:** Implement `identity.get`. Four fields, no params.
Used by biomeOS observability and cross-spring composition validation.

### 3. Consumed Capabilities Declaration

wetSpring now declares what it needs from other primals (22 capabilities):

| Atomic | Capabilities |
|--------|-------------|
| Tower | `crypto.sign_ed25519`, `crypto.verify_ed25519`, `crypto.blake3_hash`, `discovery.find_primals`, `discovery.announce` |
| Node | `compute.dispatch.submit`, `math.tensor`, `math.stats`, `math.spectral`, `shader.compile.wgsl` |
| Nest | `storage.store`, `storage.retrieve`, `dag.session.create`, `dag.event.append`, `spine.create`, `entry.append`, `braid.create`, `braid.commit` |
| Meta | `ai.complete`, `inference.complete`, `inference.embed`, `render.dashboard` |

**Action for biomeOS:** Use `consumed_capabilities` to validate composition
completeness at deploy time — if a spring declares it needs `dag.session.create`
and no primal in the graph provides it, flag a composition gap.

**Action for primals:** Ensure your `provided_capabilities` includes all
capabilities springs consume from you.

### 4. WireWitnessRef Provenance Events

Per Attestation Encoding Standard v2.0, provenance handlers now emit
`witnesses` arrays with self-describing events:

```json
{
  "session_id": "...",
  "provenance": "available",
  "witnesses": [{
    "agent": "wetspring:pipeline",
    "kind": "timestamp",
    "evidence": "",
    "witnessed_at": 1744300800000000000,
    "encoding": "none",
    "tier": "open",
    "context": "provenance:begin:experiment_name"
  }]
}
```

Witness `kind` values: `signature`, `hash`, `checkpoint`, `marker`, `timestamp`.

**Action for trio primals (rhizoCrypt, loamSpine, sweetGrass):** Accept
`witnesses` array in your APIs. Pass witnesses through opaquely — the trio
carries them, never interprets or transforms evidence.

### 5. barraCuda 0.3.11 Compatibility

`crate::gpu::context` module went private in 0.3.11. `GpuContext` is now
re-exported directly under `crate::gpu`. Any spring/primal referencing
`crate::gpu::context::GpuContext` must change to `crate::gpu::GpuContext`.

**Action for springs using barraCuda GPU:** Search for `gpu::context::GpuContext`
and update to `gpu::GpuContext`.

### 6. Provenance Trio IPC Wiring (Partial)

wetSpring now has runtime IPC paths for all three provenance primals:
- `dag.session.create`, `dag.event.append`, `dag.dehydrate` → rhizoCrypt
- `session.commit` → loamSpine
- `braid.create`, `braid.commit` → sweetGrass

All paths degrade gracefully when the trio is unavailable. Once trio primals
are IPC-ready, wetSpring's existing wiring routes to them transparently.

**Action for trio teams:** Publish stable IPC endpoints. wetSpring is ready
to call them.

---

## Composition Patterns for NUCLEUS Deployment via Neural API

### Socket Discovery Cascade

```
$NEURAL_API_SOCKET → $BIOMEOS_SOCKET_DIR → $XDG_RUNTIME_DIR/biomeos/ → temp_dir()
```

Socket name: `neural-api-{FAMILY_ID}.sock`

### Composition Health Probes

wetSpring implements 5 composition health handlers per `COMPOSITION_HEALTH_STANDARD.md`:

| Method | Atomic | What it probes |
|--------|--------|---------------|
| `composition.science_health` | Spring-specific | Science pipeline, GPU, provenance trio |
| `composition.tower_health` | Tower | BearDog (security) + Songbird (discovery) |
| `composition.node_health` | Node | BearDog + ToadStool (compute) |
| `composition.nest_health` | Nest | BearDog + NestGate (storage) |
| `composition.nucleus_health` | NUCLEUS | Tower + Node + Nest + provenance trio |

Each probes primals via `capability.discover` over the Neural API socket.
Response shape per standard: `{healthy, atomic, spring, components, ...}`.

### Deploy Graph → Proto-nucleate → Niche Alignment

Validated chain:
1. `primalSpring/graphs/downstream/wetspring_lifescience_proto_nucleate.toml` (14 nodes)
2. `niche.rs` DEPENDENCIES (9 primals: 5 required + 4 optional)
3. `niche.rs` CAPABILITIES (46 methods)
4. `niche.rs` CONSUMED_CAPABILITIES (22 from other primals)
5. `capability_domains.rs` DOMAINS (21 groups, 41 methods)
6. `dispatch.rs` (42 routed methods including identity.get)
7. Cross-check tests enforce sync in CI

**Pattern for other springs:** Wire your niche to your proto-nucleate TOML at
test time. Add cross-check tests. Declare both provided and consumed capabilities.

---

## plasmidBin Harvest Status

| Field | Value |
|-------|-------|
| `manifest.lock` version | 0.8.0 (aligned) |
| `metadata.toml` version | 0.8.0 |
| `barracuda_version` | 0.3.11 |
| `tests` | 1,946 |
| `capabilities` | includes `identity.get` |
| `checksum_sha256` | pending `./harvest.sh wetspring` |

**Next step:** Build `musl` static binaries, copy to plasmidBin, run `./harvest.sh`.

---

## Primal Evolution Asks

### For barraCuda
- No new asks — 0.3.11 alignment complete, 150+ primitives consumed

### For toadStool
- PG-05 still open: `discover_toadstool()` helper exists but no active compute
  dispatch calls. Will become relevant at NUCLEUS deployment.

### For Songbird / biomeOS
- PG-03: Capability discovery is still name-based (`discover_squirrel()` etc.).
  Need `capability.resolve` → socket path mapping for true capability-first routing.
- `consumed_capabilities` field is ready for biomeOS to parse for composition
  completeness validation.

### For rhizoCrypt / loamSpine / sweetGrass
- IPC wiring exists in wetSpring. Waiting for stable trio endpoints.
- `WireWitnessRef` format ready for trio to accept.

### For NestGate
- PG-04: Still declared-but-not-wired for storage IPC.

### For primalSpring
- Binary naming: proto-nucleate says `wetspring_primal`, plasmidBin says `wetspring`.
  Recommend aligning on `wetspring`.
- Deploy graph `wetspring_deploy.toml` fragments metadata says `tower_atomic` only
  but nodes include Node/Nest/Meta primals. Recommend updating fragments to
  `["tower_atomic", "node_atomic", "nest_atomic", "meta_tier"]`.

---

## Quality Gates

| Check | Status |
|-------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy --all-features -D warnings` | 0 warnings |
| `cargo test --workspace` | 1,620 passed, 0 failed |
| `cargo test --all-features` | 1,686 passed, 4 GPU-hardware-only |
| Wire Standard | L2 + L3 |
| `identity.get` | Implemented |
| `WireWitnessRef` | Integrated |
| `forbid(unsafe_code)` | Enforced |
| `#[allow()]` | 0 in production |
| Proto-nucleate test | 97/97 |

---

*This handoff is maintained by wetSpring and archived in
`infra/wateringHole/handoffs/`. Previous handoffs: V139 (composition validation),
V138 (primal composition patterns), V137 (provenance + tolerance + IPC).*
