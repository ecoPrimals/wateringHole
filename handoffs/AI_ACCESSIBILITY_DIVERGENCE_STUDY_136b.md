# AI Accessibility Divergence Study — Wave 136b

**Date**: Jul 11, 2026
**Gate**: eastGate
**Type**: Accessibility divergence analysis — how different AI agents experience primals.eco

---

## Context

An external Claude agent (Anthropic, browser session via `web_fetch`) performed an
independent review of primals.eco. Their review revealed both real bugs and
diagnostic artifacts that together form a valuable test matrix for AI accessibility.

## Timeline

1. **Agent reports**: philosophy/story essay tables render "header row only" — zero essay links visible
2. **We investigate**: links ARE in the HTML, but fetch-to-text tools strip `<a href>` from `<table>` cells
3. **Fix deployed**: tables converted to ordered lists, JSON-LD `hasPart` arrays added
4. **Pipeline divergence found**: golgi had two checkouts, Caddy served from the stale one (30 commits behind)
5. **Pipeline fixed**: correct checkout updated, Zola rebuilt in serving directory
6. **Agent re-checks**: still sees old version (tool-side cache), but confirms site-wide crawling now open
7. **Agent files formal review**: diagnoses "JS hydration" as cause (incorrect — content was always static)

## Divergence Matrix

| AI System | Philosophy Index | Essay Links | Leaf Pages | Cache Behavior |
|-----------|-----------------|-------------|------------|----------------|
| **Claude (web_fetch)** | Loads, tables truncated | Invisible (links stripped from table cells) | Inconsistent (some fail) | Aggressive, byte-identical across retries |
| **Google Search AI** | Full access | Full access | Full access | Fresh on each query |
| **Direct curl** | Full HTML correct | All `<a href>` present | All 200 | No cache |
| **WebFetch (Cursor)** | Loads, links stripped from tables | Text visible, URLs stripped | Full access | Light caching |

## Three Layers of the Problem

### Layer 1: Content Structure (FIXED)
Tables with links inside cells. HTML is valid, but HTML-to-text/markdown conversion
tools strip link targets from table cells, leaving only the text.

**Fix**: Ordered lists (`1. **[Title](url)** — description`). Links survive text extraction.

### Layer 2: Structured Data (FIXED)
No machine-readable index of child pages in structured data.

**Fix**: JSON-LD `hasPart` arrays on philosophy, thesis, and story section pages.
Every child page URL is now in structured data parseable without DOM traversal.

### Layer 3: Pipeline Topology (FIXED, AAR filed)
Caddy served from a stale checkout. Even after fixing layers 1-2, the live site
didn't reflect changes because the build pipeline targeted the wrong directory.

**Fix**: Rebuilt in correct serving directory. AAR filed for permanent resolution.

## Agent Diagnostic Accuracy

| Agent Claim | Actual Cause | Notes |
|-------------|-------------|-------|
| "Table rows not present in server HTML" | Rows present, links stripped by tool | Correct symptom, wrong diagnosis |
| "Likely JS hydration" | Pure static HTML (Zola SSG, zero JS for content) | Reasonable inference, but site has no client-side content injection |
| "Architecture page: full fetch failure" | Tool-side URL allowlisting | Architecture loads fine via curl and other agents |
| "Leaf page fetch failures inconsistent" | Agent correctly flags as possibly tool-side | Good self-awareness of diagnostic uncertainty |

The agent's Issue 1 diagnosis (JS hydration) is understandable — "I see header but no data rows"
is classically a hydration symptom. But the actual cause (link stripping in table-to-text conversion)
is more subtle and more broadly applicable.

## Test Matrix for AI Accessibility

### Recommended test agents (minimum coverage)
1. **Claude (web_fetch)** — aggressive caching, strips links from tables
2. **Google Search AI** — full rendering, fresh on each query
3. **GPT (browse)** — unknown table behavior, test needed
4. **Perplexity** — unknown, test needed
5. **Raw HTTP (curl/wget)** — baseline, no conversion artifacts

### Test pages (high-value targets)
- `/philosophy/` — ordered list with 12+ links (was table, now list)
- `/story/` — ordered list with 3 links
- `/thesis/` — section listing with 18 chapters
- `/architecture/` — section listing with 22+ pages
- `/primals/` — taxonomy listing (Zola-generated)
- `/sitemap/` — full site navigation

### Verification checklist per agent
- [ ] Can discover child page URLs from section index
- [ ] Can follow discovered URLs to leaf pages
- [ ] JSON-LD `hasPart` parseable
- [ ] `sitemap.xml` parseable
- [ ] Content renders after `---` horizontal rules
- [ ] Ordered list links survive text extraction
- [ ] Taxonomy pages accessible

## Accessibility Principle

> AI on behalf of users solves issues for all sorts of capability ranges.

A blind developer using Claude to navigate primals.eco hits the same table-link
stripping that the review agent hit. A motor-impaired scientist using an AI assistant
to find the right essay hits the same cache behavior. Testing with AI agents IS
testing assistive technology — the agents ARE the assistive technology.

This is not a separate concern from WCAG compliance. It is the same concern viewed
through a different capability profile.

## References

- `SPOREPRINT_DUAL_CHECKOUT_AAR_136b.md` — pipeline divergence AAR
- Commit `9948650` — ordered lists + JSON-LD hasPart fix
- `specs/EVOLUTION_QUEUE.md` P2 — accessibility test matrix target
