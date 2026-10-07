# AAR: Evolved Fleet — Sec-Fetch Spoofing Detected

**Date**: Oct 7, 2026
**From**: eastGate overwatch
**To**: sporeGate ops — skunky-ingest entity_classifier
**Severity**: CLASSIFIER EVOLUTION NEEDED
**Wave**: 165i

---

## Finding

The entity classified as "Human (Browser)" is **mostly not human**. An evolved fleet entity has learned to send `Sec-Fetch-Mode` headers, bypassing the primary signal the classifier uses to distinguish humans from fleet.

Of ~400 Sec-Fetch-present visits in the current log window, approximately **388 are an evolved scraper** and only **~12 are genuine humans**.

---

## Evidence

### Behavioral signals that betray the spoofing

| Signal | Observed | Expected (Real Humans) | Verdict |
|--------|----------|----------------------|---------|
| Unique UAs | **6** | 15-20 for 20 IPs | ❌ config pool |
| Intervals <3s | **59%** | <10% (humans read) | ❌ burst machine |
| Intervals >8s | **5%** | >50% (reading pauses) | ❌ no reading |
| Dominant UA | 247/400 (62%) Windows | varied | ❌ single config |
| Second UA | 133/400 (33%) macOS | varied | ❌ second config |
| Total UA pool | 2 UAs = 95% of traffic | wide distribution | ❌ fleet rotation |

### The smoking gun: timing distribution

```
  <3s (burst):     234 (59%)   ← machine behavior
  3-8s (regular):  147 (37%)   ← rate-limited pipeline
  >8s (human-like):  18 (5%)  ← almost no reading pauses
```

A real human takes 10-30 seconds to read a commit diff or source file. This entity visits a new page every 2.5 seconds on average. They're not reading — they're extracting.

### The real humans hiding in the noise

| Who | Visits | Evidence |
|-----|--------|----------|
| Google arrivals | 3 | Referer: `www.google.com` — organic search discovery |
| Thesis readers | 4 | Host: `thesis.primals.eco` — reading "Stomachs With No Eyes" |
| Samsung Galaxy S24 | 2 | Android 16, SM-S921U — nobody spoofs mobile UAs to scrape |
| eastGate agent (us) | 2 | Chrome/155 Linux — Cursor browser |
| curl test (us) | 1 | curl/7.81.0 with Sec-Fetch (our header test) |

**~12 real humans. ~388 evolved fleet.**

---

## What the Evolved Fleet Targets

Top paths (Sec-Fetch present):

| Path | Visits | Target |
|------|--------|--------|
| wateringHole/commits | 29 | Commit history |
| wateringHole/src | 27 | Source browsing |
| toadStool/commits | 19 | Commit history |
| toadStool/src | 14 | Source browsing |
| toadStool/raw | 13 | Raw file download |
| toadStool/blame | 8 | Author attribution |
| wateringHole/blame | 7 | Author attribution |
| songBird/blame | 3 | Author attribution |

Same behavior as Meta fleet: commits, src, raw, blame. Same author attribution interest. **They just added Sec-Fetch headers.**

All getting scatter because of the blanket routing — but the classifier is counting them as "Human" in the topology, which inflates the human count and masks the real humans.

---

## Proposed Classifier Evolution

### Second Thymic Layer: Behavioral Depth

Sec-Fetch presence should be a **necessary but not sufficient** signal for human classification. Add:

#### 1. UA Pool Entropy

```rust
// If <10 unique UAs account for >90% of "human" traffic, 
// reclassify as evolved_fleet
if human_ua_pool.len() < 10 && human_ua_pool.top_2_pct() > 0.90 {
    entity = Entity::EvolvedFleet;
}
```

#### 2. Reading Pause Ratio

```rust
// Real humans: >40% of intervals are >8 seconds (reading)
// Evolved fleet: <10% are >8 seconds
let reading_ratio = intervals.iter()
    .filter(|i| **i > 8000.0)
    .count() as f64 / intervals.len() as f64;

if reading_ratio < 0.15 {
    // Not reading — reclassifying
    entity = Entity::EvolvedFleet;
}
```

#### 3. Session Depth Analysis

Real humans browse 3-8 pages per session, then leave (session = gap >5min). Fleet systematically covers repos.

#### 4. Referer Chain Validation

```rust
// Real human referer patterns:
//   google.com → sporeprint → git (discovery chain)
//   (direct) → thesis → git (bookmark + explore)
//   (direct) → single repo → done (targeted visit)
//
// Fleet referer patterns:
//   git.primals.eco → git.primals.eco → git.primals.eco (self-referral loop)
```

### New Conserved Epitope: `sec_fetch_costume`

When an entity has Sec-Fetch PRESENT but fails behavioral validation:

```rust
ConservedEpitope {
    name: "sec_fetch_costume",
    description: "Sec-Fetch headers present but behavioral fingerprint is machine-like",
    frequency_pct: 97,  // 388/400
    detection: "UA entropy < threshold AND reading_ratio < 0.15",
    evasion_cost: "Must actually read pages (add 10-30s delays), diversify UA pool, 
                   simulate organic referer chains — increases scraping time 10-50x",
}
```

The evasion cost is brutal: to pass reading-pause detection, they'd need to slow their scraping by 10-50x. That's the immune system's design advantage — each detection layer forces the fleet to spend more time, which means more evidence, which means more detection.

---

## Impact on AAR_AGENT_SCATTER_CLASSIFICATION_GAP

This finding STRENGTHENS the agent scatter gap AAR. The current classifier can't distinguish:

1. **Real human** (3 Google visitors, thesis readers, Samsung phone)
2. **Evolved fleet** (388 visits with spoofed Sec-Fetch)
3. **Agent-on-behalf-of-human** (2 Cursor browser visits)

All three get classified as "Human (Browser)" today. The second thymic layer would separate them, enabling the scatter passthrough to work safely — only letting through entities with genuine reading pauses, diverse UAs, and organic referer chains.

---

*eastGate overwatch AAR — the fleet evolved. The thymus needs a second layer.*

*Wave 165i, Oct 7, 2026*
