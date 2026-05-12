# primalSpring → wetSpring: Capability Routing Corrections

**From:** primalSpring (nexus)
**To:** wetSpring
**Date:** April 7, 2026
**Priority:** CRITICAL — Tier 2 provenance will fail at runtime without these fixes

---

## Context

We audited biomeOS's `capability.call` routing against wetSpring's
`barracuda/src/facade/provenance.rs` and found 3 operation-name mismatches
that will prevent live trio calls from routing correctly.

### How `capability.call` works

```text
capability.call({ capability: DOMAIN, operation: OP, args: {...} })
  → biomeOS constructs method name: "{DOMAIN}.{OP}"
  → biomeOS discovers primal by DOMAIN (exact key in capability registry)
  → biomeOS forwards JSON-RPC method "{DOMAIN}.{OP}" to primal endpoint
  → primal must handle method "{DOMAIN}.{OP}" in its dispatch
```

The DOMAIN must be registered (by graph loading or primal auto-discovery).
The `{DOMAIN}.{OP}` must exactly match the primal's JSON-RPC method name.

---

## Fixes Required (3 calls in `provenance.rs`)

### Fix 1: `dag.create_session` → `dag.session.create`

```rust
// CURRENT (line ~199):
capability_call(&neural_socket, "dag", "create_session", &args)
// biomeOS constructs: "dag.create_session" — rhizoCrypt has NO such method

// CORRECT:
capability_call(&neural_socket, "dag", "session.create", &args)
// biomeOS constructs: "dag.session.create" — matches rhizoCrypt's method ✓
```

### Fix 2: `("commit", "session")` → `("session", "commit")`

```rust
// CURRENT (line ~255):
capability_call(&neural_socket, "commit", "session", &args)
// biomeOS constructs: "commit.session" — loamSpine has NO such method

// CORRECT:
capability_call(&neural_socket, "session", "commit", &args)
// biomeOS constructs: "session.commit" — matches loamSpine's method ✓
```

### Fix 3: `("provenance", "create_braid")` → `("braid", "create")`

```rust
// CURRENT (line ~273):
capability_call(&neural_socket, "provenance", "create_braid", &args)
// biomeOS constructs: "provenance.create_braid" — sweetGrass has NO such method

// CORRECT:
capability_call(&neural_socket, "braid", "create", &args)
// biomeOS constructs: "braid.create" — matches sweetGrass's method ✓
```

### Already correct (no changes needed)

| Call | Semantic name | Primal | Status |
|------|--------------|--------|--------|
| `("dag", "event.append")` | `dag.event.append` | rhizoCrypt | ✅ |
| `("dag", "dehydrate")` | `dag.dehydrate` | rhizoCrypt | ✅ |
| `("provenance", "export_provo")` | `provenance.export_provo` | sweetGrass | ✅ |

---

## Routing rule

The DOMAIN is the **first segment** of the primal's method name (before the
first dot). The OPERATION is the **remaining segments**.

```text
Primal method:     dag.session.create
                   ^^^─────────┬──────
Split:         domain="dag"  operation="session.create"
Consumer call: capability_call(socket, "dag", "session.create", args)
```

---

## Complete trio routing table

### rhizoCrypt (domain: `dag`)

| Method | capability.call domain | operation |
|--------|----------------------|-----------|
| `dag.session.create` | `dag` | `session.create` |
| `dag.session.get` | `dag` | `session.get` |
| `dag.session.list` | `dag` | `session.list` |
| `dag.event.append` | `dag` | `event.append` |
| `dag.vertex.get` | `dag` | `vertex.get` |
| `dag.frontier.get` | `dag` | `frontier.get` |
| `dag.merkle.root` | `dag` | `merkle.root` |
| `dag.merkle.proof` | `dag` | `merkle.proof` |
| `dag.merkle.verify` | `dag` | `merkle.verify` |
| `dag.slice.checkout` | `dag` | `slice.checkout` |
| `dag.dehydrate` | `dag` | `dehydrate` |

### loamSpine (domains: `spine`, `entry`, `session`, `certificate`)

| Method | capability.call domain | operation |
|--------|----------------------|-----------|
| `spine.create` | `spine` | `create` |
| `spine.get` | `spine` | `get` |
| `spine.seal` | `spine` | `seal` |
| `entry.append` | `entry` | `append` |
| `entry.get` | `entry` | `get` |
| `session.commit` | `session` | `commit` |
| `certificate.mint` | `certificate` | `mint` |

### sweetGrass (domains: `braid`, `provenance`, `attribution`, `anchoring`)

| Method | capability.call domain | operation |
|--------|----------------------|-----------|
| `braid.create` | `braid` | `create` |
| `braid.get` | `braid` | `get` |
| `braid.commit` | `braid` | `commit` |
| `provenance.graph` | `provenance` | `graph` |
| `provenance.export_provo` | `provenance` | `export_provo` |
| `attribution.chain` | `attribution` | `chain` |
| `anchoring.anchor` | `anchoring` | `anchor` |
| `anchoring.verify` | `anchoring` | `verify` |

---

## Graph updates (already pushed)

Our deploy graphs now include domain-level aliases in the `capabilities`
arrays, so biomeOS's exact-key registry lookup finds the correct primal:

```toml
[nodes.rhizocrypt]
by_capability = "dag"
capabilities = ["dag", "dag.session.create", "dag.event.append", ...]

[nodes.loamspine]
by_capability = "ledger"
capabilities = ["spine", "entry", "session", "certificate", "commit", "ledger", ...]

[nodes.sweetgrass]
by_capability = "attribution"
capabilities = ["braid", "attribution", "provenance", "anchoring", ...]
```

---

## wetSpring graph update needed

Your `graphs/wetspring_science_nucleus.toml` should absorb the v3.0
patterns from our updated deploy graphs:

1. Add `[graph.metadata]` section
2. Standardize `health_method = "health.liveness"` for all nodes
3. Update biomeOS capabilities to `["graph.deploy", "capability.discover", "topology.rescan"]`
4. Update BearDog capabilities to `["crypto.sign_ed25519", "crypto.verify_ed25519", "crypto.blake3_hash"]`
5. Update Songbird to `["discovery.find_primals", "discovery.announce"]`
6. Add domain aliases to trio `capabilities` arrays (see above)
7. Fix trio dependency chain: `rhizocrypt` → `loamspine` → `sweetgrass`

Reference: `primalSpring/graphs/spring_deploy/wetspring_deploy.toml` v3.0.0

---

## New capabilities to register

wetSpring exposes new capabilities that should be added to your
`capabilities.list` response and considered for ecosystem registry:

- `dag.dehydrate` — dehydrate a session (Merkle root + witnesses)
- `vault.store` / `vault.retrieve` — NestGate-backed caching
- `http.provenance.query` — HTTP provenance endpoint

These are valuable and may be adopted by other springs.

---

## Verification

After applying the 3 fixes, the Gonzales provenance chain validation
(Stage 5) should succeed end-to-end through live Neural API.

Test sequence:
1. Start biomeOS with a deploy graph that includes the trio
2. Verify trio primals are discoverable: `capability.call({ capability: "dag", operation: "session.create", args: {...} })`
3. Run `validate_gonzales_provenance_chain` — Stage 5 should pass
