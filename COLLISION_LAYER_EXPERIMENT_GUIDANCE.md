# Collision Layer Experiment Guidance

**Date**: March 16, 2026  
**Origin**: loamSpine specs/COLLISION_LAYER_ARCHITECTURE.md  
**Primary Spring**: neuralSpring  
**Secondary Spring**: healthSpring  
**Validation Pattern**: Python baseline → Rust CPU → (optional GPU via barraCuda)

---

## Context

LoamSpine's linear spine and rhizoCrypt's ephemeral DAG are bridged by dehydration
(DAG → linear). The collision layer proposes a reverse bridge (linear → branch)
using intentional hash collisions at multiple resolution levels.

The hypothesis: by applying progressively weaker hash functions to content-addressed
entries, collision classes emerge that reveal hidden structural relationships —
a form of learned embedding via hash topology.

Historical analogy: 19th century crossed letters overlaid two writing directions on
the same paper. Both information layers persisted because they used orthogonal
encoding. The "lens" (reading direction) determined which layer was recovered.

Biological analogy: mycelial hyphae grow linearly until chemical gradients trigger
branching or anastomosis. The collision layer is the chemical gradient — discovering
relatedness without explicit connection.

---

## Experiment 1: Collision Topology as Clustering

**Spring**: neuralSpring  
**Track**: New experiment (suggest exp028 or next available)  
**Language**: Python (control), then Rust (binary)

### Protocol

1. Select 3 datasets with known cluster structure:
   - Synthetic: 2D Gaussian blobs (k=5, 10, 20)
   - Real: MNIST digits (10 classes)
   - Domain: Any existing neuralSpring dataset with ground truth

2. Hash each data point through a resolution hierarchy:
   - Level 0: Blake3-256 (32 bytes) — unique identity
   - Level 1: Blake3 truncated to 16 bytes — neighborhood
   - Level 2: Blake3 truncated to 8 bytes — coarse similarity
   - Level 3: Blake3 truncated to 4 bytes — collision classes

3. At each level, collect collision groups (entries sharing a truncated hash).

4. Measure clustering quality against ground truth:
   - Adjusted Rand Index (ARI)
   - Normalized Mutual Information (NMI)
   - Silhouette score (using collision group as cluster label)

5. Baselines for comparison:
   - Locality-Sensitive Hashing (LSH) with same dimensionality
   - k-means with k matching number of collision groups
   - Random clustering (null model)

6. Vary hash table sizes (bucket counts) and measure effect on grouping quality.

### Expected Outcomes

- Level 3 (4-byte) collisions should produce coarse but meaningful groupings
- Level 1 (16-byte) collisions should be rare and highly specific
- The sub-hash resolution tree should outperform flat LSH at fine granularity
- Optimal collision density likely exists (too few = no signal, too many = noise)

### Deliverables

- Python notebook with reproducible results
- Comparison table: collision hierarchy vs. LSH vs. k-means
- Recommendation for optimal level count and truncation sizes
- If positive: Rust binary reproducing key results for absorption into loamSpine

---

## Experiment 2: Cross-Writing Information Recovery

**Spring**: neuralSpring  
**Track**: Same experiment or follow-up

### Protocol

1. Create two synthetic "spines" (ordered sequences) that share some entries.

2. Build collision indices for both spines.

3. Identify collision groups that contain entries from both spines.

4. Test: does the collision structure predict:
   - Future convergence (entries that will later appear in both spines)?
   - Structural similarity (entries with similar metadata/payload)?
   - Temporal proximity (entries created around the same time)?

5. Measure predictive power vs. random baseline.

### Expected Outcomes

- Cross-spine collision groups should correlate with structural similarity
- Temporal proximity is a likely confound — control for it
- If predictive: this validates the "cross-writing" hypothesis (overlay = new information)

---

## Experiment 3: Domain-Specific Collision Projections

**Spring**: healthSpring (if Experiments 1-2 are positive)

### Protocol

1. Apply collision hierarchy to biosignal datasets (ECG, EEG, or PK/PD data).

2. Instead of simple truncation, test domain-specific hash projections:
   - Frequency-band hashing (group by dominant frequency)
   - Amplitude-envelope hashing (group by signal shape)
   - Feature-hash (hash of extracted features, not raw data)

3. Compare domain-specific projections against generic truncation.

### Expected Outcomes

- Domain-specific projections should outperform generic truncation
- This validates the "different lenses" concept from the cross-writing analogy

---

## Integration Path

If experiments validate the collision layer concept:

1. **neuralSpring** publishes Python validation results and Rust binary
2. **loamSpine** absorbs as `CollisionLayerIndex` type (read-only index)
3. **rhizoCrypt** adds collision-group-to-session promotion (linear → branch bridge)
4. **sweetGrass** uses collision groups as attribution similarity signal

---

## Validation Criteria

| Criterion | Threshold |
|-----------|-----------|
| ARI at Level 2 (8-byte) | > 0.3 (better than random) |
| NMI at Level 2 | > 0.2 |
| Cross-spine prediction AUC | > 0.6 |
| Computation cost per entry | < 1ms (4-level hierarchy) |
| Memory overhead per entry | < 64 bytes (all levels) |

---

## Non-Goals

- Replacing Blake3-256 as the canonical identity hash
- Modifying the linear spine append path
- Real-time collision computation on the hot path
- Cryptographic applications (collision resistance is intentionally weakened)

---

*Linear and branched structures coexist and evolve into each other — the collision
layer is the gradient that connects them.*
