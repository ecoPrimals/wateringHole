# primalSpring v0.9.17 — genomeBin Cross-Architecture Depot Handoff

**From**: primalSpring (syntheticChemistry/primalSpring)
**To**: All primal teams and spring teams
**Date**: April 19, 2026
**Trigger**: plasmidBin evolved to full genomeBin depot — 42 binaries across 6 target triples

---

## What Changed

plasmidBin is now a **genomeBin-compliant cross-architecture binary depot** per the
ecoBin Architecture Standard v3.0. It ships pre-built binaries for every plausible
Rust target, not just x86_64.

### Before (v0.9.16)
- plasmidBin had 14 x86_64 musl-static binaries + 5 aarch64 binaries
- Flat directory layout: `primals/` (x86_64) + `primals/aarch64/`
- Build script: `build_ecosystem_musl.sh` (x86_64 + aarch64 only)

### After (v0.9.17)
- **42 binaries across 6 target triples**
- genomeBin layout: `primals/{target-triple}/{binary}`
- Backward-compat symlinks: `primals/{binary}` → `x86_64-unknown-linux-musl/{binary}`
- Build script: `build_ecosystem_genomeBin.sh` (9 targets, 3 tiers)

---

## Target Matrix

| Target Triple | Tier | Primals Built | Notes |
|---------------|------|---------------|-------|
| x86_64-unknown-linux-musl | Tier 1 MUST | 13/14 | Primary deployment target |
| aarch64-unknown-linux-musl | Tier 1 MUST | 12/14 | ARM64 servers, Pixel/GrapheneOS |
| armv7-unknown-linux-musleabihf | Tier 1 MUST | 10/14 | Raspberry Pi, ARM32 embedded |
| x86_64-pc-windows-gnu | Tier 2 SHOULD | 1 (barraCuda) | Windows cross-compile via mingw |
| aarch64-linux-android | Tier 2 SHOULD | 5 | Pixel/GrapheneOS native |
| riscv64gc-unknown-linux-musl | Tier 3 NICE | 1 (primalSpring) | RISC-V; all others cargo-check pass |
| x86_64-apple-darwin | Tier 2 SHOULD | 8 check-pass | No osxcross; proves pure Rust |
| aarch64-apple-darwin | Tier 2 SHOULD | 8 check-pass | No osxcross; proves pure Rust |

---

## What Primal Teams Need to Know

### 1. Your binaries are now cross-compiled to multiple architectures

Every primal that links successfully on a target gets a BLAKE3-checksummed entry in
`plasmidBin/checksums.toml`. If your primal doesn't appear on a target, check the
documented gaps below.

### 2. Documented gaps — action items for primal teams

**nestgate**: Binary is in workspace member `nestgate-bin`, but cross-compilation
with `--manifest-path` builds only the root lib crate on non-x86_64 targets. **Fix**:
ensure the root `Cargo.toml` produces a binary, or add `--workspace` support to the
build script.

**skunkbat**: Library-only crate — no binary target. This is by design but means
skunkBat capabilities must be consumed via library linking, not IPC. If skunkBat
needs to be an IPC primal, add a `[[bin]]` target.

**toadstool on armv7**: `1024 * 1024 * 1024 * 4` overflows on 32-bit usize in
`crates/runtime/gpu/src/unified_memory/backends/cpu.rs:43`. **Fix**: use `u64`
instead of `usize` for the allocation constant, or gate with `#[cfg(target_pointer_width)]`.

**biomeos on armv7**: `1_usize << 53` overflows on 32-bit in
`crates/biomeos-types/src/cast.rs:41`. Same fix: use `u64` or conditional compilation.

### 3. macOS and Windows gaps are NOT bugs

Most primals use Unix Domain Sockets (`tokio::net::UnixListener`) which don't exist
on Windows or aren't available in macOS cross-compilation without osxcross. The
`cargo check` pass proves the Rust code compiles; the link failure is a toolchain
limitation, not a code issue.

**For primal teams wanting macOS/Windows**: Abstract socket creation behind a
platform-aware trait, or use TCP-only mode when UDS is unavailable. beardog's
`tunnel` crate and songbird's network stack already have this pattern partially.

### 4. How to test your primal on a new target

