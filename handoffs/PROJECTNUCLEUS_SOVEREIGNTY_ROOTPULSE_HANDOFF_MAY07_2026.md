# projectNUCLEUS — Sovereignty Evolution, RootPulse, and Gap Discovery Handoff

**Date**: 2026-05-07
**From**: projectNUCLEUS (ironGate)
**For**: primalSpring, all primal teams, spring teams
**Scope**: System hardening, sovereignty dependency mapping, RootPulse commit
workflow validation, Forgejo calibration instrument, and 14 upstream gaps
discovered across petalTongue, NestGate, and biomeOS/RootPulse.

---

## Summary

projectNUCLEUS completed a sovereignty evolution cycle on ironGate:

1. **System hardened** — UFW deny-by-default, JupyterHub security headers,
   three-layer pen test, zero open gaps
2. **35 external dependencies mapped** across 6 clusters with primal
   replacement status for each
3. **Forgejo v15.0.0 installed** as git self-hosting calibration instrument
   at `git.primals.eco`, projectNUCLEUS mirrored
4. **RootPulse commit workflow tested** end-to-end against live primals —
   5/6 phases pass, Phase 5 (LoamSpine commit) has API mismatch
5. **14 upstream gaps documented** in 3 handback documents with severity,
   owner, and blocking relationships
6. **benchScale framework created** with 5 parity scenarios and 3 pentest
   scripts for validating external dependency replacements
7. **Hourly Cloudflare baselines capturing** for systematic tunnel evolution

---

## Infrastructure Changes

### New Services on ironGate

| Service | Type | Port | Systemd Unit | Purpose |
|---------|------|------|-------------|---------|
| Forgejo v15.0.0 | System | 3000 | `forgejo.service` | Git calibration instrument |
| Cloudflare Tunnel | User | outbound | `cloudflared-tunnel.service` | Routes lab + git subdomains |

### New DNS Routes

| Hostname | Target | Purpose |
|----------|--------|---------|
| `git.primals.eco` | `http://127.0.0.1:3000` | Forgejo web UI + git operations |

### UFW Firewall (new)

Deny-by-default. Allow: SSH (22), localhost, LAN (192.168.1.0/24).
All primals remain localhost-only. Tunnel traffic is outbound-only.

### JupyterHub Security Headers (new)

X-Frame-Options: DENY, X-Content-Type-Options: nosniff,
Referrer-Policy: same-origin, Server: NUCLEUS (version suppressed).

---

## Upstream Gaps Discovered

### petalTongue — 5 Gaps (PT-1 → PT-5)

**Source**: `projectNUCLEUS/validation/PETALTONGUE_GAPS_HANDBACK.md`
**Test**: Started `petaltongue web --bind 127.0.0.1:9901`, tested arbitrary paths.

| Gap | Severity | Issue | Blocks |
|-----|----------|-------|--------|
| PT-1 | High | `web` mode has 6 hardcoded routes, no catch-all for static files | GitHub Pages replacement (Step 3a) |
| PT-2 | High | No NestGate backend integration for content resolution | Content-addressed serving |
| PT-3 | Medium | No web-mode config schema (docroot, backend, cache) | Production deployment |
| PT-4 | Medium | Deploy mode mismatch (`server` vs `web`) | Dual IPC+HTTP deployment |
| PT-5 | Low | `--workers` flag accepted but unused | Production tuning |

**Shortest fix for PT-1**: ~10 lines of Rust — `ServeDir` fallback with `--docroot` flag.
`tower-http::ServeDir` is already imported in `web_mode.rs`.

### NestGate — 4 Gaps (NG-1 → NG-4)

**Source**: `projectNUCLEUS/validation/NESTGATE_CONTENT_GAPS_HANDBACK.md`
**Test**: JSON-RPC calls to `storage.store`, `storage.store_blob`,
`storage.retrieve`, `storage.fetch_external`, `content.put`, `content.get`.

| Gap | Severity | Issue | Blocks |
|-----|----------|-------|--------|
| NG-1 | High | No content-addressed storage (BLAKE3 hash as auto-key) | Publishing pipeline |
| NG-2 | Medium | No collection/manifest for versioned releases | Atomic site deployment |
| NG-3 | Medium | Blob store and KV store are separate namespaces | Content enumeration |
| NG-4 | Low | No streaming store for large content | Large file publishing |

