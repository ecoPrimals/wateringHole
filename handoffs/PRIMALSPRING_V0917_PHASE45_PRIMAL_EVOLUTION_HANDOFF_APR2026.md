# primalSpring v0.9.17 — Per-Primal Evolution Handoff

## From: primalSpring Phase 45 + ludoSpring V46
## For: All primal teams
## Date: April 20, 2026

---

## What Happened

primalSpring deployed the full 12-primal NUCLEUS from genomeBin, ran the
6-layer guidestone certification (**86/86 PASS**, 6 expected SKIP), refined
all local gaps (base64 encoding, tensor API, capability symlinks, discovery),
and validated ludoSpring's game science parity against the live stack.
Three new `game.*` methods were wired for esotericWebb garden absorption.

This handoff documents what we learned about each primal's IPC surface,
the gaps we hit, the fixes we made locally, and the evolution we recommend
upstream.

---

## Composition Pattern (How Primals Are Used)

```
biomeOS
  └── deploys NUCLEUS via graph TOML
        ├── Tower (beardog + songbird)       ← security + discovery
        ├── Node  (toadstool + barracuda     ← compute + tensor
        │          + coralreef)              ← shader
        └── Nest  (nestgate + squirrel)      ← storage + ai
              + Meta (rhizocrypt + loamspine  ← dag + ledger
                     + sweetgrass)           ← provenance
              + petaltongue                  ← visualization
```

Springs validate science against this stack. Gardens compose products from it.
Neither springs nor gardens are binaries — they are validation environments
and composition graphs, respectively.

### Discovery Flow

1. `start_primal.sh` launches primal and creates capability symlinks
   (e.g., `security.sock → beardog-{FAMILY_ID}.sock`)
2. Discovery probes all `.sock` files in `$XDG_RUNTIME_DIR/biomeos/`
3. `health.check` or `lifecycle.status` identifies the primal
4. Capabilities inferred from response fields or well-known prefixes
5. Callers use `discover_by_capability("tensor")` — never hardcoded names

### neuralAPI Deployment (biomeOS)

biomeOS serves as the Neural API substrate: it reads deploy graph TOMLs,
resolves fragments, computes topological startup ordering, and manages the
primal lifecycle. Gardens submit their graphs to biomeOS for deployment.

biomeOS itself speaks HTTP over UDS (not raw JSON-RPC). This is expected
behavior and documented as a SKIP in JSON-RPC probes. biomeOS is the
orchestrator, not a peer primal.

---

## Per-Primal Findings and Evolution Guidance

### BearDog (security / crypto / btsp)

**What works:**
- `crypto.sign` (ed25519) — requires base64-encoded message, returns signature
- `crypto.blake3_hash` — deterministic, base64-encoded
- `crypto.ed25519_generate_keypair` — returns `{public_key, secret_key}`
- `health.check` — name, status, version
- `capability.list` — comprehensive (150+ methods)
- BTSP Phase 2 cascade operational across all 12 primals

**What we fixed locally:**
- guidestone now base64-encodes raw message before `crypto.sign`
  (BearDog parses message as base64 bytes, rejects raw strings with `_`)

**Upstream evolution recommended:**
- `crypto.sign` returns `key_id: "default_signing_key"` but no `public_key`.
  `crypto.verify` requires `public_key`. **Sign→verify roundtrip is broken.**
  Fix: include `public_key` in sign response, or add `crypto.default_public_key` method.
- BearDog sometimes returns URL-safe base64 (uses `_` and `-`). Consumers
  must tolerate both URL-safe and standard base64. Recommend standardizing
  on one encoding.

---

### Songbird (discovery / network)

**What works:**
- `health.check` — returns status + version
- Discovery routing by capability

**Upstream evolution recommended:**
- `Songbird.resolve("beardog")` fails — Songbird routes by **capability**,
  not by primal name. This is correct behavior but underdocumented.
  Document that `resolve("security")` is the correct call, not `resolve("beardog")`.
- Consider adding `resolve_by_name()` as a convenience alias.

---

### toadStool (compute / display)

