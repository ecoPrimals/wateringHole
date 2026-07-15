# Orthogonal Dimensions Review — Reusable Checklist

**Purpose**: Systematic reassessment checklist for overwatch cascade reviews.
Use at wave boundaries or whenever a comprehensive posture check is needed.

---

## 1. Temporal

- [ ] `wave.toml` reflects current wave ID, sub, and posture
- [ ] Gate heads published (`heads/*.toml`) — all active gates have recent timestamps
- [ ] `freshness.toml` uses tree hashes (DAG, not cyclic graph)
- [ ] Active impulses triaged — stale impulses fossilized
- [ ] No stale diverge impulses older than 2 waves

## 2. Ecological (Primal Health)

- [ ] All primals compile (`cargo check` / `cargo test` green)
- [ ] Zero P1 blockers in any primal
- [ ] All primal repos converged across remotes (ahead=0, behind=0)
- [ ] Transport injection adopted across all non-exempt primals
- [ ] Neural API methods shipped by all primal teams
- [ ] Test counts stable or increasing (no regression)

## 3. Hardware / Topology

- [ ] `HARDWARE_INVENTORY.md` reflects current physical state
- [ ] All online gates reachable (SSH, mesh, or WireGuard)
- [ ] Gate roles match manifest `[topology]` section
- [ ] Network backbone operational (CRS310, MikroTik, switches)
- [ ] Pending hardware actions documented (westGate power-on, etc.)
- [ ] SoloKey / HSM / StrongBox status current

## 4. Sovereignty / Membranes

- [ ] K-Derm three-layer model intact (external outer → sovereign outer → inner)
- [ ] Cloudflare outer membrane operational (wildcard DNS, DDoS protection)
- [ ] Sovereign outer membrane operational (Caddy TLS, bearDog ACME)
- [ ] Inner membrane zero-commercial (primal.eco data path)
- [ ] S1-S4 sovereignty shadows all graduated
- [ ] DNSSEC enabled on sovereign domains
- [ ] Cross-membrane validation scenario operational

## 5. Depot / Build Pipeline

- [ ] Depot authority identified and operational (sporeGate — 13-target build authority)
- [ ] ecoBins built as musl-static stripped (post-primordial standard)
- [ ] `checksums.toml` / `signatures.toml` current
- [ ] `require-signed` enforced system-wide
- [ ] SIGN-VERIFY-ON-FETCH operational in cellMembrane
- [ ] All 4 depot architectures built for all 14 primals (see Dimension 12 for matrix)
- [ ] Exotic architectures expanded to depot as primal adoption completes
- [ ] Depot layout consistent across depot authority and relay mirrors
- [ ] `plasmid.harvest` → `plasmid.fetch` pipeline tested end-to-end
- [ ] `depot_sync --push` operational (builder → VPS)

## 6. Website / Public Surface / Security

- [ ] `primals.eco` returning 200 (sporePrint)
- [ ] `primals.eco/footprint/` returning 200 (GIS composition)
- [ ] `live.primals.eco` returning 200 (petalTongue dashboard)
- [ ] Security headers deployed (HSTS, CSP, X-Frame-Options, X-Content-Type)
- [ ] fail2ban active on SSH endpoints
- [ ] Rate limiting configured
- [ ] TLS certificates auto-renewing (ACME / Let's Encrypt)
- [ ] No new CRITICAL exposures

## 7. Glacial Shift

- [ ] All 8 glacial criteria assessed (document status in GLACIAL_SHIFT_READINESS.md)
- [ ] No regression on previously cleared criteria
- [ ] Next glacial goal (Universal Substrate Evolution) tracked
- [ ] SHOW_HN readiness rubric updated

## 8. Compositions / RustScript / External

- [ ] Live compositions operational (footPrint, tideGlass status)
- [ ] Drawbridge weak bond registrations current
- [ ] RustScript absorption path documented
- [x] protoKarya projects registered in manifest (Wave 140a — footPrint + tideGlass)
- [ ] JupyterHub / ABG access operational
- [ ] Composition routing standard applied
- [ ] primalSpring E2E scenarios for protoKarya compositions (5 identified gaps)

## 9. Documentation / Fossil Record

- [ ] Blurb reflects current wave scope and status
- [ ] Stale handoffs fossilized
- [ ] whitePaper gen5/ current with architectural state
- [ ] wateringHole document count stable (no unbounded growth)
- [ ] GLACIAL_SHIFT_READINESS.md last-updated date current

## 10. Cascade Pipeline / Convergence

- [ ] `membrane temporal.cascade` runs without hanging
- [ ] All repo remotes converged (zero ahead/behind)
- [ ] sporeGate-direct push mechanism functional (or documented workaround)
- [x] No cyclic divergence in freshness records (Wave 138c — tree hashes)
- [ ] Forgejo mirrors operational (bidirectional repos functional)

## 11. Content-Addressed Convergence (CAC — Newton-Leibniz Pattern)

- [x] Git repos: tree hashes in freshness.toml (Wave 138c)
- [x] Depot binaries: BLAKE3 diff in depot_sync --push (Wave 139e)
- [ ] Heads metadata: TreeParity for auto-publish conflicts (FRAGO issued 140a)
- [ ] Impulses: content-hash deduplication (FRAGO issued 140a)
- [ ] rhizoCrypt: SessionTreeHash primitive (FRAGO issued 140a)
- [ ] Cascade divergence: tree-parity before agentic policy dispatch (FRAGO issued 140a)
- [ ] primalSpring: content-addressed-convergence scenario (FRAGO issued 140a)
- [x] Pattern formalized in whitePaper/gen5/foundations/ (Wave 140a)

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

### Per-Primal Cross-Compile Adoption

- [ ] Transport abstraction adopted: _/14 primals use `TransportEndpoint` (not raw UDS)
- [ ] Signal abstraction adopted: _/3 affected primals use `ProcessManager`
- [ ] FS abstraction adopted: _/3 affected primals use `Platform::detect()`
- [ ] toadStool hw-safe feature-gated behind `linux-hw`
- [ ] petalTongue Android target is cdylib (not binary)
- [ ] portable-atomic feature enabled in all workspace Cargo.toml
- [ ] primalSpring: `full-cross-compile` scenario (all primals, all depot architectures)
- [ ] primalSpring: `depot-architecture-coverage` scenario (track expansion)

### Code Divergence Tracking (constrained evolution)

`#[cfg()]` boundaries are not technical debt — they are constrained evolution
targets. Each platform-specific code path is a site where the ecosystem
adapts to hardware reality. Track them:

- [ ] `#[cfg(unix)]` / `#[cfg(windows)]` divergences documented per primal
- [ ] Platform-specific code paths have paired tests on both sides
- [ ] No `#[cfg()]` block exceeds 50 lines without extraction to platform module
- [ ] Fallback paths exist for all `#[cfg()]` branches (no dead-end compile)
- [ ] New architectures assessed at each wave boundary (RISC-V board availability, etc.)
- [ ] Console/embedded targets assessed when hardware acquired

### Subsystem Convergence

- [ ] Transport: `primal-transport` crate published (UDS/NamedPipe/TCP dispatch)
- [ ] Lifecycle: `ProcessManager` adopted by all signal-using primals
- [ ] Discovery: `Platform::socket_dir()`, `Platform::config_dir()`, `Platform::bin_dir()`
- [ ] Data backends: storage access via transport layer (not raw UDS)
- [ ] Credential store: platform-aware (Keyring/Keychain/DPAPI)

---

*Last used*: Wave 141a (Jul 15, 2026)
*Created*: Wave 139a
