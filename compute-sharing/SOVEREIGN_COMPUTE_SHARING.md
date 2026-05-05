# Sovereign Compute Sharing — The "Lend a GPU to a Friend" Pattern

**Version**: 0.2.0
**Date**: May 2026
**Audience**: Any primal team, any operator with hardware to share
**Status**: Guidance — Phase 0 active, Phase 1 validated (Nest Atomic + provenance pipeline)

---

## The Pattern

Anyone with a GPU should be able to lend compute to a friend. That's it.

The friend sends data and a workload. The operator runs it on local hardware.
The friend gets results. The operator gets real-world pressure on their tools.
Over time, the manual process evolves into an automated, encrypted, composable
platform — but it starts with a human running a job for another human.

This document describes the pattern, not a specific deployment. Any machine,
any friend, any domain. ABG (Accelerated Bioinformatics Group) is the first
instance. The architecture is machine-agnostic.

---

## Physical Topology

The ecoPrimals cluster is physically co-located — ~11 machines in a basement
connected by Cat6e ethernet with a 10G backbone switch. This is a covalent
LAN, not a distributed mesh. Every gate can reach every other gate at wire
speed.

This matters for compute sharing because the **intake node** and the
**workload node** don't have to be the same machine.

### The NUC Intake Pattern

```
Internet → [NAT/Tunnel] → NUC (intake) → Cat6e LAN → workload gate
```

An Intel NUC (or similar expendable node) sits at the network edge as the
external-facing intake. It runs the tunnel endpoint and JupyterHub proxy.
The NUC has no valuable data — it's a sacrificial relay. If compromised,
wipe and rebuild.

Actual compute happens on internal gates (strandGate for bioinformatics,
biomeGate for HBM2 work, etc.). The NUC routes requests over the LAN to
whichever gate owns the workload.

This is a **covalent bonding challenge** for the NUCLEUS model. The NUC
and the workload gate must trust each other (genetic trust via bearDog)
and coordinate (biomeOS routing). Early phases use manual coordination;
later phases use the full covalent mesh.

| Component | Role | Example |
|-----------|------|---------|
| **Intake node** | Tunnel endpoint, reverse proxy, expendable | Intel NUC, NucBox M6 |
| **Workload gate** | Runs JupyterHub kernels, GPU compute | strandGate, biomeGate, southGate |
| **Cold storage** | Results archival, ZFS snapshots | westGate (76 TB) |

Long-term, biomeOS deploy graphs handle the intake → workload → storage
routing automatically. Short-term, the operator manually starts JupyterHub
on the right gate and the NUC is just a tunnel relay.

### sporePrint Deployment Evolution

The public site (primals.eco) and the compute platform share a convergent
path:

```
Now:     GitHub Pages + Cloudflare  →  static Zola site
Next:    + secure tunnel            →  JupyterHub for compute users
Then:    + petalTongue web          →  dynamic site + compute dashboard
Later:   + songBird NAT traversal   →  self-hosted, Cloudflare optional
Finally: + full BTSP                →  BTSP-only tunnel, zero externals
```

Each step eliminates an external dependency. The end state is a sovereign
site served over BTSP with no reliance on GitHub, Cloudflare, or any
third-party tunnel provider. We get there in cycles — each cycle is
validated by real users generating real pressure.

---

## Security Model: Assume Insecure, Evolve to BTSP

```
Phase 0: Manual         — "I know you from Discord"
Phase 1: Tunnel + Auth  — "I can see you're who you say you are"
Phase 2: BTSP Auth      — "bearDog cryptographically verifies your identity"
Phase 3: BTSP Transport — "ChaCha20-Poly1305 encrypts the session"
Phase 4: Full BTSP      — "Policy automation, agentic workloads"
```

### The Principle

**Start by assuming we are insecure.** No automation. Human approves every
action. This is honest and safe.

BTSP (BearDog Trust Security Protocol) progressively replaces human trust
with cryptographic trust. Each phase produces real security validation data
for bearDog and songBird. The security evolution IS the product — not a
prerequisite for shipping.

### Phase-by-Phase Security

| Phase | Trust Model | Automation | Recovery |
|-------|------------|------------|----------|
| 0 | Social ("I know you") | None — human runs everything | N/A |
| 1 | Tunnel + simple auth | None — human monitors | Pull the plug |
| 2 | BTSP Phase 2 (cryptographic identity) | Manual approval, crypto identity | Revoke key |
| 3 | BTSP Phase 3 (encrypted transport) | Partial — channel is AEAD-protected | Session invalidation |
| 4 | Full BTSP (policy + agentic) | Full — policy-based | Automated isolation |

