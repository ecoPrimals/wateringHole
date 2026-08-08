# primalSpring — Wave 157a Dispatch Fix Verification

**Date**: Aug 8, 2026 (evening session)
**Team**: primalSpring code team (eastGate)
**Wave**: 157a
**Context**: biomeOS dispatch reorder (`44c40191`) + routing gaps (`6f60cccf`) shipped

## Summary

The biomeOS Neural API dispatch reorder fix has been **verified live on eastGate**.
The 15-second timeout is eliminated. Capability routing and graph execution are
fully operational. A new experiment (exp121) specifically validates the remaining
riboCipher auto-detect gap.

## Results

### N2-N5 Verification (Dispatch Fix Confirmed)

| Experiment | Result | Key Improvement |
|-----------|--------|-----------------|
| exp118: Graph Execution | **14/14 ALL PASS** | Was 6/12 → now 14/14. Graph.list, graph.execute, graph.status all work |
| exp119: PathwayLearner | **12/12 ALL PASS** | 919 exec/s throughput, CV=0.60 timing consistency |
| exp120: Self-Registration | **29/29 ALL PASS** | 34 caps, 58 methods, 11/11 domains resolve |
| exp121: riboCipher Auto-Detect | **32/36 PASS** | Dispatch proven (mean 1.3ms, max 2.5ms). Gap confirmed. |

### Dispatch Reorder Verification

| Metric | Before (Jul 15 binary) | After (44c40191) |
|--------|------------------------|-------------------|
| Mean latency | 15,000ms (timeout) | **1.3ms** |
| Max latency | 15,000ms | **2.5ms** |
| Forwarding success | 0/11 primals | **9/11 primals** |
| Graph execution | 0 (not found) | **55 graphs, 1.2ms/exec** |

### Protocol Classification (exp121 Phase 1+2)

| Primal | Protocol Affinity | Forward via Neural API |
|--------|-------------------|----------------------|
| beardog | Plain only | **PASS** |
| songbird | Dual-lane | **PASS** |
| skunkbat | Dual-lane | **PASS** |
| sweetgrass | **riboCipher ONLY** | FAIL (auto-detect gap) |
| rhizocrypt | Dual-lane | **PASS** |
| loamspine | Dual-lane | **PASS** |
| toadstool | N/A (TARPC) | FAIL (protocol mismatch) |
| coralreef | Dual-lane | **PASS** |
| barracuda | Dual-lane | **PASS** |
| squirrel | Dual-lane | **PASS** |
| petaltongue | Dual-lane | **PASS** |

## What Was Delivered

### exp121: riboCipher Dispatch Auto-Detect (NEW)

A targeted experiment that:
1. Probes each primal directly to classify protocol affinity
2. Tests Neural API `capability.call` forwarding per-primal
3. Measures dispatch timing to prove reorder fix
4. Identifies the riboCipher auto-detect gap

This experiment serves as the **acceptance test** for when biomeOS ships
the auto-detect fix: once sweetGrass accepts forwarded calls, exp121 will
go from 32/36 → 36/36.

### exp118 Fix

Updated to use `health.check` (working method) instead of `sign_ed25519`
(requires beardog-specific operation), and added `"primals"` field check
in `capability.discover` response parsing.

## Remaining Gap: riboCipher Auto-Detect

**Status**: Pool exists (`send_ribocipher_jsonrpc()`), auto-detect NOT wired.

The biomeOS neural-api forwards ALL capability.call requests using **plain
JSON-RPC**. This works for 9/11 primals. But sweetGrass (G68) enforces
riboCipher and rejects plain connections with:

```
riboCipher signal required. Send [0xEC/0xED, protocol_type] prefix.
```

**Required fix** (biomeOS team): When forwarding `capability.call` to a primal,
check the primal's `signal_tier` from the announce registration:
- If `signal_tier` includes "nest" (sweetGrass, rhizoCrypt G68) → use `send_ribocipher_jsonrpc()`
- Otherwise → use plain JSON-RPC forwarding (current behavior)

The dual-lane pool already exists per `44c40191`. The missing piece is the
conditional dispatch based on the target primal's tier.

**Note**: rhizoCrypt currently accepts BOTH plain and riboCipher (dual-lane).
Only sweetGrass strictly enforces riboCipher. This may change if rhizoCrypt
is updated to enforce G68 riboCipher policy.

### toadStool Protocol Mismatch

toadStool uses TARPC (not JSON-RPC) on `compute-tarpc.sock`. The Neural API
JSON-RPC forwarding is fundamentally incompatible. This requires either:
- toadStool adds a JSON-RPC shim endpoint, OR
- Neural API adds TARPC forwarding support

This is a longer-term architecture decision, not a P1.

## Test Results

- 1,219 workspace tests pass (3 pre-existing env failures)
- 99 experiments (exp121 added)
- 198 validation scenarios (15 tracks, 3 tiers)
- Zero new regressions

## Infrastructure Notes

- Neural API debug binary (with fix) must be used; depot binary is Jul 15 (pre-fix)
- Graph executor requires `~/graphs` symlink → primalSpring graphs dir
- Primal sockets require services to be running (not just process alive)
- songBird needs stale PID cleanup before restart
