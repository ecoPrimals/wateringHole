# projectNUCLEUS: Workspace Scaffolding + Compute Usability + darkforest v0.2.0

**Date**: 2026-05-08
**From**: projectNUCLEUS (sporeGarden)
**For**: primalSpring, biomeOS, spring teams, primalSpring reviewers
**Phase**: 60 (enforced) — v0.9.25

---

## Context

Phase 60 is enforced. Horizon 1 (External Security & ABG Hosting) is complete.
ABG is live with 4 tiers: admin (`kmok`), compute (`tamison`), reviewer
(`abgreviewer`), observer (`abg-test`). JupyterHub at `lab.primals.eco` via
Cloudflare tunnel. 13/13 NUCLEUS primals deployed and healthy on ironGate.

This handoff covers three areas of work completed on 2026-05-08:

1. **Workspace scaffolding** — structured workspace for ABG collaboration
2. **Compute usability** — per-user Python environments and offline package install
3. **darkforest v0.2.0** — modular Rust security validator replacing legacy scripts

---

## 1. Workspace Scaffolding

### Shared workspace layout (`/home/irongate/shared/abg/`)

```
commons/        Group scratch — quick experiments, no structure required
pilot/          Structured experiments (hypothesis, decision criteria, timeline)
projects/       Formal project spaces (notebooks, data, results)
data/           Shared datasets (NCBI, reference genomes, calibration)
templates/      Starter notebooks, workload TOMLs, tier-appropriate welcome notebooks
showcase/       Polished work for external review + Voila dashboards
validation/     Surfaced darkforest JSON reports
wheelhouse/     Python package cache for offline pip install
```

### Pilot lifecycle

```
scratch (per-user ~/notebooks/scratch/)
  → commons (group scratch)
    → pilot (structured experiment: hypothesis, criteria, timeline)
      → projects (formal, versioned, cited)
        → showcase (polished, reviewer-visible)
          → public (sporePrint publication)
```

New subcommand: `abg_accounts.sh create-pilot <name> <owner>` creates a pilot
directory with a README template (hypothesis, decision criteria, timeline,
current state).

### Per-user landing zone

Every user gets on login:

- `~/notebooks/Welcome.ipynb` — symlinked to tier-appropriate welcome notebook
- `~/notebooks/scratch/` — private workspace (chmod 700, compute/admin only)
- `~/notebooks/shared/` — symlink to full `ABG_SHARED` tree (compute/admin)
  OR `~/notebooks/showcase/` — symlink to `ABG_SHARED/showcase/` only (reviewer)

### Reviewer showcase-only visibility

Reviewers see `~/notebooks/showcase/` instead of `~/notebooks/shared/`. This is
enforced at the symlink level in both `abg_accounts.sh setup_shared_dirs()` and
`jupyterhub_config.py ensure_shared_symlinks()`. Reviewers cannot navigate to
`commons/`, `pilot/`, `projects/`, or `data/` through the notebook interface.

### Validation dashboard

`showcase/validation-dashboard.ipynb` reads `validation/darkforest-latest.json`
and renders overall summary, results by suite, dark forest findings, and failed
checks. Served via Voila at `/services/voila/` — reviewers see security posture
without kernel access.

### Patterns learned

| Pattern | Implementation | Relevance |
|---------|---------------|-----------|
| Symlink-level RBAC | `ln -sf` to tier-appropriate targets | Filesystem-level access control without ACLs |
| `pre_spawn_hook` tier dispatch | JupyterHub hook reads `NUCLEUS_TIER` → configures PATH, symlinks, resources | Per-login environment customization |
| Voila compute contracts | Server-side notebook execution, no client kernel | Expose pipelines to non-compute users |
| NoKernelManager as kernel gate | `c.Spawner.kernel_manager_class` override | More reliable than `allowed_kernelspecs` filtering |
| Root-owned 550 filesystem | `chmod 550`, `chown root:root` | Immutable notebook directories |
| Group-sticky workspace | `chmod 2775`, `chown :abg-compute` | Shared write with automatic group inheritance |

---

## 2. Compute Usability

### Per-user Python venvs

Each compute/admin user gets `~/.venv/bioinfo/` created with
`--system-site-packages` (inherits shared bioinfo conda env). The venv's
`pip.conf` points to the local wheelhouse:

```ini
[global]
no-index = true
find-links = /home/irongate/shared/abg/wheelhouse
```

### Wheelhouse for offline pip

Admin utility `deploy/wheelhouse_sync.sh` provides `add`, `list`, `update`,
`remove` subcommands to manage `/home/irongate/shared/abg/wheelhouse/`. Uses
`pip download` to fetch wheels. Users run `%pip install <pkg>` in notebooks
with zero internet access — packages resolve from local wheelhouse.

