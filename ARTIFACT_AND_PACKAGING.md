# Artifacts and Packaging — Binary Distribution and Validation

**Version:** 1.0.0  
**Date:** April 4, 2026  
**Status:** Active  

This document consolidates: `GENOMEBIN_ARCHITECTURE_STANDARD.md`, `GUIDESTONE_STANDARD.md`, `EXTERNAL_VALIDATION_ARTIFACT_STANDARD.md`, `UNIFIED_ARTIFACT_EVOLUTION.md`, `LIVESPORE_DEPLOYMENT_REVIEW.md`, `DOMAIN_INFRASTRUCTURE.md`.

---

## genomeBin Architecture

**Status:** Ecosystem standard. **Compliance:** Optional for mature ecoBins. **Reference implementation:** sourDough meta-circular genomeBin tooling (see sourDough repo).

**Operational surface (March 2026):** [ecoPrimals/plasmidBin](https://github.com/ecoPrimals/plasmidBin) implements the practical subset: per-primal `metadata.toml`, `manifest.lock`, `fetch.sh`, `harvest.sh`, `start_primal.sh`, `ports.env`. Full capability registry / tiers may live in `wateringHole/genomeBin/manifest.toml` as reference spec.

### Core principle

**genomeBin = ecoBin + deployment machinery** for autonomous cross-system deployment: one-command install, zero manual configuration where fully realized.

**Stages:**

| Stage | Definition |
|-------|------------|
| **UniBin** | One binary, multiple modes (subcommands); may be arch-specific or have C deps |
| **ecoBin** | UniBin + pure Rust + cross-compile + static musl + validation |
| **genomeBin** | ecoBin + wrapper: detect OS/arch/init, install, service integration, health, updates, rollback, uninstall |

**Formula:** genomeBin = ecoBin + deployment wrapper + system integration (services, config, health, updates).

### Tier requirements (summary)

**Tier 1 — ecoBin prerequisite:** UniBin; pure Rust; `x86_64` + `aarch64` musl builds; static; no C symbols in production path; `ldd` shows static.

**Tier 2 — deployment wrapper:** Detect OS, arch, init, privilege; select embedded ecoBin; verify checksum/signature; install to `/usr/local/bin` or `~/.local/bin/`.

**Tier 3 — system integration:** systemd / launchd / rc.d templates; smart default config under `/etc`, `~/.config`, etc.

**Tier 4 — health:** `primal doctor` (or equivalent); JSON output option; meaningful exit codes.

**Tier 5 — lifecycle:** update, rollback, uninstall with options.

### Self-extracting layout (file format)

```
primal.genome (executable shell + embedded data)
├── Wrapper script: detection, install, services, validation
├── Embedded payload (tar.gz)
│   ├── ecoBins/ (per-arch binaries)
│   ├── configs/ (templates)
│   ├── services/ (systemd, launchd, rc.d)
│   └── scripts/ (health-check, update)
└── Optional GPG signature
```

**Build sketch:**

```bash
cd genome/ && tar -czf ../payload.tar.gz *
cat wrapper-script.sh payload.tar.gz > primal.genome
chmod +x primal.genome
```

### Distribution URL pattern (illustrative)

```
https://install.primal.dev/
├── genome          # latest symlink
├── v0.9.0/
│   ├── primal.genome
│   ├── primal.genome.asc
│   └── primal.genome.sha256
```

**Installation examples:**

```bash
curl -sSf https://install.primal.dev/genome | sh
curl -sSf https://install.primal.dev/v0.9.0/primal.genome | sh
```

### Certification levels (from standard)

- **Bronze:** Tiers 1–3  
- **Silver:** + health (Tier 4)  
- **Gold:** + lifecycle (Tier 5)  
- **Platinum:** all tiers + UX  

### Current ecosystem note

Primals listed as genomeBin-ready in the original standard included BearDog, NestGate, ToadStool, biomeOS (ecoBin certified); others were in progress. **Live binary distribution** for most workflows is **plasmidBin**, not necessarily a `.genome` self-extractor.

**Related:** `UNIBIN_ARCHITECTURE_STANDARD.md`, `ECOBIN_ARCHITECTURE_STANDARD.md`.

### Build cleanliness for public binaries

Development builds embed host-specific paths (panic messages, debug info, proc-macro expansions). Public genomeBin releases MUST strip these.

**Required `.cargo/config.toml`:**

```toml
[build]
rustflags = [
    "--remap-path-prefix", "/home/builder=build",
    "--remap-path-prefix", "/rustc/=rustc/",
]

[profile.release]
strip = true
lto = true
```

**Verification (before publishing to plasmidBin):**

```bash
strings <binary> | grep -i '/home/'     # must be empty
strings <binary> | grep '192\.168\.'    # must be empty (unless intentional LAN default)
```

**CI builds preferred:** Ephemeral containers with generic paths eliminate host leakage at source. When building locally, `--remap-path-prefix` covers panic/debug paths; `strip = true` removes DWARF sections.

**Full standard:** `SECRETS_AND_SEEDS_STANDARD.md` § Build Cleanliness.

---

## guideStone Verification

**Status:** Ecosystem Standard v1.0. **Compliance:** Recommended for ecoBins producing verifiable output.

guideStone is a **verification class**, not a primal, binary type, or deployment class. It describes **what output means**: reproducible, self-proving computation.

### Three axes (orthogonal)

```
Structure:     UniBin → ecoBin → genomeBin
Deployment:    NUCLEUS → Niche → fieldMouse
Verification:  guideStone
```

### Five properties (all required for certification)

1. **Deterministic output:** Same inputs + same binary → same outputs within named tolerances across hardware; substrate may vary; FP tolerances allowed with justification.
2. **Reference-traceable:** Every numeric claim traces to paper, standard, constant, proof, NIST vectors, or calibration — not “floating” numbers.
3. **Self-verifying:** CHECKSUMS, CRC/Merkle/signature as appropriate; minimum CHECKSUMS validated before run (aligns with External Validation Artifact).
4. **Environment-agnostic:** ecoBin-style portability; no network/sudo/package manager required for core path; CPU path must cover full mathematical result where applicable.
5. **Tolerance-documented:** Thresholds in output metadata with physical/mathematical justification — not “test passes at this epsilon.”

Example metadata fragment:

```json
{
  "name": "chiral_condensate_4x4x4x8",
  "measured": 0.0847,
  "threshold": 0.01,
  "comparison": "absolute_error",
  "tolerance_justification": "stochastic estimator with N_noise vectors; error bounded by 1/sqrt(N_noise) * lattice_volume",
  "paper": "Bazavov et al., Phys. Rev. D 85, 054503 (2012)"
}
```

### Naming

```
<artifact>-guideStone-<version>
```

Examples: `hotSpring-guideStone-v0.7.0`, `bearDog-guideStone-v0.9.0`.

### Certification

Self-certified: artifact either satisfies the five properties or it does not; audit is public replication.

**Checklist topics:** deterministic cross-substrate; reference traceability; CHECKSUMS/integrity; ecoBin portability; tolerances documented (see original standard for full checkbox list).

### Evolution path (composition)

Bare guideStone → + BearDog signing → + rhizoCrypt DAG → + loamSpine certificate → + sweetGrass → + public chain anchor → Novel Ferment Transcript (full stack).

### Relationships

| Standard | Relation |
|----------|----------|
| ecoBin | guideStone builds on ecoBin output discipline |
| External Validation Artifact | Spring validation artifact is a specialized guideStone |
| genomeBin | Optional; guideStone does not require installer wrapper |
| plasmidBin | Releases may use `-guideStone-` infix |

---

## External Validation Artifacts

**Status:** Ecosystem Standard v1.1. **Compliance:** Required for springs; recommended for primals. **License:** AGPL-3.0-or-later.

**Goal:** One directory — USB, HPC, air-gapped — same command, no install conversation.

### Unified layout (v2 — arch-first)

```
validation/
├── hotspring          # Single entry point (spring-named; hotSpring example)
├── _lib.sh            # integrity_check, detect_arch, detect_gpu, resolve_binary
├── run                # Backward compat → ./hotspring validate
├── benchmark          # Backward compat → ./hotspring benchmark
├── README             # Plain text, 80 columns
├── bin/
│   ├── x86_64/
│   │   ├── static/    # musl — CPU-only universal
│   │   └── gpu/       # glibc — Vulkan dlopen
│   └── aarch64/
│       └── static/
├── shaders/*.wgsl
├── expected/*.json
├── results/           # runtime output
├── CHECKSUMS
└── LICENSE
```

**Legacy v1:** `bin/validate-x86_64`, flat names — may exist as symlinks for compatibility.

**Unified entry point:**

```bash
./hotspring validate
./hotspring benchmark
./hotspring generate
./hotspring deploy
./hotspring help
```

**Env overrides:** `HOTSPRING_NO_GPU=1`, `HOTSPRING_FORCE_GPU=1`.

### Binary/runtime behavior

Static musl: broad Linux compatibility. **Inside binary:** probe Vulkan/GPU; dual-path GPU vs CPU validation when applicable; CPU-only must run full suite.

**Terminal + JSON output:** JSON includes substrate, engine, checks with paper refs and `tolerance_justification` (see consolidated hotSpring example in original standard).

### One-artifact properties

| Property | Mechanism |
|----------|-----------|
| One directory | Copy entire tree |
| Two archs | `bin/<arch>/` |
| Dual binary | static + gpu folders; auto-select |
| No network / sudo / Rust | Prebuilt ELF |
| Self-verifying | CHECKSUMS |
| Portable in time | musl static |

### Container deployment (v1.1)

```
validation/
├── container/hotspring-guidestone.tar   # OCI image
├── hotspring.bat
└── Dockerfile (at project root for rebuild)
```

- Base example: Ubuntu 22.04; `libvulkan1`, `mesa-vulkan-drivers`  
- `docker run --rm ... validate`; GPU: `--device /dev/dri`  

**Cross-OS:** Linux native; macOS shell dispatches to Docker/Podman; Windows `hotspring.bat` → WSL2 or Docker Desktop.

**exFAT / noexec:** `resolve_binary()` may copy to `$TMPDIR` and chmod.

### Per-spring requirements (summary)

1. Static musl for `x86_64` and `aarch64` in layout.  
2. CPU-only must run **full** validation suite.  
3. Each check: name, paper (if applicable), measured, threshold, comparison, justification, duration.  
4. `expected/` with provenance.  
5. `CHECKSUMS` (SHA-256).  
6. Plain `README`.  
7. AGPL `LICENSE`.

**barraCuda / hotSpring:** WGSL as auditable source; Chuna papers cited per check — see original for domain specifics.

---

## Artifact Evolution

**Record:** v1.1. **Spring:** hotSpring (first adopter). **Standard:** External Validation Artifact.

### Problem (pre-unification)

Multiple entry points (`run`, `benchmark`, `chuna-engine`, `deploy-nucleus`, etc.) duplicated GPU and integrity logic; capability-first `bin/static/...` did not match benchScale/plasmidBin `arch/name` conventions; x86_64 only.

### Solution (unified entry)

- **Single entry:** `./hotspring` shell dispatcher with subcommands (not one giant Rust binary — avoids 50MB+ merge and feature coupling).  
- **Arch-first:** `bin/x86_64/static/validate` not `bin/static/validate-x86_64`.  
- **Shared `_lib.sh`:** `integrity_check`, `detect_arch`, `detect_gpu`, `resolve_binary`.  
- **aarch64:** `cargo build --target aarch64-unknown-linux-musl` for static; GPU binaries typically native-only.  
- **Backward compatibility:** Thin forwarders preserve old script names.

### benchScale / agentReagents

- Multi-substrate Docker tests (CPU, NVIDIA, AMD, Alpine; optional aarch64 qemu-user).  
- VM template `gate-hotspring-validation.yaml` (Ubuntu, Vulkan, optional GPU passthrough).

### Universal substrate layer (v1.1)

- `detect_os()` → non-Linux container dispatch.  
- `hotspring.bat` for Windows.  
- OCI image in `container/`.  
- `prepare-usb.sh` ext4 vs exFAT dual mode.  
- aarch64 cross-validation via qemu-user (40/40 bit-identical observables in reported runs).

### Deployment matrix (from evolution doc)

| Platform | Runtime | GPU |
|----------|---------|-----|
| Linux x86_64 | Native | Auto |
| Linux aarch64 | Native static | CPU-only |
| Linux | Docker/Podman | Passthrough |
| Windows | WSL2 / Docker | Per launcher |
| macOS | Docker/Podman | CPU typical |

### Future (from evolution doc)

Rust dispatcher; genomeBin manifest alignment with `liveSpore.json`; primalSpring graph-produced artifacts; aarch64 GPU when hardware matrix allows; biomeOS graph awareness for container path.

---

## liveSpore Field Report

**Status:** Field report v1.0 (hotSpring ColdSpore). **Artifact:** hotSpring-guideStone-v0.7.0 era. **Medium:** USB (ext4, 15 GB example).

### What worked

- **Static musl:** Zero dynamic deps on x86_64 Linux.  
- **CHECKSUMS:** Caught stale binaries until regenerated.  
- **Cross-GPU determinism:** ~1e-11 relative plaquette agreement across NVIDIA/AMD/llvmpipe.  
- **ext4 USB:** Execute + write results on medium.  
- **liveSpore.json:** Self-knowledge manifest of runs.

### Critical lessons

1. **FAT32:** No real execute bits — use **ext4** for Linux-first USB, or exFAT + **tmpdir copy** pattern (now in `_lib.sh`).  
2. **Static musl cannot dlopen Vulkan:** GPU path needs **glibc GPU binary** separate from musl static; dispatch in wrapper (`hotspring` / `run`).  
3. **Production vs validation drift:** GPU HMC in generate but not overnight validate — keep consumers in sync.  
4. **Asymmetric lattices:** Finite-T QCD needs Ns ≠ Nt — wire parsers consistently.  
5. **Benchmarks:** Added `./benchmark` for hardware profiling; unified benchmark schema still an ecosystem evolution item.

### Friction / gaps (snapshot)

- **toadStool socket on ColdSpore:** Logs noise when biomeOS absent; prefer `BIOMEOS_DEPLOYMENT_MODE=cold` behavior.  
- **ILDG guided generation:** Not fully exposed from USB workflow.  
- **genomeBin manifest:** `liveSpore.json` vs `manifest.toml` convergence TBD.  
- **primalSpring composition:** Payloads hand-written vs graph-generated — evolution target.

### Post-review resolutions (April 2026)

- aarch64 static in `bin/aarch64/static/`; benchScale qemu validation.  
- exFAT tmpdir execution fallback.  
- OCI image + cross-OS launchers.  
- Remaining: toadStool noise, ILDG UX, manifest convergence, primalSpring pipeline, container graph in biomeOS, aarch64 GPU binaries.

### Performance snapshot (from report)

| Mode | Checks | Notes |
|------|--------|-------|
| CPU musl | 59/59 | Slower, universal |
| GPU glibc | 71/71 | Vulkan dlopen path |

---

## Domain Infrastructure

**Updated:** 2026-03-29.

### Overview

| Domain | Purpose | Hosting | DNS | Registrar |
|--------|---------|---------|-----|-----------|
| nestgate.io | BirdSong beacon, Dark Forest rendezvous, STUN/NAT relay | Cloudflare Tunnel → biomeOS UDS | Cloudflare proxied | Porkbun |
| primals.eco | Public portal, docs, binary index | GitHub Pages (sporePrint) | Cloudflare proxied | Porkbun |

### nestgate.io

Public BirdSong entry. Without valid mito genetics, endpoint returns noise (e.g. HTTP 403 with strict headers).

**Path:** Internet → Cloudflare (TLS, DDoS) → QUIC tunnel → `cloudflared` (user systemd) → Unix socket → biomeOS API (Dark Forest gate, beacon verification, rendezvous).

**DNS:** `api`, `tower`, `beacon` subdomains as CNAME to `<tunnel-uuid>.cfargotunnel.com`.

**Example `~/.cloudflared/config.yml`:**

```yaml
tunnel: nestgate-api
credentials-file: <home>/.cloudflared/<tunnel-uuid>.json

ingress:
  - hostname: api.nestgate.io
    service: unix:<runtime>/biomeos/biomeos-api-<family-id>.sock
  - hostname: tower.nestgate.io
    service: unix:<runtime>/biomeos/biomeos-api-<family-id>.sock
  - hostname: beacon.nestgate.io
    service: unix:<runtime>/biomeos/biomeos-api-<family-id>.sock
  - service: http_status:404
```

**User services:** `biomeos-beacon.service`, `cloudflared-beacon.service`; `loginctl enable-linger`.

**Connection priority (conceptual):** IPv6 direct → IPv4 → LAN mDNS/Dark Forest → STUN → family relay → future onion overlay.

**Security:** TLS at edge; QUIC PQXDH; application-layer family gate; endpoint noise to non-family.

### primals.eco

**Architecture:** Cloudflare → GitHub Pages (`ecoPrimals/sporePrint`).

**DNS:** A records to GitHub Pages IPs (`185.199.108-111.153`); `www` CNAME to `ecoprimals.github.io`. HTTPS enforced.

### LAN cloud (multi-machine)

Multiple `cloudflared` connectors for same tunnel (HA). Roles: Primary / Standby / Relay. Songbird LAN mesh for redundancy. Future: threshold beacon crypto.

### Operations

```bash
systemctl --user status biomeos-beacon cloudflared-beacon
systemctl --user restart biomeos-beacon cloudflared-beacon
curl -s -o /dev/null -w "%{http_code}" https://api.nestgate.io/   # expect 403 (Dark Forest)
```

**Not documented in original:** tunnel secrets, account tags, `.family.seed` contents, specific machine IPs.

---

## Version History

| Version | Date | Notes |
|---------|------|-------|
| 1.0.0 | 2026-04-04 | Consolidated artifact, packaging, validation, and domain docs listed in header. |

**Sources consolidated:** `GENOMEBIN_ARCHITECTURE_STANDARD.md`, `GUIDESTONE_STANDARD.md`, `EXTERNAL_VALIDATION_ARTIFACT_STANDARD.md`, `UNIFIED_ARTIFACT_EVOLUTION.md`, `LIVESPORE_DEPLOYMENT_REVIEW.md`, `DOMAIN_INFRASTRUCTURE.md`.

**Related:** `ECOBIN_ARCHITECTURE_STANDARD.md`, `SEMANTIC_METHOD_NAMING_STANDARD.md`, plasmidBin README, sporePrint repo.
