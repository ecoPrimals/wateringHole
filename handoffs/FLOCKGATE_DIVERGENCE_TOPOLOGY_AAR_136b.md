# AAR: flockGate Divergence + Topology Issues — Wave 136b

**Date**: 2026-07-11 21:40 EDT  
**Author**: flockGate overwatch  
**Wave**: 136b  
**Severity**: P2 (data divergence) + P2 (mesh topology gap)

---

## Executive Summary

Two issues surfaced during flockGate's 136b sync and WAN probe cycle:

1. **DIVERGENCE** — `s_cascade_provenance_match` scenario reported 0 checksums despite `checksums.toml` having 14 entries per architecture. Parser was reading at the wrong TOML nesting level.
2. **TOPOLOGY** — songBird mesh has **zero peers** from flockGate. Federation port 7700 is not reachable on the WireGuard overlay. `capability.call` remains fully blocked — not just missing `DRAWBRIDGE_ROUTES`, but no mesh connectivity at all.

---

## Issue 1: Checksums Parser Divergence

### Symptom

```
[FAIL] xref:checksums_loaded: 0 entries in checksums.toml
[FAIL] xref:all_have_checksums: checksum coverage: 0/13 (missing: barracuda, beardog, ...)
```

Suite reported 0 checksums despite the file containing 28 entries (14 per architecture).

### Root Cause

`load_checksums()` in `s_cascade_provenance_match.rs` assumed a flat structure:

```toml
barracuda = { blake3 = "...", size = ... }
```

Actual structure is arch-nested:

```toml
[x86_64-unknown-linux-musl]
barracuda = { blake3 = "...", size = ... }

[aarch64-unknown-linux-musl]
barracuda = { blake3 = "...", size = ... }
```

The parser iterated top-level keys (arch triples), found tables, and looked for `blake3` directly in the arch table rather than iterating into the per-primal entries within.

### Fix

Committed as `fb03030` on primalSpring. Parser now iterates into architecture sub-tables:

```rust
for (_key, section) in &table {
    if let Some(arch_table) = section.as_table() {
        for (slug, entry) in arch_table {
            if let Some(t) = entry.as_table() {
                if let Some(hash) = t.get("blake3").and_then(|v| v.as_str()) {
                    map.insert(slug.clone(), hash.to_owned());
                }
            }
        }
    }
}
```

### Impact

- `cascade-provenance-match` scenario was silently FAILING on all gates
- `registry_all_rust_tier_pass` integration test caught it (asserts 0 failures for all Rust-tier scenarios)
- Without `ECOPRIMALS_ROOT` + `ECOPRIMALS_PLASMID_BIN` env vars, the test was skipped rather than failing — masking the bug on CI-like environments

### Recommendation

- Gates running primalSpring should set both `ECOPRIMALS_ROOT` and `ECOPRIMALS_PLASMID_BIN` for full depot validation coverage
- Consider adding a `[meta]` key to `checksums.toml` that declares the structure version, so parsers can validate expectations

---

## Issue 2: Mesh Topology — Federation Port Unreachable

### Symptom

```json
{"error":{"code":-32603,"message":"No local provider for 'jupyter' and no reachable mesh peers for remote dispatch"}}
```

songBird on flockGate initializes fine (`mesh.init` succeeds, `mesh.announce` succeeds) but has **0 peers** — no remote dispatch possible.

### Topology Observed

```
flockGate (NYC)
  └── WireGuard wg0 → 10.13.37.x/24
       └── Peer: golgiBody (157.230.3.183 / 10.13.37.1)
            ├── ICMP: 0% loss, ~30ms RTT ✓
            ├── Port 443 (Caddy): REACHABLE via public DNS ✓
            ├── Port 7700 (songBird federation): CONNECTION REFUSED ✗
            ├── Port 8080 (drawbridge): TIMEOUT ✗
            └── Port 9090 (alt): TIMEOUT ✗
```

### Root Cause (Compound)

1. **UFW on golgi** does not allow port 7700 on the WireGuard interface (`wg0`). songBird federation listens on localhost or is not bound at all on golgi.
2. **No songBird process running on golgi/sporeGate** with `--federation-port 7700` exposed to the mesh network.
3. **Even if federation were exposed**, `SONGBIRD_DRAWBRIDGE_ROUTES` is not configured on sporeGate — so `capability.call("jupyter")` would still fail to route.

### Impact

- **capability.call is 100% non-functional from WAN** — not degraded, completely inoperative
- The HTTP data path works fine (flockGate → Cloudflare → Caddy → backend) but this bypasses the mesh entirely
- Mesh peer discovery, capability advertisement, and remote dispatch are all blocked by the same topology gap

### Required Actions (sporeGate/golgi)

| # | Action | Owner |
|---|--------|-------|
| 1 | Start songBird with `--federation-port 7700` on golgi | sporeGate |
| 2 | UFW: `ufw allow in on wg0 to any port 7700 proto tcp` | sporeGate |
| 3 | Set `SONGBIRD_DRAWBRIDGE_ROUTES=/hub=jupyter` in songBird env | sporeGate |
| 4 | Verify from flockGate: `curl http://10.13.37.1:7700/` returns songBird handshake | flockGate |

### Workaround

HTTP transport via `membrane.primals.eco` works at ~138ms p50. Direct WireGuard ICMP at ~30ms. If songBird federation were exposed, mesh RTT should be ~30-35ms (WG direct) vs ~138ms (public internet + Cloudflare + Caddy overhead).

---

## Latency Baseline (136b)

| Path | p50 | p95 | Method |
|------|-----|-----|--------|
| flockGate → membrane.primals.eco (HTTPS) | 138ms | 150ms | curl to /depot/ (5 samples) |
| flockGate → golgi (WireGuard ICMP) | 30ms | 32ms | ping -c3 10.13.37.1 |
| flockGate → golgi (federation 7700) | — | — | UNREACHABLE |
| flockGate → capability.call mesh | — | — | 0 PEERS |

---

## Validation State

| Metric | Value |
|--------|-------|
| primalSpring SHA | `fb03030` |
| Tests | 1,104 |
| Scenarios | 132 |
| Failures | 0 |
| Suite | GREEN |
| Env required | `ECOPRIMALS_ROOT` + `ECOPRIMALS_PLASMID_BIN` |

---

## Summary

The divergence was a parser bug — straightforward fix, now green. The topology gap is the same blocker from Wave 134c, now more precisely characterized: it's not just a missing env var, it's a completely absent federation listener on the WireGuard overlay. Until golgi/sporeGate exposes songBird federation on port 7700 over wg0, the mesh is WAN-partitioned and `capability.call` is dead from any external gate.

**Priority**: sporeGate should address items 1-3 above. flockGate will re-probe immediately upon notification.
