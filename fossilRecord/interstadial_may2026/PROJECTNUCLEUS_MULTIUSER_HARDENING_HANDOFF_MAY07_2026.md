# projectNUCLEUS — Multi-User Hardening, JupyterHub Patterns, and Security Pentest Handoff

**Date**: 2026-05-07
**From**: projectNUCLEUS (ironGate)
**For**: primalSpring, BearDog, biomeOS, NestGate, skunkBat teams, spring teams
**Scope**: Live multi-user security pentest from authenticated JupyterHub session,
4 hardening layers applied, 8 patterns abstracted from JupyterHub deployment,
5 new upstream gaps (1 critical), compute/save separation pattern.

---

## Summary

projectNUCLEUS ran a multi-user security validation from an authenticated
compute-tier user (tamison) via JupyterHub on ironGate. This is the first
pentest from *inside* the composition — testing what an authenticated user
can do, not what an external attacker can do.

**Critical finding**: `NUCLEUS_READONLY=1` was a convention flag with zero
enforcement. Reviewer-tier users could execute arbitrary code on ironGate.
Fixed locally with 4 hardening layers. Abstracted into 8 patterns for
upstream primal evolution.

### Results at a Glance

| Category | Finding | Action |
|----------|---------|--------|
| Primal reachability | 13/13 on localhost | Expected — JH-0 upstream gap |
| Filesystem isolation | 10/10 PASS | Strong — shadow, homes, configs denied |
| NestGate write | ALLOWED without auth | Confirms JH-0 |
| Outbound internet | GitHub, PyPI reachable (IPv4+IPv6) | **FIXED** — iptables owner match |
| Process visibility | All primal PIDs visible | **FIXED** — hidepid=2 |
| Reviewer code exec | Could execute code | **FIXED** — server flags + filesystem |
| Shared notebook save | Compute could overwrite shared | **FIXED** — chmod 444 + per-user results |

---

## Hardening Layers Applied

### Layer 1: Process Isolation (`hidepid=2`)

ABG users can no longer see other users' processes or primal PIDs via `ps aux`.

- Method: `mount -o remount,hidepid=2,gid=0 /proc`
- Persistent: `/etc/fstab` entry
- Effect: tamison sees 4 own processes (previously saw 600+, including 13 primal PIDs with full paths and memory usage)

### Layer 2: Outbound Network Restriction

ABG users cannot reach the internet. Prevents data exfiltration from compromised notebooks.

- Method: iptables + ip6tables owner match DROP for UID 1001-1099
- Preserved: localhost (127.0.0.0/8), LAN (RFC1918), DNS (port 53)
- Persistent: systemd `restore-iptables.service`
- IPv6 was the initial leak — iptables alone insufficient

### Layer 3: Reviewer/Observer Read-Only Enforcement

No code execution, no terminal access, no file creation.

- JupyterLab server flags: `--ServerApp.terminals_enabled=False`, `--KernelSpecManager.allowed_kernelspecs=set()`
- Filesystem: `chmod 550` root-owned notebook directory
- Applied via `pre_spawn_hook` and `enforce_readonly_notebook_dir()` in `jupyterhub_config.py`

### Layer 4: Shared Notebook Immutability

Shared notebooks are templates — run but don't save.

- Notebooks: `chmod 444` (irongate-owned)
- Commons directory: `chmod 2755` (irongate-owned, not group-writable)
- Per-user results: `~/notebooks/results/` (user-owned, writable)
- Pattern: "Save As" to personal space, shared originals immutable

---

## 8 Patterns Abstracted

See `projectNUCLEUS/validation/JUPYTERHUB_PATTERNS_HANDBACK.md` for full analysis.

| Pattern | Lesson | Current Mechanism | Sovereign Replacement |
|---------|--------|-------------------|----------------------|
| 0 (Critical) | Convention flags are not security | `NUCLEUS_READONLY` env var | RPC dispatcher capability check |
| 1 | Identity is a system primitive | PAM + Linux groups | BearDog identity + ionic tokens |
| 2 | Resource scoping needs composition awareness | `pre_spawn_hook` Python | Token-carried resource envelope |
| 3 | Shared workspace is content-addressed | Filesystem symlinks | NestGate named collections |
| 4 | Trust boundaries need cryptographic origin | CF header inspection | BTSP connection origin signal |
| 5 | Process lifecycle needs hot-reload | `systemctl restart` | biomeOS `composition.reload` |
| 6 | Credential distribution needs UX | `echo 'pass' \| chpasswd` | BearDog token issuance |
| 7 | Observability needs unified event surface | `journalctl` per-service | skunkBat log aggregation |

---

## 5 New Upstream Gaps

| Gap | Severity | Owner | Blocks | Detail |
|-----|----------|-------|--------|--------|
| JH-0 | **Critical** | All primal teams | Secure multi-user compositions | Every primal's RPC dispatcher must check capability tokens before executing methods. Currently, any localhost process can call any method on any primal. |
| JH-1 | High | BearDog | Step 2b (BTSP auth) | `identity.create`, `auth.issue_ionic`, `auth.verify_ionic` needed. PAM case-sensitivity bugs prove identity must be primal-native. |
| JH-2 | High | biomeOS + ToadStool | neuralAPI enforcement | Ionic tokens need resource envelope fields (mem, cpu, method allowlist) that spawners enforce. |
| JH-3 | Medium | biomeOS | Rolling updates | `composition.reload` for swapping a single primal without full composition restart. |
| JH-4 | Medium | BearDog + primalSpring | User onboarding | Token delivery mechanism for non-technical researchers. |
| JH-5 | Medium | skunkBat | Security monitoring | Log aggregation across heterogeneous sources (systemd, primal logs, tunnel) with provenance pipeline feed. |

