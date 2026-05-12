<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->

# biomeOS v2.91 — Deep Debt: Large File Refactoring + Targeted Coverage + Dep Audit

**Date**: April 6, 2026
**From**: biomeOS → primalSpring, all teams
**Status**: PRODUCTION READY — Zero blocking debt

## Summary
Continued deep debt resolution: 4 large production files refactored below 500 LOC, 27 new targeted tests, full transitive dependency audit.

## Version History
| Version | Change |
|---------|--------|
| v2.91 | 4 large file refactors, 27 new tests, dep audit |
| v2.90 | Neural API semantic routing, provenance trio translations, composition health |

## Large File Refactoring (v2.91)
| File | Before | After | Tests File |
|------|--------|-------|------------|
| topology.rs (biomeos-api) | 869 | 433 | topology_tests.rs |
| rendezvous.rs (biomeos-api) | 862 | 321 | rendezvous_tests.rs |
| verify.rs (biomeos-cli) | 859 | 500 | verify_tests.rs |
| orchestrator.rs (biomeos-atomic-deploy) | 855 | 427 | orchestrator_tests.rs |

## New Test Coverage (v2.91)
- storage_tests.rs (+6): VolumeType variants, VolumeProjection, VolumeSpec round-trip
- networking_services_tests.rs (+6): MeshEgressSpec, VirtualService redirect/rewrite, GatewaySpec, TrafficPolicy
- topology_tests.rs (+4): proprioception degraded, connections, primals, motor coordination
- capability_tests.rs (+4): providers, discover, register_route, route+metrics
- lifecycle_tests.rs (+7, new): status, shutdown_all, resurrect/apoptosis, register+get

## Dependency Audit (v2.91)
All 25 duplicate dependency roots are transitive:
- thiserror v1 ← rtnetlink, tungstenite (we use v2)
- rand v0.8 ← tarpc, tungstenite (we use v0.9)
- itertools v0.10 ← criterion dev-dep (we use v0.12)
- linux-raw-sys, rustix, socket2, cpufeatures, hashbrown, getrandom — async/tokio ecosystem splits

## Quality Gates
- 7,638 tests (0 failures, 0 ignored, fully concurrent)
- clippy PASS, fmt PASS
- Zero unsafe, zero TODO/FIXME, zero deprecated APIs
- 90%+ coverage maintained
- Edition 2024, rust-version 1.87

---

*© 2025–2026 ecoPrimals — AGPL-3.0-or-later / CC-BY-SA-4.0 / ORC*
