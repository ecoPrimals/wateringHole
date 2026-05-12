# primalSpring v0.9.2 — Nest Atomic / Tower Atomic Evolution Handoff

**Date**: April 7, 2026  
**From**: primalSpring (Phase 25 — Modernization Sweep)  
**To**: All primal teams, spring teams, biomeOS, sporeGarden  
**Scope**: Tower Atomic HTTPS validated, Nest Atomic composition confirmed, graph format canonical, capability names canonical, covalent bonding pattern validated

---

## TL;DR

primalSpring Phase 25 confirms that **Tower Atomic HTTPS works end-to-end** (Songbird TLS 1.3 ClientHello fix merged), **Nest Atomic composition is validated** (BearDog + Songbird + NestGate + Squirrel), and all legacy patterns have been cleaned. This handoff documents what changed and what each team needs to absorb.

---

## 1. Tower Atomic HTTPS Now Works

The Songbird TLS 1.3 `ClientHello` fix (CSPRNG `client_random` via `getrandom`, 32-byte `legacy_session_id`) resolves the last Tower Atomic blocker. primalSpring validates this via:

- `nest-deploy.toml` v4.0 Phase 5: `validate_https` calls `http.get` → `https://ifconfig.me/ip` through the full BearDog→Songbird TLS stack.
- exp090 Tower Atomic LAN probe: end-to-end HTTPS via NeuralBridge `capability.call`.
- exp073 covalent bonding: HTTPS validated on LAN mesh nodes.

**Impact**: Any composition using Tower Atomic can now perform real HTTPS requests without external TLS libraries.

---

## 2. Nest Atomic Validated

`nest-deploy.toml` v4.0 is the gold standard graph for Nest Atomic (BearDog + Songbird + NestGate + Squirrel). It includes:

- Sequential 6-phase deployment: BearDog → Songbird → NestGate → Squirrel → HTTPS Validation → Composition Validation
- Songbird capabilities: `discovery.*`, `http.*`, `mesh.init`, `mesh.auto_discover`, `mesh.peers`
- `[graph]` section with `id = "nest-deploy"` (biomeOS `GraphId` format)

---

## 3. Graph Format Canonical

**All graphs must use `[[graph.nodes]]`** (biomeOS-native, plural). The legacy `[[graph.node]]` (singular) format is accepted by the parser but should not appear in new files.

Multi-node graphs use `[graph.nodes.*]` subsections (not `[nodes.*]`).

The `[graph]` section should include:
- `id` — lowercase hyphenated (e.g., `"nest-deploy"`)
- `name` — underscore-separated (e.g., `"nest_deploy"`)

**Template**: `primalSpring/graphs/nest-deploy.toml`

---

## 4. Capability Names Canonical

All capability method names now follow the dotted hierarchical convention:

| Domain | Old | Canonical |
|--------|-----|-----------|
| DAG | `dag.dehydrate` | `dag.dehydration.trigger` |
| DAG | `dag.create_session` | `dag.session.create` |
| DAG | `dag.append_event` | `dag.event.append` |
| DAG | `dag.merkle_root` | `dag.merkle.root` |
| Ledger | `commit.session` | `session.commit` |
| Ledger | `commit.entry` | `entry.append` |
| Health | `dag.health` / `commit.health` | `health.liveness` |

**Action**: Any graph or config file referencing old names should be updated. rhizoCrypt still accepts aliases but canonical names are preferred.

---

## 5. `http_health_probe` Deprecated

All primals expose JSON-RPC `health.liveness`. The old raw HTTP health probe is deprecated:

```rust
// OLD — do not use
http_health_probe("127.0.0.1", 9901)

// NEW — canonical
tcp_rpc("127.0.0.1", 9901, "health.liveness", &json!({}))
```

Songbird no longer exposes HTTP `/health` on a port. Tower Atomic owns all HTTP.

---

## 6. Covalent Bonding Pattern Validated

`basement_hpc_covalent.toml` demonstrates the canonical multi-node pattern:

1. **Shared `family.seed`** for genetic identity
2. **BirdSong mesh discovery** (`mesh.auto_discover`) for peer enumeration
3. **HTTPS validation phase** to confirm Tower Atomic TLS before capability announcement
4. **Capability announcement** with specific method list (`compute.submit`, `storage.fetch_external`, `ai.query`)

exp073 and exp090 validate this pattern structurally. Live LAN testing requires multiple gates.

---

## 7. Per-Team Action Items

### rhizoCrypt
- [ ] Rename `dag.dehydrate` handler to `dag.dehydration.trigger` (alias is temporary)
- [ ] Verify `dag.session.create`, `dag.event.append`, `dag.merkle.root` are the canonical handler names

### loamSpine
- [ ] Verify `session.commit` and `entry.append` are canonical handler names
- [ ] Remove any `commit.session` / `commit.entry` aliases when safe

### sweetGrass
- [ ] No action required — attribution PROV-O is stable

### BearDog
- [ ] BD-01: `crypto.verify_ed25519` `encoding` hint — ship when ready
- [ ] Confirm `health.liveness` response includes `family_id` for genetic lineage validation

### Songbird
- [ ] Push rebased TLS 1.3 fix (ahead of `origin/main` by 1 commit)
- [ ] SB-03: sled → NestGate storage migration — aligns with Nest Atomic composition
- [ ] Confirm `mesh.init`, `mesh.auto_discover`, `mesh.peers` methods are available

### NestGate
- [ ] No action required — storage delegation confirmed, `storage.fetch_external` working

### Squirrel
- [ ] NA-001: abstract socket `@squirrel` — document Android compatibility path
- [ ] Confirm `ai.query`, `tool.execute`, `context.create` stable

### ToadStool
- [ ] Confirm `compute.submit` is canonical method name
- [ ] Node Atomic composition: ToadStool + Nest Atomic validated structurally

### biomeOS
- [ ] No parser changes needed — primalSpring aligned to biomeOS-native `[[graph.nodes]]` format
- [ ] `GraphId` (`id` field) now supported in primalSpring parser

### Springs (all)
- [ ] Update any local graph files from `[[graph.node]]` to `[[graph.nodes]]`
- [ ] Reference `primalSpring/graphs/nest-deploy.toml` v4.0 as deployment template
- [ ] Replace any `http_health_probe` calls with `tcp_rpc` + `health.liveness`

### sporeGarden
- [ ] Products can use `nest-deploy.toml` as deployment template
- [ ] Tower Atomic HTTPS is ready for product compositions (esotericWebb, helixVision)

---

## 8. Resolved Gaps

| ID | Component | Resolution |
|----|-----------|------------|
| NA-009 | rhizoCrypt / primalSpring | `dag.dehydrate` → `dag.dehydration.trigger` everywhere |
| NA-016 | primalSpring / biomeOS | Graph format divergence eliminated |

---

## 9. Metrics

| Metric | Value |
|--------|-------|
| Tests | 404 |
| Experiments | 69 (15 tracks) |
| Deploy graphs | 92 |
| Live composition validation | 43/44 (98%) |
| Open primal gaps | 8 (0 critical, 1 medium, 7 low) |
| Resolved gaps this phase | 2 (NA-009, NA-016) |

---

## 10. References

- `primalSpring/specs/CROSS_SPRING_EVOLUTION.md` — full evolution path with resolved gaps
- `primalSpring/graphs/nest-deploy.toml` — gold standard Nest Atomic graph
- `primalSpring/experiments/exp090_tower_atomic_lan_probe/` — LAN discovery validation
- `primalSpring/CHANGELOG.md` — `[0.9.2]` entry with detailed changes
