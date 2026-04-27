# Songbird v0.2.1 Wave 173 — PG-51: Crypto Provider Socket Discovery Fix

**Date**: April 27, 2026
**From**: Songbird team
**For**: primalSpring, healthSpring, wetSpring, ecosystem
**Triggered by**: primalSpring PG-51 — "No Crypto provider" when BearDog at `security-{fid}.sock`

## Root Cause

Both `discover_security_socket` functions (in `songbird-crypto-provider` and
`songbird-http-client`) checked for:
- `security.sock` (plain, no family suffix)
- `crypto-{family_id}.sock` (family-scoped crypto domain)

But **never** tried:
- `security-{family_id}.sock` (family-scoped security — where BearDog actually binds in NUCLEUS)
- `beardog-{family_id}.sock` (legacy naming — where some deployments still bind)

## Fix

### Discovery chain (new priority order)

1. `$SECURITY_PROVIDER_SOCKET` env var
2. `$SECURITY_SOCKET` env var
3. `$CRYPTO_PROVIDER_SOCKET` env var
4. `$XDG_RUNTIME_DIR/biomeos/security.sock` (capability symlink)
5. **NEW**: `$XDG_RUNTIME_DIR/biomeos/security-{family_id}.sock` (family-scoped)
6. `$XDG_RUNTIME_DIR/biomeos/crypto-{family_id}.sock` (domain socket)
7. **NEW**: `$XDG_RUNTIME_DIR/biomeos/beardog-{family_id}.sock` (legacy on-disk)
8. `$BEARDOG_SOCKET` env var (legacy, deprecated)
9. `{temp}/biomeos/security.sock` (temp fallback)

### Files changed

- `crates/songbird-crypto-provider/src/socket_discovery.rs` — added family-scoped steps + helper fns
- `crates/songbird-http-client/src/crypto/socket_discovery.rs` — same fix + added missing `$SECURITY_SOCKET`
- `crates/songbird-orchestrator/src/crypto/discovery.rs` — `discover_crypto_socket_for_family()` now checks `security-{fid}.sock` before `crypto-{fid}.sock`
- `crates/songbird-orchestrator/src/bin_interface/server.rs` — security socket fallback now uses full `discover_security_socket()` instead of hardcoded temp path

## Other PG-51 items

- **CLI flag naming**: `--security-socket` is canonical, `--beardog-socket` is alias. Both work. No change needed (Wave 170).
- **Songbird own socket**: `songbird-{fid}.sock` path is set by launcher via `--socket` flag. Songbird binds to exactly what it's given.

## Verification

healthSpring/wetSpring can remove `beardog-{fid}.sock → security-{fid}.sock` symlink workaround.
After rebuilding Songbird, it will discover `security-{fid}.sock` directly.

```bash
cargo fmt --check          # clean
cargo clippy --workspace -- -D warnings  # 0 warnings
cargo test -p songbird-crypto-provider --lib   # 56 passed
cargo test -p songbird-http-client --lib       # 437 passed
cargo test -p songbird-orchestrator --lib      # 1,506 passed
```
