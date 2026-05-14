# sourDough v0.3.0 — Deployment Internalization Handoff

**Date**: May 14, 2026
**From**: sourDough team
**Context**: First phase of the deployment internalization contract
(primalSpring/docs/SOURDOUGH_DEPLOYMENT_INTERNALIZATION.md)

## What Shipped

### `sourdough sign` (top-level CLI)

Ed25519 detached signatures, wired from the `sourdough-genomebin::signing` module
that was built in v0.2.0 but was not exposed via CLI.

- `sourdough sign <binary>` — signs any file, produces `.sig` sidecar
- `sourdough sign --generate-key` — generates Ed25519 keypair (`signing.key` + `signing.pub`)
- `sourdough sign --key <path>` — uses a custom signing key
- `sourdough verify <binary>` — verifies signature against public key
- `sourdough verify --pub-key <path>` — custom public key path
- `sourdough genomebin sign` now delegates to real signing (was sequoia-openpgp error stub)

Roundtrip verified: generate key → sign binary → verify → tamper → detect invalid.

### `sourdough validate ecobin` evolved

The command now auto-detects path type:

- **File path** (compiled binary): validates static linking (via `file` + `ldd`),
  stripped status, ELF format, size budget (50 MB default)
- **Directory path** (project source): existing behavior — C dependency scan,
  code formatting, clippy lint check

### Internalization Contract Status

| Pattern | Contract Phase | Status |
|---------|---------------|--------|
| `sourdough sign` | v0.3.0 | **Shipped** |
| `sourdough validate ecobin` (binary) | v0.3.0 | **Shipped** |
| `sourdough validate composition` | v0.4.0 | Planned |
| `sourdough scaffold --systemd` | v0.3.0 | Planned |
| `sourdough layout --triple-first` | v0.3.0 | Planned |
| `sourdough harvest` | v0.4.0 | Planned |
| `sourdough package` | v0.5.0 | Planned |
| `sourdough deploy` | v0.6.0 | Planned |

### Open Questions (from contract)

1. **Key management**: Should `sourdough sign` use age-encrypted keys or
   integrate with BearDog BTSP credential store? Currently uses plain hex files.
2. **CI ownership**: Does `auto-harvest.yml` call `sourdough harvest` or
   does sourDough provide its own GitHub Action?
3. **Remote deploy transport**: SSH (current) vs BTSP-tunneled commands?

## Quality Gates

- 256 tests passing (0 failures, 0 ignored)
- `cargo clippy --workspace --all-targets` zero warnings
- `cargo deny check` passing
- `cargo doc --workspace --no-deps` zero warnings
- `cargo fmt --all -- --check` clean
