<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# BearDog v0.9.0 — Wave 100: TLS Termination & Rate Limiting (H2-10/H2-11)

**Date**: May 10, 2026
**Primal**: bearDog v0.9.0
**Audit Source**: primalSpring coordination — May 9, 2026 — interstadial + sovereignty goals
**Registry**: 123 methods
**Tests**: 14,905+ passing, 0 failures
**Quality Gates**: `cargo fmt`, `cargo clippy -D warnings`, `RUSTDOCFLAGS="-D warnings" cargo doc`, `cargo test --workspace` — all clean

---

## Resolved Audit Items

### H2-10: X.509/TLS Termination

**Audit**: "projectNUCLEUS needs X.509/ACME TLS listener (Let's Encrypt client, SNI routing, cert auto-renewal) + connection/request rate limiting to replace Cloudflare TLS/DDoS. Blocked until this ships."

**Resolution**: Native TLS termination shipped behind `tls-server` feature flag (default-enabled).

**Architecture**:
- `rustls 0.23` (ring crypto backend) + `tokio-rustls 0.26` for async TLS acceptance
- Certificate chain and private key loaded from PEM files
- SNI hostname validation via `rustls` built-in support
- TLS connections transparently upgraded in the TCP accept loop
- Decrypted traffic shares the same `handle_plaintext_connection` codepath as cleartext

**Configuration**:
```bash
# Enable TLS termination
export BEARDOG_TLS_CERT_PATH=/etc/letsencrypt/live/example.com/fullchain.pem
export BEARDOG_TLS_KEY_PATH=/etc/letsencrypt/live/example.com/privkey.pem
beardog server --listen 0.0.0.0:443
```

**Supported key formats**: PKCS8, PKCS1 (RSA), SEC1 (ECDSA)

**ACME/Let's Encrypt**: Certificate files are loaded from disk. External cert management (certbot, acme.sh) can renew certs; a server restart picks up new certs. In-process ACME client is deferred to a future wave.

### H2-11: Connection/Request Rate Limiting

**Resolution**: Per-IP sliding-window rate limiter wired into the TCP accept loop.

**Architecture**:
- `DashMap<IpAddr, Vec<Instant>>` for lock-free concurrent tracking
- Connections rejected before TLS handshake or JSON-RPC parsing
- Loopback IPs (127.0.0.1, ::1) always allowed
- Stale IP buckets auto-pruned every 5 minutes

**Configuration**:
```bash
export BEARDOG_RATE_LIMIT_MAX_CONN=100     # per IP per window (default 100)
export BEARDOG_RATE_LIMIT_WINDOW_SECS=60   # sliding window (default 60s)
export BEARDOG_RATE_LIMIT_MAX_TOTAL=1000   # total concurrent connections (default 1000)
```

### JH-11: Cross-Primal Token Federation — CONFIRMED RESOLVED

Wave 99's `auth.public_key` endpoint is the key distribution API requested by the audit. Any primal can call `auth.public_key` once at startup, cache the Ed25519 verifying key, and verify ionic tokens locally. No further BearDog work needed for the "key distribution" item. Downstream primals should wire the `BearDogVerifier`/`TokenVerifier` pattern to consume it.

---

## Sovereignty Roadmap Impact

| Step | Item | Status |
|------|------|--------|
| 3b | BearDog TLS | **SHIPPED** (H2-10, Wave 100) |
| 3b | Rate limiting | **SHIPPED** (H2-11, Wave 100) |
| 3b | ACME auto-renewal | Deferred — use external cert management for now |
| 3c | Songbird NAT | Not BearDog scope |
| 2b | BTSP auth federation | Unblocked by JH-11 (Wave 99) |

---

## Remaining BearDog Debt

| ID | Item | Status | Notes |
|----|------|--------|-------|
| ACME | In-process ACME client | Deferred | Use certbot/acme.sh externally |
| BD-IONIC-PERSIST | Ionic bond durable persistence | Open | In-memory only; needs NestGate/ledger |
| HSM-P3 | HSM signing path | Open (low) | Mocks correctly `#[cfg(test)]`-gated |

---

## Files Modified

- `Cargo.toml` — `rustls`, `tokio-rustls`, `rustls-pemfile` added as workspace deps
- `crates/beardog-tunnel/Cargo.toml` — `tls-server` feature, `dashmap` dep
- `crates/beardog-tunnel/src/tcp_ipc/mod.rs` — new module exports
- `crates/beardog-tunnel/src/tcp_ipc/server.rs` — TLS + rate limit integration, `handle_plaintext_connection` refactor
- `crates/beardog-tunnel/src/tcp_ipc/tls.rs` — **NEW**: TLS acceptor module
- `crates/beardog-tunnel/src/tcp_ipc/rate_limiter.rs` — **NEW**: rate limiter module
- `STATUS.md`, `CHANGELOG.md` — updated metrics and wave entry
