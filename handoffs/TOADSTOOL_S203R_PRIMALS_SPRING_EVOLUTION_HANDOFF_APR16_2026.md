# ToadStool S203r: Primals & Spring Teams — Evolution Handoff

**Date**: April 16, 2026
**Session**: S203r
**Audience**: All primal teams + primalSpring + downstream springs
**Purpose**: Document patterns, lessons, and composition guidance for ecosystem absorption

---

## 1. What ToadStool Achieved (S203a–S203r)

Over 18 sessions (Apr 12–16, 2026), ToadStool evolved from "mostly clean" to
**zero-debt, zero-proc-macro, fully capability-based**:

| Metric | Before (S203a) | After (S203r) |
|--------|----------------|---------------|
| Tests | ~20,000 | **22,061** (0 failures) |
| `async-trait` | 158 annotations, 13 crates | **0 annotations, 0 crates, banned** |
| `ring` | present | **banned** (`deny.toml`) |
| Hardcoded ports/paths | scattered | **0** (constants + capability discovery) |
| Production TODO/FIXME | some | **0** |
| Production unwrap/panic | some | **0** |
| File size (>500 LOC) | 38 files | **25 files** (all <700, pure hw drivers) |
| Env var literals | scattered | **fully interned** (`socket_env` constants) |
| System monitoring | hardcoded stubs | **real** (sysmon + statvfs) |
| I/O-logic separation | mixed | **5 modules refactored** |
| Unsafe | ~66 blocks | **~66 blocks** (all documented, debug_assert, 46/46 lint) |

## 2. async-trait Deprecation — Pattern for All Primals

### Why It Matters
`async-trait` is a proc macro that desugars `async fn` to `Pin<Box<dyn Future>>`.
It adds compile-time cost (proc macro expansion) and is unnecessary now that we
can write the same desugaring by hand. Removing it:
- Eliminates a proc-macro dependency from the hot compilation path
- Makes the code self-documenting (you see exactly what the compiler sees)
- Aligns with ecoBin v3 "minimize proc macros" principle

### How to Migrate (for other primals)

**Step 1**: Audit usage — `rg "#\[async_trait" --type rust -c`

**Step 2**: For each trait with `dyn` usage (Box<dyn T>, Arc<dyn T>):
```rust
// Replace this:
#[async_trait]
pub trait Foo: Send + Sync {
    async fn bar(&self, x: &str) -> Result<T>;
}

// With this:
pub trait Foo: Send + Sync {
    fn bar<'a>(&'a self, x: &'a str)
        -> Pin<Box<dyn Future<Output = Result<T>> + Send + 'a>>;
}
```

**Step 3**: For impl blocks:
```rust
impl Foo for MyType {
    fn bar<'a>(&'a self, x: &'a str)
        -> Pin<Box<dyn Future<Output = Result<T>> + Send + 'a>> {
        Box::pin(async move {
            // same body as before
        })
    }
}
```

**Step 4**: For traits with NO dyn usage — just use native `async fn`:
```rust
pub trait Foo: Send + Sync {
    async fn bar(&self) -> Result<T>;
}
```

**Step 5**: Remove from Cargo.toml, add to deny.toml

### Ecosystem Status
| Primal | async-trait status |
|--------|-------------------|
| ToadStool | **Banned** (S203r) |
| Songbird | **Banned** (SONGBIRD_V021_WAVE145) |
| biomeOS | **Banned** (BIOMEOS_V316) |
| Others | Check per-primal `deny.toml` |

## 3. Composition Patterns for NUCLEUS

### What ToadStool Exposes via IPC

ToadStool is a **compute infrastructure primal** that exposes capabilities via
Unix-socket JSON-RPC:

- **Primary socket**: `compute.sock` (JSON-RPC, biomeOS routes here)
- **Hot-path socket**: `compute-tarpc.sock` (tarpc binary protocol)
- **Override**: `TOADSTOOL_SOCKET` / `TOADSTOOL_TARPC_SOCKET` env vars
- **Family**: `compute-{family_id}.sock` / `compute-{family_id}-tarpc.sock`

