# projectNUCLEUS: Deep Debt Evolution Sweep Handoff

**Date**: 2026-05-09
**From**: projectNUCLEUS (sporeGarden)
**For**: primalSpring, all primal teams, spring teams
**Supersedes**: Tier 3 code quality table in `PROJECTNUCLEUS_UPSTREAM_GAPS_CONSOLIDATED_MAY08_2026.md`

---

## Summary

projectNUCLEUS completed a comprehensive debt sweep across all Rust, Python,
and Bash tooling. The gate infrastructure is now gate-agnostic (portable to any
hardware identity), error-propagating (zero `expect()`/`unwrap()` in hot paths),
and centrally configured (single source of truth for all paths, ports, and
credentials).

This handoff documents what was done, what primal teams should absorb, and
what upstream gaps remain post-sweep.

---

## 1. What Changed

### Rust: tunnelKeeper

| Change | Before | After |
|--------|--------|-------|
| `Client::new()` | `expect()` on header + client build | Returns `Result<Self, ApiError>` with `InvalidHeader` variant |
| tokio features | `features = ["full"]` | `features = ["rt-multi-thread", "macros"]` |
| RNG | `rand = "0.8"` | `rand_core = "0.6"` |
| Credential paths | `const CLOUDFLARED_DIR = "/home/irongate/.cloudflared"` | `cloudflared_dir()` reads `CLOUDFLARED_DIR` / `HOME` env vars |
| Config default | `--config /home/irongate/.cloudflared/config.yml` | `--config` reads `CLOUDFLARED_CONFIG` env, defaults `~/.cloudflared/config.yml` |

### Rust: darkforest

| Change | Before | After |
|--------|--------|-------|
| Primal roster | `static PRIMALS: &[Primal]` constant | `load_primals()` reads env vars, compiled fallback array |
| Hub port | `const HUB_PORT: u16 = 8000` | `hub_port()` reads `JUPYTERHUB_PORT` env, defaults 8000 |
| Crypto paths | Hardcoded `/home/irongate/...` in `crypto.rs` | `CryptoConfig` struct with `gate_home()`, `cookie_secret_path()`, `sqlite_path()`, `cf_dir()` |
| Primal count | 13 primals | 14 primals (added `rhizocrypt-rpc:9602`) |
| Fuzz target | `addr.parse().unwrap()` | `let Ok(sock_addr) = addr.parse() else { break }` |

### Bash: deploy scripts

`deploy/nucleus_config.sh` is the single source of truth. All 7 deploy scripts
source it and use environment variables:

| Variable | Replaces |
|----------|----------|
| `$GATE_HOME` | `/home/irongate` |
| `$SPOREPRINT_REPO` | `/home/irongate/Development/ecoPrimals/infra/sporePrint` |
| `$SPOREPRINT_LOCAL_PORT` | `8880` |
| `$SITE_URL` | `primals.eco` |
| `$CF_TUNNEL_ID` | `d4c15fb6-d047-40fe-82d6-e324a5593421` |
| `$CF_ZONE_NAME` | `primals.eco` |
| `$CF_API_TOKEN_FILE` | `~/.cloudflare-api-token` |
| `$BEARDOG_PORT` through `$LOAMSPINE_PORT` | Hardcoded port numbers |

Scripts wired: `sporeprint_local.sh`, `sporeprint_verify.sh`, `sporeprint_dns.sh`,
`rotate_cookie_secret.sh`, `gate_switch.sh`, `tier_enforcement_test.sh`,
`external_validation.sh`, `security_validation.sh`, `tier_test_all.sh`.

### Python: deploy scripts

`deploy/nucleus_paths.py` provides centralized config for Python scripts:

```python
GATE_HOME = os.environ.get("GATE_HOME", os.path.expanduser("~"))
ABG_SHARED = os.path.join(GATE_HOME, "shared", "abg")
JUPYTERHUB_PORT = int(os.environ.get("JUPYTERHUB_PORT", "8000"))
```

Scripts wired: `pappusCast.py`, `tier_test_compute.py`, `tier_test_reviewer.py`,
`tier_test_observer.py`, `jupyterhub_tier_test.py`.

`pappusCast.py` exception handling narrowed from broad `except Exception` to
specific types: `subprocess.SubprocessError`, `json.JSONDecodeError`, `OSError`,
`urllib.error.URLError`, `ValueError`.

### Documentation

