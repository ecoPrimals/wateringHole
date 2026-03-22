# Public Surface Standard — GitHub Accessibility, PII Review, and AI Discoverability

**Purpose:** Every public repo in ecoPrimals and syntheticChemistry must be
independently understandable by a cold reader — human or machine. This standard
defines the public-facing metadata, PII hygiene, and context blocks that make
repos discoverable, scannable, and safe to publish.

**Companion:** `SPRING_PRIMAL_PRESENTATION_STANDARD.md` (internal repo structure)
**Audience:** Every primal and spring maintainer  
**Last Updated:** March 22, 2026

---

## Why This Exists

When someone — or some AI — lands on one of our GitHub repos cold, they get
almost nothing. The code is clean, the tests pass, but there is no on-ramp.
No repo description. No topics. No context block explaining what this binary
is or how it fits into a larger system. The result: external tools score our
repos as opaque, and potential collaborators bounce.

This is a workflow problem, not a documentation problem. Each primal and spring
must own its own public surface as part of every version bump — the same way
it already owns its handoff, its changelog, and its test suite.

---

## The Five Layers

### Layer 1: GitHub Repo Metadata

Every repo needs a one-line description and a topic set. These are the first
things GitHub search, Sourcegraph, and AI crawlers see.

**Description:** One sentence. What it does, in what language, for what purpose.
No marketing. If the repo is small or its purpose is narrow, say so.

**Topics:** A curated tag set. Always include `rust` and `pure-rust`. Add
domain-specific tags from the table below. Do not add tags the repo doesn't
earn — if it doesn't touch FHE, don't tag `fhe`.

**How to apply:**

```bash
gh repo edit <org>/<repo> --description "<one-line description>"
gh repo edit <org>/<repo> --add-topic rust --add-topic pure-rust --add-topic <domain>
```

**Each primal/spring session that bumps a version should verify these are current.**

### Layer 2: Root README.md — The Public On-Ramp

The `SPRING_PRIMAL_PRESENTATION_STANDARD.md` already defines the internal
README structure. For public surface, add or verify these sections exist
at the top of every root README:

1. **One paragraph** explaining what this repo does and who it is for.
   Write for someone who has never heard of ecoPrimals. No jargon without
   inline definition. No assumed context.

2. **Architecture section** (if warranted) — how the binary is structured,
   what protocols it uses, what it depends on. Keep it short. A diagram or
   a 5-line ASCII box is better than 3 paragraphs.

3. **Code/usage example** (if applicable) — the shortest path from clone
   to seeing the thing work. `cargo test` is fine if that's the proof.
   A `cargo run --release --bin validate_*` invocation with expected output
   is better.

4. **"Part of ecoPrimals" footer** — a standard block linking to the org
   and the ecosystem context:

```markdown
---

## Part of ecoPrimals

This repo is part of the [ecoPrimals](https://github.com/ecoPrimals) sovereign
computing ecosystem — a collection of pure Rust binaries that coordinate via
JSON-RPC, capability-based routing, and zero compile-time coupling.

See [wateringHole](https://github.com/ecoPrimals/wateringHole) for ecosystem
documentation, standards, and the primal registry.
```

For syntheticChemistry repos, use:

```markdown
---

## Part of ecoPrimals (syntheticChemistry)

This repo is a domain validation spring in the
[ecoPrimals](https://github.com/ecoPrimals) sovereign computing ecosystem.
Springs reproduce published scientific results using pure Rust and
[barraCuda](https://github.com/ecoPrimals/barraCuda) GPU primitives.

See [wateringHole](https://github.com/ecoPrimals/wateringHole) for ecosystem
documentation and standards.
```

### Layer 3: AI Context Block (`CONTEXT.md`)

This is the critical missing piece. When an AI tool scans a repo, it reads
the README and maybe `Cargo.toml`. It does not read wateringHole. It does not
read the white papers. It has no idea what "primal" means or why JSON-RPC
matters.

Every repo must maintain a `CONTEXT.md` at the root. This file exists solely
to be ingested by AI tools, search indexers, and automated review systems.

**Template:**

