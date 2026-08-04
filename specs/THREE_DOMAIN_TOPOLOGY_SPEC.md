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

### Phase 3: Federated CAS + Compute Memoization

nestgate.io becomes the **data federation surface** — not just one gate's CAS,
but a federated view across all gates:

- `/cas/{hash}` — retrieve any CAS object by BLAKE3 hash, federated across gates
- `/cas/{hash}/provenance` — full provenance chain (DAG → spine → Merkle → braid)
- `/cas/{hash}/replicate` — replication instructions (which gates hold copies)
- `/compute/configs/` — memoized compute configurations (thermalized lattices, etc.)
- `/compute/configs/{hash}` — retrieve a cached compute config with its provenance

**Data Federation Pattern**: nestgate.io resolves CAS queries by consulting
nestGate instances on multiple gates via songBird mesh. A request for a hash
checks westGate (data NAS), strandGate (compute configs), ironGate (consumer
data), and any gate with a local CAS. The first gate holding the object serves
it. This is the same content-addressed pattern as git — the hash is the address,
the gate is an implementation detail.

**Compute Memoization for QCD**: strandGate's thermalized lattice configs
(38 MB at 16⁴, deterministic on `dims,β,seed,n_therm,integrator`) are CAS
objects with provenance braids. hotSpring can request a config via nestgate.io
and get it from whichever gate holds it — strandGate (origin), biomeGate
(cross-vendor validation), or any future compute gate. The 37-minute CPU
thermalization becomes a one-time cost stored forever.

**Replication**: Any researcher can hit `/cas/{hash}/replicate` to get:
1. The object itself (or a download link to the gate holding it)
2. The full provenance chain proving its lineage
3. Instructions to reproduce it independently (parameters, code commit, gate)

### Phase 4: Validation Endpoint

Public validation API:
- `/validate/cas/{hash}` — verify a CAS object exists and return its provenance
- `/validate/dataset/{name}` — verify all objects in a dataset, report completeness
- `/validate/replicate/{name}` — generate replication package (hashes + instructions)

This is what makes nestgate.io the "trust surface" — external researchers can
independently verify that the data they received matches the provenance chain.

### Phase 5: git Migration

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

## Data Federation Architecture

nestgate.io is not a single-gate service — it's a **federated CAS front door**
backed by nestGate instances running on every NUCLEUS gate:

```
                    nestgate.io (golgi / petalTongue)
                         │
              ┌──────────┼──────────────┐
              │          │              │
         westGate    strandGate     ironGate
         (data NAS)  (compute)     (consumer)
         519 GB       lattice       footPrint
         130 datasets configs       projects
         AlphaFold    QCD memos     GIS cache
```

### Federation Flow

1. **Request**: `GET nestgate.io/cas/{hash}`
2. **Resolve**: petalTongue queries local nestGate → not found →
   songBird `content.locate` mesh broadcast → westGate responds "I have it"
3. **Serve**: petalTongue proxies the response from westGate's nestGate
4. **Cache**: golgi optionally caches hot objects locally (L1 cache for public)

### What Lives Where

| Gate | CAS Contents | Federation Role |
|------|-------------|-----------------|
| **westGate** | 519 GB science data, AlphaFold, LINCS, PDB, SRA | Primary data origin |
| **strandGate** | Thermalized lattice configs, QCD production results | Compute memoization origin |
| **ironGate** | footPrint GIS projects, esotericWebb game state | Consumer data origin |
| **golgi** | Hot object cache, depot binaries | Public edge / L1 cache |
| **biomeGate** | Cross-vendor validation configs | Compute validation |

### Why This Matters

- **For hotSpring QCD**: thermalized configs computed on strandGate are available
  to any gate via nestgate.io. biomeGate can pull a config for cross-vendor
  parity checks. A future compute gate joins the mesh and immediately has access
  to all cached configs — no manual transfer.

- **For tideGlass NF**: GPS platform data on westGate is retrievable from any
  gate via nestgate.io. When tideGlass runs on ironGate (or any future gate),
  it fetches data by hash, not by knowing which gate has it.

- **For replication**: A reviewer hits `nestgate.io/cas/{hash}` with a hash
  from a paper. nestgate.io resolves it across the mesh and returns the object
  with its full provenance chain. The reviewer can independently verify that
  the data is what the paper claims.

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