### pre_spawn_hook PATH priority

The JupyterHub `pre_spawn_hook` prepends `~/.venv/bioinfo/bin` to PATH for
compute and admin users. User-installed packages take precedence over system
packages without breaking the shared environment.

### Onboarding

`Getting-Started.ipynb` in commons walks new users through: pre-installed
packages, `%pip install` usage, package requests, available kernels, and
workspace layout.

---

## 3. darkforest v0.2.0 — Modular Rust Security Validator

### Architecture

```
validation/darkforest/
├── Cargo.toml          (v0.2.0, serde + serde_json + clap)
└── src/
    ├── main.rs         CLI + runner
    ├── check.rs        Structured types (Status, Severity, Category, CheckResult, CheckBuilder)
    ├── net.rs          TCP/HTTP helpers (send_raw, send_jsonrpc, http_get, sudo_cmd)
    ├── pentest.rs      3 threat actors (external, compute, reviewer/observer)
    ├── fuzz.rs         Protocol fuzzing (13 primals + JupyterHub)
    ├── crypto.rs       13 crypto strength checks (CRY-01 → CRY-13)
    └── report.rs       Pipe format + JSON structured output
```

939KB static binary. Zero runtime dependencies.

### Check categories

| Suite | Count | What |
|-------|-------|------|
| Pen test | ~80 | 3 threat actors: external (unauthenticated), compute (authorized user), reviewer/observer (restricted) |
| Fuzz | ~70 | Malformed JSON-RPC, binary probes, oversized payloads, auth bypass, timing analysis for all 13 primals + JupyterHub |
| Crypto | 13 | Cookie entropy (CRY-01), age (CRY-02), permissions (CRY-03), shadow hash algo (CRY-04), rounds (CRY-05), ionic token tamper (CRY-06), expiry (CRY-07), BTSP cipher negotiation (CRY-08), MethodGate enforcement sweep (CRY-09), ionic scope rejection (CRY-10), file permission sweep (CRY-11), DNS restriction (CRY-12), supply chain (CRY-13) |

### Structured output

`--output <path>` writes JSON report:

```json
{
  "timestamp": "2026-05-08T...",
  "version": "0.2.0",
  "summary": {
    "total": 181,
    "pass": 175,
    "fail": 0,
    "dark_forest": 6,
    "known_gap": 0
  },
  "checks": [
    {
      "id": "CRY-01",
      "suite": "crypto",
      "category": "crypto_strength",
      "severity": "critical",
      "status": "PASS",
      "title": "Cookie secret entropy",
      "evidence": "...",
      "remediation": null,
      "elapsed_ms": 2,
      "timestamp": "..."
    }
  ]
}
```

### Current results

**175 PASS, 0 FAIL, 6 DARK_FOREST**

DARK_FOREST findings are accepted risks or informational items (version
disclosure, systemd enumeration, etc.) — not exploitable vulnerabilities.

### Legacy script archival

`deploy/darkforest_pentest.sh` and `deploy/darkforest_fuzz.py` moved to
`validation/archive/legacy/` as fossil record. The Rust binary is the
authoritative validator going forward.

---

## 4. Composition Patterns for Upstream

### NUCLEUS atomic composition (confirmed)

The Tower/Node/Nest atomic model is validated under real load:

- **Tower** (BearDog + Songbird): Trust boundary — all crypto, identity, BTSP
- **Node** (Tower + ToadStool + barraCuda + coralReef): Compute — workload dispatch
- **Nest** (Tower + NestGate + rhizoCrypt + loamSpine + sweetGrass): Storage — provenance

Full NUCLEUS = Tower + Node + Nest + Squirrel + biomeOS

### Deploy graph patterns validated

13 primals + enforced MethodGate + ionic tokens. All deployed via systemd user
services with `NUCLEUS_AUTH_MODE=enforced`. Deploy sequence:

1. BearDog (identity + crypto) — must be first
2. Songbird (discovery + networking)
3. Remaining primals in any order (all discover BearDog for auth)
4. biomeOS (orchestration — discovers all primals)

### Neural API dispatch

biomeOS `composition.reload` enables hot-swap of single primals without full
restart. Resource envelopes (`timeout_ms`, `cpu_cores`, `mem_mb`) enforced on
all dispatch paths via biomeOS v3.48 + ToadStool S232.

### Provenance pipeline (operational)

ToadStool dispatch → rhizoCrypt DAG → loamSpine ledger → sweetGrass braid.
BLAKE3 content addressing on all artifacts. SessionCommit with Merkle root.
Ed25519 attribution via sweetGrass W3C PROV witness.

