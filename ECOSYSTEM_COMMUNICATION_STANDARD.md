# Ecosystem Communication Standard — Three-Layer Coordination

**Authority**: primalSpring coordination
**Status**: Active (Wave 63+)
**Prerequisites**: `IMPULSE_POTENTIAL_STANDARD.md`, `CONTEXT_BRAID_STANDARD.md`, `WATERFALL_PATTERN.md`
**Lineage**: Synthesizes inter-gate coordination patterns into a unified standard

---

## The Problem

Before Wave 63, inter-gate coordination relied on two incompatible patterns:

1. **Git commits** — permanent, structured, but noisy for short-lived coordination
2. **Copy-paste blurbs** — fast, expressive, but ephemeral (lost with the terminal session)

A gate team finishing a sprint would compose a handoff blurb in Markdown, paste it into
another gate's IDE, and hope the context survived. These blurbs carried critical state:
what was completed, what's next, what's blocked, what primals to rebuild. But they had
no schema, no discoverability, no lifecycle, and no provenance trail. They vanished
when the tab closed.

The three-layer model solves this by giving each communication need its own layer with
the right lifetime, schema, and propagation mechanism — all riding on the same
waterFall sync infrastructure that already connects every gate.

---

## The Three Layers

```
                    Permanent                          Ephemeral
                    ←──────────────────────────────────→

   ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
   │  Git Commits      │   │  Impulses         │   │  Context Braids   │
   │  (loamSpine)      │   │  (rhizoCrypt)     │   │  (sweetGrass)     │
   │                   │   │                   │   │                   │
   │  "What happened"  │   │  "What to do"     │   │  "What's the      │
   │                   │   │                   │   │   story right now" │
   │  Linear           │   │  Event DAG        │   │  Woven strands    │
   │  Forever          │   │  Time-bounded     │   │  TTL auto-decay   │
   │                   │   │  Archived/wave    │   │  Superseding      │
   └──────────────────┘   └──────────────────┘   └──────────────────┘
         │                       │                       │
         │   All three sync via waterFall cascade-pull   │
         └───────────────────────┴───────────────────────┘
```

### Layer 1: Git Commits (Permanent Record)

The bedrock. Every code change, document update, and configuration shift is captured
in git commits. These form the permanent ledger — analogous to loamSpine's anchored
blockchain records. Git commits answer: *what happened?*

- **Schema**: Git commit messages (conventional commits encouraged)
- **Lifetime**: Forever
- **Transport**: SSH/HTTPS push/pull through waterFall temporal sync
- **Discovery**: `git log`, `membrane temporal.check`
- **Biological analog**: loamSpine ledger

### Layer 2: Impulses (Event-Driven Actions)

The coordination nerve. When a gate completes work that another gate needs to know
about — rebuild this binary, pull this repo, validate this pattern — it fires an
**impulse**. Impulses are discrete, time-bounded, actionable messages that propagate
through the membrane alongside code. They answer: *what should I do?*

- **Schema**: TOML files in `impulses/active/` (`IMPULSE_POTENTIAL_STANDARD.md`)
- **Lifetime**: Active until acknowledged, archived per wave
- **Transport**: Git push through waterFall; auto-discovered via `potential.sense`
- **Discovery**: `membrane potential.sense`, `cascade-pull.sh` auto-trigger
- **Biological analog**: rhizoCrypt DAG sessions (fire, propagate, acknowledge)
- **Subtypes**: FRAGO (fragmentary order), AUDIT (validation request), SYNC (merge request)

### Layer 3: Context Braids (Ephemeral Developer State)

The working memory. When a gate is mid-sprint, it weaves a context braid — what's in
focus, what breadcrumbs led here, what the next steps are. Context braids are the
structured replacement for copy-paste blurbs. They answer: *what's the story right now?*

- **Schema**: TOML files in `context/{gate}/` (`CONTEXT_BRAID_STANDARD.md`)
- **Lifetime**: TTL-based auto-decay, superseding (new weave replaces old)
- **Transport**: Git push through waterFall
- **Discovery**: `membrane context.sense`, Cursor rules/hooks on session start
- **Biological analog**: sweetGrass braids (weave provenance, but ephemeral)

---

## The Internal/External Mirror

Each layer has a biological primal analog that handles the *internal* (data provenance)
equivalent. The three communication layers are the *external* (developer coordination)
mirror:

| Internal (data)              | External (developers)              | Parallel |
|------------------------------|------------------------------------|----------|
| loamSpine ledger             | Git commits                        | Permanent record |
| rhizoCrypt DAG sessions      | Impulses (fire, propagate, ack)    | Event-driven actions |
| sweetGrass braids            | Context braids (weave, sense, clear) | Woven state |

This symmetry is intentional. The same patterns that make data provenance trustworthy
make developer coordination trustworthy. The ecosystem's internal organs and its
external communication use the same architecture.

---

## Neural API Triad Mapping

The three layers map directly to the Neural API triad:

| Layer | Triad Domain | Direction | CLI |
|-------|-------------|-----------|-----|
| Git commits | rootPulse (ACTION) | Create artifacts | `git commit`, `git push` |
| Impulses | rootPulse + quorumSignal | Fire + sense | `membrane impulse.post`, `membrane potential.sense` |
| Context braids | quorumSignal (SENSE) | Observe state | `membrane context.weave`, `membrane context.sense` |
| All three | waterFall (SYNC) | Propagate across mesh | `cascade-pull.sh --source temporal` |

The triad cycle with all three layers:

```
1. Gate A completes work
   ├── git commit + push             (rP: permanent record)
   ├── membrane impulse.post         (rP: fire action potential)
   └── membrane context.weave        (qS: update working state)

2. waterFall propagates              (wF: cascade-pull sync)
   ├── git changes flow to all gates
   ├── impulse TOML appears in impulses/active/
   └── context TOML appears in context/{gateA}/

3. Gate B pulls and discovers
   ├── potential.sense → "2 pending impulses"
   ├── context.sense → "gateA is working on cellMembrane bridge.rs"
   └── Developer reads impulse, acks, continues
```

---

## Lifecycle

### Creating Communication

```bash
# Layer 1: Git commit (always happens)
git add . && git commit -m "feat: impulse signing via bearDog"
git push forgejo main    # K-Derm relay propagates to GitHub automatically

# Layer 2: Fire an impulse (when other gates need to act)
membrane impulse.post \
  --type frago \
  --to flockGate \
  --subject "rebuild membrane for impulse signing" \
  --body "pull cellMembrane, cargo build --release, cp to ~/.local/bin/"

# Layer 3: Weave context (update your gate's working state)
membrane context.weave \
  --repo gardens-cellmembrane \
  --focus "impulse.rs bearDog signing integration" \
  --breadcrumbs "bridge.rs NeuralBridge, impulse.rs try_sign_impulse, main.rs dispatch" \
  --next-steps "test signing with live bearDog UDS, validate TOML schema, push to forgejo"
```

### Discovering Communication

After `cascade-pull.sh` syncs, discovery happens automatically:

```bash
# cascade-pull already runs potential.sense at the end
# But you can also discover manually:

membrane potential.sense              # List pending impulses
membrane potential.sense --count      # Just the count
membrane context.sense                # See all gates' current context
membrane context.sense --gate eastGate  # One gate's context
```

### Acknowledging and Clearing

```bash
# Ack an impulse (marks it handled, doesn't archive yet)
membrane impulse.ack --id 2026-05-31T09-30_flockGate__rebuild-membrane

# Archive spent impulses (end of wave)
membrane impulse.archive

# Clear your own context (sprint complete, context stale)
membrane context.clear --repo gardens-cellmembrane
```

---

## When to Use Each Layer

| Situation | Layer | Why |
|-----------|-------|-----|
| Shipped code | Git commit | Permanent record of what changed |
| Another gate needs to rebuild a binary | Impulse (FRAGO) | Actionable, time-bounded, auto-discovered |
| Requesting validation of a new pattern | Impulse (AUDIT) | Directed, needs acknowledgment |
| Documenting your current sprint focus | Context braid | Ephemeral, superseding, helps other gates understand your state |
| Long-term architecture decision | Git commit + handoff `.md` | Permanent, lives in `handoffs/` |
| "Hey, pull wateringHole and rebuild membrane" | Impulse (FRAGO) | Short, actionable, replaces a Slack message |
| "I'm mid-sprint on bridge.rs, don't touch impulse.rs" | Context braid | Working state, auto-decays when you move on |

### Anti-Patterns

- **Don't use impulses for permanent decisions** — use a handoff document committed to git
- **Don't use context braids for action requests** — use an impulse (braids are observation, not direction)
- **Don't use git commits for ephemeral coordination** — commits are forever, coordination state is not
- **Don't paste blurbs into IDE chat** — weave a context braid and fire an impulse instead