**What works:**
- `compute.health` — returns `{healthy, status, active_workloads, uptime_secs}`
- `compute.dispatch` — submit compute workloads
- `display.*` — DRM/KMS window management (when display backend active)
- Creates both JSON-RPC and tarpc sockets

**No upstream gaps identified.** toadStool is well-behaved.

---

### barraCuda (tensor / math / stats / activation / noise)

**What works (actual IPC surface):**
- `stats.mean` `{data: [f64]}` → `{result: f64}`
- `stats.variance` `{data: [f64]}` → `{result: f64, convention, denominator}`
- `stats.std_dev`, `stats.correlation`, `stats.weighted_mean`
- `activation.fitts` `{distance, width}` → `{index_of_difficulty, movement_time}`
- `activation.hick` `{n_choices}` → result
- `noise.perlin2d`, `noise.perlin3d`
- `tensor.matmul_inline` `{lhs: [[f64]], rhs: [[f64]]}` → `{result: [[f64]], shape}`
- `linalg.solve`, `linalg.eigenvalues`
- `spectral.fft`, `spectral.power_spectrum`
- `fhe.ntt`, `fhe.pointwise_mul`

**What we fixed locally:**
- exp068 was calling `math.dot`, `math.l2_norm` — **these don't exist**.
  Rewired to `stats.mean`, `stats.variance`, `activation.fitts`.
- guidestone was calling `tensor.matmul` with inline data — barraCuda
  returns nested 2D arrays. Fixed `validate_parity_vec` to flatten nested arrays.
  Also switched to `tensor.matmul_inline` (correct method for inline data).

**Upstream evolution recommended:**
- `tensor.create` / `tensor.matmul` (handle-based) require GPU. On headless
  hosts they return "No GPU device available". Consider CPU fallback for
  small tensors, or document the GPU requirement clearly.
- The `math.*` namespace is mostly empty (`math.sigmoid`, `math.log2` only).
  All numeric operations are under `stats.*`, `activation.*`, `linalg.*`.
  Consider documenting which namespace to use for what.
- Socket naming: barraCuda creates `math-{FAMILY_ID}.sock`, not
  `barracuda-{FAMILY_ID}.sock` for its IPC socket. The `barracuda-*.sock`
  exists but may not be the IPC socket. Document which socket is authoritative.

---

### coralReef (shader)

**What works:**
- Shader validation and compilation via tarpc protocol
- Creates both `coralreef-core-default.sock` (JSON-RPC) and
  `coralreef-{FAMILY_ID}.sock` (tarpc binary protocol)
- `shader.capabilities` returns supported architectures

**Upstream evolution recommended:**
- The tarpc socket rejects JSON-RPC probes (binary protocol). This is
  expected. Ensure JSON-RPC `health.check` is available on the
  `coralreef-core-default.sock` socket. Currently works but the socket
  naming is confusing.

---

### NestGate (storage)

**What works:**
- `storage.store` `{key, value}` — stores data
- `storage.retrieve` `{key}` → `{value}`
- Full roundtrip validated by guidestone

**No upstream gaps identified.** Storage is clean.

---

### Squirrel (ai)

**What works:**
- `health.check` — responsive
- AI inference capabilities

**No blocking gaps identified.**

---

### rhizoCrypt (dag / memory)

**What works:**
- Server mode via `--unix` flag
- DAG storage capabilities

**Upstream evolution recommended:**
- rhizoCrypt resets connections without BTSP handshake — plain
  `health.check` probes fail with EPIPE/ECONNRESET.
  Accept unauthenticated `health.check` (liveness only) before
  requiring BTSP for data operations.

---

### sweetGrass (attribution / provenance / commit)

**What works:**
- Server mode with family-qualified sockets
- Attribution and provenance tracking

**Upstream evolution recommended:**
- Same BTSP-first behavior as rhizoCrypt — plain health probes rejected.
  Same fix: allow unauthenticated `health.check`.

---

### loamSpine (ledger)

**What works:**
- Server mode operational

