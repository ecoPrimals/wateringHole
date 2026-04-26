# Songbird v0.2.1 Wave 170 — CLI Flag Alignment Confirmation

**Date**: April 26, 2026
**From**: Songbird team
**For**: primalSpring, ludoSpring, all launcher maintainers
**Triggered by**: primalSpring Live Composition Validation (April 26, 2026)

## Summary

primalSpring asked to confirm Songbird's canonical CLI flag for the
BearDog/security provider socket path. Confirmation:

**Canonical**: `--security-socket`
**Alias**: `--beardog-socket` (supported, works identically)

Both resolve to the same `security_socket` field. The alias exists for
backward compatibility with older launcher scripts and `primal_launch_profiles.toml`.

### Code Reference

```rust
// crates/songbird-orchestrator/src/bin_interface/mod.rs line 93
#[arg(long = "security-socket", alias = "beardog-socket")]
pub security_socket: Option<String>,
```

### Environment Variable Fallback (when neither flag is passed)

1. `$SECURITY_PROVIDER_SOCKET`
2. `$XDG_RUNTIME_DIR/biomeos/security-{family_id}.sock` (capability symlink)
3. `$BEARDOG_SOCKET` (legacy)

### What This Means for Launchers

- `nucleus_launcher.sh` already passes `--security-socket` — correct
- `primal_launch_profiles.toml` uses `--beardog-socket` — works (alias), no breakage
- Either flag is safe to use; `--security-socket` is preferred for new scripts

### Correction

The ludoSpring V53 handoff (line 271) incorrectly stated "Songbird expects
`--beardog-socket` (not `--security-socket`)". This has been corrected in-place.
Songbird accepts both; `--security-socket` is canonical.

## No Code Changes

No Songbird code changes were needed. The CLI definition already supports both
flag names. This wave is documentation/alignment only.

## Verification

```bash
# Both of these are equivalent:
songbird server --security-socket /path/to/beardog.sock
songbird server --beardog-socket /path/to/beardog.sock
```
