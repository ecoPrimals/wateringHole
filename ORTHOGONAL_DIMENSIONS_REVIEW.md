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

- [ ] Depot authority identified and operational (sporeGate)
- [ ] ecoBins built as musl-static stripped (post-primordial standard)
- [ ] `checksums.toml` / `signatures.toml` current
- [ ] `require-signed` enforced system-wide
- [ ] SIGN-VERIFY-ON-FETCH operational in cellMembrane
- [ ] All target architectures built (x86_64, aarch64 at minimum)
- [ ] Depot layout consistent across depot authority and relay mirrors
- [ ] `plasmid.harvest` → `plasmid.fetch` pipeline tested end-to-end

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
- [ ] protoKarya projects registered in manifest
- [ ] JupyterHub / ABG access operational
- [ ] Composition routing standard applied

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
- [ ] No cyclic divergence in freshness records
- [ ] Forgejo mirrors operational (bidirectional repos functional)

---

*Last used*: Wave 139c (Jul 15, 2026)
*Created*: Wave 139a
