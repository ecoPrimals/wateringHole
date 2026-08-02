# westGate Data Federation — Download Schedule

**Gate**: westGate (ZFS raidz1, 50.7 TB available)
**Connection**: 1 Gbps fiber (residential — avoid saturation)
**Policy**: Download in batches, off-peak preferred, never >80% sustained for >1h
**Every byte with provenance = latent value (zero egress at 10G LAN)**
**Updated**: Aug 2, 2026 10:50 EDT

---

## COMPLETED (on ZFS with full provenance)

| Dataset | Size | Files | Provenance | Source |
|---------|------|-------|-----------|--------|
| PDB mmCIF (full mirror) | 88 GB | 257,179 | Manifest + BLAKE3 | RCSB rsync |
| UniRef90 | 30 GB | 1 | FULL | UniProt FTP |
| LINCS L1000 Level 5 + metadata | 20 GB | 6 | FULL | NCBI GEO |
| ChEMBL 37 | 15 GB | 2 | FULL | EBI |
| PubChem (SMILES + InChI-Key + Synonym + Mass) | 11 GB | 5 | FULL | NCBI FTP |
| NOAA GHCND | 3.5 GB | 3 | FULL | NOAA |
| GTEx V8 expression | 2.4 GB | 4 | FULL | GTEx Portal |
| UniProt Swiss-Prot | 764 MB | 3 | FULL | UniProt FTP |
| PDB structures (506 individual) | 361 MB | 506 | FULL | RCSB |
| SILVA 138.1 (16S ref) | 188 MB | 1 | FULL | SILVA |
| ZINC20 SMILES (drug-like subset) | 160 MB | 110 | FULL | ZINC20 |
| USDA NASS Census 2017 | 132 MB | 1 | FULL | USDA |
| MassBank NIST reference spectra | 63 MB | 1 | FULL | MassBank |
| PhysioNet MIT-BIH | 22 MB | 1 | FULL | PhysioNet |
| AME2020 nuclear masses | 1.2 MB | 2 | FULL | IAEA/NDS |
| LTEE REL606 genome | 5.8 MB | 1 | FULL | NCBI |
| USGS earthquake catalog (monthly) | 2.1 MB | 1 | FULL | USGS |
| UniProt TrEMBL FASTA + DAT | 148 GB | 2 | FULL | UniProt FTP |
| PDB70 HHsearch profiles | 27 GB | 1 | FULL | MPI Bioinformatics |
| GEO SOFT (cancer curated) | 3.0 GB | 4 | FULL | NCBI GEO |
| TCGA Pan-Cancer (Xena) | 449 MB | 3 | FULL | UCSC Xena |
| PubChem BioAssay | 11 GB | 5 | FULL | NCBI FTP |
| NCBI Taxonomy | 74 MB | 1 | FULL | NCBI FTP |
| NCBI Gene (Info+GO+Acc) | 7.0 GB | 3 | FULL | NCBI FTP |
| RefSeq Human GRCh38 + GTF | 981 MB | 2 | FULL | NCBI FTP |
| Reactome pathways | 96 MB | 2 | FULL | Reactome |
| MONDO disease ontology | 103 MB | 1 | FULL | MONDO |
| Molecular Force Fields (CHARMM36) | 1.1 MB | 1 | FULL | MacKerell Lab |
| PhysioNet PTB-XL | 1.5 GB | 1 | FULL | PhysioNet |
| NF Data Portal — NF1 drug screen + NF2 kinomics | 666 MB | 658 | FULL | Synapse |
| **TOTAL COMPLETE** | **~356 GB** | **~259K** | | |

---

## IN PROGRESS

None currently running — all in-flight downloads completed.

---

## REMAINING — Batch 2/3 (this week)

| Dataset | Est. Size | Priority | Spring/Garden | Notes |
|---------|-----------|----------|---------------|-------|
| GEO SOFT (curated subset) | ~50 GB | P1 | wetSpring | API crawl |
| PubChem BioAssay full SDF | ~15 GB | P2 | healthSpring | FTP |
| BRENDA enzyme kinetics | ~2 GB | P2 | hotSpring | Requires registration |
| EPA CompTox PFAS | ~1 GB | P1 | wetSpring PFAS | Needs browser session |
| BindingDB | ~1 GB | P2 | healthSpring | Needs browser session |
| NIST PFAS Reference Data | ~500 MB | P1 | wetSpring PFAS | |
| EcoCyc E. coli metabolism | ~1 GB | P2 | hotSpring | Requires license |
| Dryad LTEE fitness data | <1 GB | P1 | wetSpring lithoSpore | DOI changed |
| **Batch 2/3 remaining** | **~72 GB** | | | |

## Batch 4 — Over 2 weeks

| Dataset | Est. Size | Priority | Spring/Garden |
|---------|-----------|----------|---------------|
| TCGA (expression + clinical) | ~200 GB | P1 | wetSpring, healthSpring |
| AmeriFlux eddy covariance | ~10 GB | P2 | airSpring |
| IRIS FDSN catalogs | ~2 GB | P1 | groundSpring |
| **Batch 4 total** | **~212 GB** | | |

## Batch 5 — Month-scale

| Dataset | Est. Size | Priority | Spring/Garden |
|---------|-----------|----------|---------------|
| HMP Phase II (gut microbiome) | ~500 GB | P2 | wetSpring |
| Cell x Gene (scRNA-seq) | ~500 GB | P3 | wetSpring |
| Earth Microbiome Project | ~200 GB | P2 | wetSpring |
| MalariaGEN Pf6 | ~50 GB | P2 | wetSpring ABG |
| AlphaFold DB v4 | ~23 TB | P2 | neuralSpring |
| NCBI SRA (curated BioProjects) | ~2 TB | P2 | wetSpring |
| SalmoBase genomes | ~20 GB | P2 | wetSpring ABG |
| ERA5-Land (Copernicus) | ~3 TB | P3 | airSpring |
| **Batch 5 total** | **~29 TB** | | |

---

## Bandwidth Management

- 1 Gbps theoretical = ~120 MB/s actual
- Residential: other users on same connection
- Policy: max 80% sustained (~96 MB/s) during off-peak, 50% during peak
- Large downloads (>100 GB): schedule overnight/weekends
- Small downloads (<10 GB): anytime, invisible impact
- Current: 3 concurrent downloads (TrEMBL FASTA + DAT + PDB70)
- Monitor: `nload` or `iftop` during large transfers

## Running Total Projection

| Milestone | Cumulative | % of ZFS | When |
|-----------|-----------|----------|------|
| Current (complete) | ~356 GB | 0.70% | Done |
| After Batch 2/3 | ~428 GB | 0.84% | This week |
| After Batch 4 | ~640 GB | 1.26% | +2 weeks |
| After Batch 5 | ~30 TB | 59% | +1 month |

Even at full capacity, we use ~60% of ZFS. The pool can grow (more HDDs) and
the data grows in latent value — every byte is one less egress charge, one more
dataset available at 10G to the mesh.