```bash
# From primalSpring root:
./scripts/build_ecosystem_genomeBin.sh --target aarch64-linux-android

# Or build everything:
./scripts/build_ecosystem_genomeBin.sh --all
```

The script automatically configures cross-linkers, runs `cargo check` first (fast
validation), then attempts full build if a linker is available.

---

## What Spring Teams Need to Know

### 1. plasmidBin layout changed — update your scripts

If your spring has scripts that reference `plasmidBin/primals/beardog` directly,
those paths still work via symlinks. But if you copy binaries (e.g., for Docker
deployment), use the canonical path: `plasmidBin/primals/x86_64-unknown-linux-musl/beardog`.

### 2. `start_primal.sh` auto-detects your architecture

The updated `start_primal.sh` uses `uname -m` to detect the target triple
automatically. No need to pass `--arch` flags.

### 3. benchScale Docker deployment works

12 primals deployed and version-verified in the `nucleus-lab` Docker container.
The `deploy-ecoprimals.sh` script now resolves from the genomeBin layout.

### 4. Pixel 8 deployment ready (gated on USB)

`deploy_pixel.sh` updated to use `aarch64-unknown-linux-musl/` layout. 12 aarch64
binaries are ready. Connect Pixel via USB and run `./deploy_pixel.sh`.

---

## Composition and Deployment Patterns for NUCLEUS

### neuralAPI from biomeOS

biomeOS's Neural API is the primary composition substrate. Springs interact with
NUCLEUS through IPC (JSON-RPC 2.0 over Unix Domain Sockets), not library linking.

**Pattern**: Spring builds → Spring discovers primals via `discover_by_capability()` →
Spring calls primal methods via `tcp_rpc_multi_protocol()` → biomeOS orchestrates
primal lifecycle.

**TCP fallback**: When UDS sockets aren't available (Docker, cross-network, Android),
primals fall back to well-known TCP ports from `plasmidBin/ports.env`. The tolerance
hierarchy defines expected latencies per fallback tier.

### Deploy graph composition

Deploy graphs are TOML files that declare primal composition. Fragment-first
composition means graphs are assembled from reusable fragments:

```
profiles/full.toml  → resolves →  fragments/tower.toml + fragments/node.toml + ...
```

Springs validate by deploying a graph and probing health, not by linking primal
libraries. This is the "external spring validation" pattern.

### Cross-architecture deployment

For deploying NUCLEUS on non-x86_64 hardware:
1. Build: `./scripts/build_ecosystem_genomeBin.sh --tier1`
2. Harvest: Copy from `/tmp/primalspring-deploy/primals/{target-triple}/`
3. Deploy: Use `start_primal.sh` (auto-detects arch) or `deploy_pixel.sh` for Android

---

## Files Changed

| Repository | Files | Summary |
|-----------|-------|---------|
| primalSpring | `scripts/build_ecosystem_genomeBin.sh` (new), CHANGELOG, README | New build script, version bump to 0.9.17 |
| plasmidBin | manifest.toml, checksums.toml, start_primal.sh, deploy_pixel.sh, fetch.sh, harvest.sh, README | genomeBin v5.0 layout, full target matrix |
| wateringHole | genomeBin/manifest.toml, PRIMAL_REGISTRY.md, ECOSYSTEM_EVOLUTION_CYCLE.md | Updated standards and registry |
| benchScale | deploy-ecoprimals.sh | genomeBin-aware binary resolution |

---

## Absorption Checklist

For primal teams:
- [ ] Review your primal's cross-compilation status in the target matrix above
- [ ] If armv7/RISC-V gaps affect you, fix 32-bit overflow or workspace binary issues
- [ ] Test: `./scripts/build_ecosystem_genomeBin.sh --target <your-target>`

For spring teams:
- [ ] Update any hardcoded plasmidBin paths to use `primals/{target-triple}/`
- [ ] If you have custom deploy scripts, update to resolve symlinks or use target-triple paths
- [ ] Test your spring's guideStone against the new layout

For downstream products (sporeGarden):
- [ ] Pull latest plasmidBin; `./fetch.sh --all` now downloads for your detected architecture
- [ ] `start_primal.sh` auto-detects target triple — no manual arch selection needed