**Building block exists**: `storage.fetch_external` already computes BLAKE3
hashes. The content-addressed method would reuse this logic for local content.

### RootPulse / biomeOS — 5 Gaps (RP-1 → RP-5)

**Source**: `projectNUCLEUS/validation/ROOTPULSE_GAPS_HANDBACK.md`
**Test**: Executed all 6 phases of `rootpulse_commit.toml` against live primals.

| Gap | Severity | Issue | Blocks |
|-----|----------|-------|--------|
| RP-1 | High | Graph→primal method name and parameter mismatches (3 phases) | Graph execution |
| RP-2 | High | Missing spine lifecycle in graph (no `spine.create` step) | Phase 5 |
| RP-3 | Medium | Graph schema lacks type information for variable interpolation | Automated execution |
| RP-4 | Medium | No standalone graph executor CLI (`biomeos graph execute`) | End-to-end testing |
| RP-5 | Medium | Entry signing lifecycle unclear (BearDog signs what, when?) | Phase 5 correctness |

**What worked**: Phases 1 (health), 2 (DAG dehydrate → merkle root),
3 (Ed25519 sign), 4 (NestGate store), 6 (sweetGrass braid with W3C PROV).
**What failed**: Phase 5 — `commit.session` doesn't exist; actual API is
`entry.append` with `SessionCommit` variant requiring `spine_id`, `committer`
(DID), `merkle_root` (byte array), and `signature`.

---

## Sovereignty Dependency Map

Full inventory in `projectNUCLEUS/specs/COMPLETE_DEPENDENCY_INVENTORY.md`.

| Cluster | Count | Priority | Primal Coverage |
|---------|-------|----------|----------------|
| 1. Cloudflare (DNS/TLS/CDN/Tunnel) | 6 | High | ~80% mapped, baselines capturing |
| 2. GitHub (Repos/CI/Pages/Releases) | ~15 | High | ~30% mapped, Forgejo calibration |
| 3. Package Registries | 4 | Low | Vendor escape hatch known |
| 4. Container Registries | 3 | Low | Config swap path known |
| 5. AI/ML APIs | 3 | Low | Ollama fallback working |
| 6. Science Data APIs | 3 | Low | Data registry operational |

---

## NUCLEUS Composition Patterns for Downstream

### How NUCLEUS Deploys (for spring teams)

```
plasmidBin (binaries) + primalSpring (graphs) + wateringHole (standards)
    ↓ deploy.sh --composition full --gate irongate
13 primals on localhost (9100-9900, all 127.0.0.1)
    ↓ biomeOS coordinates via discovery hierarchy
Workloads dispatched through toadStool
    ↓ provenance_pipeline.sh wraps execution
BLAKE3 → rhizoCrypt DAG → loamSpine ledger → sweetGrass braid
```

### neuralAPI Deployment Pattern

Springs interact with primals via JSON-RPC over TCP/UDS. The composition
pattern validated on ironGate:

1. biomeOS discovers primals via 5-tier hierarchy
2. Springs call primals directly (TCP fallback ports, not Neural API routing)
3. Each primal has a canonical TCP port from Phase 59 table
4. All calls use JSON-RPC 2.0 with method namespacing (`primal.method`)

**Gap for Neural API routing**: Direct JSON-RPC works today. Neural API
routing (biomeOS → capability → primal) is specified but not validated
in production. This is the Gen3→Gen4 bridge that RootPulse needs.

### Deploy Graph Pattern for primalSpring

The `rootpulse_commit.toml` graph demonstrates the pattern:
- `rpc_call` nodes target primals by name with `method` + `params`
- `capability_call` nodes use `capability` string for discovery routing
- Sequential coordination via `depends_on` arrays
- Timeout constraints per node

**Key finding**: The graph TOML files are design documents, not tested
integration contracts. A graph validation pass that checks method names
and parameter schemas against live primal capabilities would catch
mismatches automatically.

---

