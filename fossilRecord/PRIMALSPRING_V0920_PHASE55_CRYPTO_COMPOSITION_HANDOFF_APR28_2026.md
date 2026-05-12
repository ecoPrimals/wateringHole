# primalSpring v0.9.20 — Phase 55 Handoff

**Date**: April 28, 2026  
**From**: primalSpring  
**For**: All upstream primal teams + downstream spring teams  
**Commits**: See primalSpring `main` branch

---

## What Changed

### Two-Tier Crypto Architecture (new)

Published seed fingerprints (BLAKE3 of primal binaries) are now used as key derivation material. The NUCLEUS has a deterministic key hierarchy:

- **Tier 0** (public DNA): `base_key = HMAC-SHA256(published_fingerprint, "primal-nucleus-v1:" + primal_name)` — anyone with the published fingerprints derives the same key. Base encryption is a "translation" not secrecy.
- **Tier 1** (family): `family_key = HMAC-SHA256(base_key + FAMILY_SEED, "family-v1:" + FAMILY_ID + ":" + primal_name)` — unique per deployment. The "nuclear envelope."
- Per-atomic **purpose keys** derived from family key: storage, dag, ledger, provenance, compute, tensor, shader, inference, visualization, coordination, security, discovery.

All derivation goes through BearDog `crypto.hmac_sha256`. Keys stored in BearDog `secrets.store`. See `wateringHole/NUCLEUS_TWO_TIER_CRYPTO_MODEL.md` for full docs.

### JWT Deprecated Within NUCLEUS

NestGate's `NESTGATE_JWT_SECRET` is a standalone feature for isolated deployments. Within NUCLEUS compositions, `NESTGATE_AUTH_MODE=beardog` signals BearDog handles all auth. JWT is centralized and deprecated in the ecosystem.

### Full Tower Wiring (all 12 primals)

Every primal now receives at startup:
- `BEARDOG_SOCKET` — crypto delegation endpoint
- `BTSP_PROVIDER_SOCKET` — BTSP tunnel provider
- `FAMILY_SEED` — Tier 1 key derivation input
- `DISCOVERY_SOCKET` — Songbird capability resolution
- `BIOMEOS_SOCKET_DIR` — socket directory

**ToadStool was missing all of these.** Fixed in `composition_nucleus.sh`.

### Composition-Level Encrypt-at-Rest

Until NestGate evolves native encryption, the composition library provides:
- `tower_encrypt(key, plaintext)` / `tower_decrypt(key, ct, nonce)`
- `encrypted_store(key_name, value)` / `encrypted_retrieve(key_name)`
- `storage_init_encryption()` — loads purpose key from BearDog secrets

Envelope format: `{"v":1,"ct":"<b64>","n":"<b64>","alg":"chacha20-poly1305"}`

### New Tools

- `tools/nucleus_crypto_bootstrap.sh` — post-startup script that derives all purpose keys, stores them, tests round-trips
- `desktop_nucleus.sh validate` now checks crypto tiers (fingerprints, HMAC derivation, BTSP session, sign/verify, secrets store/retrieve)

---

## Per-Primal Evolution Needed

### BearDog (Tower)
- **Working**: key derivation (HMAC chain), Ed25519 sign/verify, ChaCha20-Poly1305, BTSP sessions, secrets store
- **Gap**: `genetic.derive_lineage_key` requires `peer_family_id` — no self-derivation for single-family NUCLEUS
- **Request**: Add `crypto.derive_purpose_key(family_key, purpose)` as first-class method

### Songbird (Tower)
- **Working**: service mesh, ipc.register/resolve, HTTP bridge, BTSP wiring
- **Gap**: service registrations not cryptographically signed
- **Request**: Sign `ipc.register` payloads so consumers verify authentic registrations

### NestGate (Nest)
- **Working**: storage.store/retrieve/list/delete, streaming, blobs
- **Gap**: stores plaintext, JWT is standalone-only
- **Request**:
  1. Respect `NESTGATE_AUTH_MODE=beardog` — bypass JWT, delegate auth to BearDog
  2. Resolve `crypto` capability → BearDog socket at startup
  3. Retrieve storage purpose key via `secrets.retrieve`
  4. Auto-encrypt on store, auto-decrypt on retrieve
  5. Accept `NESTGATE_ENCRYPTION_KEY` env var as bootstrap override

