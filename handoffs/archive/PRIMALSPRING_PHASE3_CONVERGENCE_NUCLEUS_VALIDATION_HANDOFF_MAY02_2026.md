# BTSP Phase 3 Convergence + NUCLEUS Validation Handoff

**Date**: May 2–3, 2026
**From**: primalSpring v0.9.24 (Phase 57) — eastGate
**Scope**: Ecosystem-wide — all 13 NUCLEUS primals + downstream springs
**Phase**: INTERSTADIAL — BTSP Phase 3 COMPLETE

---

## 1. Phase 3 Convergence Certification

**BTSP Phase 3 is COMPLETE: 13/13 primals ship `btsp.negotiate` + ChaCha20-Poly1305 AEAD.**

Every NUCLEUS primal now implements:
- `btsp.negotiate` JSON-RPC method returning `cipher: "chacha20-poly1305"` + base64 server nonce
- HKDF-SHA256 key derivation: `SessionKeys` from `HKDF(ikm=handshake_key, salt="btsp-v1", info=client_nonce||server_nonce)`
- ChaCha20-Poly1305 AEAD on wire with `[4B length (big-endian u32)][12B nonce][ciphertext + tag]` framing
- `zeroize` on drop for all key material

### Final Three Convergence Commits (May 2, 2026)

| Primal | Commit | What Shipped |
|--------|--------|--------------|
| **loamSpine** | `3dcd6b7` | `btsp/phase3.rs` (382 LOC): `SessionKeys`, HKDF-SHA256, ChaCha20-Poly1305 encrypt/decrypt, zeroize. Pattern B (Tower-provided key from BearDog verify). Null cipher graceful fallback when no handshake key. Deps: `chacha20poly1305 0.10`, `hkdf 0.13`, `zeroize 1.8.2`. Ionic bond blocker **resolved**. |
| **coralReef** | `f2d6bcf` | `unix_jsonrpc.rs` updated: checks for `btsp.negotiate`, retrieves `SessionKeys`, switches to `process_encrypted_frames` loop. `dead_code` annotations removed from crypto. Wire-level AEAD active. |
| **NestGate** | `ef3ac568f` | `pub mod btsp_phase3;` declared in `rpc/mod.rs`. `hkdf` + `zeroize` deps added to workspace `Cargo.toml`. `try_phase3_negotiate` + `run_encrypted_frame_loop` wired into both `unix_socket_server/mod.rs` and `isomorphic_ipc/server/mod.rs` accept paths. |

### Full Phase 3 Roster

| # | Primal | Phase 3 | Key Acquisition | Notes |
|---|--------|---------|-----------------|-------|
| 1 | BearDog | FULL | Pattern A (self-derive from FAMILY_SEED) | Tower — crypto authority, key exporter |
| 2 | rhizoCrypt | FULL | Pattern A | Encrypted loop in `serve_after_handshake`, 16 tests |
| 3 | barraCuda | FULL | Pattern B (Tower-provided) | Transport-layer intercept, typed `NegotiateError` |
| 4 | petalTongue | FULL | Pattern B | Both framed + JSON-line paths |
| 5 | toadStool | FULL | Pattern B | JSON-line relay + encrypted framing |
| 6 | sweetGrass | FULL | Pattern B | Transport refactor, UDS+TCP encrypted frame loop |
| 7 | Songbird | FULL | Pattern A (BearDog key export) | Binary-framed + NDJSON paths, 28 tests |
| 8 | Squirrel | FULL | Pattern B | Handshake key from verify, HKDF compatible |
| 9 | skunkBat | FULL | Pattern B | Registry-stored key, E2E test |
| 10 | biomeOS | FULL | Pattern A | `handle_encrypted_stream`, 16MB frame guard |
| 11 | loamSpine | FULL | Pattern B | Ionic bond blocker resolved (was null-by-design) |
| 12 | coralReef | FULL | Pattern B | Crypto wired to transport (was dead code) |
| 13 | NestGate | FULL | Pattern B | Both accept paths wired (was module-pending) |

---

## 2. Live NUCLEUS Validation Results

**Platform**: eastGate (primary dev system)
**Binaries**: plasmidBin v2026.05.03 (remote fetch via `tools/fetch_primals.sh`)
**Stack**: 13/13 primals launched via `tools/nucleus_launcher.sh`

### guidestone Results

| Layer | Score | Notes |
|-------|-------|-------|
| Layer 0 (Bare) | 41/41 | Workspace integrity, CHECKSUMS |
| Layer 0.5 (Seed Provenance) | PASS | FAMILY_SEED derivation |
| Layer 1 (BTSP Auth) | 13/13 | All primals BTSP-authenticated |
| Layer 1.5 (biomeOS Substrate) | PASS | Neural API liveness, graph executor |
| Layer 3 (Bonding Model) | ALL PASS | Covalent, Metallic, Ionic, Weak, OrganoMetalSalt |
| Layer 7 (Cellular) | 69/70 | 9/10 cell graphs validated |
| **Total** | **157/170** | 20 skipped, 13 failures |

### Failure Categories