**BTSP Phase 3 is already shipped.** As of May 2, 2026, all 13 primals
support `btsp.negotiate` → ChaCha20-Poly1305 AEAD with HKDF-SHA256
directional session keys. The cryptographic infrastructure exists. The
question is when external-facing use cases catch up to it.

---

## Evolution Phases

### Phase 0: Manual (Current)

The operator runs jobs on behalf of friends. Communication via Discord or
whatever channel exists. Data transferred via file sharing. Results returned
the same way.

**What this tests**: Nothing architectural. But it generates the first real
external workloads and builds human trust.

**Operator gets**: Real-world data for their validation pipelines. Every
standard-tool result (QIIME2, DESeq2, AlphaFold, Scanpy) becomes a
validation target for Rust reimplementations. The pattern:
published results → standard tools → Rust → primal compositions.

**Friend gets**: Free compute on hardware that outperforms cloud notebooks.

### Phase 1: JupyterHub on Any Machine

Stand up JupyterHub on a machine. Which machine doesn't matter. The pattern
is "make a Linux box with a GPU usable by a remote human."

**What to stand up**:

- JupyterHub (multi-user) with per-user notebook environments
- Pre-installed kernels for the friend's domain
  - For bioinformatics: Python (scanpy, pydeseq2, QIIME2), R (Seurat, DESeq2)
  - For other domains: whatever the friend needs
- Secure tunnel for external access (WireGuard, Tailscale, or SSH)
- Per-user storage on local disk
- Resource limits (cgroups/containers) for isolation

**Topology option**: If the cluster is a LAN (as with ecoPrimals), the
tunnel terminates on a NUC or lightweight intake node, and JupyterHub
runs on a heavier internal gate. The intake node is expendable. See
"The NUC Intake Pattern" above.

**Security posture**: Assume insecure. Human monitors all activity. The
tunnel is the only external surface. If compromised, pull the plug and
rebuild. No data on the intake node that can't be recreated.

**What this tests**:

- **Egress**: First time a machine serves an external user. Firewall rules,
  traffic patterns, unexpected behavior.
- **LAN routing**: Intake → workload gate forwarding over Cat6e. Does the
  NUC relay introduce latency or bottlenecks?
- **Multi-user isolation**: Do per-user notebook environments actually
  prevent cross-user interference?
- **Storage lifecycle**: User data creation, archival, deletion on someone
  else's machine.
- **Covalent bonding (early)**: Two machines (intake + workload) must
  coordinate. Manual now, bearDog-authenticated later.
- **The general question**: Is JupyterHub + tunnel sufficient for "lend
  compute to a friend"? What breaks?

**What this is NOT**: A production platform. A secure system. A permanent
deployment. It's a prototype for learning what the real problems are.

### Phase 2: petalTongue Web Alongside JupyterHub

Extend `petalTongue web` mode to serve interactive content alongside
JupyterHub. This is the convergence point — petalTongue progressively
replaces Zola as the sporePrint renderer (per
`wateringHole/petaltongue/SPOREPRINT_EVOLUTION_ROADMAP.md`) and
simultaneously grows compute-facing features.

**New petalTongue capabilities**:

- Job status dashboard (SSE-powered, existing `/api/events` endpoint)
- Result visualization (grammar-of-graphics engine)
- Notebook launch links (redirect to JupyterHub with environment config)

**Security evolution**: BTSP Phase 2 authentication starts here. bearDog
verifies who the user is cryptographically before they reach JupyterHub.
Identity is no longer "I know your Discord handle" — it's key-based.

**Primal involvement**: petalTongue (UI), bearDog (auth), songBird
(networking/egress patterns learned from Phase 1).

### Phase 3: Workload Submission

sporePrint becomes a platform. Users (human or agentic) submit workloads
through petalTongue's web interface. The full primal composition handles
the lifecycle:

1. User submits workload via petalTongue web
2. petalTongue creates a biomeOS deploy graph (TOML DAG)
3. biomeOS routes to appropriate hardware via toadStool
4. toadStool dispatches to the target machine
5. Results stored in nestGate (content-addressed)
6. Results served back through petalTongue
7. Provenance chain recorded by loamSpine