### New Data Streams for skunkBat

The pentest revealed specific events skunkBat should monitor:

- JupyterHub auth events (success, failure, blocked) from systemd journal
- NestGate storage writes with caller context (who wrote what)
- Outbound connection attempts that hit iptables DROP rules
- Process enumeration attempts (if hidepid can be bypassed)
- File creation attempts in read-only directories

---

## Dual-Port Architecture Clarification

The pentest initially flagged sweetGrass as "accepting plaintext" (BTSP failure).
This is actually correct dual-port behavior:

| Primal | IPC Port (plaintext JSON-RPC) | BTSP Port (encrypted) |
|--------|-------------------------------|----------------------|
| sweetGrass | 9850 | 9851 |
| rhizoCrypt | 9602 | 9601 |

IPC ports are for primal-to-primal localhost communication. The gap is that
they accept calls from *any* localhost process (JH-0), not just other primals.

---

## Binding Exposure (5 primals on 0.0.0.0)

| Primal | Port | Bind | Mitigated By |
|--------|------|------|-------------|
| skunkBat | 9140 | 0.0.0.0 | UFW |
| ToadStool | 9400 | 0.0.0.0 | UFW |
| petalTongue | 9900 | 0.0.0.0 | UFW |
| biomeOS | 9800 | 0.0.0.0 | UFW |
| sweetGrass | 9850 | 0.0.0.0 | UFW |

These bind to `0.0.0.0` at the application level but are blocked from WAN
by UFW. They should be rebound to `127.0.0.1` via `--bind` flags when the
deploy.sh composition is updated.

---

## Composition Patterns for Downstream Absorption

### JupyterHub as Pattern Validator

JupyterHub is the first real multi-user service on NUCLEUS. Every
friction point reveals what primals must internalize:

- **PAM → BearDog identity**: calibrates the auth model
- **`pre_spawn_hook` → neuralAPI**: calibrates resource scoping
- **Symlinks → NestGate collections**: calibrates content-addressed sharing
- **CF headers → BTSP origin**: calibrates trust boundary signals
- **systemd → biomeOS lifecycle**: calibrates hot-reload

Each calibration produces metrics that the sovereign replacement must match.

### Compute/Save Separation Pattern

Shared notebooks are read-only templates. Users execute them (outputs in
browser memory) and "Save As" to their own results directory. This maps to:

- NestGate: shared collections are read-only for compute-tier tokens
- Per-user results: personal NestGate collections with write access
- Provenance: every run creates a sweetGrass braid linking user, inputs, outputs

### Security-First Deployment Checklist

For any new multi-user service on NUCLEUS:

1. Disable all execution capabilities for read-only tiers (application level)
2. Enforce with filesystem permissions (OS level)
3. Block outbound network for user processes (iptables)
4. Hide process info from non-root users (hidepid)
5. Make shared content immutable (chmod)
6. Provide per-user writable space for outputs
7. Never trust environment variable conventions for access control

---

## Documents Updated

| Document | Change |
|----------|--------|
| `projectNUCLEUS/README.md` | Added hardening layers, JH-0 gap, updated dependency count |
| `projectNUCLEUS/PHASES.md` | Added multi-user pentest results, reviewer lockdown detail |
| `projectNUCLEUS/validation/SECURITY_HANDBACK_MAY06_2026.md` | Added Phase 2a multi-user pentest section |
| `projectNUCLEUS/validation/JUPYTERHUB_PATTERNS_HANDBACK.md` | New: 8 patterns, 5 gaps |
| `projectNUCLEUS/specs/TUNNEL_EVOLUTION.md` | Step 2b updated with JH-0/JH-1/JH-4 prerequisites |
| `projectNUCLEUS/specs/COMPLETE_DEPENDENCY_INVENTORY.md` | Added Cluster 7 (internal primal gaps) |
| `whitePaper/gen3/baseCamp/README.md` | Added multi-user hardening paragraph |

---

## Recommended Next Steps

### For primalSpring
- Codify "enforcement at the gate" as ecosystem standard (JH-0)
- Review all primals for convention-based access control lacking enforcement
- Add RPC dispatcher capability check pattern to wateringHole standards

### For BearDog Team
- Implement `identity.create`, `auth.issue_ionic`, `auth.verify_ionic` (JH-1)
- Define the caller-identity-in-RPC-dispatch pattern all primals will adopt (JH-0)
- Design token delivery UX for non-technical users (JH-4)

### For biomeOS Team
- Add token-carried resource envelope to neuralAPI (JH-2)
- Implement `composition.reload` for per-primal hot-swap (JH-3)

### For skunkBat Team
- Wire log aggregation across systemd journal + primal logs + tunnel (JH-5)
- Monitor the new data streams identified in this pentest

### For NestGate Team
- Cross-reference NG-2 (collections) — validated as real deployment need by Pattern 3

### For All Primal Teams
- Rebind the 5 remaining `0.0.0.0` primals to `127.0.0.1` via `--bind` flag
- Prepare for RPC dispatcher capability check integration (JH-0)