1. **Phase 3 client-server interop gap** (see Section 3): 8 failures
2. **Discovery routing via cleartext aliases**: 5 failures (shader, ai, dag, ledger, visualization)

---

## 3. Phase 3 Client-Server Interop Gap (CRITICAL)

**This is the single most important finding from NUCLEUS validation.**

### The Problem

primalSpring client correctly:
1. Calls `btsp.negotiate` → server responds `{ cipher: "chacha20-poly1305", server_nonce: "..." }`
2. Derives `SessionKeys` via HKDF-SHA256
3. Sends the next RPC as an encrypted frame: `[4B len][12B nonce][ciphertext+tag]`

But the server (BearDog confirmed, others likely same):
1. Returns the negotiate response with `cipher: "chacha20-poly1305"` ✓
2. **Does NOT switch its transport** to encrypted framing
3. Sends the next response as **plaintext JSON-RPC**

The client reads the plaintext `{"js` as a frame header → `0x7B226A73` = 2,065,853,043 bytes → `frame too large` error.

### The Fix (Per Primal)

Each server's post-negotiate accept loop must:
1. After sending the `btsp.negotiate` response, **immediately enter `run_encrypted_frame_loop`**
2. All subsequent reads must use `read_encrypted_frame` (not `read_line` or `BufReader`)
3. All subsequent writes must use `write_encrypted_frame`

The code exists in most primals (Phase 3 modules were shipped). The gap is in **wiring**: the accept path calls `negotiate_btsp` and returns the response, but doesn't switch the transport mode for subsequent messages on that connection.

### Verification Checklist (All Teams)

```
[ ] After btsp.negotiate response is sent, confirm the connection
    transitions to encrypted frame I/O (not cleartext JSON-RPC)
[ ] Send an encrypted frame from a test client after negotiate —
    verify the server decrypts it and responds with an encrypted frame
[ ] Confirm no plaintext JSON-RPC is sent on a post-negotiate connection
```

---

## 4. NestGate JWT Standalone Gate

**Issue**: NestGate requires `NESTGATE_JWT_SECRET` (≥32 bytes) on startup, even in `--socket-only` mode within a NUCLEUS stack where BearDog provides all authentication via BTSP.

**Context**: JWT is a standalone security mechanism for NestGate solo deployments. Within the eco, BearDog + BTSP is the auth layer. Even plaintext IPC is encrypted via the public seed.

**Recommended Fix**: When `--socket-only` is passed and BTSP handshake succeeds, skip the JWT secret requirement. This allows NestGate to participate in NUCLEUS compositions without configuring an unused auth mechanism.

**Workaround**: Set `NESTGATE_JWT_SECRET=$(openssl rand -base64 48)` in the launcher.

---

## 5. Discovery Routing Gaps

5 of 12 capabilities connect via cleartext capability aliases without full BTSP socket resolution:

| Capability | Current Resolution | Gap |
|-----------|-------------------|-----|
| `shader` | Alias to barraCuda socket | No BTSP handshake on alias path |
| `ai` | Alias to Squirrel socket | Same |
| `dag` | Alias to rhizoCrypt socket | Same |
| `ledger` | Alias to loamSpine socket | Same |
| `visualization` | Alias to petalTongue socket | Same |

**Fix**: guidestone (and downstream consumers) should resolve all capabilities through biomeOS `capability.discover` → BTSP-aware socket path, rather than direct capability-alias symlinks.

---

## 6. Per-Team Blurbs

### All 13 Primals

**Verify Phase 3 transport switch**: Your primal ships `btsp.negotiate` returning `chacha20-poly1305`. Confirm that after the negotiate response is sent, the connection **actually transitions** to encrypted frame I/O. Test: send an encrypted frame after negotiate and verify the server decrypts + responds encrypted. This is the last interop step before full E2E encrypted NUCLEUS.

### BearDog

Phase 3 interop gap confirmed against your Wave 79 binary. Your `negotiate_btsp` handler returns the correct cipher and nonce, but the accept loop does not enter `run_encrypted_frame_loop` after responding. Verify that the connection handler switches transport mode after the negotiate response is written. BearDog is the Tower — this fix cascading through BearDog is the reference pattern for all other primals.

### NestGate

Two items: (1) Skip JWT secret requirement when operating in BTSP/socket-only mode within a NUCLEUS stack — the JWT gate blocks startup for an auth mechanism the eco never uses. (2) Confirm Phase 3 wiring in **both** accept paths (`unix_socket_server/mod.rs` and `isomorphic_ipc/server/mod.rs`) — verify `try_phase3_negotiate` → `run_encrypted_frame_loop` transition is live, not just compiled.

### loamSpine

Your Phase 3 shipped cleanly (`3dcd6b7`). Confirm the new `phase3.rs` integrates with the latest plasmidBin binary (Pattern B key acquisition from BearDog verify). The ionic bond blocker is resolved — `CRYPTO_CONSUMPTION_HIERARCHY.md` now lists loamSpine as FULL AEAD. Verify post-negotiate encrypted frame loop is reachable from the accept path.

### coralReef

