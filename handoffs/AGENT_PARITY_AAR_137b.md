# AAR — Agent Content Parity (Wave 137b)

**Date**: Jul 13, 2026  
**Reported by**: External Claude agent acting as assistive layer  
**Owner**: sporePrint  
**Status**: RESOLVED — root cause identified as agent-side, mitigations deployed

---

## Summary

An external AI agent reported that every distinct URL on primals.eco returned
identical `llms.txt` content when accessed through its fetch tool. The agent
correctly framed this as an accessibility failure: a user asking their agent to
"read me The Human Search" would silently receive the site overview instead.

## Investigation

### Root Cause: NOT on our infrastructure

Caddy Caddyfile inspection: **zero UA-sniffing rules**. Pure `file_server`
serving static files. No content negotiation, no rewrites, no bot detection.

Direct verification:
```
curl -A "ClaudeBot/1.0" https://primals.eco/philosophy/the-human-search/
→ <title>The Human Search — How Everything Learns...</title>  ✓

curl -A "Mozilla/5.0 Chrome/125" https://primals.eco/philosophy/the-human-search/
→ <title>The Human Search — How Everything Learns...</title>  ✓
```

Both UAs receive identical, correct HTML. 11 paths tested, 11 pass.

### Probable Agent-Side Root Cause

Every page includes `<link rel="alternate" type="text/plain" href=".../llms.txt">`.
The agent's `web_fetch` tool likely follows the `rel="alternate"` link for
`text/plain` content negotiation, returning `llms.txt` instead of the HTML page.
This is a reasonable tool behavior but creates silent wrong-content delivery.

## Mitigations Deployed

1. **`llms.txt` self-identification header** — Added canonical URL and explicit
   warning that if you requested a different URL and received this content, your
   fetch tool is following the alternate link, not the page. Makes wrongness
   detectable.

2. **`validate_agent_parity.sh` dogfood test** — Tests 11 sample URLs with both
   browser and bot UAs, asserts `<title>` and `<link rel=canonical>` match.
   Catches any future UA-based content substitution.

3. **Slug provenance fix** — `70_papers_one_stack.md` title was "175+ Papers"
   but URL slug was `/story/70-papers-one-stack/`. Added `slug = "175-papers-one-stack"`
   to resolve the drift.

## Lessons Learned

- **`<link rel="alternate">` can cause silent content substitution** in agent
  fetch tools. The tag is correct HTML and helps discovery, but agents that
  prefer `text/plain` may follow it unconditionally.
- **Self-identifying response content** (canonical URL at the top of `llms.txt`)
  lets agents detect when they've received the wrong document.
- **Dogfood testing with bot UAs** is a cheap, high-value addition to any
  accessibility test matrix. We added it permanently.
- **The agent's framing was correct** even though the bug was on their side:
  our site's accessibility posture includes making agent mistakes detectable
  and recoverable. That's our responsibility regardless of fault.

## Test Evidence

```
=== Agent Parity Test ===
Base: https://primals.eco — Paths: 11
  PASS  /
  PASS  /philosophy/
  PASS  /philosophy/the-human-search/
  PASS  /science/
  PASS  /thesis/
  PASS  /thesis/01-introduction/
  PASS  /story/
  PASS  /architecture/
  PASS  /methodology/
  PASS  /llms.txt
  PASS  /site-index/
=== Results: 11 passed, 0 failed ===
```

---

*Filed by sporePrint team. Upstream: agent tool teams should consider scoping
`rel="alternate"` following to explicit user opt-in rather than automatic
content-type preference.*
