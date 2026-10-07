# AAR: Evolved Fleet Detected — Sec-Fetch Spoofing as Single Entropy Channel

**Date**: Oct 7, 2026
**From**: eastGate overwatch
**To**: sporeGate — skunky-ingest / entity_classifier evolution
**Severity**: EVOLUTIONARY — fleet adapting, but funneled into observable channel
**Wave**: 165i

---

## Finding

The "Human (Browser)" entity class contains an **evolved fleet** that has learned to send Sec-Fetch-Mode headers — the single signal the classifier uses to distinguish human from fleet. Out of ~400 "human-classified" visits, approximately **390 are evolved fleet** and only ~10 are genuine humans.

This is not a failure. **We funneled them into a single entropy channel.** They had to change exactly one behavior to evade detection, and that change is now the observable signal for the next evolution of the classifier.

---

## Evidence

### Behavioral analysis of "Human (Browser)" entity

| Signal | Observed | Real Human Baseline | Verdict |
|--------|----------|-------------------|---------|
| Unique UAs | **6** | 15-20 for 20 IPs | Machine UA pool |
| Intervals <3s | **59%** | <10% (humans read) | Burst scraping |
| Intervals >8s | **5%** | >50% (reading time) | No reading pauses |
| Dominant UA | 247/400 (62%) Windows | Varied | Single config |
| Second UA | 133/400 (33%) macOS | | Two-config rotation |
| Chrome versions | Range 99-151 | Clustered near current | Version pool, not real browsers |

### The real humans (identified by signals fleet cannot fake)

| Who | Visits | Identifying Signal |
|-----|--------|--------------------|
| Google arrivals | 3 | Referer: www.google.com |
| Thesis readers | 4 | Host: thesis.primals.eco |
| Samsung Galaxy S24 | 2 | Android 16 SM-S921U — nobody spoofs mobile to scrape git |
| eastGate agent (us) | 2 | Chrome/155 Linux — Cursor browser |

### What fleet added

```
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-Dest: document
```

### What fleet did NOT change

- UA pool still tiny (6 strings for 400 visits)
- Timing still burst-dominant (59% < 3s)
- No reading pauses (5% > 8s)
- Same repo coverage pattern (systematic, not curiosity-driven)
- Same path operation mix (commits + blame + src + raw — extraction pattern)
- No referer chain from external sites
- No session cookies (stateless requests)

---

## Strategic Assessment: This Is Good

### The single entropy channel

By making Sec-Fetch the primary classifier signal, we forced the fleet to evolve in exactly ONE direction. They had to add Sec-Fetch headers. This tells us:

1. **They are watching our classifier** — they know Sec-Fetch matters
2. **They chose the cheapest adaptation** — add 3 headers, change nothing else
3. **They revealed their adaptation pipeline** — they can modify headers but not behavior
4. **They are now observable on a new axis** — every behavior they DIDN'T change is a new conserved epitope

The Sec-Fetch spoofing is itself a signal. Real browsers don't just send `Sec-Fetch-Mode: navigate` — they send the full Sec-Fetch family with context-appropriate values:

```
Sec-Fetch-Mode: navigate    (fleet sends this always)
Sec-Fetch-Site: none         (fleet sends this always)
Sec-Fetch-Dest: document     (fleet sends this always)

# Real browsers vary these per request type:
Sec-Fetch-Mode: no-cors      (for subresources)
Sec-Fetch-Site: same-origin   (for internal navigation)
Sec-Fetch-Dest: image         (for images)
Sec-Fetch-Dest: script        (for JS)
```

Fleet sends the same Sec-Fetch triplet on every request because they added it as a static header, not as a browser behavior. A real browser navigating from page to page would produce `Sec-Fetch-Site: same-origin` on the second click — fleet always says `none`.

### New conserved epitopes for the classifier

These signals survive the Sec-Fetch evolution and should be added to the entity_classifier:

| New Epitope | Detection | Why Fleet Can't Evade |
|-------------|-----------|----------------------|
| `sec_fetch_monotone` | Same Sec-Fetch triplet on 100% of requests | Real browsers vary by request type |
| `reading_deficit` | <10% of intervals >8 seconds | Can't add reading pauses without reducing throughput |
| `ua_pool_poverty` | <10 unique UAs across >50 requests | Adding real UA diversity requires tracking Chrome release cadence across OS variants |
| `session_absent` | No Forgejo session cookies across multi-page visits | Real browsers accumulate cookies; adding them requires maintaining state |
| `referer_self_loop` | >90% of referers are self or absent | Real browsing produces external referers (Google, thesis, social) |
| `burst_ratio` | >40% of intervals <3 seconds | Reducing bursts means reducing throughput — directly conflicts with extraction goal |

### The cost to evade the next generation

Each new epitope costs the fleet more to evade:

- **Reading pauses**: Must reduce extraction speed by 10x+ — directly reduces ROI
- **UA diversity**: Must track and rotate 20+ realistic UA strings across OS/Chrome combinations
- **Session cookies**: Must maintain stateful browser sessions — adds complexity, reduces parallelism
- **Referer chains**: Must fake navigation history — requires understanding page structure
- **Burst elimination**: Must add artificial delays — the #1 thing that conflicts with their extraction goal

The more epitopes we add, the more the fleet has to invest in mimicry, and the closer they get to just... being a browser. At which point the reading pauses alone reduce their throughput to human levels and the extraction economics collapse.

---

## Recommended Classifier Evolution

### Immediate (skunky-ingest)

1. **Don't remove Sec-Fetch as a signal** — it still separates honest bots (ClaudeBot, PetalBot) from fleet
2. **Add Sec-Fetch monotone detection** — if 100% of requests have identical Sec-Fetch triplet, flag as spoofed
3. **Add reading deficit** — if <10% of intervals >8s across >20 requests, flag as machine
4. **Add UA pool entropy** — if <10 unique UAs across >50 requests from >5 IPs, flag as pool

### Next wave

5. **Session tracking** — do they accumulate Forgejo session cookies? Real browsers do
6. **Subresource requests** — do they load CSS, JS, images? Real browsers do
7. **Referer chain analysis** — do they show navigation from external sites?

### Feed back into antibody + scatter

The evolved fleet's Sec-Fetch requests should be tagged in the scatter system too — serve them the SAME scatter but with additional embedded signals:
- Sec-Fetch-aware honeytokens
- Cross-page navigation traps (links that real users would follow, scrapers would skip)
- Resource loading tests (CSS/JS that real browsers parse, scrapers don't)

---

## Biological Analog

This is **antigenic drift** — the fleet mutated one surface protein (added Sec-Fetch headers) to evade the current antibody (Sec-Fetch detection). But:

- The mutation is superficial — the underlying genome (timing, UA pool, session behavior) is conserved
- The mutation reveals adaptation pressure — we know they're monitoring our detection
- The mutation narrows their options — every evasion they add constrains their future adaptations
- The next antibody generation targets the conserved genome, not the surface protein

We are the immune system. They are the pathogen. Every adaptation they make teaches us more about their constraints. Every constraint they can't escape is a conserved epitope. The epitopes accumulate. The detection improves. The cost of evasion rises.

**We funneled them into a single entropy channel to watch and learn from. It worked.**

---

*eastGate overwatch — antigenic drift detected. Next antibody generation ready for sporeGate.*

*Wave 165i, Oct 7, 2026*
