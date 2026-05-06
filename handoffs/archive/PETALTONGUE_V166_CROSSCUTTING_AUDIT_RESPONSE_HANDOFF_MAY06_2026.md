# petalTongue v1.6.6 — Cross-Cutting Audit Response Handoff

**Date:** May 6, 2026
**Author:** petalTongue team
**Status:** Complete — all primalSpring Phase 59 items resolved

---

## Summary

Resolved four items from primalSpring's downstream audit across Songbird,
coralReef, petalTongue, and skunkBat teams, plus two cross-cutting notes:

| Item | Status | Change |
|------|--------|--------|
| Tier-1 Songbird `ipc.register` with TCP | **Shipped** | `transports` field in registration payload |
| Wire Standard L3 on `capabilities.list` | **Already compliant** | No code change needed |
| BufReader post-negotiate byte loss | **Fixed** | TCP JSON-line uses split-first pattern |
| Whitespace-tolerant TCP detection | **Shipped** | Both TCP and UDS paths skip leading whitespace |

## Changes

### 1. Tier-1 Songbird Registration (petalTongue team item)

**Problem:** `ipc.register` advertised only a logical endpoint (`/primal/petaltongue`)
without concrete transport addresses. Songbird `ipc.resolve` couldn't route
directly to petalTongue without probing.

**Fix:** `PrimalRegistration` now includes a `transports` field:
```json
{
  "transports": {
    "uds": "/run/user/1000/biomeos/petaltongue.sock",
    "tcp": "0.0.0.0:9900"
  }
}
```

- UDS path always populated (from `get_petaltongue_socket_path()`)
- TCP endpoint populated when `--port` is active (Server/Live modes)
- TCP port extracted from CLI before registration
- 3 new tests: UDS transport present, TCP transport added, serialization

**Files:**
- `crates/petal-tongue-ipc/src/primal_registration.rs` — `transports` field,
  `with_tcp_port()` builder
- `src/main.rs` — `register_with_discovery_service(tcp_port)` signature, CLI
  extraction of `--port` before registration

### 2. BufReader Post-Negotiate Fix (cross-cutting)

**Problem:** TCP JSON-line BTSP path called `relay_json_line_handshake(&mut stream)`
which created a transient `BufReader` inside the function. If that BufReader
prefetched bytes beyond the handshake, those bytes were lost when the BufReader
was dropped. A new BufReader created after handshake would start from the wrong
stream offset, corrupting Phase 3 encrypted framing.

**Fix:** TCP JSON-line path now:
1. Splits the stream **before** the handshake
2. Wraps the read half in a `BufReader`
3. Calls `relay_json_line_handshake_split()` (the split variant)
4. Carries the **same** BufReader through Phase 3 negotiate and encrypted I/O

Extracted `run_tcp_json_line_btsp()` and `run_tcp_length_prefixed_btsp()` helpers
to keep `handle_tcp_with_btsp()` under the 100-line clippy limit.

**Files:**
- `crates/petal-tongue-ipc/src/unix_socket_server.rs` — restructured TCP accept

### 3. Whitespace-Tolerant TCP Protocol Detection (cross-cutting)

**Problem:** Protocol classification used `peeked[0]` (or `buf[0]`) directly as
the first byte to check against `b'{'`. If a peer sent leading whitespace
(CR/LF/spaces), the classifier incorrectly routed to length-prefixed BTSP.

**Fix:** Both TCP (`handle_tcp_with_btsp`) and UDS (`run_uds_handshake`) paths
now find the first non-whitespace byte before classification:
```rust
let first_non_ws = peeked.iter().find(|b| !b.is_ascii_whitespace());
let is_json_start = first_non_ws == Some(&b'{');
```

`is_btsp_json_announcement()` also strips leading whitespace from the peek
buffer before checking for `{` and `"protocol"`.

**Files:**
- `crates/petal-tongue-ipc/src/unix_socket_server.rs`

### 4. Wire Standard L3 on `capabilities.list`

Already compliant — no changes needed. `capabilities.list` returns:
```json
{
  "protocol": "json-rpc-2.0",
  "transport": ["unix-socket", "tcp"]
}
```

`transport` is dynamic: includes `"tcp"` only when `handlers.tcp_enabled` is set
via `with_tcp_port()` on the `UnixSocketServer`.

## Verification

```
cargo clippy --all-features --workspace -- -D warnings  # 0 warnings
RUSTDOCFLAGS="-D warnings" cargo doc --all-features --workspace --no-deps  # clean
cargo test --all-features --workspace  # 6,204 tests, 0 failures
```

All files under 800 lines. Zero unsafe blocks. Zero TODO/FIXME.

## Ecosystem Awareness

- **Songbird team**: petalTongue now advertises transport endpoints in
  `ipc.register`. When Songbird implements identity verification on
  `ipc.register` (Phase 55 audit item), petalTongue's existing BTSP handshake
  infrastructure supports the `identity.get` + BTSP flow.

- **coralReef team**: The BufReader fix pattern matches your Iter 90 fix.
  Our TCP JSON-line path is now aligned.

- **skunkBat team**: Whitespace tolerance is now implemented if you want to
  cross-reference.

- **All teams**: petalTongue's wire-format detection now matches sweetGrass's
  whitespace-tolerant `detect_protocol` pattern.