**Upstream evolution recommended:**
- Socket naming doesn't follow the `{primal}-{FAMILY_ID}.sock` convention.
  Discovery can't find loamSpine by the `capability:ledger` query.
  Fix: use family-qualified naming, or let `start_primal.sh` create the
  `ledger.sock` symlink (which we now do automatically).

---

### petalTongue (visualization / ui)

**What works:**
- `visualization.capabilities` — returns data binding variants, grammar types
- `visualization.render.grammar`, `.dashboard`, `.scene`, `.stream`
- Creates socket and responds to health checks

**Upstream evolution recommended:**
- `visualization.render` with spring-specific data needs parameter alignment.
  The `SpringDataAdapter` in petalTongue recognizes ludoSpring `GameScene`
  and `GameChannel` payloads, but the exact parameter format for
  `visualization.render` differs from what ludoSpring pushes.
  Align parameter schema between `game.push_scene` (ludoSpring) and
  `visualization.render.scene` (petalTongue).

---

## start_primal.sh Improvements (For All Teams)

The unified startup wrapper now:
1. Maps generic flags to primal-specific CLIs
2. Creates capability symlinks after launch (`create_capability_symlinks()`)
3. Handles BTSP seed propagation via environment
4. Logs primal PID, socket path, family, and symlinks created

Symlink map (auto-created):
```
beardog      → security, crypto, btsp, ed25519, x25519
songbird     → discovery, network
toadstool    → compute
barracuda    → tensor, math
coralreef    → shader
nestgate     → storage
squirrel     → ai
petaltongue  → visualization, ui
rhizocrypt   → dag, memory
loamspine    → ledger
sweetgrass   → attribution, provenance, commit
```

---

## Validation Scorecard

| Component | Score |
|-----------|-------|
| primalSpring guidestone | **86/86 PASS** (6 expected SKIP) |
| primalSpring exp094 parity | 15/18 (Songbird name-resolution) |
| ludoSpring exp067 tower | **18/19** (1 expected SKIP) |
| ludoSpring exp068 barraCuda | **6/6 PASS** |
| ludoSpring exp072 composition | 24/31 (biomeOS HTTP + ludoSpring not deployed as primal) |
| ludoSpring local math | 152/152 |
| ludoSpring pipeline | 11/11 |
| ludoSpring game.* methods | **15** (was 12 — +record_action, push_scene, query_vertices) |

---

## What Primal Teams Should Do

1. **Pull latest `infra/wateringHole/`** for updated standards and gap tables
2. **Read your primal section above** for specific evolution guidance
3. **Test with `start_primal.sh`** — verify your primal launches correctly
   and capability symlinks are created
4. **Validate `health.check` works without authentication** — this is the
   universal liveness probe. BTSP should gate data operations, not health.
5. **Document your IPC surface** — which namespace (stats vs math vs tensor),
   which params, which response format. Consumers are guessing.
6. **Run primalSpring guidestone against your primal** to verify composition
   compatibility

---

## Key References

- Depot workflow: `primalSpring/wateringHole/PLASMINBIN_DEPOT_PATTERN.md`
- guideStone standard: `primalSpring/wateringHole/GUIDESTONE_COMPOSITION_STANDARD.md` (v1.2.0)
- Composition guidance: `primalSpring/wateringHole/PRIMALSPRING_COMPOSITION_GUIDANCE.md`
- Downstream manifest: `primalSpring/graphs/downstream/downstream_manifest.toml`
- Gap registry: `primalSpring/docs/PRIMAL_GAPS.md`
- Ecosystem alignment: `infra/wateringHole/NUCLEUS_SPRING_ALIGNMENT.md`
- Taxonomy: `infra/wateringHole/PRIMAL_SPRING_GARDEN_TAXONOMY.md`
- Webb handoff: `infra/wateringHole/handoffs/ESOTERICWEBB_COMPOSITION_EVOLUTION_HANDOFF_APR2026.md`
- This handoff: `infra/wateringHole/handoffs/PRIMALSPRING_V0917_PHASE45_PRIMAL_EVOLUTION_HANDOFF_APR2026.md`

---

**License**: AGPL-3.0-or-later
