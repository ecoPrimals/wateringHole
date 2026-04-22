# ToadStool S203b — LD-04/LD-05: Persistent Connections + Socket Separation

**Date**: April 12, 2026
**Session**: S203b
**Primal**: toadStool
**Author**: toadStool team
**Prior**: S203 (composition elevation + deep debt)
**Context**: primalSpring downstream audit — LD-04 (UDS single-shot) + LD-05 (socket namespace collision)

---

## Summary

Resolved two primalSpring audit findings that blocked reliable multi-step
dispatch sequences and inter-primal socket coexistence:

**LD-04** — JSON-RPC UDS/TCP server was single-shot in HTTP mode: processed one
request, wrote `Connection: close`, and returned. Clients doing submit → status →
result dispatch sequences got broken pipe on the second call. NDJSON mode also
broke on blank lines between requests. Evolved to HTTP/1.1 keep-alive loop and
resilient NDJSON handling.

**LD-05** — JSON-RPC and tarpc both bound the same `compute.sock`. The tarpc
`serve_unix` removed the JSON-RPC socket file and re-bound, orphaning the
JSON-RPC listener. Clients connecting to `compute.sock` would silently reach
tarpc binary framing instead of JSON-RPC. Separated: JSON-RPC on `compute.sock`
(primary), tarpc on `compute-tarpc.sock` (secondary).

## Changes

### LD-04: Persistent Connections

- **HTTP/1.1 keep-alive loop** — `handle_http_keepalive_unix` / `_tcp` process
  multiple HTTP requests on a single connection. Default is keep-alive per
  HTTP/1.1 spec; closes on `Connection: close` header or EOF.
- **NDJSON resilience** — `handle_ndjson_unix` / `_tcp` skip empty lines
  between JSON-RPC requests instead of breaking the connection.
- **Both transports fixed** — `connection/unix.rs` and `connection/tcp.rs`
  share the same pattern.

### LD-05: Socket Namespace Separation

- **JSON-RPC primary**: `compute.sock` (dev) / `compute-{fid}.sock` (prod)
- **tarpc secondary**: `compute-tarpc.sock` (dev) / `compute-{fid}-tarpc.sock` (prod)
- **Legacy symlink**: `toadstool.sock → compute.sock` (unchanged)
- **Shutdown cleanup**: Both sockets removed on graceful shutdown
- **Namespace partition**: toadStool claims `compute*.sock`, leaving
  `compute-math*.sock` available for barraCuda

## Code Health (S203b State)

| Metric | Value |
|--------|-------|
| Tests | 21,600+ passing (0 failures) |
| Clippy | 0 warnings (workspace-wide `--all-targets`) |
| Doc warnings | 0 |
| New tests | +7 (keep-alive, NDJSON, socket naming) |

## For primalSpring Gap Registry

- **LD-04 (UDS single-shot)**: RESOLVED — HTTP/1.1 keep-alive + NDJSON
  persistent connections on both UDS and TCP transports.
- **LD-05 (socket namespace)**: RESOLVED — JSON-RPC and tarpc on separate
  sockets. barraCuda can use `compute-math.sock` without collision.

## For barraCuda Team (LD-05 Coordination)

toadStool now claims the following socket names under `$XDG_RUNTIME_DIR/biomeos/`:

| Socket | Protocol | Family-scoped |
|--------|----------|---------------|
| `compute.sock` | JSON-RPC 2.0 (primary) | `compute-{fid}.sock` |
| `compute-tarpc.sock` | tarpc (secondary) | `compute-{fid}-tarpc.sock` |
| `toadstool.sock` | Legacy symlink → compute.sock | `toadstool-{fid}.sock` |

barraCuda should use a **distinct** domain stem (e.g. `compute-math.sock`) to
avoid bind collision. If both primals need to share the `compute` domain,
coordinate via primalSpring on sub-domain naming convention.
