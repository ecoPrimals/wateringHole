<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# LoamSpine v0.9.16 — musl-static ecoBin Deployment

**Date**: April 7, 2026
**Primal**: loamSpine
**Version**: 0.9.16
**Type**: Deployment Debt Resolution

---

## Summary

Resolved the deployment debt identified by primalSpring audit: LoamSpine was shipping glibc binaries, blocking container deployment via benchScale. Now builds musl-static following the nestgate/biomeOS reference pattern.

---

## Changes

### 1. `.cargo/config.toml` — musl-static targets

Added `[target.x86_64-unknown-linux-musl]` and `[target.aarch64-unknown-linux-musl]` with:
- `linker = "musl-gcc"` (x86_64) / `"aarch64-linux-gnu-gcc"` (aarch64)
- `rustflags`: `+crt-static`, `link-arg=-static`, `relocation-model=static`
- `relocation-model=static` prevents the musl ≤1.2.2 static-PIE segfault (Ubuntu 22.04 ships musl 1.2.2)

Convenience aliases: `cargo build-x64`, `cargo build-arm64`.

### 2. `Cargo.toml` — release profile

Added `[profile.release]` with `lto = true`, `codegen-units = 1`, `panic = "abort"`, `strip = true`. Aligns with rhizoCrypt's ecoBin release profile.

### 3. `Dockerfile` — musl-static container

Converted from `rust:slim` + `debian:bookworm-slim` (glibc) to:
- **Builder**: `rust:1.87-slim` + `musl-tools`, builds with `--target x86_64-unknown-linux-musl`
- **Runtime**: `alpine:3.20` (7MB base vs ~80MB debian:slim)
- Binary is fully statically linked — no libc dependency at runtime

### 4. Showcase cleanup

- `showcase/03-songbird-discovery/` archived to `fossilRecord/loamspine/showcase-songbird-apr2026/` — all Songbird discovery APIs were deprecated and removed in v0.9.15
- `showcase/scripts/start_songbird.sh` and `stop_songbird.sh` archived alongside
- `showcase/04-inter-primal/` renumbered to `03-inter-primal/`
- Showcase indexes (`00_SHOWCASE_INDEX.md`, `00_START_HERE.md`) updated

### 5. Root docs updated

README, STATUS, WHATS_NEXT, KNOWN_ISSUES, CONTRIBUTING, CONTEXT, CHANGELOG all updated to reflect musl-static deployment capability.

---

## Verification

```
$ file target/x86_64-unknown-linux-musl/release/loamspine
ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, stripped

$ ldd target/x86_64-unknown-linux-musl/release/loamspine
	not a dynamic executable

$ ls -lh target/x86_64-unknown-linux-musl/release/loamspine
4.3M
```

---

## Trio Status (post-handoff)

| Primal | musl-static | Owner |
|--------|------------|-------|
| **loamSpine** | DONE | loamSpine team |
| rhizoCrypt | **DONE** — musl-static x86_64 shipped (5.4M, Alpine runtime), plasmidBin updated (April 2026) | rhizoCrypt team |
| sweetGrass | Pending — partial `.cargo/config.toml` (missing `link-arg=-static`, `relocation-model=static`, `linker`), no CI cross-compile job, no Dockerfile | sweetGrass team |

---

## Remaining for plasmidBin

1. **Harvest**: Run `harvest.sh` to copy the musl-static `loamspine` binary to `infra/plasmidBin/primals/loamspine/latest/`
2. **Checksums**: Update `checksums.toml` — replace `x86_64-linux-gnu` with `x86_64-linux-musl` hash
3. **Manifest**: Update `manifest.toml` — set `static = true`, `stripped = true` for loamspine entries

---

## Exposed by

primalSpring inventory audit — "Trio binaries are glibc, not musl-static. This blocks container deployment via benchScale."

---

*loamSpine: Where memories become permanent.*