---

## VPS Mediator Pattern (Phase 4 Inversion — Wave 63+)

All three layers propagate through the VPS as sovereign mediator:

```
Gate ──covalent──→ golgiBody-inner (cis: Forgejo)
                       │ metallic
                   peptidoglycan (structural: sync + impulse cascade)
                       │ ionic
                   golgiBody-ext (trans: ships to extracellular)
                       │ weak
                   GitHub (external linear ledger)
```

**Push Target**: Gates push only to Forgejo (`push_target = "forgejo"` in manifest).
The K-Derm diderm relay chain propagates through all three VPS nodes with proper
bond-type degradation. Gates no longer need GitHub SSH keys.

**GitHub as External Linear Ledger**: GitHub serves the same conceptual role as
loamSpine → BTC/ETH stamping: an external, immutable, publicly-discoverable
record of ecosystem evolution. It is a trailing mirror, not the source of truth.

| Operation | Target | Bond | Mechanism |
|-----------|--------|------|-----------|
| `git push` | Forgejo (inner) | Covalent | Gate SSH to golgiBody |
| Sync relay | peptidoglycan | Metallic | Post-receive webhook → `pepti-sync-relay.sh` |
| GitHub mirror | GitHub | Weak | `ext-github-push.sh` on golgiBody-ext |
| Impulse relay | Mesh | — | peptidoglycan `potential.sense` → songbird |
| Context sync | All gates | — | waterFall cascade-pull |

See `WATERFALL_PATTERN.md` Phase 4, `hooks/forgejo/README.md` for relay chain,
and `graphs/waterfall_publish.toml` for cascade specification.

---

## Primal Graduation Path

Today, all three layers are implemented as direct filesystem operations in
`membrane-shadow`. As primals graduate, the operations compose through biomeOS graphs:

| Layer | Shadow (today) | Graduated (future) |
|-------|----------------|---------------------|
| Impulses | `membrane impulse.post` writes TOML, git pushes | bearDog signs, rhizoCrypt records DAG event, songbird relays, nestGate stores |
| Context | `membrane context.weave` writes TOML | sweetGrass validates schema, loamSpine anchors completed braids |
| Git | `git commit/push` | rootPulse graph: dehydrate → sign → store → commit → attribute |

The graduation graphs are defined in:
- `infra/wateringHole/graphs/impulse_post_signed.toml`
- `infra/wateringHole/graphs/context_weave_anchored.toml`
- `infra/wateringHole/graphs/waterfall_publish.toml` (full cascade composition)

The NeuralBridge in `membrane-shadow` (feature-gated) already attempts to route
through biomeOS before falling back to shadow implementations.

---

## K-NOME Interaction

The three-layer model formalizes the K-NOME programming pattern for multi-gate
development:

**Before** (manual K-NOME):
1. Human composes a long context blurb
2. Pastes it into a fresh IDE chat
3. AI reads specs, docs, wateringHole standards
4. AI works, produces results
5. Human copies results, pastes to next gate

**After** (structured K-NOME):
1. Human fires an impulse with action directives
2. Human weaves context with sprint state
3. AI on receiving gate runs `context.sense` → instant context
4. AI reads impulses via `potential.sense` → knows what to do
5. AI works, weaves its own context, fires completion impulse
6. waterFall propagates everything to all gates

The copy-paste blurb becomes a structured, discoverable, version-controlled
artifact that any gate can consume without human relay.

---

## Standards Reference

| Standard | File | Domain |
|----------|------|--------|
| This document | `ECOSYSTEM_COMMUNICATION_STANDARD.md` | Unified coordination model |
| Impulse/Potential | `IMPULSE_POTENTIAL_STANDARD.md` | Layer 2: event-driven actions |
| Context Braids | `CONTEXT_BRAID_STANDARD.md` | Layer 3: ephemeral developer state |
| WaterFall Pattern | `WATERFALL_PATTERN.md` | Transport: temporal sync across mesh |
| Semantic Methods | `SEMANTIC_METHOD_NAMING_STANDARD.md` | Method naming conventions |
| Capability Registry | `primalSpring/config/capability_registry.toml` | Registered capabilities |

---

*"The ecosystem communicates in three voices: the permanent voice of git that remembers
everything, the urgent voice of impulses that demands action, and the quiet voice of
context that says 'this is where I am right now.' All three travel on the same water."*
