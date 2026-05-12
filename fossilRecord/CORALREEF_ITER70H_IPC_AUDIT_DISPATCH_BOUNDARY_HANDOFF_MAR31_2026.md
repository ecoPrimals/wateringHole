# coralReef ITER70H — IPC Audit + Dispatch Boundary Handoff

**Date**: 2026-03-31
**Scope**: coral-glowplug IPC compliance, dispatch boundary documentation, post-S169 routing

## Summary

Addressed deep debt from the wateringHole V2 `PRIMAL_RESPONSIBILITY_MATRIX.md`
audit and `primalSpring` gap registry. Focused on `coral-glowplug` IPC compliance
gaps and documenting the transitional dispatch boundary with `toadStool`.

## Changes

### 1. `capabilities.list` completed (coral-glowplug)

**File**: `crates/coral-glowplug/src/socket/handlers/device_ops.rs`

Previous `capabilities.list` advertised 18 methods but omitted:

- `device.dispatch` — compute execution via CUDA (marked `"transitional": true`)
- `device.oracle_capture` — MMU page table diagnostics
- `mailbox.create`, `mailbox.post`, `mailbox.poll`, `mailbox.complete`, `mailbox.drain`, `mailbox.stats`
- `ring.create`, `ring.submit`, `ring.consume`, `ring.fence`, `ring.peek`, `ring.stats`

Now advertises all 32 handled methods. The `"transitional"` array flags methods
that will eventually move to `toadStool`.

### 2. `--port` flag added to glowplug daemon

**File**: `crates/coral-glowplug/src/main.rs`

Per ecoBin IPC standard, all daemons must offer `--port` for raw newline TCP
JSON-RPC as a fallback transport. Added:

```
coral-glowplug --bdf 0000:4a:00.0 --port 9100
```

When set, binds `127.0.0.1:{port}` as a second listener alongside the primary
Unix domain socket. Both transports share the same dispatch logic via
`handle_client_stream`. TCP handle is properly aborted on shutdown.

### 3. `device.sock` domain symlink

**File**: `crates/coral-glowplug/src/socket/mod.rs`

Added `install_domain_symlink()` — creates `device.sock` -> `coral-glowplug-{family}.sock`
in the `$XDG_RUNTIME_DIR/biomeos/` directory at socket bind time. Enables
capability-based discovery without knowing the instance name.

Overridable via `CORALREEF_GLOWPLUG_DOMAIN` env var (default: `device`).

### 4. Dispatch boundary documentation

**File**: `crates/coral-glowplug/DISPATCH_BOUNDARY.md`

Created in-crate documentation formalizing:

- Current architecture (coralreef-core → glowplug → driver, ember as fd holder)
- Eventual architecture (coralReef compiles, toadStool dispatches)
- Why `device.dispatch` is transitional (sovereign VFIO compute under development)
- Capability advertisement guidance for consumers
- Post-S169 spring routing via domain symlinks

## IPC Compliance Matrix (post-audit)

| Component      | UDS | TCP (`--port`) | Domain Symlink | `capabilities.list` | Health |
|----------------|-----|----------------|----------------|---------------------|--------|
| coralreef-core | C   | C              | `shader.sock`  | C                   | C      |
| coral-glowplug | C   | C              | `device.sock`  | C                   | C      |
| coral-ember    | C   | C              | —              | C                   | C      |

C = Compliant

`coral-ember` does not need a domain symlink — it is service-to-service only
(glowplug ↔ ember), not discoverable by springs.

## Flags for Other Primals

### toadStool socket namespace inconsistency

`toadStool` S169 uses `$XDG_RUNTIME_DIR/ecoPrimals/{capability}.sock` while
the ecosystem standard (wateringHole) is `$XDG_RUNTIME_DIR/biomeos/`. This is
a toadStool-side issue — not a coralReef change. Flagged for `toadStool` next
iteration.

### Spring routing post-S169

After `toadStool` removed `shader.compile.*` proxy methods, springs must now
discover and call `coralReef` directly:

1. Scan `$XDG_RUNTIME_DIR/biomeos/` for `shader.sock` → connects to `coralreef-core`
2. Call `capabilities.list` to confirm `shader.compile.*` is available
3. For GPU device operations: discover via `device.sock` → connects to `coral-glowplug`

No spring code changes are needed in coralReef — discoverability is handled by
the domain symlinks and capabilities advertisement.

## Remaining Gaps

| Gap | Owner | Priority |
|-----|-------|----------|
| `device.dispatch` move to toadStool | toadStool | Deferred (GPU stabilization) |
| toadStool socket namespace (`ecoPrimals/` vs `biomeos/`) | toadStool | Next iteration |
| Sovereign VFIO dispatch (`NvVfioComputeDevice` + GPFIFO) | coralReef | Active development |
| Warm handoff validation across GPU generations | coralReef | Active development |
| JIT shared memory support (Cranelift) | coralReef | Post-interpreter validation |

## Test Verification

```
cargo check -p coral-glowplug         ✓  (zero errors)
cargo clippy -p coral-glowplug        ✓  (zero glowplug warnings)
cargo test  -p coral-glowplug         ✓  (all tests pass)
```
