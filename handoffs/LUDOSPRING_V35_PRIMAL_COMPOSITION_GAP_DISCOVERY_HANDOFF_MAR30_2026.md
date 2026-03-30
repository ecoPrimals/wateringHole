# ludoSpring V35 — Primal Composition Gap Discovery

**Date:** March 30, 2026
**From:** ludoSpring V35 (Track 26: Primal Composition Validation)
**To:** barraCuda, biomeOS, coralReef, toadStool, primalSpring, esotericWebb, Squirrel, petalTongue, all primals
**Previous:** `LUDOSPRING_V32_COMPREHENSIVE_AUDIT_DEEP_DEBT_HANDOFF_MAR29_2026.md`
**Status:** Gap discovery complete — 5 composition experiments run against live primals

---

## Summary

V35 introduces a new evolution tier: replicate ludoSpring's validated game
science using ONLY primal composition. No ludoSpring binary participates.
Instead, experiments probe whether existing deployed primals — composed via
biomeOS deploy graphs and Neural API routing — can reproduce the same
validated baselines.

Every failure is a documented gap with a specific primal owner and evolution
target. When primals evolve to fill these gaps, the experiments start passing
— proving ludoSpring's science is replicable through composition alone.

esotericWebb (gen4) should learn from these composition graphs rather than
depending on a ludoSpring process.

**Live test environment:** beardog + songbird + biomeOS Neural API + coralReef +
toadStool running from plasmidBin (v2026.03.25 release). UDS at
`/run/user/1000/biomeos/` and `/tmp/biomeos-sockets/`.

---

## Live Results

| Exp | Target | Passed | Blocking gap |
|-----|--------|--------|-------------|
| 084 | barraCuda math IPC | 0/12 | barraCuda not in plasmidBin |
| 085 | Shader dispatch chain | 2/8 | coralReef HTTP-wrapped JSON-RPC vs raw UDS |
| 086 | Tensor composition | 0/10 | barraCuda not in plasmidBin |
| 087 | Neural API pipeline | 1/7 | Primals not registered; graphs not deployed |
| 088 | Continuous game loop | 2/10 | Primals not registered; 5 domains absent |

**Positive findings:**
- coralReef and toadStool UDS sockets discoverable via standard paths
- biomeOS Neural API starts and responds on UDS
- `capability.call` round-trip latency is sub-millisecond on UDS (well within 16ms budget)
- biomeOS `graph.execute`, `graph.execute_pipeline`, `graph.start_continuous` are implemented in routing layer

---

## Part 1: For barraCuda Team

### Gap: Not in plasmidBin

barraCuda is the only primal without a binary in the `plasmidBin` GitHub
Release (v2026.03.25). All 11 other primals were fetched successfully via
`fetch.sh`. This blocks ALL math composition experiments (exp084, exp086).

**Action:** Build and harvest barraCuda via `harvest.sh` so it appears in the
next release. The binary needs to:
1. Start as `./barracuda server` (UniBin pattern)
2. Bind to UDS at `$XDG_RUNTIME_DIR/biomeos/barracuda.sock` (or `/tmp/biomeos-sockets/barracuda.sock`)
3. Bind TCP on port 9010 (per `plasmidBin/ports.env`)

### Gap: Math methods not on JSON-RPC

exp084 probes 12 math methods over IPC:

| Method | Domain | ludoSpring lib equivalent |
|--------|--------|--------------------------|
| `math.sigmoid` | activation | `barracuda::ops::sigmoid` |
| `math.log2` | activation | `barracuda::ops::log2` |
| `stats.mean` | statistics | `barracuda::stats::mean` |
| `stats.std_dev` | statistics | `barracuda::stats::std_dev` |
| `stats.weighted_mean` | statistics | `barracuda::stats::weighted_mean` |
| `noise.perlin2d` | procedural | ludoSpring `procedural::noise::perlin2d` (upstream candidate) |
| `noise.perlin3d` | procedural | ludoSpring `procedural::noise::perlin3d` (upstream candidate) |
| `rng.uniform` | random | seedable RNG |
| `tensor.create` | tensor API | `barracuda::tensor` |
| `tensor.matmul` | tensor API | `barracuda::tensor::matmul` |
| `activation.fitts` | HCI | ludoSpring's Fitts model (upstream candidate) |
| `activation.hick` | HCI | ludoSpring's Hick model (upstream candidate) |

**Action:** Expose existing barraCuda math as JSON-RPC methods following
`SEMANTIC_METHOD_NAMING_STANDARD.md`. The ops and stats modules already
exist in the Rust crate — they just need IPC wiring.

