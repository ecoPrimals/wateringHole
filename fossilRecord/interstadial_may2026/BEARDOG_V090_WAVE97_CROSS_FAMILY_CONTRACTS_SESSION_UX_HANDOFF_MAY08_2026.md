<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 Wave 97 — Cross-Family Contract Signing & Session Token UX

**Date**: May 8, 2026
**Primal**: BearDog (Security / Crypto)
**Commit**: (pending)
**Audit Reference**: primalSpring Phase 60 update (May 8)

---

## Context

primalSpring Phase 60 audit confirmed JH-0 (13/13 adopted) and JH-1 (ionic tokens) as RESOLVED (Wave 93+94). Two items remained:

1. **JH-4 (Medium)**: Token issuance UX for non-technical researchers
2. **Ionic bond cross-family contract signing (Open)**: Multi-party contract signing not exposed as IPC

Both are now resolved.

---

## Delivered

### 1. Cross-Family Contract Lifecycle (3 new IPC methods)

| Method | Description |
|--------|-------------|
| `crypto.contract.propose` | Proposer signs terms, receives `contract_id` for counterparty |
| `crypto.contract.countersign` | Counterparty signs same terms; both signatures verified; contract sealed |
| `crypto.contract.verify` | Verify both signatures on a sealed contract |

**Architecture**: Pending contracts stored in `IonicBondHandler` with TTL expiry. Uses same Ed25519 primal identity as ionic bonds and `crypto.sign_contract`. Countersigner provides their own signature and public key; BearDog verifies before sealing.

**Types added** (`beardog-types::ionic_bond`):
- `ContractProposeParams`, `ContractProposeResponse`
- `ContractCountersignParams`, `ContractCountersignResponse`
- `CrossFamilyContract`, `ContractVerifyParams`, `ContractVerifyResponse`

**Unblocks**:
- hotSpring GAP-HS-005 (cross-family GPU lease)
- healthSpring dual-tower ionic
- wetSpring provenance cross-spring

### 2. `auth.issue_session` (JH-4)

Simplified token issuance for non-technical researchers. Accepts `purpose` + optional `user` instead of explicit scope patterns:

| Purpose | Scope | Default TTL |
|---------|-------|-------------|
| `jupyterhub` / `notebook` | `crypto.*`, `health.*`, `capabilities.*`, `identity.*`, `auth.verify_ionic` | 8h |
| `desktop` | Above + `secrets.*` | 24h |
| `admin` | `*` | 1h |
| `research` (default) | `crypto.*`, `health.*`, `capabilities.*`, `identity.*` | 8h |

Response includes `usage` hint: "Set BEARDOG_TOKEN=\<token\> or pass as Bearer header."

Gate-handled as public method (no auth required to obtain a token).

### 3. Pre-existing Doc Fixes (bonus)

Fixed 7 broken rustdoc links across `beardog-config` and `beardog-tunnel` that caused `RUSTDOCFLAGS="-D warnings" cargo doc` to fail.

---

## Quality Gates

| Gate | Status |
|------|--------|
| `cargo fmt --check` | Clean |
| `cargo clippy --workspace -- -D warnings` | 0 errors |
| `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` | Clean |
| `cargo test --workspace` | **14,883+ passed, 0 failed** |

---

## Metrics Snapshot

| Metric | Value |
|--------|-------|
| Tests | 14,883+ |
| Crates | 29 |
| JSON-RPC Methods | 384 |
| New tests this wave | 17 (7 cross-family contract, 7 session token, 3 method gate) |
| Coverage | 90.51% |

---

## Remaining Known Debt

| Item | Status | Owner |
|------|--------|-------|
| JH-2: Token-carried resource envelope | OPEN — High | biomeOS + ToadStool |
| JH-3: Composition hot-reload | OPEN — Medium | biomeOS team |
| BTSP Phase 3: HSM signing path | OPEN | BearDog (non-blocking) |
| Cross-family contract persistence | Architectural: in-memory. Persistence via NestGate `storage.store` when available | NestGate |

---

## Files Modified

- `crates/beardog-types/src/ionic_bond.rs` — 7 new types
- `crates/beardog-tunnel/src/unix_socket_ipc/handlers/ionic_bond/contract.rs` — cross-family lifecycle
- `crates/beardog-tunnel/src/unix_socket_ipc/handlers/ionic_bond/mod.rs` — 3 new methods registered
- `crates/beardog-tunnel/src/unix_socket_ipc/handlers/ionic_bond/tests.rs` — 7 new tests
- `crates/beardog-tunnel/src/ionic_token_handlers.rs` — `handle_auth_issue_session` + 7 tests
- `crates/beardog-tunnel/src/method_gate.rs` — `auth.issue_session` in gate + public list
- `crates/beardog-tunnel/src/method_gate_tests.rs` — 3 new tests
- `crates/beardog-tunnel/src/unix_socket_ipc/handlers/capabilities.rs` — capability manifest updates
- 5 doc-fix files in `beardog-config` and `beardog-tunnel`