96 "ironGate" display references scrubbed across 23 markdown files. Gate-specific
text replaced with "the active gate" or equivalent gate-anonymous phrasing.
Filesystem paths (`/home/irongate`) left unchanged where they describe the
current deployment.

---

## 2. Lessons for Primal Teams

### Gate portability requires env-var indirection

Any primal that hardcodes a path to a specific user home directory is not
gate-portable. The pattern:

```rust
fn gate_home() -> String {
    std::env::var("GATE_HOME")
        .or_else(|_| std::env::var("HOME"))
        .unwrap_or_else(|_| "/home/nobody".to_string())
}
```

This fallback chain (`GATE_HOME` → `HOME` → safe default) should be standard
for any primal that touches the filesystem.

### `expect()` / `unwrap()` in network paths are deployment failures

tunnelKeeper's `Client::new()` called `expect()` on header construction.
On a misconfigured gate (empty API token, invalid characters), this panics
the entire health check binary. Converting to `Result` propagation costs
3 lines and makes the tool resilient to bad config.

**Audit target**: any primal that calls `expect()` or `unwrap()` in:
- Network client construction
- File path resolution
- Configuration parsing
- Credential loading

### Dependency slimming compounds

tunnelKeeper's `tokio = { features = ["full"] }` pulled in `io-util`, `net`,
`signal`, `sync`, and `time` — none of which it used. Slimming to
`rt-multi-thread + macros` reduces compile time and binary size. `rand` → `rand_core`
is similar: if you only need `OsRng`, you don't need the full PRNG suite.

**Recommendation**: all Rust primals should audit their `tokio` features and
`rand` usage. The ecosystem defaults to `features = ["full"]` far too often.

---

## 3. Upstream Gap Reconciliation (post-sweep)

### Resolved since May 8 consolidated gaps

| ID | What | Resolution |
|----|------|------------|
| DF-2 | toadStool `TOADSTOOL_AUTH_MODE` env var | toadStool S233 — `auth.mode` env + `eprintln` → `tracing` |
| DF-3 | songbird/squirrel silent on `auth.mode` TCP | songbird — `CallerContext` wired (TCP transport-aware) |
| U5 | sweetGrass port 39085 vs 9850 | sweetGrass v0.7.32 — port 9850 canonical |

### Still open

| ID | Owner | Severity | What |
|----|-------|----------|------|
| JH-11 | bearDog/biomeOS | **HIGH** | Cross-primal token federation |
| GAP-06 | rhizoCrypt | MEDIUM | No UDS transport |
| GAP-03 | biomeOS | MEDIUM | Cell graph live deploy not tested |
| GAP-09 | biomeOS | MEDIUM | Neural API registration endpoint |
| GAP-12 | primalSpring | LOW | 15 ludoSpring IPC methods need canonical registration |
| U1 | primalSpring | LOW | CHECKSUMS stale after Phase 59 refactoring |
| U2 | primalSpring | LOW | 5 deploy graphs missing `by_capability` |
| U3 | primalSpring | LOW | 8 profile graphs missing `bonding_policy` |

### Tier 3 code quality (from May 8 — unchanged, primal team backlogs)

| Priority | Primal | Issue |
|----------|--------|-------|
| 1 | coralReef | `eprintln!` → `tracing` |
| 2 | barraCuda | `unwrap()` → `?` in session/ops |
| 3 | nestGate | `unwrap()` → `?` in rpc/discovery |
| 4 | biomeOS | Mock helpers mixed with production code |
| 5 | bearDog | HSM mock not feature-gated |
| 6 | petalTongue | Bare `#[allow]` without reason |
| 7 | squirrel | 1105-line test file |

---

## 4. Verification

```
cargo clippy (tunnelKeeper): 0 warnings
cargo clippy (darkforest): 0 warnings
cargo check (both): success
bash -n (all deploy scripts): pass
python3 -c "import py_compile; ..." (all .py): pass
TODO/FIXME/HACK grep: 0 matches across *.rs, *.py, *.sh
```

---

## References

- `projectNUCLEUS/deploy/nucleus_config.sh` — bash config source of truth
- `projectNUCLEUS/deploy/nucleus_paths.py` — python config module
- `projectNUCLEUS/specs/EVOLUTION_GAPS.md` — living gap tracker (updated)
- `projectNUCLEUS/PHASES.md` — phase architecture (updated)
- `projectNUCLEUS/validation/PRIMAL_DEEP_DEBT_HANDBACK.md` — detailed per-primal debt audit
