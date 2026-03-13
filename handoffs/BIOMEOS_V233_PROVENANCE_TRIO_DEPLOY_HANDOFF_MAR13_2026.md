# biomeOS V2.33 — Provenance Trio Graph Deployments

**Date**: March 13, 2026
**From**: biomeOS v2.33
**To**: loamSpine, rhizoCrypt, sweetGrass, all springs
**Tests**: 4,033 passing (0 failures, 165 ignored)
**Clippy**: 0 warnings | **Format**: PASS | **C deps**: 0

---

## Summary

Integrated the RootPulse provenance trio (loamSpine + rhizoCrypt + sweetGrass) as
fully deployable primals with biomeOS Neural API capability routing.

---

## Deployment Graphs Created

| Graph | Primal | Ports | Capabilities |
|-------|--------|-------|-------------|
| `loamspine_deploy.toml` | LoamSpine | tarpc 9001, JSON-RPC 8301 | permanence, spine, certificate, proof, commit |
| `rhizocrypt_deploy.toml` | rhizoCrypt | tarpc 9400 | dag, session, merkle, dehydration, slice |
| `sweetgrass_deploy.toml` | sweetGrass | HTTP 8302, tarpc 8091 | attribution, braid, provenance, contribution |
| `provenance_trio_deploy.toml` | All three | All above | Combined deployment in dependency order |

### Dependency Order

```
Tower (BearDog + Songbird) → LoamSpine → rhizoCrypt + sweetGrass
```

LoamSpine starts first as the permanence layer. rhizoCrypt and sweetGrass start
after LoamSpine is healthy, as they dehydrate/anchor to it.

---

## Capability Translations (35+)

Registered in `config/capability_registry.toml`:

### Ephemeral Workspace (rhizoCrypt → 13 translations)
`dag.create_session`, `dag.append_event`, `dag.get_vertex`, `dag.get_frontier`,
`dag.query_vertices`, `dag.dehydrate`, `dag.get_merkle_root`, `dag.get_merkle_proof`,
`dag.verify_proof`, `dag.checkout_slice`, `dag.get_slice`, `dag.health`, `dag.metrics`

### Permanent Storage (LoamSpine → 18 translations)
`commit.session`, `commit.braid`, `spine.create`, `spine.get`, `spine.seal`,
`entry.append`, `entry.get`, `entry.get_tip`, `certificate.mint`, `certificate.transfer`,
`certificate.loan`, `certificate.return`, `proof.generate_inclusion`, `proof.verify_inclusion`,
`permanent-storage.commitSession`, `permanent-storage.verifyCommit`,
`permanent-storage.getCommit`, `permanent-storage.healthCheck`

### Attribution (sweetGrass → 11 translations)
`provenance.create_braid`, `provenance.get_braid`, `provenance.query_braids`,
`provenance.graph`, `provenance.attribution_chain`, `provenance.calculate_rewards`,
`provenance.record_contribution`, `provenance.record_session`, `provenance.export_provo`,
`provenance.compress_session`, `provenance.health`

---

## Workflow Graphs (Pre-existing, Now Executable)

| Graph | Purpose |
|-------|---------|
| `provenance_pipeline.toml` | Universal provenance for any Spring experiment |
| `rootpulse_commit.toml` | RootPulse commit: dehydrate → sign → store → commit → attribute |

These workflows assume the trio is deployed (via `provenance_trio_deploy.toml`).

---

## For Spring Teams

Any Spring can use the provenance pipeline by:
1. Deploy trio: `graph.execute provenance_trio_deploy`
2. Create experiment session in rhizoCrypt
3. Execute: `graph.execute provenance_pipeline` with `SESSION_ID` and `EXPERIMENT_ID`

The pipeline handles dehydration, signing, storage, and attribution automatically.

---

## For loamSpine Team

biomeOS deploys LoamSpine via `loamspine server` with env vars:
- `LOAMSPINE_TARPC_PORT=9001`
- `LOAMSPINE_JSONRPC_PORT=8301`
- `DISCOVERY_ENDPOINT=http://127.0.0.1:8080` (Songbird)
- `LOAMSPINE_STORAGE_PATH=${XDG_DATA_HOME}/biomeos/loamspine`

Health check via JSON-RPC `health.check` on port 8301.

## For rhizoCrypt Team

biomeOS deploys rhizoCrypt via `rhizocrypt server` with env vars:
- `RHIZOCRYPT_RPC_PORT=9400`
- `RHIZOCRYPT_DISCOVERY_ADAPTER=http://127.0.0.1:8080` (Songbird)
- `PERMANENT_STORAGE_ENDPOINT=http://127.0.0.1:8301` (LoamSpine)

Health check via tarpc `health` on port 9400.

## For sweetGrass Team

biomeOS deploys sweetGrass via `sweet-grass-service server` with:
- `--http-address 0.0.0.0:8302`
- `--tarpc-address 0.0.0.0:8091`
- `--storage sled --sled-path ${XDG_DATA_HOME}/biomeos/sweetgrass`
- `DISCOVERY_ADDRESS=127.0.0.1:8080` (Songbird)

Health check via HTTP `GET /health` on port 8302.
