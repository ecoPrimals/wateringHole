# plasmidBin ecoBin Compliance — All Primals Handoff

**Date**: March 28, 2026
**From**: primalSpring (composition + cross-deploy validation)
**To**: All 14 primal teams
**Priority**: High — blocks universal deployment
**Context**: Cross-hardware deployment testing (Eastgate x86_64 + Pixel aarch64/GrapheneOS) revealed per-primal gaps. plasmidBin has been overhauled with fresh ecoBin-compliant binaries. This handoff defines what each team needs to do to reach full compliance.

---

## Universal Requirements (All Primals)

Every primal must:

1. **Build musl-static** for `x86_64-unknown-linux-musl` (and `aarch64-unknown-linux-musl` when cross-compile is set up)
2. **Strip debug info** — `[profile.release] strip = true` in Cargo.toml, or `strip -s` post-build
3. **Support TCP listener** — `--listen addr:port` or `--port PORT` flag for JSON-RPC over TCP
4. **Expose `health.liveness`** — via raw newline-delimited TCP JSON-RPC (not HTTP-only)
5. **Start without identity** — run without `FAMILY_ID`/`NODE_ID` in standalone mode
6. **Submit to plasmidBin** — via `harvest.sh` after verification

### Standard TCP ports

| Primal | Port |
|--------|------|
| beardog | 9100 |
| songbird | 9200 |
| nestgate | 9300 |
| toadstool | 9400 |
| squirrel | 9500 |
| biomeos | 9800 |
| petaltongue | 9600 |
| rhizocrypt | 9700 |
| loamspine | 9710 |
| sweetgrass | 9720 |

---

## Per-Primal Status and Actions

### BearDog (v0.9.0) — CLOSE to full compliance

**plasmidBin status**: x86_64 A++, aarch64 A++

**What works**:
- musl-static builds on both arches
- TCP via `--listen 0.0.0.0:9100` — confirmed on Pixel
- `health.liveness` and `health.readiness` — canonical names
- `--abstract` flag exists (abstract socket binds, but logs filesystem path)

**Remaining actions**:
- [ ] Default `FAMILY_ID` to `standalone` when unset (currently hard-fails, breaks UniBin standalone requirement)
- [ ] Add `--audit-dir` / `BEARDOG_AUDIT_DIR` env var (crashes on read-only filesystem when writing `audit.log` to CWD)
- [ ] Fix `--abstract` socket logging — should confirm abstract namespace bind, not log `@biomeos_beardog_*` as filesystem path
- [ ] Wire `birdsong.generate_encrypted_beacon` into server RPC handler
- [ ] Add `beardog seed generate/export/verify` subcommand

---

### Songbird (v0.2.1) — CLOSE to full compliance

**plasmidBin status**: x86_64 A++, aarch64 A++

**What works**:
- musl-static builds on both arches
- TCP via `--listen 0.0.0.0:9200` — confirmed on Pixel, full 14 capabilities
- HTTP `/health` endpoint

**Remaining actions**:
- [ ] Expose `health.liveness` as canonical JSON-RPC method name (currently only responds to `health` short name)
- [ ] Add `--dark-forest` CLI flag (currently env-only via `SONGBIRD_DARK_FOREST=true`)
- [ ] Add `--pid-dir` / `SONGBIRD_PID_DIR` for Android/container substrates (writes PID to CWD by default)

---

### NestGate (v0.1.0 / v4.50 internal) — NEEDS WORK

**plasmidBin status**: x86_64 A++ (fixed from dynamic to musl-static March 28), aarch64 MISSING

**What works**:
- x86_64 musl-static binary now functional (was segfaulting on older build)
- Filesystem socket path conformant

**Remaining actions**:
- [ ] **Critical**: Set up aarch64-unknown-linux-musl cross-compile (add `.cargo/config.toml` with musl linker)
- [ ] Wire `--port` to actual TCP bind (flag exists but non-functional)
- [ ] Accept `server` as alias for `daemon` subcommand
- [ ] Verify `health.liveness` method exists
- [ ] Submit aarch64 binary to plasmidBin when ready

**Note**: NestGate is the oldest primal and is entering an evolution week. Cross-compile and TCP are the priorities for plasmidBin compliance.

---

### Squirrel (v0.1.0) — CLOSE to full compliance

**plasmidBin status**: x86_64 A++, aarch64 A++

**What works**:
- musl-static builds on both arches
- Abstract socket `@squirrel` confirmed working on GrapheneOS (SELinux-safe)
- HTTP `--port 9500` works on Pixel

**Remaining actions**:
- [ ] Add filesystem socket in `$XDG_RUNTIME_DIR/biomeos/squirrel.sock` alongside abstract socket (for desktop discovierability)
- [ ] Add `health.liveness` / `health.readiness` / `health.check` method handlers (currently uses `system.health` / `system.status` — non-standard)
- [ ] Alias `system.*` health methods to `health.*` canonical names

---

### ToadStool (v0.1.0) — NEEDS WORK

**plasmidBin status**: x86_64 A++, aarch64 A++

**What works**:
- musl-static builds on both arches
- Executes on Pixel (capabilities mode works)

**Remaining actions**:
- [ ] **Critical**: Wire `--port` flag to actual TCP server bind (flag exists but not forwarded to implementation)
- [ ] Verify/add `health.liveness` via JSON-RPC
- [ ] Verify standalone server mode works without `biome.yaml`

---

### biomeOS (v0.1.0 / v2.76 internal) — NEEDS TCP MODE

**plasmidBin status**: x86_64 A++, aarch64 A+ (unstripped — need cross-strip tooling)

**What works**:
- musl-static builds on both arches
- Graph execution, NUCLEUS orchestration, Neural API on desktop
- `health.liveness`, `health.readiness`, `health.check` all canonical

