# Orthogonal Dimensions Review — Reusable Checklist

**Purpose**: Systematic reassessment checklist for overwatch cascade reviews.
Use at wave boundaries or whenever a comprehensive posture check is needed.

---

## 1. Temporal

- [x] `wave.toml` reflects current wave ID, sub, and posture (Wave 143a)
- [x] Gate heads published (`heads/*.toml`) — all active gates have recent timestamps
- [x] `freshness.toml` uses tree hashes (DAG, not cyclic graph)
- [x] Active impulses triaged — 5 stale fossilized, 2 active remain (CAC + Phase 2)
- [x] No stale diverge impulses older than 2 waves
- [x] ecosystem_manifest.toml version current (v3.1.0)

## 2. Ecological (Primal Health)

- [x] All primals compile (`cargo check` / `cargo test` green) — all 4 depot arch
- [x] Zero P1 blockers in any primal
- [x] All primal repos converged across remotes (38/39 synced)
- [x] Transport injection adopted across all non-exempt primals
- [x] Neural API methods shipped by all primal teams
- [x] Test counts stable or increasing (toadStool 9,232; coralReef 3,650; sourDough 490)
- [x] Phase 2 abstraction shipping (songBird IpcStream, petalTongue platform, skunkBat TransportEndpoint)

## 3. Hardware / Topology

- [x] `HARDWARE_INVENTORY.md` reflects current physical state
- [ ] All online gates reachable — **RustDesk transient to ironGate + flockGate**
- [x] Gate roles match manifest `[topology]` section
- [x] Network backbone operational (CRS310, MikroTik, switches)
- [x] Pending hardware actions documented (northGate enrollment, westGate offline)
- [x] SoloKey / HSM / StrongBox status current

## 4. Sovereignty / Membranes

- [ ] K-Derm three-layer model intact (external outer → sovereign outer → inner)
- [ ] Cloudflare outer membrane operational (wildcard DNS, DDoS protection)
- [ ] Sovereign outer membrane operational (Caddy TLS, bearDog ACME)
- [ ] Inner membrane zero-commercial (primal.eco data path)
- [ ] S1-S4 sovereignty shadows all graduated
- [ ] DNSSEC enabled on sovereign domains
- [ ] Cross-membrane validation scenario operational

## 5. Depot / Build Pipeline

- [x] Depot authority identified and operational (sporeGate — 13-target build authority)
- [x] ecoBins built as musl-static stripped (post-primordial standard)
- [x] `checksums.toml` / `signatures.toml` current (59 binaries, Wave 143a)
- [x] `require-signed` enforced system-wide
- [x] SIGN-VERIFY-ON-FETCH operational in cellMembrane
- [x] All 4 depot architectures built for all 14 primals (Windows 14/14 COMPLETE)
- [ ] Exotic architectures expanded to depot as primal adoption completes
- [x] Depot layout consistent across depot authority and relay mirrors
- [x] `plasmid.harvest` → `plasmid.fetch` pipeline tested end-to-end
- [x] `depot_sync --push` operational (builder → VPS)

## 6. Website / Public Surface / Security

