# Ecosystem Tools: Deep Debt Resolution + Public Readiness Sprint

**Date:** April 5, 2026
**Scope:** bingoCube, benchScale, agentReagents, rustChip
**Result:** All 4 tools at Grade A. bingoCube, benchScale, agentReagents cleared for public.

---

## Sprint Summary

Seven-phase sprint executing deep debt resolution and public readiness across all
ecosystem tools. Started from: bingoCube (A), benchScale (B), agentReagents (B),
rustChip (B). Ended with all four at Grade A.

## Phase Results

### Phase 1 — Public-Readiness Scrub
- **bingoCube**: Deleted internal docs (REPO_EXTRACTION_PLAN.md, AUDIO_DEPENDENCY_EVOLUTION_NOTE.md), scrubbed /home/ paths, fixed AGPL wording, made petalTongue animation path dep optional, fixed whitePaper license and broken links
- **benchScale**: Aligned README license to -or-later, scrubbed archive paths, migrated 7 #[allow( to #[expect(, fixed 2 stale SPDX headers
- **agentReagents**: Documented benchScale path dep with sibling clone workflow, aligned license, scrubbed archive paths, migrated 9+ #[allow(, added security note for template passwords

### Phase 2 — Test Coverage (60% gate)
| Tool | Before | After | Tests |
|------|--------|-------|-------|
| bingoCube | 62.6% | 83.4% | 73 |
| benchScale | 35.5% | 61.9% | 343 |
| agentReagents | 7.1% | 60.2% | 89 |
| rustChip | 0% | 60.8% | 237 |

tarpaulin.toml with fail-under=60.0 added to all 4 repos.

### Phase 3 — Unsafe Code Evolution
- **benchScale**: EnvGuard RAII for env var tests, LeaseList safe FFI abstraction for libvirt DHCP leases, libc::kill replaced with nix::sys::signal::kill
- **rustChip**: 31 unsafe blocks documented with // SAFETY: comments, deny(unsafe_op_in_unsafe_fn) enforced workspace-wide

### Phase 4 — Large File Refactoring
- **bingoCube**: shell.rs (995) → shell.rs (789) + snapshot.rs (147) + evolve.rs (112)
- **benchScale**: vm_lifecycle → vm_state (83), pipeline → stages (731), config_legacy → config/legacy
- **rustChip**: vfio/mod → ioctls (273) + container (116), hybrid/mod → software (79)

### Phase 5 — Dependency Modernization
- benchScale: thiserror 1.0 → 2.0, nix 0.29 added
- C deps (virt/libvirt, sqlite3/sqlx, libc for VFIO) documented in deny.toml across all tools

### Phase 6 — Hardcoding and Mock Evolution
- **agentReagents**: Hardcoded Songbird registration → capability-based RegistrationSettings (REGISTRY_SOCKET env var)
- **rustChip**: create_stub_model → create_reference_model, SoftSystemBackend → SoftwareBackend, cross-primal doc refs marked as ecosystem context
- **benchScale**: Libvirt feature-gate documented as intentional compile-time gating

### Phase 7 — Root Docs Cleanup (April 5)
- All 4 repos: README/CONTEXT/CHANGELOG updated, versions bumped, archive READMEs added, debris moved to docs/, stale scripts documented
- bingoCube: 0.1.0 → 0.1.1, benchScale: 3.0.0 → 3.1.0, agentReagents: 0.1.0 → 0.2.0, rustChip: CONTEXT.md fully rewritten
- rustChip: DEPRECATED.md, PR_DESCRIPTION.md, BEYOND_SDK.md moved from root to docs/
- Zero TODO/FIXME/HACK in production code across all 4 repos

### rustChip Grade A Sprint (April 5)
- 828 clippy warnings → 0 (workspace cast allows for numeric code, comprehensive source fixes)
- 0 → 237 test functions across 5 crates
- 60.8% coverage (hardware VFIO/mmap excluded via tarpaulin.toml)
- missing_docs: 0 warnings

---

## Public-Ready Status

| Tool | Grade | Coverage | Public-Ready | Blockers |
|------|-------|----------|-------------|----------|
| bingoCube | A | 83.4% | Yes | None |
| benchScale | A | 61.9% | Yes | None |
| agentReagents | A | 60.2% | Yes | Requires benchScale sibling checkout |
| rustChip | A | 60.8% | Pending | Org decision (syntheticChemistry) |

---

## Remaining Roadmap (Not Sprint Scope)

- Coverage: push all repos toward 90% target (current: 60-83%)
- benchScale: missing_docs warnings (22K lines — gradual doc effort)
- agentReagents: missing_docs, path dep on benchScale (consider git dep when public)
- rustChip: akida-driver unsafe (VFIO/DMA) is inherent; documented
- Primal ecosystem: 14 primals tracked separately in PRIMAL_GAPS.md

---

## Compliance Matrix

See `ECOSYSTEM_COMPLIANCE_MATRIX.md` v2.1.0 for full tier-by-tier breakdowns.
