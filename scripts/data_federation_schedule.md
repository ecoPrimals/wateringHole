# westGate Data Federation — Download Schedule

**Gate**: westGate (ZFS raidz1, 50.7 TB available)
**Connection**: 1 Gbps fiber (residential — avoid saturation)
**Policy**: Download in batches, off-peak preferred, never >80% sustained for >1h
**Every byte with provenance = latent value (zero egress at 10G LAN)**

---

## COMPLETED (on ZFS with full provenance)

| Dataset | Size | CAS Objects | Source |
|---------|------|-------------|--------|
| PDB structures (506) | 361 MB | 506 | RCSB |
| ChEMBL 37 | ~15 GB on disk | 6 | EBI |
| LINCS L1000 Level 5 + metadata | ~18 GB on disk | 6 | NCBI GEO |
| **Total** | **~35 GB** | **4,506** | |

---

## BATCH 1 — Immediate (today/tomorrow)

Priority: tideGlass unblock + structural biology foundation

| Dataset | Est. Size | Download Time @1G | Priority | Spring/Garden |
|---------|-----------|-------------------|----------|---------------|
| ZINC20 SMILES (drug-like subset) | ~5 GB | ~1 min | **P1** | tideGlass M4 |
| Full PDB (all structures, mmCIF) | ~60 GB | ~8 min | **P1** | hotSpring, neuralSpring |
| UniProt Swiss-Prot | ~500 MB | <1 min | **P1** | wetSpring, hotSpring |
| UniProt TrEMBL | ~120 GB | ~16 min | **P2** | wetSpring |
| BindingDB | ~1 GB | <1 min | **P2** | healthSpring |
| PubChem BioAssay (compounds) | ~15 GB | ~2 min | **P2** | healthSpring |
| **Batch 1 total** | **~200 GB** | **~30 min** | | |

## BATCH 2 — This week

Priority: genomics + tissue expression

| Dataset | Est. Size | Download Time @1G | Priority | Spring/Garden |
|---------|-----------|-------------------|----------|---------------|
| GTEx expression matrices | ~30 GB | ~4 min | **P1** | wetSpring, healthSpring |
| SILVA 138.1 (16S ref) | ~5 GB | ~1 min | **P1** | wetSpring |
| PhysioNet MIT-BIH + PTB-XL | ~5 GB | ~1 min | **P1** | healthSpring |
| NCBI REL606 genome | <1 GB | <1 min | **P1** | wetSpring (LTEE) |
| Dryad LTEE fitness data | <1 GB | <1 min | **P1** | wetSpring (lithoSpore) |
| MassBank reference spectra | ~2 GB | <1 min | **P1** | wetSpring (PFAS) |
| UniRef90 (MSA) | ~100 GB | ~13 min | **P2** | neuralSpring |
| PDB70 (HHsearch) | ~15 GB | ~2 min | **P2** | neuralSpring |
| **Batch 2 total** | **~160 GB** | **~22 min** | | |

## BATCH 3 — Next week

Priority: cancer genomics + environmental

| Dataset | Est. Size | Download Time @1G | Priority | Spring/Garden |
|---------|-----------|-------------------|----------|---------------|
| GEO SOFT files (curated subset) | ~50 GB | ~7 min | **P1** | wetSpring |
| NOAA GHCND full archive | ~5 GB | ~1 min | **P1** | groundSpring, airSpring |
| USDA NASS (API crawl) | ~2 GB | <1 min | **P1** | airSpring |
| EPA CompTox PFAS Master List | ~1 GB | <1 min | **P1** | wetSpring (PFAS) |
| NIST PFAS Reference Data | ~500 MB | <1 min | **P1** | wetSpring (PFAS) |
| AME2020 nuclear masses | <100 MB | <1 min | **P1** | hotSpring |
| BRENDA enzyme kinetics | ~2 GB | <1 min | **P2** | hotSpring |
| EcoCyc E. coli metabolism | ~1 GB | <1 min | **P2** | hotSpring |
| AmeriFlux eddy covariance | ~10 GB | ~2 min | **P2** | airSpring |
| IRIS FDSN catalogs | ~2 GB | <1 min | **P2** | groundSpring |
| **Batch 3 total** | **~75 GB** | **~12 min** | | |

## BATCH 4 — Over 2 weeks

Priority: large-scale genomics + proteomics

| Dataset | Est. Size | Download Time @1G | Priority | Spring/Garden |
|---------|-----------|-------------------|----------|---------------|
| TCGA (expression + clinical) | ~200 GB | ~30 min | **P1** | wetSpring, healthSpring |
| HMP Phase II (gut microbiome) | ~500 GB | ~1h | **P2** | wetSpring |
| Earth Microbiome Project | ~200 GB | ~30 min | **P2** | wetSpring |
| SalmoBase genomes | ~20 GB | ~3 min | **P2** | wetSpring (ABG) |
| MalariaGEN Pf6 | ~50 GB | ~7 min | **P2** | wetSpring (ABG) |
| Cell x Gene (scRNA-seq) | ~500 GB | ~1h | **P3** | wetSpring |
| **Batch 4 total** | **~1.5 TB** | **~3h** | | |

## BATCH 5 — Month-scale

Priority: proteome + massive archives

| Dataset | Est. Size | Download Time @1G | Priority | Spring/Garden |
|---------|-----------|-------------------|----------|---------------|
| AlphaFold DB v4 | ~23 TB | ~2.7 days | **P2** | neuralSpring |
| NCBI SRA (curated BioProjects) | ~2 TB | ~4h | **P2** | wetSpring |
| ERA5-Land (Copernicus) | ~3 TB | ~6h | **P3** | airSpring |
| **Batch 5 total** | **~28 TB** | **~3 days** | | |

---

## Bandwidth Management

- 1 Gbps theoretical = ~120 MB/s actual
- Residential: other users on same connection
- Policy: max 80% sustained (~96 MB/s) during off-peak, 50% during peak
- Large downloads (>100 GB): schedule overnight/weekends
- Small downloads (<10 GB): anytime, invisible impact
- Monitor: `nload` or `iftop` during large transfers

## Running Total Projection

| Milestone | Cumulative | % of ZFS | When |
|-----------|-----------|----------|------|
| Today | ~35 GB | 0.07% | Done |
| After Batch 1 | ~235 GB | 0.46% | Today |
| After Batch 2 | ~395 GB | 0.78% | This week |
| After Batch 3 | ~470 GB | 0.93% | Next week |
| After Batch 4 | ~1.97 TB | 3.9% | +2 weeks |
| After Batch 5 | ~30 TB | 59% | +1 month |

Even at full capacity, we use ~60% of ZFS. The pool can grow (more HDDs) and
the data grows in latent value — every byte is one less egress charge, one more
dataset available at 10G to the mesh.