## Forgejo Calibration Targets for RootPulse

Forgejo provides real-world baselines that RootPulse must match:

| Metric | How to Measure | Significance |
|--------|---------------|-------------|
| Clone time | `git clone` via tunnel, time | End-to-end repo fetch |
| Push latency | `git push`, time | Write path |
| Web UI TTFB | `curl -w '%{time_starttransfer}'` | User experience |
| Storage per repo | `du -sh /var/lib/forgejo/repos/` | Efficiency |
| Operations per workflow | Count RPCs for commit+push | Complexity budget |

These are the RootPulse team's parity targets once the commit workflow
(RP-1 through RP-5) is resolved.

---

## Files Created/Modified

### New Files (projectNUCLEUS)

| File | Purpose |
|------|---------|
| `specs/COMPLETE_DEPENDENCY_INVENTORY.md` | 35 dependencies, 6 clusters, replacement mappings |
| `specs/SOVEREIGNTY_VALIDATION_PROTOCOL.md` | Master cutover document |
| `validation/PETALTONGUE_GAPS_HANDBACK.md` | 5 petalTongue gaps |
| `validation/NESTGATE_CONTENT_GAPS_HANDBACK.md` | 4 NestGate gaps |
| `validation/ROOTPULSE_GAPS_HANDBACK.md` | 5 RootPulse/biomeOS gaps |
| `validation/PENTEST_AND_VALIDATION_PHASE2A_MAY07_2026.md` | Pen test results |
| `validation/security-20260507-110312/*` | Security scan artifacts |
| `validation/baselines/capture_tunnel_metrics.sh` | Hourly baseline capture |
| `validation/baselines/summarize_baselines.sh` | 7-day summary generator |
| `graphs/rootpulse_commit.toml` | Ported from biomeOS for testing |
| `infra/benchScale/*` | Load generation + pentest framework |

### Modified Files

| File | Change |
|------|--------|
| `README.md` | Added sovereignty status, services table, repo structure |
| `PHASES.md` | Updated Phase 2 with hardening + sovereignty + RootPulse |
| `specs/README.md` | Added SOVEREIGNTY_VALIDATION_PROTOCOL + DEPENDENCY_INVENTORY |
| `specs/TUNNEL_EVOLUTION.md` | Concrete implementation for Steps 2b→4 |
| `~/.cloudflared/config.yml` | Added `git.primals.eco` ingress |

### System Configuration

| Change | Location |
|--------|----------|
| Forgejo binary | `/opt/forgejo/forgejo` (v15.0.0) |
| Forgejo data | `/var/lib/forgejo/` (SQLite + repos) |
| Forgejo config | `/var/lib/forgejo/custom/conf/app.ini` |
| Forgejo service | `/etc/systemd/system/forgejo.service` |
| UFW rules | deny-default + allow SSH/LAN/localhost |
| JupyterHub config | Security headers added |
| Cron job | Hourly tunnel baseline capture |

---

## Recommended Next Steps for Upstream Teams

### For petalTongue Team
1. Add `--docroot <path>` flag to `web` mode (~10 lines, `ServeDir` fallback)
2. Consider NestGate backend integration for Phase 3a
3. Align deploy modes (`server` vs `web`) or document the distinction

### For NestGate Team
1. Add `content.put` method (accept content, auto-compute BLAKE3, return hash)
2. Unify blob/KV namespaces or add `storage.list_blobs`
3. Consider collection/manifest concept for atomic deployments

### For biomeOS Team
1. Update `rootpulse_commit.toml` method names to match current primal APIs
2. Add `spine.create` as Phase 0 prerequisite in commit graph
3. Consider a `biomeos graph execute <file.toml>` CLI for integration testing
4. Clarify entry signing lifecycle (who signs what, when)

### For LoamSpine Team
1. Document `entry.append` parameter requirements (SessionCommit struct)
2. Consider convenience method matching `commit.session` graph spec
3. Clarify DID format expectations for `committer` field

### For primalSpring
1. Validate all graph TOML files against live primal capability lists
2. Consider adding a graph validation CI step
3. Review the 14 upstream gaps for inclusion in the next phase roadmap