- [ ] `primals.eco` returning 200 — **P0: ROOT 404** (sporePrint rebuild needed)
- [x] `primals.eco/footprint/` returning 200 (GIS composition)
- [x] `live.primals.eco` returning 200 (petalTongue dashboard)
- [x] Security headers deployed (HSTS, CSP, X-Frame-Options, X-Content-Type)
- [x] fail2ban active on SSH endpoints
- [x] Rate limiting configured
- [x] TLS certificates auto-renewing (ACME / Let's Encrypt)
- [x] No new CRITICAL exposures

## 7. Glacial Shift

- [x] All 8 glacial criteria assessed — ALL CLEAR (since Wave 137b)
- [x] No regression on previously cleared criteria
- [x] Next glacial goal (Universal Substrate Evolution) tracked
- [ ] SHOW_HN readiness rubric updated
- [x] GLACIAL_SHIFT_READINESS.md trimmed (551→90 lines, history fossilized)

## 8. Compositions / RustScript / External

- [x] footPrint LIVE at `primals.eco/footprint/` — client operational
- [ ] tideGlass — Phase 0 not started (Gonzales NF)
- [x] Drawbridge weak bond registrations current (songBird 16 bonds)
- [x] RustScript absorption path documented (gen5/RUSTSCRIPT_LAST_MILE.md)
- [x] protoKarya projects registered in manifest (Wave 140a — footPrint + tideGlass)
- [ ] JupyterHub / ABG access — RustDesk transient to ironGate
- [x] Composition routing standard applied
- [ ] primalSpring E2E scenarios for protoKarya compositions (5 identified gaps)

## 9. Documentation / Fossil Record

- [x] Blurb reflects current wave scope and status (Wave 143a)
- [x] Stale handoffs fossilized (21 handoffs → fossilRecord/wave143a_dimensional_review/)
- [x] whitePaper gen5/ current with architectural state
- [x] wateringHole document count stable (36→15 handoffs, 7→2 impulses)
- [x] GLACIAL_SHIFT_READINESS.md last-updated date current (trimmed Wave 143a)

## 10. Cascade Pipeline / Convergence

- [x] `membrane temporal.cascade` runs without hanging
- [x] All repo remotes converged (38/39 synced — wateringHole diverge resolved)
- [ ] sporeGate-direct push mechanism — shallow/non-ff rejected (workaround: forgejo)
- [x] No cyclic divergence in freshness records (Wave 138c — tree hashes)
- [x] Forgejo mirrors operational (bidirectional repos functional)

## 11. Content-Addressed Convergence (CAC — Newton-Leibniz Pattern)

- [x] Git repos: tree hashes in freshness.toml (Wave 138c)
- [x] Depot binaries: BLAKE3 diff in depot_sync --push (Wave 139e)
- [x] Heads metadata: TreeParity for auto-publish (cellMembrane Wave 143b — tree hashes in publish_gate_heads)
- [x] Impulses: content-hash deduplication (cellMembrane f4da0ae, Wave 141b)
- [x] rhizoCrypt: SessionTreeHash primitive SHIPPED (Wave 143b — ce3d534, full RPC wire)
- [x] Cascade divergence: tree-parity before policy dispatch (cellMembrane Wave 143b — try_local_tree_parity)
- [ ] primalSpring: content-addressed-convergence scenario (FRAGO issued 140a)
- [x] Pattern formalized in whitePaper/gen5/foundations/ (Wave 140a)
- **ALL 6 IMPLEMENTATION LAYERS SOLVED (Wave 144a)**

## 12. Architecture / OS Parity (Silicon Atheism)

### Depot Architectures (must compile ALL primals)

- [ ] x86_64-unknown-linux-musl — 14/14 primals (reference architecture)
- [ ] aarch64-unknown-linux-musl — 14/14 primals (Pixel, ARM gates)
- [ ] aarch64-linux-android — 14/14 primals (grapheneGate, mobile)
- [ ] x86_64-pc-windows-gnu — 14/14 primals (northGate, Windows mesh)

### Validated Exotic (songBird proven — expand to all primals as adoption completes)

- [ ] riscv64gc-unknown-linux-gnu — open silicon (StarFive, SiFive). P2 depot candidate
- [ ] armv7-unknown-linux-gnueabihf — RPi/IoT/embedded. P2 depot candidate
- [ ] arm-unknown-linux-gnueabihf — RPi Zero, industrial PLCs
- [ ] i686-unknown-linux-gnu — legacy 32-bit desktops, thin clients
- [ ] powerpc64le-unknown-linux-gnu — IBM POWER9/10 HPC, AI servers
- [ ] powerpc64-unknown-linux-gnu — IBM POWER classic, PS3 Linux
- [ ] s390x-unknown-linux-gnu — IBM Z mainframes (banks, airlines)
- [ ] sparc64-unknown-linux-gnu — Sun/Oracle SPARC T-series

### Blocked / Pending

- [ ] powerpc-unknown-linux-gnu — 32-bit PPC (AtomicU64). Fix: tokio portable-atomic feature
- [ ] wasm32-wasip2 — browser + edge computing. Untested but Rust target exists
- [ ] aarch64-unknown-fuchsia — Google capability-based OS
- [ ] x86_64-unknown-freebsd — BSD servers (Netflix CDN)
- [ ] riscv64gc-unknown-none-elf — bare metal RISC-V (no OS)
- [ ] loongarch64-unknown-linux-gnu — Chinese MIPS successor (Loongson)

### Phase 1: Cross-Compile Adoption (COMPLETE — Wave 142a)

- [x] 14/14 primals compile for all 4 depot architectures
- [x] `#[cfg(target_os)]` gating applied where needed (Phase 1)
- [x] portable-atomic feature shipped by cellMembrane
- [ ] primalSpring: `full-cross-compile` scenario (all primals, all depot architectures)
- [ ] primalSpring: `depot-architecture-coverage` scenario (track expansion)

### Phase 2: Abstraction Over Gating (ACTIVE — Wave 142a+)

**Principle**: Don't exclude systems via `#[cfg]` — abstract them to universal
trait interfaces. Every platform is a first-class evolution substrate.

**Reference implementation**: petalTongue `petal-tongue-platform` (`1af1a98`)

**Shipping primals (Wave 143a)**:
- songBird: `IpcStream` platform abstraction (`12099d84`)
- petalTongue: Phase 2 metrics trait + Android paths + WS bridge (`337e1d0`)
- skunkBat: `TransportEndpoint` adoption
- toadStool: glowplug `WgpuGpuDiscovery` Vulkan backend (S332)

- [ ] Each primal audits `#[cfg()]` boundaries → identify abstraction candidates
- [x] Transport: `TransportEndpoint` trait — 10/14 SHIPPED (songBird, skunkBat, sweetGrass, rhizoCrypt, coralReef, loamSpine, barraCuda, petalTongue, toadStool, cellMembrane)
- [x] Device discovery: trait-based — toadStool glowplug Vulkan backend (S332)
- [ ] Health monitoring: trait-based (not procfs-hardcoded)
- [ ] Credential store: trait-based (fs/Keystore/DPAPI backends)
- [x] Platform lifecycle: trait-based — petalTongue `PlatformLifecycle` trait shipped
- [ ] No `#[cfg()]` block exceeds 50 lines without extraction to trait + backend module
- [ ] Each `#[cfg()]` gated module has a corresponding platform backend (not empty stub)
- [ ] New architectures assessed at each wave boundary

### Code Divergence Tracking (constrained evolution)

`#[cfg()]` boundaries are constrained evolution targets — sites where the
ecosystem adapts to hardware reality. In Phase 2, these evolve from exclusion
fences into trait backend selections:

```
Phase 1: #[cfg(unix)] mod uds;          // excluded on Windows
Phase 2: impl Transport for Uds { ... } // one backend among many
```

- [ ] `#[cfg()]` divergences documented per primal (what → which trait)
- [ ] Platform-specific backends have paired tests on each platform
- [ ] Fallback paths exist (TCP fallback for transport, stub for missing HW)
- [ ] Console/embedded targets assessed when hardware acquired

### Subsystem Convergence

- [ ] Transport: `primal-transport` crate published (UDS/NamedPipe/TCP dispatch)
- [ ] Lifecycle: `ProcessManager` adopted by all signal-using primals
- [ ] Discovery: `Platform::socket_dir()`, `Platform::config_dir()`, `Platform::bin_dir()`
- [ ] Data backends: storage access via transport layer (not raw UDS)
- [ ] Credential store: platform-aware (Keyring/Keychain/DPAPI)

---

*Last used*: Wave 143a (Jul 16, 2026)
*Created*: Wave 139a