### rhizoCrypt (Nest)
- **Working**: DAG sessions, event append, merkle roots, slices, frontier
- **RESOLVED (S52)**: Vertex signing delegated to crypto provider — `sign_vertex_if_available` calls `crypto.sign_ed25519` via capability-discovered signing provider. BLAKE3 content hashing remains local (content addressing). Graceful degradation when no provider is present. 5 new tests, 1,546 total (all-features).
- **Remaining**: Vertex signature verification on retrieval (read-path optional check)

### loamSpine (Nest)
- **Working**: spine create, entry append, seal
- **Gap**: declares BTSP consumed but no active channels; entries not signed
- **Request**: Sign each `entry.append` via `crypto.sign`, store signature in entry metadata

### sweetGrass (Nest)
- **Working**: braid create/query, provenance graphs
- **Gap**: local hashing for braid provenance, not cryptographically signed
- **Request**: Delegate signing to BearDog `crypto.sign` for verifiable provenance

### ToadStool (Node)
- **Fixed**: now has BEARDOG_SOCKET, BTSP_PROVIDER_SOCKET, FAMILY_SEED, DISCOVERY_SOCKET
- **Gap**: compute jobs dispatched in plaintext
- **Request**: Encrypt job payloads using `compute` purpose key

### barraCuda (Node)
- **Working**: tensor ops, BEARDOG_SOCKET wired
- **Gap**: tensor data transmitted in plaintext
- **Request**: Optional encryption for sensitive tensor data

### coralReef (Node)
- **Working**: shader compilation, BTSP wired
- **Gap**: shader artifacts not signed
- **Request**: Sign compiled shaders for integrity verification

### Squirrel (Meta)
- **Working**: AI inference, BEARDOG_SOCKET wired, Ollama bridge
- **Gap**: inference context (prompts, responses) not encrypted in transit
- **Request**: Encrypt inference payloads using `inference` purpose key

### petalTongue (Meta)
- **Working**: live desktop GUI, scene rendering, sensor streams, proprioception
- **Gap**: scene graphs not integrity-verified
- **Request**: Sign scene pushes for verifiable UI updates

### biomeOS (Coordinator)
- **Working**: cellular deployment, graph bootstrap, Neural API
- **Gap**: deployment graphs not signed
- **Request**: Sign cell graphs before deployment, verify on load

---

## For Downstream Springs

### What This Means for You

The full NUCLEUS stack now has:
1. **Deterministic crypto from published seeds** — deploy from plasmidBin and get base encryption automatically
2. **Family isolation** — different `FAMILY_SEED` = different encryption namespace
3. **Composition-level encrypted storage** — use `encrypted_store`/`encrypted_retrieve` from the composition library
4. **Full Tower wiring** — all 12 primals can reach BearDog for crypto delegation
5. **JWT-free NUCLEUS** — `NESTGATE_AUTH_MODE=beardog` in all composition scripts

### Your Next Step

1. Pull primalSpring and `infra/wateringHole`
2. Review `wateringHole/NUCLEUS_TWO_TIER_CRYPTO_MODEL.md` for the full architecture
3. In your compositions: source `nucleus_composition_lib.sh` and call `storage_init_encryption()` after startup to enable encrypted storage
4. Run `tools/nucleus_crypto_bootstrap.sh` after NUCLEUS startup to derive purpose keys
5. Run `tools/desktop_nucleus.sh validate` to verify crypto tiers

### Key References

| Document | Location |
|----------|----------|
| Two-tier crypto model | `wateringHole/NUCLEUS_TWO_TIER_CRYPTO_MODEL.md` |
| Composition library | `primalSpring/tools/nucleus_composition_lib.sh` |
| Crypto bootstrap | `primalSpring/tools/nucleus_crypto_bootstrap.sh` |
| Desktop NUCLEUS deployment | `wateringHole/DESKTOP_NUCLEUS_DEPLOYMENT.md` |
| IPC method map | `primalSpring/docs/NUCLEUS_IPC_METHOD_MAP.md` |
| Composition patterns | `wateringHole/SPRING_COMPOSITION_PATTERNS.md` |
| Seed fingerprints | `primalSpring/validation/seed_fingerprints.toml` |

---

## Version Summary

| Metric | Value |
|--------|-------|
| Version | 0.9.20 |
| Phase | 55 |
| Tests | 631 (585 passed + 46 ignored) |
| Experiments | 76 (17 tracks) |
| Deploy Graphs | 69 TOMLs (12 cell graphs) |
| guideStone | Level 4 — 187/187 live, 13/13 BTSP |
| Crypto | Two-tier (public DNA + family seed) |
| Desktop | Live petalTongue GUI with branching DAG state |
