# Three-Domain Topology Spec

**Date**: Aug 4, 2026 | **Wave**: 156b | **From**: sporeGate (eastGate overwatch)
**Owner**: sporeGate topology team
**Status**: SPEC — nestgate.io redirect LIVE, evolution to petalTongue in progress

---

## Domain Architecture

The ecoPrimals ecosystem operates across three distinct DNS domains,
each mapped to a K-Derm envelope layer:

```
┌────────────────────────────────────────────────────────────────┐
│                     INTERNET (public)                          │
│                                                                │
│  primals.eco ─────────── OUTER MEMBRANE                        │
│  ├── sporeprint.primals.eco   Public research site (Zola)      │
│  ├── lab.primals.eco          Lab gateway (Caddy → Tower)      │
│  └── *.primals.eco            Public-facing services           │
│                                                                │
│  nestgate.io ────────── PEPTIDOGLYCAN LAYER                    │
│  ├── git.primals.eco          Forgejo (sovereign git)          │
│  ├── nestgate.io/data/        CAS data braids (petalTongue)    │
│  ├── nestgate.io/depot/       Binary depot browser             │
│  ├── nestgate.io/provenance/  Provenance chain viewer          │
│  └── nestgate.io/validate/    Replication validation endpoint  │
│                                                                │
│  primal.eco ─────────── INNER MEMBRANE                         │
│  ├── WireGuard mesh only      Gate-to-gate (10.13.37.0/24)     │
│  ├── UDS/JSON-RPC             Primal-to-primal IPC             │
│  └── songBird mesh            Federation + drawbridge           │
└────────────────────────────────────────────────────────────────┘
```

### Domain Responsibilities

| Domain | Envelope | Serves | Served By | DNS |
|--------|----------|--------|-----------|-----|
| **primals.eco** | Outer membrane | Public site, publications, lab access | sporePrint (Zola) + Caddy | Cloudflare |
| **nestgate.io** | Peptidoglycan | CAS braids, depot, provenance, validation, git | petalTongue + Forgejo + Caddy | Porkbun/CF |
| **primal.eco** | Inner membrane | Mesh-only gate comms, NUCLEUS IPC | WireGuard + UDS + songBird | Internal only |

### Why Three Domains

1. **primals.eco** is the public face — researchers, PIs, anyone can see publications
   and the research catalog. Zola static site, maximum security posture.

2. **nestgate.io** is the validation surface — where CAS data braids are exposed so
   others can validate provenance, replicate datasets, and verify computational results.
   This is NOT the public site; it's the PI/researcher-facing "trust surface" where
   data integrity is proven. Served by **petalTongue** (not Zola), making it a
   validated system that dogfoods the primals.

3. **primal.eco** is the inner mesh — gate-to-gate communication, NUCLEUS IPC,
   songBird federation. Never exposed publicly. WireGuard mesh only.

---

## nestgate.io Evolution Plan

### Current State (LIVE)

nestgate.io redirects to `sporeprint.primals.eco/data/`:
```
nestgate.io → 301 → https://sporeprint.primals.eco/data/
```

DNS: A record → 157.230.3.183 (golgi), TLS: Let's Encrypt via Caddy, DNSSEC: ON

### Phase 1: petalTongue Data Surface

Replace the redirect with petalTongue serving the data braids natively:

```
nestgate.io {
    reverse_proxy unix//run/membrane/petaltongue.sock
}
```

petalTongue renders:
- `/data/` — CAS-backed data domain browser (W3C PROV-O braids inline)
- `/data/{domain}/` — per-domain page with dataset provenance
- `/data/transplant/` — pseudoSpore/lithoSpore replication guide

**Advantage**: Data pages are served by a primal, not a static site. petalTongue
can query nestGate CAS in real-time, showing live provenance chains, BLAKE3
verification results, and dataset freshness.

### Phase 2: Depot + Provenance Browser

Add depot and provenance inspection:
- `/depot/` — browse binary depot by architecture and primal
- `/depot/{arch}/{primal}` — BLAKE3 checksum, build provenance, source commit
- `/provenance/` — full provenance chain viewer (CAS → DAG → spine)
- `/provenance/{hash}` — single-object provenance tree

### Phase 3: Validation Endpoint

Public validation API:
- `/validate/cas/{hash}` — verify a CAS object exists and return its provenance
- `/validate/dataset/{name}` — verify all objects in a dataset, report completeness
- `/validate/replicate/{name}` — generate replication package (hashes + instructions)

This is what makes nestgate.io the "trust surface" — external researchers can
independently verify that the data they received matches the provenance chain.

### Phase 4: git Migration

Move `git.primals.eco` under nestgate.io:
- `nestgate.io/git/` or `git.nestgate.io` — Forgejo
- CAS + git + depot all under the peptidoglycan layer

---

## Caddy Configuration (golgi)

### Current (redirect)
```
nestgate.io {
    redir https://sporeprint.primals.eco/data{uri} permanent
}
```

### Target (petalTongue)
```
nestgate.io {
    reverse_proxy unix//run/membrane/petaltongue.sock {
        header_up Host {upstream_hostport}
    }
}
```

---

## CAS Data Braids Divergences (Upstream → Overwatch)

These divergences from the tideGlass CAS wiring AAR affect all primals
consuming CAS data. **Owned by upstream overwatch, not sporeGate topology.**

| DIV | Issue | Owner |
|-----|-------|-------|
| DIV-1 | DATA_ACCESS.md wrong hash format (`blake3:abc123` vs plain hex) | overwatch |
| DIV-2 | No `content.query` — only exact hash retrieval | nestGate team |
| DIV-3 | DATA_ACCESS.md references nonexistent methods | overwatch |
| DIV-4 | GPS data is NumPy/pickle — needs converter | westGate data |
| DIV-5 | groundSpring, airSpring stale CAS clients | overwatch |
| DIV-6 | `content.get` 64 MiB limit — needs streaming | nestGate team |

**Recommendation from tideGlass**: Publish canonical `nestgate-client` crate.

---

## DNS Ownership

| Domain | Registrar | DNS Provider | Managed By |
|--------|-----------|--------------|------------|
| primals.eco | Porkbun | Cloudflare | sporeGate |
| nestgate.io | Porkbun | Cloudflare | sporeGate |
| primal.eco | Porkbun | Internal only | sporeGate |

All DNS changes flow through sporeGate topology team.
Cloudflare and Porkbun credentials accessible from sporeGate.
