# cellMembrane — Wave 155k Sovereign CI Polish Items

**Date:** 2026-07-30
**Author:** sporeGate ops
**Scope:** 3 code items surfaced during sovereign CI activation. Pipeline is
live and automated — these are polish/hardening.

---

## Context

Sovereign CI is now live on sporeGate. The full chain works:

```
Forgejo push → golgi post-receive hook → SSH → sporeGate
  → sovereign.ci.trigger → harvest → sandbox → refresh → depot push
```

Validated end-to-end with squirrel primal. The following items surfaced during
activation and are non-blocking polish for the cellMembrane code team.

---

## P2: Wire `mesh.build_pending` Notification

**File:** `crates/membrane-shadow/src/plasmid/mod.rs` — `notify_mesh_build_pending()`

**Current state:** Function exists, logs to tracing, does NOT publish to songBird UDS.
The sibling `notify_mesh_depot_updated()` in `harvest_support.rs` publishes correctly.

**Ask:** Copy the songBird UDS JSON-RPC pattern from `notify_mesh_depot_updated()` into
`notify_mesh_build_pending()`, using topic `depot.build_pending` instead of `depot.updated`.
Consumer gates would then know a build is in progress and can delay fetch until
`depot.updated` arrives.

**Effort:** ~20 LOC. Pattern already exists in `harvest_support.rs`.

---

## P2: HTTP/UDS Webhook Listener (Optional)

**Files:** `crates/membrane-shadow/src/webhook/mod.rs`, `pipeline.rs`

**Current state:** All webhook dispatch logic works (HMAC-SHA256 verify, Forgejo/GitHub
provider detection, push event classification, harvest/cascade pipeline dispatch).
CLI path works: `membrane webhook.test '<json>'`. But there is no HTTP/UDS server
to receive Forgejo webhook POSTs directly.

**Current workaround:** The bash `golgi-post-receive-ci.sh` hook SSHes to sporeGate
and calls `sovereign.ci.trigger`. This works and is validated.

**Ask:** When convenient, add an axum/hyper UDS listener or HTTP endpoint that receives
Forgejo webhook POSTs and calls the existing `handle_push()` dispatch. Architecture
comment in `webhook/mod.rs` references `Forgejo → Caddy → membrane UDS` as the
intended path. `WebhookProvider::detect()` is `#[allow(dead_code)]` waiting for this.

**Effort:** ~200 LOC. Not blocking — bash hook is production-stable.

---

## P1: membrane.exe Windows Cross-Compile

**Current state:** `membrane.exe` fails to cross-compile. `UnixStream` and
`handshake_async` in the SSH/IPC modules are not `#[cfg(unix)]` gated.

**Impact:** blueGate (Windows) cannot run membrane natively. This blocks:
- blueGate as a sub-builder (can't run `sovereign.ci.trigger` locally)
- blueGate running `temporal.cascade` for self-sync
- Native depot_sync from blueGate

**Workaround:** sporeGate can SSH to blueGate and run plain `cargo build` commands
without membrane. But the full sovereign CI path requires membrane on blueGate.

**Ask:** Gate the remaining `UnixStream`, `tokio::net::UnixStream`, and `handshake_async`
uses with `#[cfg(unix)]` and provide Windows stubs or skip-paths. Same pattern
bearDog used in Wave 155k (`#[cfg(unix)]` gate on `BtspListenerUnix`).

---

## Not Requested (Already Working)

These items were audited and confirmed working — no code team action needed:

- `plasmid.harvest` full pipeline (clone, build, strip, checksum, stage, push)
- `targets_for_primal()` manifest integration
- `drift::has_upstream_changes` commit detection
- `depot_sync_push_standalone` BLAKE3-gated SCP
- `provenance.toml` auto-write with commit+builder+rustc
- `publish_gate_heads()` auto-commit + push
- `notify_mesh_depot_updated()` songBird UDS publish
- `auto_fetch::handle_depot_updated()` consumer pull + BLAKE3 verify
- `sandbox::validate()` fail-closed health check
- `sovereign.ci.trigger` full typed pipeline

---

*sporeGate Wave 155k — sovereign CI live and validated. 3 polish items for
cellMembrane: wire build_pending (20 LOC), optional webhook listener (200 LOC),
membrane.exe fix (P1, blocks blueGate sub-builder).*