```markdown
# Context — <Repo Name>

## What This Is

<Repo Name> is a pure Rust binary that <does X>. It is part of the ecoPrimals
sovereign computing ecosystem — a collection of self-contained binaries that
coordinate via JSON-RPC 2.0 over Unix sockets, with zero compile-time coupling
between components.

## Role in the Ecosystem

<1-3 sentences: what domain this covers, what it replaces or enables, how other
components depend on it>

## Technical Facts

- **Language:** 100% Rust, zero C dependencies
- **Architecture:** Single binary (UniBin), multiple operational modes
- **Communication:** JSON-RPC 2.0 over platform-agnostic IPC
- **License:** AGPL-3.0-only
- **Tests:** <count>
- **Coverage:** <percentage if tracked>
- **MSRV:** <version>
- **Crate count:** <N> workspace crates

## Key Capabilities (JSON-RPC methods)

<List the primary method domains: crypto.sign, compute.dispatch, etc.>

## What This Does NOT Do

<Clarify boundaries: does not compile shaders (that's coralReef), does not
manage hardware (that's toadStool), etc.>

## Related Repositories

- [wateringHole](https://github.com/ecoPrimals/wateringHole) — ecosystem standards and registry
- <list direct dependencies/consumers>

## Design Philosophy

These binaries are built using AI-assisted constrained evolution. Rust's
compiler constraints (ownership, lifetimes, type system) reshape the fitness
landscape and drive specialization. Primals are self-contained — they know
what they can do, never what others can do. Complexity emerges from runtime
coordination, not compile-time coupling.
```

**Requirements:**
- Keep it under 150 lines. AI tools have context limits.
- Update the test count and coverage on every version bump.
- Do not duplicate the full README — link to it for details.
- Do not include internal planning, roadmaps, or handoff state.

### Layer 4: PII Review

Before any repo goes public or receives a visibility change, run this checklist.
This is non-negotiable. A single leaked email address or internal hostname is a
permanent exposure.

#### PII Scan Checklist

| Category | What to Look For | Where to Look |
|----------|-----------------|---------------|
| **Email addresses** | Personal emails, institutional emails, internal aliases | All `.md`, `.toml`, `.rs` comments, git log `--format='%ae'` |
| **Names** | Full names of non-public individuals, internal team names | READMEs, changelogs, comments, git log `--format='%an'` |
| **Hostnames / IPs** | Internal hostnames, private IPs, VPN endpoints | Config files, test fixtures, hardcoded strings |
| **File paths** | Home directories (`/home/<user>/`), internal mount points | Tests, build scripts, error messages, panic traces |
| **API keys / tokens** | GitHub tokens, SSH keys, service credentials | `.env`, config files, test fixtures, git history |
| **Institutional details** | Internal project codes, grant numbers (unless public), internal URLs | Documentation, comments |
| **Git history** | Author names/emails in commits that shouldn't be public | `git log --all --format='%an <%ae>'  \| sort -u` |

#### Automated Scan Commands

Run these before any visibility change:

```bash
# Email addresses
rg -i '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}' --type md --type toml --type rust

# Home directory paths
rg '/home/[a-z]' --type md --type toml --type rust
rg '/Users/[A-Z]' --type md --type toml --type rust

# IP addresses (private ranges)
rg '(10\.\d+\.\d+\.\d+|172\.(1[6-9]|2\d|3[01])\.\d+\.\d+|192\.168\.\d+\.\d+)' --type-add 'all:*' --type all

# API keys / tokens (common patterns)
rg '(sk-|ghp_|gho_|AKIA|token|secret|password|Bearer )' -i --type-add 'all:*' --type all

# Git author audit
git log --all --format='%an <%ae>' | sort -u

# Cargo.toml author fields
rg 'authors\s*=' **/Cargo.toml
```

**If any hit is found:** Evaluate whether it belongs in a public repo. If not,
remove it from the current tree AND scrub it from git history if it was ever
committed. Use `git filter-repo` or `BFG` for history rewrites.

#### Git Author Hygiene

All commits on public repos should use the project identity, not personal
email addresses. Verify before pushing:

```bash
git log --format='%an <%ae>' | sort -u
# Should show project/org identity, not personal emails
```

### Layer 5: The Public Surface Task