---

## 5. Upstream Primal Evolution Targets

### For primalSpring

- **Deploy graph validation**: 13 primals + MethodGate enforced confirms the
  composition model works in production. NUCLEUS atomic composition proven.
- **Neural API**: `composition.reload` is essential for ABG operations (swap
  primal without downtime). Recommend promoting to stable API.
- **Resource envelopes**: biomeOS + ToadStool enforcement validated. Consider
  standardizing envelope schema in wateringHole.

### For biomeOS

- **JH-11 Cross-primal token federation**: BearDog-issued ionic tokens are not
  verifiable by other primals. Each MethodGate validates independently. The
  intended path is `_resource_envelope` forwarding in biomeOS compositions.
  This is the key remaining gap for multi-primal authenticated workflows.

### For ToadStool

- **DF-2**: `TOADSTOOL_AUTH_MODE=enforced` env var is read but `auth.mode`
  reports `permissive`. Env var name mapping or implementation gap.

### For petalTongue

- **PT-1 → PT-5**: Voila compute contracts are the calibration instrument for
  petalTongue sovereignty replacement. Key capabilities needed:
  - Catch-all route for static file serving
  - NestGate backend integration
  - Config schema for web mode
  - Markdown rendering
  - Dashboard embedding

### For NestGate

- **NG-1 → NG-4**: Content pipeline for sporePrint self-hosting:
  - `content.put` method
  - Collection/directory concept
  - Unified blob/KV namespace
  - Content-type metadata

### For spring teams

- **Workspace pattern**: The pilot lifecycle (commons → pilot → projects →
  showcase) is a pattern that applies to any multi-user primal deployment.
  Consider absorbing into wateringHole as a standard.
- **Wheelhouse pattern**: Offline package management via local cache is
  reusable for any deployment where internet access is restricted.
- **darkforest pattern**: Modular Rust security validation with structured
  JSON output is reusable for any primal deployment. Check definitions in
  `check.rs` follow OCSF-inspired schema.

---

## 6. File Manifest

### projectNUCLEUS (changed/new)

| File | Change |
|------|--------|
| `README.md` | Updated counts, workspace, usability |
| `PHASES.md` | Updated dependency count, added workspace/usability/darkforest entries |
| `specs/EVOLUTION_GAPS.md` | Updated darkforest counts to 175/0/6 |
| `specs/SHARED_WORKSPACE.md` | Rewritten with pilot/, validation/, per-user landing, lifecycle |
| `deploy/abg_accounts.sh` | Added setup_user_venv, create-pilot, tier-aware symlinks, scratch |
| `deploy/wheelhouse_sync.sh` | New — admin utility for wheelhouse management |
| `validation/darkforest/` | v0.2.0 — 7 modules, 181 checks |
| `validation/archive/legacy/` | Archived `darkforest_pentest.sh`, `darkforest_fuzz.py` |

### Shared workspace (new)

| File | Purpose |
|------|---------|
| `shared/abg/pilot/README.md` | Pilot directory documentation |
| `shared/abg/data/README.md` | Data directory documentation |
| `shared/abg/projects/README.md` | Projects directory documentation |
| `shared/abg/validation/README.md` | Validation results documentation |
| `shared/abg/validation/darkforest-latest.json` | Latest security scan results |
| `shared/abg/templates/welcome-{admin,compute,reviewer,observer}.ipynb` | Tier-specific welcome notebooks |
| `shared/abg/showcase/Welcome.ipynb` | Showcase landing page |
| `shared/abg/showcase/validation-dashboard.ipynb` | Voila dashboard for darkforest results |
| `shared/abg/commons/Getting-Started.ipynb` | Compute user onboarding |

---

## 7. Existing Upstream Gaps (unchanged)

These remain tracked in `PROJECTNUCLEUS_UPSTREAM_GAPS_CONSOLIDATED_MAY08_2026.md`:

| ID | What | Owner |
|----|------|-------|
| DF-2 | ToadStool `TOADSTOOL_AUTH_MODE` env var mapping | toadStool |
| DF-3 | songbird/squirrel silent on `auth.mode` TCP | Each team |
| U1 | primalSpring `CHECKSUMS` stale | primalSpring |
| U2 | 5 deploy graphs missing `by_capability` | primalSpring |
| U3 | 8 profile graphs missing `bonding_policy` | primalSpring |
| U5 | sweetGrass port 39085 vs 9850 | sweetGrass |
| JH-11 | Cross-primal token federation | biomeOS/primalSpring |