**Security**: BTSP Phase 3 encrypted transport protects the full channel.
ChaCha20-Poly1305 AEAD, HKDF-SHA256 session keys, directional encryption.
Workload submission can begin to automate because the channel is encrypted
and the identity is authenticated.

**Human/agentic hybrid**: Initially, the operator (or their AI tooling)
reviews and approves submissions. The approval loop is manual but execution
is automated. Over time, approval evolves from human-in-the-loop to
policy-based to fully agentic.

**Primal involvement**: All of the above plus biomeOS (orchestration),
toadStool (dispatch), nestGate (storage), loamSpine (provenance).

### Phase 4: Full Compositional Platform

The general pattern is now a sovereign compute sharing platform. Any
primal operator can offer compute to any trusted peer.

| Primal | Role |
|--------|------|
| petalTongue | Interface (web, TUI, API) |
| biomeOS | Orchestration (deploy graphs, capability routing) |
| toadStool | Dispatch (CPU/GPU/NPU allocation) |
| songBird | Networking (secure external access, federation) |
| bearDog | Auth / BTSP (identity, keys, policy) |
| nestGate | Storage (content-addressed results, archival) |
| loamSpine | Provenance (audit trail, reproducibility) |
| squirrel | AI orchestration (agentic workload management) |

The platform doesn't need to be designed upfront. It evolves from real
use. Each friend who uses it generates selective pressure on the primals.

---

## How External Workloads Become Spring Validation Data

This is the key insight for why compute sharing is mutually beneficial.

The operator's Rust pipelines are validated against published results. The
friend runs standard tools (Python, R, established bioinformatics packages)
on the operator's hardware. Those standard-tool outputs become new validation
targets:

```
Friend's QIIME2 run         → wetSpring 16S validation target
Friend's DESeq2 analysis     → healthSpring DE validation target
Friend's AlphaFold prediction → helixVision structure target
Friend's Scanpy clustering    → neuralSpring ML validation target
```

The friend doesn't need to know about springs. They just use their tools.
The operator captures the outputs as ground truth for their Rust
reimplementations. The more friends use the hardware, the more validation
data accumulates, and the more the Rust tools evolve.

This is not extraction — it's the same pattern used internally. Published
results → standard tools → Rust → primal compositions. The friend's
science drives the direction of what the operator builds next.

---

## First Instance: ABG (Accelerated Bioinformatics Group)

ABG is a bioinformatics research Discord (~30 members, grad students through
professors). They need compute for scRNA-seq, bulk RNA-seq, metagenomics,
and structure prediction. They were told to use Google Colab.

**Phase 0 (active)**: Tamison runs jobs manually for ABG members.

**Phase 1 (validated 2026-05-04)**: JupyterHub + Nest Atomic + ToadStool (9 primals) on ironGate. Pre-installed: scanpy, pydeseq2, QIIME2, Seurat, DESeq2. 235+ wetSpring checks passing through toadStool dispatch, real NCBI data (PRJNA488170, 11.9M reads) processed, full provenance pipeline operational (BLAKE3 → rhizoCrypt DAG → loamSpine ledger → sweetGrass braid). See `COMPOSITION_VALIDATION_LOG.md` and `projectNUCLEUS/validation/` for details.

**Domain-specific validation targets**:
- scRNA-seq outputs → wetSpring / neuralSpring
- Bulk RNA-seq DESeq2 → healthSpring
- Metagenomics → wetSpring (16S, QS gene analysis)
- Structure prediction → helixVision
- Immune pathway analysis → healthSpring (Anderson immunological framework)

**Relevant prior work** (published at primals.eco/science/):
- Papers 01, 05: 16S pipeline, cold seep metagenomics (6,600+ checks)
- Paper 12: Anderson in immunological signaling (329 checks)
- Paper 09: Field genomics architecture
- Paper 13: Sovereign human health (PK/PD, drug discovery)

---

## Future Instances

The pattern generalizes. Potential future friends:

- A physics lab that needs GPU time for simulation
- A game developer who needs compute for procedural generation testing
- A student who needs to run ML training but can't afford cloud
- Another primal operator offering reciprocal compute

Each instance follows the same phases. The domain-specific kernels and
validation targets change; the pattern doesn't.

---

*This document is a living pattern. Update after each phase transition
with observed friction points, security learnings, and primal evolution
triggered by external use.*