This is the ingestible blurb. When an AI session is working on a primal or
spring and needs to do a public surface pass, hand it this block. The primal
or spring is responsible for maintaining its own metadata — wateringHole
defines what's expected; each repo executes.

---

**Copy-paste task for any primal/spring AI session:**

> **Task: Public surface pass for this repository**
>
> This repo is part of the ecoPrimals sovereign computing ecosystem (GitHub orgs:
> `ecoPrimals` and `syntheticChemistry`). It is a pure Rust binary built using
> AI-assisted constrained evolution. It communicates via JSON-RPC 2.0,
> capability-based routing, zero compile-time coupling between primals.
>
> Do the following:
>
> 1. **Read the source** to understand what this repo does. Read `Cargo.toml`,
>    `src/main.rs` or `src/lib.rs`, and the existing README if any.
>
> 2. **Verify or create `CONTEXT.md`** at the repo root following the template in
>    `wateringHole/PUBLIC_SURFACE_STANDARD.md`. This file must be understandable
>    by an AI with zero prior context about ecoPrimals.
>
> 3. **Verify or update `README.md`** to include: one paragraph explaining what
>    it does and who it's for, a short architecture section if warranted, a
>    code/usage example if applicable, and a "Part of ecoPrimals" footer.
>
> 4. **Run the PII scan** (see `PUBLIC_SURFACE_STANDARD.md` Layer 4). Report any
>    findings. Do not commit PII to a public repo.
>
> 5. **Output `gh repo edit` commands** for description and topics that I can run.
>    Use the topic vocabulary from `PUBLIC_SURFACE_STANDARD.md`.
>
> Don't write marketing. Write honest technical descriptions. If the repo is
> small or its purpose isn't clear from source alone, say so and write what you
> can confirm from the code.

---

## Topic Vocabulary

Use these consistently across all repos. Only add tags the repo earns.

### Universal (all repos)

| Topic | When to Use |
|-------|-------------|
| `rust` | Always |
| `pure-rust` | No C dependencies in application code |
| `json-rpc` | Exposes or consumes JSON-RPC 2.0 methods |
| `sovereign-computing` | Part of the sovereign compute thesis |
| `ecoprimals` | All repos in the ecosystem |

### Domain-Specific

| Topic | Repos |
|-------|-------|
| `cryptography` | BearDog |
| `ed25519`, `blake3`, `x25519`, `chacha20` | BearDog |
| `networking`, `tls`, `mdns`, `tor` | Songbird |
| `gpu`, `wgsl`, `shaders`, `f64` | barraCuda, coralReef |
| `ntt`, `fft` | barraCuda |
| `fhe`, `homomorphic-encryption` | barraCuda (if FHE primitives present) |
| `gpu-driver`, `vfio`, `drm` | coralReef |
| `nouveau`, `amdgpu` | coralReef |
| `hardware-discovery`, `sysinfo` | toadStool |
| `neuromorphic`, `akida`, `npu` | rustChip |
| `orchestration`, `process-management` | biomeOS |
| `content-addressed-storage` | NestGate |
| `dag`, `merkle-tree` | rhizoCrypt |
| `provenance`, `attribution` | sweetGrass |
| `immutable-ledger` | LoamSpine |
| `thermal-simulation`, `molecular-dynamics` | hotSpring |
| `metagenomics`, `microbiome`, `analytical-chemistry`, `bioinformatics`, `life-science` | wetSpring |
| `evapotranspiration`, `irrigation`, `soil-physics`, `agriculture` | airSpring |
| `geochemistry`, `mineral-dissolution` | groundSpring |
| `neural-networks`, `spiking-networks` | neuralSpring |
| `gpu-computing` | Springs consuming barraCuda GPU primitives |
| `scientific-computing` | All springs |
| `paper-reproduction` | All springs |

## Repo Reference Table

Current repos across both orgs with expected descriptions and topics.
Each maintainer should verify and apply these, then update this table
with `[applied]` when done.

### ecoPrimals org