### Gap: Tensor element-wise ops missing from IPC

exp086 needs `tensor.add`, `tensor.scale`, `tensor.clamp`, `tensor.reduce`,
`tensor.sigmoid` over IPC for composite engagement scoring.

**Action:** Wire element-wise tensor ops as JSON-RPC methods. This is the
composition equivalent of TensorSession — each op is a graph node.

---

## Part 2: For biomeOS Team

### Gap: Running primals not registered with Neural API

When biomeOS Neural API starts, it only exposes 5 bootstrap capabilities.
Other running primals (beardog, toadStool, coralReef, songbird, squirrel,
etc.) are NOT auto-discovered. `capability.list` returns only bootstrap
entries. `capability.call` for `compute`, `ai`, `visualization`, `dag`,
`security` domains all fail with "Capability not registered."

**Action (two options):**
1. **Auto-discovery**: biomeOS scans socket directory at startup (or watches
   with inotify) and probes each socket's `capabilities.list` method
2. **Registration protocol**: Each primal calls `capability.register` on the
   Neural API socket at startup (requires primals to know where Neural API lives)

Option 1 is more sovereign (no startup ordering dependency). The socket
directory convention (`/run/user/$UID/biomeos/`) already provides discovery.

### Gap: Nucleus graphs should be bundled, not runtime-deployed

exp087 tried to execute `ludospring_math_pipeline.toml` via `graph.execute`.
biomeOS looked for it in its `graphs/` directory and failed. The distinction:

- **Nucleus graphs** (biomeOS's own bootstrap/health/routing graphs) should
  be embedded in the biomeOS binary, compiled in at build time
- **Runtime graphs** (consumer compositions like ludoSpring's) should be
  deployed at runtime via `graph.save` or a deploy directory

Currently there's no clear separation. biomeOS should bundle its nucleus
graphs internally and accept runtime graphs through the API.

**Action:** Separate nucleus (built-in) from runtime (deployed) graphs.
Expose `graph.save` for runtime graph deployment. Document the convention.

### Gap: Continuous executor is a stub

`graph.start_continuous` session lifecycle works — sessions get IDs, can be
started/stopped. But node execution within continuous sessions is a
placeholder. The 60Hz game loop (exp088) needs nodes to actually fire at
tick rate.

**Action:** Implement node dispatch within continuous sessions. Each tick
should route `by_capability` through `capability.call` to registered primals.

### Positive: capability.call latency is excellent

exp088 measured sub-millisecond `capability.call` round-trip on UDS. This
confirms the transport layer is fast enough for 60Hz composition (16ms
budget). The bottleneck is registration and executor completeness, not speed.

---

## Part 3: For coralReef Team

### Gap: HTTP-wrapped JSON-RPC vs raw newline-delimited

exp085 discovered coralReef and connected to its UDS socket. But the
`shader.compile.wgsl` call failed because coralReef wraps JSON-RPC in HTTP
(Content-Length framing), while the ecosystem standard
(`PRIMAL_IPC_PROTOCOL.md`) specifies raw newline-delimited JSON-RPC.

**Action:** Add a raw newline-delimited JSON-RPC mode to coralReef's server
(either as default on UDS, or as a `--raw-jsonrpc` flag). HTTP framing can
remain for TCP compatibility. The UDS path should speak raw protocol for
zero-overhead IPC with other primals.

### Positive: Socket discovery works

coralReef's UDS socket at `/run/user/$UID/biomeos/coralreef.sock` was
correctly discovered by exp085. The socket path convention is solid.

---

## Part 4: For toadStool Team

### Gap: Dispatch chain untested E2E

The sovereign shader pipeline (compile → dispatch → readback) has never been
tested end-to-end across primal boundaries:

```
coralReef (compile WGSL → binary)
    ↓ IPC
toadStool (dispatch binary to GPU → readback result)
    ↓ IPC
consumer (validate result)
```

exp085 confirmed both primals' sockets are discoverable but the compile step
fails (coralReef transport mismatch, see Part 3). Once coralReef's transport
is fixed, toadStool needs to accept compiled shader binary via IPC and
dispatch it.

**Action:** Implement `shader.dispatch` method that accepts a compiled binary
(from coralReef's `shader.compile.wgsl` output) and returns compute results.

---

## Part 5: For primalSpring Team

### Composition validation patterns

ludoSpring's 5 composition experiments use patterns that primalSpring should
absorb into its composition testing framework:

1. **Socket probe**: Check socket exists before attempting RPC (skip vs fail)
2. **TCP fallback**: Try UDS first, fall back to TCP using `ports.env` assignments
3. **Method probe**: Send JSON-RPC and classify response (method exists vs not found vs transport error)
4. **Capability chain**: Call `capabilities.list` to discover what a primal offers before probing specific methods
5. **Composition graphs**: TOML deploy graphs with `by_capability` routing that can be validated against Neural API

ludoSpring's graphs are at `graphs/composition/*.toml` — 4 focused DAGs that
serve as templates for primalSpring's own composition experiments.

### primalSpring's `ludospring_validate.toml` graph drift

primalSpring's `graphs/spring_validation/ludospring_validate.toml` references
capabilities that don't match ludoSpring's actual IPC surface. Now that
ludoSpring is V35 (with composition as the evolution target, not a shipped
binary), primalSpring should update its ludoSpring graph to validate the
composition path instead.

---

## Part 6: For esotericWebb Team

### Composition-first architecture

ludoSpring V35 proves that the gen4 architecture should be composition-first:
instead of `esotericWebb → ludoSpring binary → game science`, the path is:

```
esotericWebb → biomeOS Neural API → [barraCuda + coralReef + toadStool + Squirrel]
```

The 4 composition graphs in `ludoSpring/graphs/composition/` are proto-patterns
for esotericWebb's own deploy graphs:

| Graph | Pattern | esotericWebb use |
|-------|---------|-----------------|
| `math_pipeline.toml` | Sequential barraCuda ops | Math-heavy game mechanics |
| `shader_dispatch_chain.toml` | Compile → dispatch pipeline | Shader-based rendering |
| `engagement_pipeline.toml` | Streaming pipeline | Real-time engagement scoring |
| `game_loop_continuous.toml` | 60Hz continuous | Full game tick loop |

**Action:** Track ludoSpring's gap resolution. As primals fill gaps,
esotericWebb can adopt the same composition graphs, replacing ludoSpring
dependency with direct primal composition.

---

## Part 7: For All Primals

### Startup registration convention

Every primal that starts a server should:
1. Bind UDS at `$XDG_RUNTIME_DIR/biomeos/{primal_name}.sock`
2. Bind TCP on its assigned port (per `plasmidBin/ports.env`)
3. Expose `health.check`, `health.liveness`, `capabilities.list` on both transports
4. (When Neural API is running) Call `capability.register` to announce itself

This enables biomeOS Neural API to route `capability.call` to the correct
primal. Without registration, the Neural API has no knowledge of running
primals — which is the single biggest blocker found in V35.

### Transport convention

UDS should speak raw newline-delimited JSON-RPC (per `PRIMAL_IPC_PROTOCOL.md`).
TCP can optionally wrap in HTTP for external consumers. coralReef's current
HTTP-on-UDS breaks the convention and should be fixed.

---

## Deploy Graph Conventions Learned

From running live composition against biomeOS:

1. Root header must be `[graph]` (not `[metadata]`) — biomeOS parses `[graph]`
2. Nodes use `[[nodes]]` array-of-tables with `by_capability = "domain.method"`
3. `required = false` (not `optional = true`) for graceful degradation
4. biomeOS's `graphs/` directory is for nucleus (bootstrap) graphs; runtime
   graphs should be deployed via `graph.save` API
5. Node `depends_on` creates execution ordering within the graph

---

## Gap Summary (Prioritized)

| Priority | Gap | Owner | Blocks | Action |
|----------|-----|-------|--------|--------|
| P0 | barraCuda not in plasmidBin | barraCuda | exp084, exp086 | Build + harvest binary |
| P0 | Primals not registered with Neural API | biomeOS | exp087, exp088 | Auto-discovery or registration protocol |
| P1 | coralReef HTTP vs raw JSON-RPC on UDS | coralReef | exp085 | Add raw mode for UDS |
| P1 | barraCuda math not on JSON-RPC | barraCuda | exp084 | Wire ops/stats as IPC methods |
| P1 | Tensor element-wise ops not on IPC | barraCuda | exp086 | Wire tensor.add/scale/clamp/reduce |
| P2 | Continuous executor stub | biomeOS | exp088 | Implement node dispatch in continuous sessions |
| P2 | Nucleus vs runtime graph separation | biomeOS | exp087 | Bundle nucleus, accept runtime via API |
| P2 | Compile→dispatch E2E chain | coralReef + toadStool | exp085 | Full pipeline with binary handoff |
| P3 | Neural API `health.liveness` missing | biomeOS | exp087 | Add to health module |
