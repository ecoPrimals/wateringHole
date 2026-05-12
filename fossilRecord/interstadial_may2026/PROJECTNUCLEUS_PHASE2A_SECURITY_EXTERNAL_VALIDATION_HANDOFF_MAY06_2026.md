<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# projectNUCLEUS — Phase 2a Security & External Validation Handoff

**Date**: May 6, 2026
**From**: projectNUCLEUS (ironGate)
**To**: primalSpring, all primal teams, wateringHole

---

## Summary

Phase 2a validated on ironGate: 13 primals deployed, Cloudflare Tunnel
ionic baseline captured, three-layer penetration testing completed, ABG
tiered access operational. This handoff documents findings that need
upstream evolution.

**Key numbers**: 13/13 primals healthy, 15/15 external validation checks,
270ms p50 tunnel latency, 235+ science checks, 7/13 primal ports rebound
to localhost. Six primals need upstream `--bind` flag.

---

## 1. Universal `--bind` Flag (UniBin v1.1)

Six primals only accept `--port` and hardcode `0.0.0.0` as bind address:

| Primal | Port | Risk | Notes |
|--------|------|------|-------|
| Songbird | 9200 | HIGH | `--listen` is IPC only, HTTP server has no bind control |
| ToadStool | 9400 | MEDIUM | Accepts workload submissions from LAN |
| skunkBat | 9140 | MEDIUM | Leaks security posture data |
| biomeOS | 9800 | MEDIUM | Neural API / orchestration exposed |
| sweetGrass | 9850 | MEDIUM | Main TCP listener; HTTP endpoint already has `--http-address` |
| petalTongue | 9900 | LOW | UI only |

Seven primals already support bind control with six different flag names
(`--listen`, `--bind`, `--bind-address`, `--host`, `--rpc-bind`,
`--http-address`). Recommendation: standardize on `--bind <host:port>` in
UniBin v1.1 with default `127.0.0.1`.

**Action**: wateringHole to update UniBin standard, each primal team to
add the flag (1 hour per primal).

---

## 2. NestGate `storage.list` Unauthenticated

`storage.list` returns results without BTSP authentication. All other
sensitive methods (`storage.get`, `storage.put`) require BTSP.

**Action**: NestGate team to add BTSP scoping for `storage.list`, or
gate it behind capability tokens.

---

## 3. Primal API Resilience (Positive)

All primals survived input fuzzing — 7 malformed JSON-RPC payloads per
primal, including path traversal in method names, oversized params,
missing required fields, and null injection. No crashes, no unhandled
panics. Rust serde + type system provides strong defaults.

No hidden debug/admin methods found via enumeration (tested 7 method
patterns per primal including `admin.*`, `debug.*`, `internal.*`).

sweetGrass and rhizoCrypt correctly reject plaintext on BTSP-enforced
ports.

---

## 4. Tunnel Baseline Metrics

Cloudflare quick tunnel (`cloudflared` 2026.3.0) via QUIC to ORD edge:

| Metric | Value |
|--------|-------|
| Latency p50 | 270ms |
| Protocol | QUIC + h2 |
| TLS | Cloudflare edge (auto) |
| Endpoints validated | JupyterHub login, API, health + 13 primal healthchecks |

These become parity targets for each tunnel evolution step (Steps 2b-2e).
See `projectNUCLEUS/specs/TUNNEL_EVOLUTION.md` for the replacement plan.

---

## 5. skunkBat Training Data

skunkBat was live during all pen testing (security.scan → security.metrics).
Detected 0 threats, quarantined 0 connections. This is expected — skunkBat
needs baseline data to distinguish normal from anomalous.

The pen test payloads (fuzz patterns, enumeration patterns, port scans)
are now available as training data for baseline learning. Recommendation:
skunkBat should learn to detect these patterns and alert when they appear
in production traffic.

---

## 6. Composition-Level Fixes Already Applied

These were fixed in `projectNUCLEUS/deploy/deploy.sh` without primal changes:

- `BIND_ADDRESS` variable (default `127.0.0.1`) controls 7 primal bind addresses
- `jupyterhub.sqlite` permissions: 644 → 600
- sweetGrass `--http-address` uses `host:port` format (was failing with host-only)
- Songbird `--listen` flag removed from HTTP launch (it's for IPC)

---

## 7. ABG Tiered Access (for compute-sharing standards)

JupyterHub PAM-based tiered access is operational:

| Tier | Linux Group | Mem Limit | CPU Limit | Execute | Visualize |
|------|-------------|-----------|-----------|---------|-----------|
| observer | `abg-observer` | 8 GB | 4 cores | No | Yes (cached) |
| compute | `abg-compute` | 32 GB | 8 cores | Yes | Yes |
| admin | `abg-admin` | 48 GB | 16 cores | Yes | Yes + API |

`pre_spawn_hook` in JupyterHub sets `NUCLEUS_TIER`, resource limits, and
primal port environment. `NUCLEUS_READONLY=1` for observers.

This pattern may be useful for wateringHole's `compute-sharing/` standards
as the canonical tiered access model for ionic bonding.

---

## Detailed Reports

| Report | Location |
|--------|----------|
| Security findings + before/after | `projectNUCLEUS/validation/SECURITY_HANDBACK_MAY06_2026.md` |
| Security spec | `projectNUCLEUS/specs/SECURITY_VALIDATION.md` |
| External pipeline validation | `projectNUCLEUS/validation/EXTERNAL_PIPELINE_VALIDATION_MAY06_2026.md` |
| Phase architecture | `projectNUCLEUS/PHASES.md` |
| Notebook elevation spec | `projectNUCLEUS/specs/NOTEBOOK_ELEVATION.md` |
| Tunnel evolution spec | `projectNUCLEUS/specs/TUNNEL_EVOLUTION.md` |

---

## Action Summary

| Action | Owner | Priority | Effort |
|--------|-------|----------|--------|
| Add `--bind` to UniBin v1.1 | wateringHole | HIGH | 1 day |
| Add `--bind` to 6 primals | Songbird, ToadStool, skunkBat, biomeOS, sweetGrass, petalTongue | HIGH | 1 hour each |
| NestGate BTSP scoping | NestGate team | MEDIUM | 1 day |
| skunkBat baseline learning | skunkBat team | MEDIUM | Evolution cycle |
| Tiered access pattern → wateringHole standard | wateringHole / compute-sharing | LOW | Documentation |