| Repo | Description | Additional Topics |
|------|-------------|-------------------|
| **squirrel** | Sovereign AI model context protocol and multi-MCP coordination in pure Rust | `ai`, `mcp`, `inference` |
| **barraCuda** | Pure Rust f64 GPU math library — 800+ WGSL shaders for NTT, FFT, physics, and FHE | `gpu`, `wgsl`, `shaders`, `f64`, `ntt`, `fft`, `fhe`, `scientific-computing` |
| **coralReef** | Pure Rust sovereign GPU compiler and driver stack — WGSL to native via naga, VFIO dispatch, PCIe lifecycle | `gpu`, `gpu-driver`, `wgsl`, `vfio`, `drm`, `nouveau`, `amdgpu`, `shader-compiler` |
| **toadStool** | Pure Rust hardware discovery and compute orchestration — CPU, GPU, NPU, WASM, containers, 20k+ tests | `hardware-discovery`, `sysinfo`, `compute-orchestration` |
| **wateringHole** | Ecosystem standards, primal registry, and coordination guidance for ecoPrimals | `documentation`, `standards` |
| **sporePrint** | Ecosystem bootstrapping and deployment tooling for ecoPrimals | `deployment`, `bootstrapping` |

### syntheticChemistry org

| Repo | Description | Additional Topics |
|------|-------------|-------------------|
| **hotSpring** | Thermal simulation and molecular dynamics validation spring — paper reproduction in pure Rust | `thermal-simulation`, `molecular-dynamics`, `scientific-computing`, `paper-reproduction` |
| **wetSpring** `[applied]` | Pure Rust metagenomics, analytical chemistry & mathematical biology — 1,500+ tests, 354 validation binaries, GPU via barraCuda | `metagenomics`, `analytical-chemistry`, `bioinformatics`, `microbiome`, `gpu-computing`, `wgsl`, `life-science`, `scientific-computing`, `paper-reproduction`, `agpl-3-0` |
| **airSpring** `[applied]` | Pure Rust FAO-56 evapotranspiration, Richards equation soil physics & precision irrigation — 950+ lib tests, 61 validation checks, GPU + NPU via barraCuda | `evapotranspiration`, `irrigation`, `soil-physics`, `agriculture`, `gpu-computing`, `wgsl`, `scientific-computing`, `paper-reproduction`, `agpl-3-0` |
| **groundSpring** | Geochemistry and mineral dissolution validation spring in pure Rust | `geochemistry`, `mineral-dissolution`, `scientific-computing`, `paper-reproduction` |
| **neuralSpring** | Spiking neural network and neuromorphic computing validation spring in pure Rust | `neural-networks`, `spiking-networks`, `neuromorphic`, `scientific-computing`, `paper-reproduction` |
| **rustChip** | Clean-room pure Rust driver for BrainChip Akida AKD1000 NPU | `neuromorphic`, `akida`, `npu`, `hardware-driver` |

---

## Workflow Integration

### On Every Version Bump

Add to the existing pre-push checklist (from `STANDARDS_AND_EXPECTATIONS.md`):

- [ ] `CONTEXT.md` exists and test count / coverage are current
- [ ] Root README has one-paragraph summary, architecture, example, footer
- [ ] PII scan passes (Layer 4 commands, zero findings)
- [ ] GitHub description matches current reality
- [ ] GitHub topics are current (check topic vocabulary table)

### On Visibility Changes (private → public)

Full Layer 4 PII audit is mandatory. This means:

1. Run all automated scan commands
2. Audit `git log --all --format='%an <%ae>'` for author leaks
3. Check `Cargo.toml` author fields
4. Review all markdown files for institutional details
5. Review test fixtures and error messages for path/hostname leaks
6. If any PII is found in git history, scrub with `git filter-repo` before publishing

### Quarterly Surface Audit

Every quarter, run the public surface task (Layer 5 blurb) against every
public repo. Track completion in the handoff for that session. This catches
drift — descriptions that reference old versions, topics that no longer apply,
CONTEXT.md files with stale test counts.

---

## Measuring Success

The goal is simple: when an AI or a human lands on any ecoPrimals or
syntheticChemistry repo cold, they can answer these questions in under
60 seconds:

1. What does this repo do?
2. What language is it written in?
3. Is it part of a larger system? Which one?
4. How do I build and test it?
5. Who is it for?

If any question takes longer than 60 seconds, the public surface needs work.