### Key Methods for Composition
```
health.liveness      → {"status":"alive"}
health.readiness     → ready + version
capabilities.list    → full capability manifest
identity.get         → primal identity
compute.execute      → direct workload execution
compute.dispatch.pipeline.submit → multi-stage DAG pipeline
```

### NUCLEUS Composition Pattern

Springs compose with ToadStool through NUCLEUS, not by importing crates:

```
[Spring Experiment]
    │
    ▼
[NUCLEUS Composition Layer]
    │
    ├─── compute.execute ──────► [ToadStool] ──► GPU/CPU/NPU
    ├─── security.encrypt ─────► [BearDog]
    ├─── storage.put ──────────► [NestGate]
    └─── coordination.route ───► [Songbird]
```

**No spring should import toadstool crates directly.** All interaction is via
IPC through capability discovery: `capability.discover("compute")` returns the
socket path, then JSON-RPC or tarpc calls flow through it.

### baseCamp Validation (Python → Rust → Primal)

The three-stage pipeline documented in `springs/primalSpring/whitePaper/baseCamp/README.md`
is the canonical pattern:

1. **Python baseline** — peer-reviewed ground truth
2. **Rust port** — matches Python within tolerance, ecoBin compliant
3. **Primal composition** — matches Rust via NUCLEUS IPC, `validate_parity()`

For ToadStool specifically: the "science" being validated IS the infrastructure.
The Python baseline is the spec. The Rust port is the implementation. The primal
composition is the live ecosystem.

## 4. Deployment via Neural API from biomeOS

### How ToadStool Gets Deployed

biomeOS manages ToadStool as an atomic:

```
biomeOS
  └── Neural API
       └── deploy_graph.submit({
             atomics: [{
               primal: "toadstool",
               socket: "compute.sock",
               capabilities: ["compute.execute", "gpu.discover", ...],
               preset: "default"
             }]
           })
```

The deploy graph specifies:
- Which atomics to deploy
- Socket paths (or let biomeOS allocate)
- Capability requirements
- Topology (standalone, tower, covalent mesh)

### Cross-Architecture Notes
- ToadStool runs on **x86_64 + aarch64** (Pixel via GrapheneOS validated)
- `--tcp-only` flag for cross-network deployment (no UDS across hosts)
- GPU features degrade gracefully on devices without GPU
- All 22,000+ tests pass on both architectures

## 5. Lessons Learned (for team absorption)

### What Worked
1. **Wave-based migration** — doing async-trait in 5 waves (quick wins → complex → ban) kept each step small and verifiable
2. **Mechanical transformation** — manual `Pin<Box<dyn Future>>` is 100% identical to what `async-trait` generates, making it a zero-risk refactor
3. **Test extraction** (S203c/e/g/i) — moving tests to companion `_tests.rs` files kept production files <500 LOC without losing coverage
4. **Constant interning** — `socket_env::TOADSTOOL_*` and `platform_paths::*` eliminate all hardcoded strings
5. **I/O-logic separation** — extracting pure parsers from I/O wrappers made testing deterministic

### What to Watch For
1. **Lifetime annotations** — `Pin<Box<dyn Future<...> + Send + 'a>>` requires explicit lifetimes when methods take reference params. The compiler tells you.
2. **clippy::type_complexity** — deeply nested generic types trigger this. Use a local type alias: `type BoxFuture<'a, T> = Pin<Box<dyn Future<Output = T> + Send + 'a>>;`
3. **Transitive deps** — even after removing `async-trait` from your code, upstream crates (axum, config, wiggle) still pull it in transitively. Use `wrappers` in deny.toml.
4. **Edge crate drift** — if a crate falls behind on API changes, it accumulates errors. Fix API drift promptly.

## 6. What's Next for ToadStool

- **Test coverage** → 90% target (currently ~83.6%, 22,000+ tests)
- **Edge crate API alignment** — resolve pre-existing RuntimeEngine drift
- **Enum dispatch optimization** — current manual boxing can be evolved to enum dispatch for bounded-set traits (performance optimization, not correctness)
- **Wire Standard L3 completion** — remaining `cost_estimates` and `operation_dependencies` methods