**Remaining actions**:
- [ ] **Critical**: Implement TCP-only API mode (`biomeos api --port PORT --tcp-only` or similar). Currently `api` mode logs "HTTP mode deprecated — using Unix socket only" and forces UDS even when `--port` is specified. This blocks mobile orchestration.
- [ ] **Critical**: Honor `gate` parameter in `capability.call` for cross-gate routing. Currently always uses primary (local) endpoint, ignoring `gate` field.
- [ ] Strip aarch64 binary (or configure `aarch64-linux-gnu-strip` in CI)
- [ ] Add `route.register` documentation for cross-gate federation

---

### petalTongue (v0.1.0) — NEEDS WORK

**plasmidBin status**: x86_64 A++ (freshly stripped), aarch64 MISSING

**What works**:
- x86_64 musl-static binary functional

**Remaining actions**:
- [ ] Build aarch64-unknown-linux-musl (headless mode — egui cross-compile may need `--no-default-features` for headless)
- [ ] Move socket to `$XDG_RUNTIME_DIR/biomeos/petaltongue.sock` (currently custom directory)
- [ ] Add `--port` flag for TCP JSON-RPC
- [ ] Submit aarch64 binary to plasmidBin when ready

---

### barraCuda (v0.3.5+) — BUILD-FROM-SOURCE

**plasmidBin status**: Not in plasmidBin (GPU deps, build-from-source only)

**What works**:
- Pure math library with WGSL shaders
- 4,162+ tests

**Actions**:
- [ ] Evaluate if a headless CLI binary can be produced as ecoBin (math-only, no GPU runtime)
- [ ] If applicable, add musl-static build target and submit to plasmidBin

---

### coralReef — BUILD-FROM-SOURCE

**plasmidBin status**: Not in plasmidBin (GPU deps, build-from-source only)

**Actions**:
- [ ] Add `--port` flag for raw newline TCP JSON-RPC (alongside jsonrpsee HTTP)
- [ ] Evaluate headless ecoBin feasibility (shader compilation without GPU runtime)

---

### sourDough (v0.1.0) — NEEDS BUILD

**plasmidBin status**: Not in plasmidBin

**Actions**:
- [ ] Build x86_64-unknown-linux-musl binary
- [ ] Submit to plasmidBin via `harvest.sh`

---

### sweetGrass — CLOSE

**plasmidBin status**: Not in plasmidBin

**What works**:
- `health.liveness` canonical
- UDS newline-conformant

**Actions**:
- [ ] Build x86_64-unknown-linux-musl binary
- [ ] Add `--port` flag (alias for port portion of `--http-address`)
- [ ] Submit to plasmidBin via `harvest.sh`

---

### rhizoCrypt — NEEDS WORK

**plasmidBin status**: Not in plasmidBin

**Actions**:
- [ ] Add newline-delimited TCP JSON-RPC listener (currently HTTP-only)
- [ ] Build x86_64-unknown-linux-musl binary
- [ ] Submit to plasmidBin

---

### LoamSpine — BLOCKED

**plasmidBin status**: Not in plasmidBin

**Blocker**: Tokio nested runtime panic in `infant_discovery` on startup.

**Actions**:
- [ ] Fix Tokio nested runtime panic (use `tokio::task::spawn_blocking` or restructure discovery)
- [ ] Add `--port` flag (alias for `--jsonrpc-port`)
- [ ] Build x86_64-unknown-linux-musl binary
- [ ] Submit to plasmidBin

---

### skunkBat — NEEDS AUDIT

**plasmidBin status**: Not in plasmidBin

**Actions**:
- [ ] Audit current build for musl-static compatibility
- [ ] Add TCP listener and `health.liveness`
- [ ] Build x86_64-unknown-linux-musl binary
- [ ] Submit to plasmidBin

---

## Summary Matrix

| Primal | x86_64 | aarch64 | TCP | health.liveness | Standalone | plasmidBin |
|--------|--------|---------|-----|-----------------|------------|------------|
| beardog | A++ | A++ | C | C | X (FAMILY_ID) | In |
| songbird | A++ | A++ | C | P | C | In |
| nestgate | A++ | MISSING | X | ? | C | Partial |
| squirrel | A++ | A++ | C | X | C | In |
| toadstool | A++ | A++ | X | ? | C | In |
| biomeos | A++ | A+ | X | C | C | In |
| petaltongue | A++ | MISSING | X | ? | C | Partial |
| barracuda | -- | -- | -- | -- | -- | Build-from-source |
| coralreef | -- | -- | X | ? | C | Build-from-source |
| sourdough | MISSING | MISSING | ? | ? | ? | Not yet |
| sweetgrass | MISSING | MISSING | X | C | C | Not yet |
| rhizocrypt | MISSING | MISSING | X | ? | C | Not yet |
| loamspine | MISSING | MISSING | X | ? | X (crash) | Blocked |
| skunkbat | MISSING | MISSING | ? | ? | ? | Not yet |

---

## Workflow for Teams

1. Build: `cargo build --release --target x86_64-unknown-linux-musl`
2. Verify: `file target/.../YOUR_PRIMAL` — must say "statically linked", not "not stripped"
3. Test on Pixel (if aarch64): `adb push ... && adb shell ... --listen 0.0.0.0:PORT`
4. Harvest: `cd ecoPrimals/infra/plasmidBin && ./harvest.sh --primal YOUR_PRIMAL`
5. Commit: plasmidBin checksums.toml + manifest.toml updates

See `plasmidBin/README.md` for full workflow, `IPC_COMPLIANCE_MATRIX.md` for detailed transport compliance, and `ECOBIN_ARCHITECTURE_STANDARD.md` for the ecoBin specification.
