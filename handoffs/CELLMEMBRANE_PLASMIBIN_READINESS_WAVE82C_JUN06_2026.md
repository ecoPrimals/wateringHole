# cellMembrane — plasmidBin Ownership Readiness (Wave 82c)

**Date**: 2026-06-06  
**Gate**: ironGate  
**Status**: Ready to receive full plasmidBin ownership  

---

## What cellMembrane Now Owns (implemented)

| Capability | Implementation | Status |
|------------|---------------|--------|
| Binary fetch from Forgejo/GitHub releases | `membrane plasmid.fetch` | LIVE |
| Binary push to VPS (atomic replace + restart) | `membrane plasmid.refresh` | LIVE |
| BLAKE3 checksum verification | `plasmid/fetch.rs` (native blake3 crate) | LIVE |
| Service registry derivation | `nucleus_primals()` from `MembraneService::all()` | LIVE |
| Source priority (Forgejo → GitHub → SSH) | `sources.toml` + `FetchSource` enum | LIVE |
| VPS deployment ops (systemd, bridges, firewall) | SSH/SCP transport in `ssh.rs` | LIVE |
| Caddy reverse proxy management | `cloudflare.rs` + manual wiring | LIVE |
| Temporal cascade (workspace sync) | `membrane temporal.cascade` | LIVE |
| K-Derm relay chain | `membrane relay.run` | LIVE |
| Gate health aggregation | `membrane gate.health` | LIVE |

## What Remains (P2 — next waves)

| Item | Priority | Notes |
|------|----------|-------|
| `plasmid.deploy` (absorb `deploy_membrane.sh deploy`) | P2 | Full deploy flow in Rust |
| `plasmid.harvest` (build from source + checksum + store) | P3 | Currently manual via `build-primal.sh` |
| CI workflow wiring (check-updates.yml, harvest.yml) | P2 | Forgejo Actions on cellMembrane org |
| Peptidoglycan self-refresh auto-fetch | P2 | Timer + Forgejo releases API |

## VPS Integration Readiness (projectNUCLEUS)

| Validation | Status |
|------------|--------|
| 13/13 primals ALIVE on VPS | CONFIRMED |
| UDS-only posture (zero external primal TCP) | CONFIRMED |
| 5-domain sovereign TLS (Caddy + Let's Encrypt) | CONFIRMED |
| `socat` bridges for UDS→private-network | OPERATIONAL |
| Federation mesh port :7700 | OPERATIONAL |
| BTSP auth enforced | SINCE 2026-06-02 |
| Dark Forest audit re-validation needed | PENDING (NUCLEUS scope) |

## For Upstream primalSpring Audit

cellMembrane codebase metrics (Wave 82c):

- **226 tests** passing (8 test modules + integration + doc-tests)
- **Zero clippy warnings** (pedantic + nursery enforced)
- **Zero unsafe code** (`#![forbid(unsafe_code)]` on both crates)
- **Zero TODOs/FIXMEs** in source
- **Zero mocks** in production code
- **Zero `#[allow]`** attributes (1 justified Clippy override for lifetime)
- **All files < 800 lines** (max 743L in test coverage module)
- **All paths capability-based** (ServicePaths, CredentialPaths, env-driven)
- **All external deps pure Rust** (reqwest+rustls, blake3, tokio, serde)
- **Proper error taxonomy** (ShadowError: Ssh, CloudflareApi, ForgejoApi, Http, Parse, Io, Json, Git, Toml)

## Gaps for Upstream Primal Teams

| Gap | Owner | Blocking |
|-----|-------|----------|
| squirrel UDS JSON-RPC dispatch not wired | eastGate | Health probe (workaround: SocketExists) |
| petaltongue UDS JSON-RPC dispatch not wired | ironGate | Health probe (workaround: SocketExists) |
| skunkBat needs `--socket` binary rebuild on VPS | eastGate | UDS-only audit |
| 6 primals missing `capability_registry.toml` | Various | Ecosystem tooling |

---

*"The membrane is ready. The depot is inherited. The pipeline flows."*