Phase 3 wiring shipped (`f2d6bcf`). Confirm `process_encrypted_frames` is reachable after `btsp.negotiate` succeeds in `unix_jsonrpc.rs`. The `dead_code` annotations have been removed — verify the crypto functions are now called in production paths. Also: GAP-04 (`tarpc` health endpoint) remains open — document if this is intentional or debt.

### Songbird

Phase 3 is solid (28 tests, binary-framed + NDJSON paths). Verify post-negotiate transport switch. GAP-06 (`discovery.register` naming) is cosmetic — close when convenient.

### Spring Teams (Downstream)

BTSP Phase 3 is complete upstream. You may now absorb encrypted compositions:

1. **Start with your proto-nucleate graph**: `graphs/downstream/{yourspring}_*_proto_nucleate.toml`
2. **Wire IPC via `CompositionContext`**: Use `CompositionContext::from_live_discovery_with_fallback()`
3. **Follow the maturity ladder**: L1 (IPC wired) → L2 (discovery) → L3 (graph-driven) → L4 (bonding-aware) → L5 (primal composition) → L6 (deploy graph validated)
4. **Reference doc**: `wateringHole/UPSTREAM_CROSSTALK_AND_DOWNSTREAM_ABSORPTION.md` Part 2

For encrypted IPC, the pattern is:
```
btsp_handshake() → btsp.negotiate → SessionKeys → encrypted frame loop
```
All bond types (Covalent, Metallic, Ionic, Weak, OrganoMetalSalt) now have full AEAD backing.

---

## 7. Development System Topology

| System | Role | Primary Projects | Responsibilities |
|--------|------|-------------------|------------------|
| **eastGate** | Primary dev | primalSpring, plasmidBin | BTSP convergence, CI/CD, assisting all remote teams with Phase 3 wiring, bonding models, composition patterns |
| **ironGate** | Sister dev (clean deploy) | ludoSpring, groundSpring | Clean deployment validation, primalSpring as consumer (not developer), independent spring evolution |

eastGate handles the most complex subprojects based on current bottlenecks. ironGate provides validation that compositions work from a clean deployment without the dev environment assumptions.

---

## 8. Composition Patterns for NUCLEUS Deployment

### Via biomeOS Neural API

```
graph.list       → enumerate available deploy graphs
graph.execute    → run a fragment-first composition
graph.status     → poll execution state
graph.save       → persist graph state
```

### Capability-Based Routing

All primal interactions route through capabilities, not identity:
```
capability.discover("storage")  → NestGate socket
capability.discover("crypto")   → BearDog socket
capability.discover("compute")  → barraCuda socket
```

### Fragment-First Composition

Deploy graphs use `resolve = true` fragments that compose into full deployments:
- **Root graphs** (13): one per primal
- **Cell graphs** (12): per-cell deployment units
- **Fragment graphs** (6): reusable composition fragments
- **Bonding graphs** (5): per-bond-type deploy patterns
- **Multi-node graphs** (5): cross-gate federation
- **Downstream graphs** (3): proto-nucleate templates for springs

### Bonding-Aware Deployment

| Bond Type | Cipher Floor | Use Case |
|-----------|-------------|----------|
| Covalent | Optional | Local tower composition |
| Metallic | Optional | GPU pool sharing |
| Ionic | **ChaCha20-Poly1305** | Cross-tower data federation |
| Weak | **ChaCha20-Poly1305** | Ephemeral session binding |
| OrganoMetalSalt | **ChaCha20-Poly1305** | Mixed topology (ionic + weak) |

---

## 9. Open Gaps

| ID | Description | Owner | Priority |
|----|-------------|-------|----------|
| **Interop Gap** | Phase 3 post-negotiate transport switch | All 13 primals | P1 |
| **NestGate JWT** | Skip JWT in BTSP/socket-only mode | NestGate | P2 |
| **Discovery** | 5 capability aliases need BTSP-aware resolution | guidestone / biomeOS | P2 |
| GAP-04 | coralReef `tarpc` health endpoint | coralReef | P3 |
| GAP-06 | Squirrel/Songbird `discovery.register` naming | Squirrel, Songbird | P4 |
| GAP-12 | petalTongue docs (capability wire surface) | petalTongue | P4 |

---

## 10. Reference Documents

| Document | Location | Purpose |
|----------|----------|---------|
| `CRYPTO_CONSUMPTION_HIERARCHY.md` | `primalSpring/wateringHole/` | Per-primal crypto posture, key patterns, escalation |
| `UPSTREAM_CROSSTALK_AND_DOWNSTREAM_ABSORPTION.md` | `primalSpring/wateringHole/` | Cross-talk rules + downstream maturity ladder |
| `CRYPTO_WIRE_CONTRACT.md` | `primalSpring/docs/` | BearDog crypto JSON-RPC surface spec |
| `PRIMAL_GAPS.md` | `primalSpring/docs/` | Gap registry with live validation findings |
| `NUCLEUS_IPC_METHOD_MAP.md` | `primalSpring/docs/` | Full IPC method map for all primals |
| `STADIAL_PARITY_GATE_APR16_2026.md` | `primalSpring/wateringHole/` | Ecosystem parity invariants |

---

*Generated by primalSpring Phase 57 — eastGate, May 3, 2026*
