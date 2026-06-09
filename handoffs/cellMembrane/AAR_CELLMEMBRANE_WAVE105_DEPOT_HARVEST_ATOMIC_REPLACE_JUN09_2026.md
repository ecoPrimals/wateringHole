# AAR: plasmid.harvest "Text File Busy" Failure + Remaining cellMembrane Work

**Date**: 2026-06-09 (Wave 105)
**From**: eastGate overwatch
**To**: cellMembrane
**Priority**: P2 (depot harvest reliability), P1 (WAN depot now SHIPPED — validate deployment)

---

## AAR: `membrane plasmid.harvest` Exit Code 1

### Incident

During Wave 104 revalidation, `membrane plasmid.harvest beardog` and
`membrane plasmid.harvest biomeos` both exited with code 1. Both ran for
~9.5 minutes before failing.

### Root Cause

The harvest attempts to overwrite a depot binary that is currently running
as a NUCLEUS primal process. Linux returns `ETXTBSY` ("Text file busy")
when writing to an executable that is mapped into a running process. The
harvest command does not stop the target primal before overwriting, nor does
it use atomic rename (write to temp → rename over original).

### Impact

Operator must manually: stop primal → copy binary → strip → restart primal
→ update checksum. This was done successfully for both bearDog and biomeOS,
but it should be zero-touch.

### Recommendation

**Option A (quick, recommended)**: Atomic rename in harvest — write to
`primals/<triple>/<name>.new`, then `rename(2)` over the original. `rename`
is atomic on the same filesystem and succeeds even when the original is
running. The running process keeps its old fd; next restart picks up the
new binary.

**Option B (thorough)**: Stop-before-harvest — harvest sends
`lifecycle.shutdown` (JSON-RPC) or `SIGTERM` to the running primal, waits
for exit, writes the binary, restarts. More correct but adds complexity and
downtime.

**Option C (hybrid)**: Try direct write; on `ETXTBSY`, fall back to atomic
rename. Log a warning that restart is needed to pick up the new binary.

### Evidence

| Primal | Old Size | New Size | Reason |
|--------|----------|----------|--------|
| bearDog | 12,878,064 | 11,243,648 | Wave 145 pure Rust crypto (aws-lc-rs eliminated) |
| biomeOS | 16,660,352 | 15,930,616 | v4.16 deep debt (error chains, hardcoding elim) |

Both binaries were manually rebuilt, deployed, checksum-updated, committed, and pushed.

---

## Status Update: cellMembrane Recent Evolution

cellMembrane has shipped significant work since Wave 103. Acknowledging:

### SHIPPED (Wave 104-105)

1. **WAN depot distribution** (`plasmid.fetch --source wan`) — P1 RESOLVED
   - HTTPS-based binary fetching from outer membrane (Caddy)
   - `caddy.depot.provision` sets up file_server on golgiBody-ext
   - WAN gates no longer need SSH access for depot binaries
   - **This resolves the sole remaining P1 blocker** (flockGate WAN depot)

2. **Cascade conflict auto-resolve** — P2 RESOLVED
   - Auto-discards dirty regenerable metadata (checksums.toml, provenance.toml, freshness.toml) before ff-only pull
   - Eliminates recurring operator intervention on ~every 2nd cascade
   - Exactly matches the recommendation from `wave104-cross-deployment-readiness.toml [aar.cascade_conflicts]`

3. **Cascade depot staleness reporting** — rebuild suggestions in cascade output
4. **Deep debt elimination** — sha2/hmac crates replace hand-rolled, zero `#[allow]`, typed phases
5. **Env var consolidation** — 39 typed `ENV_*` constants, zero custom string literals
6. **depot.rs extraction** — harvest.rs 811→644 lines, clean module boundary

### REMAINING WORK

| ID | Priority | Description | Status |
|----|----------|-------------|--------|
| CM-HARVEST-ATOMIC | P2 | Atomic rename in plasmid.harvest (this AAR) | **ALREADY SHIPPED** (stage_to_depot uses .new + rename(2), refresh SCPs to .new + mv) |
| CM-WAN-VALIDATE | P2 | Validate plasmid.fetch --source wan on flockGate | **DEPLOYED** — validated from ironGate, 13/13 OK over HTTPS. Awaiting flockGate team. |
| CM-AARCH64-SWEEP | P2 | Cross-compile remaining 11/14 primals for aarch64 | **COMPLETE** — 14/14 built, zero C-dep violations, checksums committed |
| CM-SOURDOUGH-SEGV | LOW | `sourdough validate depot` segfaults — investigate | KNOWN |
| CM-CADDY-PROVISION | P2 | Deploy caddy.depot.provision on golgiBody (production) | **DEPLOYED** — `/depot/` route live on membrane.primals.eco |

### Dependency Map

```
CM-WAN-VALIDATE (validate plasmid.fetch on flockGate)
  └→ flockGate NUCLEUS deployment (first WAN gate with binaries)
       └→ WAN covalent mesh validation
            └→ Stadial criterion 4 (remote covalent over WAN)

CM-AARCH64-SWEEP (cross-compile 11 remaining primals)
  └→ grapheneGate bootstrap (Pixel trust anchor)
  └→ ARM VPS deployment
  └→ ecoBin universal portability

CM-HARVEST-ATOMIC (atomic rename in harvest)
  └→ Zero-touch depot refresh across all gates
       └→ Autonomous gate self-healing
```

---

## Ecosystem Snapshot (Wave 105, Jun 9 2026)

- **Mesh**: LIVE (eastGate↔strandGate, 13h+ stable)
- **Transport**: 11/11 non-exempt COMPLETE
- **Depot**: 14/14 x86_64-musl VERIFIED (BLAKE3 checksums confirmed)
- **bearDog**: v0.9.0 Wave 145 pure Rust — depot binary fresh (11.2MB)
- **biomeOS**: v4.16 — depot binary fresh (15.9MB)
- **Cascade**: 38/38 synced, zero failures
- **NUCLEUS**: All JSON-RPC primals alive, tarpc sockets nominal
- **P1 blockers**: **ZERO** (WAN depot SHIPPED by cellMembrane, bearDog RESOLVED Wave 145)
- **Sovereignty**: S1-S3 GRADUATED, S4 gate ending today
