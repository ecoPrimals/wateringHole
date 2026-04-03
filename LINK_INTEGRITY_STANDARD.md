# Link Integrity Standard — Dead-End Free InfraNet

**Status**: Ecosystem Standard v1.0
**Adopted**: April 3, 2026
**Authority**: WateringHole Consensus
**Compliance**: Required for sporePrint, recommended for all public repos
**License**: AGPL-3.0-or-later

---

## Purpose

Every link in the ecoPrimals public surface must resolve. Dead links are
broken trust — the same way a guideStone artifact with a bad CHECKSUMS
file is broken trust. The reader (human or AI) follows a link expecting
knowledge and finds a 404. The ecosystem promised a path and delivered
a wall.

This standard defines how ecoPrimals maintains a **dead-end free infranet**:
every internal and external link is validated at build time, and broken
links block deployment.

---

## The Problem

sporePrint v0.4.0 launched with 19 broken links. Every spring repo URL
pointed to `github.com/ecoPrimals/` when the springs live under
`github.com/syntheticChemistry/`. These were invisible because raw GitHub
Markdown rendering does not validate links — it renders them as blue text
regardless of whether the target exists.

The same class of problem occurs in:
- README files with stale cross-repo links
- Handoff documents referencing moved files
- Specs with URLs to deprecated endpoints
- CHANGELOG entries with invalid anchor links

---

## The Solution: Build-Time Link Validation

### For sporePrint (Zola-powered site)

sporePrint uses **Zola** (Rust static site generator). Zola provides two
levels of link validation:

**Internal links** — validated at `zola build` time. An `@/section/page.md`
reference that does not resolve causes a build failure. Broken internal
links cannot reach production.

**External links** — validated by `zola check`. HTTP HEAD requests to every
external URL in the content. 404s, timeouts, and connection failures are
reported. `zola check` runs as a CI gate in the GitHub Actions workflow:
broken external links block deployment.

```yaml
# .github/workflows/deploy.yml
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install Zola
        run: |
          curl -sL https://github.com/getzola/zola/releases/.../zola-...tar.gz | tar xz
          sudo mv zola /usr/local/bin/
      - name: Check links
        run: zola check

  build:
    needs: check    # build only runs if check passes
    ...
```

### For Spring and Primal READMEs

Springs and primals do not use Zola. Their link integrity relies on:

1. **`lychee`** — a Rust link checker (single binary, like Zola). Can be
   run locally or in CI:
   ```bash
   lychee --exclude-private --no-progress README.md docs/
   ```

2. **Manual audit at version bump** — the `PUBLIC_SURFACE_STANDARD.md`
   already requires surface verification at every version bump. Link
   checking is now part of that verification.

3. **Cross-repo link conventions** — when linking to another ecoPrimals
   repo, use the organization-qualified URL:
   - Springs: `https://github.com/syntheticChemistry/<spring>`
   - Primals: `https://github.com/ecoPrimals/<primal>`
   - Products: `https://github.com/sporeGarden/<product>`
   - Site: `https://primals.eco/<section>/<page>/`

### For wateringHole Documents

wateringHole documents are internal Markdown, not rendered by a site
generator. Link integrity for standards and handoffs:

1. Relative links to other wateringHole docs are verified by the
   existing `bootstrap.sh` setup check (file existence).
2. External links in standards should use the canonical URL forms above.
3. Handoff documents referencing moved files should note the move
   explicitly rather than linking to the old path.

---

## Link Patterns

### Internal Links (within a Zola site)

Use Zola's `@/` path syntax. These are validated at build time.

```markdown
[For Faculty and PIs](@/audience/FOR_FACULTY_AND_PIS.md)
```

### Cross-Repo Links

Always use the full HTTPS URL with the correct organization:

```markdown
[wetSpring](https://github.com/syntheticChemistry/wetSpring)
[toadStool](https://github.com/ecoPrimals/toadStool)
[sporePrint](https://primals.eco)
```

### Anchor Links

When linking to a heading within the same document, verify the anchor
matches the rendered slug. Zola uses GitHub-compatible slugification
(lowercase, hyphens for spaces, strip special chars).

---

## Compliance Checklist

| Requirement | sporePrint | Springs | Primals |
|-------------|:----------:|:-------:|:-------:|
| Internal links validated at build time | Required (Zola) | Recommended (lychee) | Recommended (lychee) |
| External links validated in CI | Required (zola check) | Recommended | Recommended |
| Broken links block deployment | Required | Recommended | Recommended |
| Cross-repo URLs use correct org | Required | Required | Required |
| Links verified at version bump | Required | Required | Required |

---

## Relationship to Other Standards

| Standard | Relationship |
|----------|-------------|
| `PUBLIC_SURFACE_STANDARD.md` | Link integrity is a new layer of public surface quality |
| `GUIDESTONE_STANDARD.md` | guideStone Property 3 (Self-Verifying) applied to documentation — CHECKSUMS for content |
| `EXTERNAL_VALIDATION_ARTIFACT_STANDARD.md` | Artifact CHECKSUMS validate binary integrity; link integrity validates documentation integrity |
| `ECOBIN_ARCHITECTURE_STANDARD.md` | ecoBin builds must not emit broken paths; documentation should not emit broken links |

---

## petalTongue Integration (Evolution Target)

petalTongue consumes Markdown + TOML front matter as structured content.
When petalTongue renders sporePrint content (conversational, audio, or
visual modality), it inherits the link integrity guarantee: every
reference in the TOML metadata resolves because Zola validated it at
build time. petalTongue can trust the links and present them as
navigable targets in any modality — spoken URL, clickable element,
braille reference.

The dead-end free property transfers from the build pipeline to the
rendering primal. The user never encounters a broken path regardless
of how they access the content.

---

## The Principle

A link is a promise. A broken link is a broken promise. In a sovereign
ecosystem where trust is earned through verifiable computation, the
documentation must be held to the same standard as the code. `zola check`
is the `cargo test` of the public surface.

*If the artifact validates itself, the documentation should too.*
