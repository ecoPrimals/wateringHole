# westGate Data Federation — Download Schedule

**Gate**: westGate (ZFS raidz1, 50.7 TB available)
**Connection**: 1 Gbps fiber (residential — avoid saturation)
**Policy**: Download in batches, off-peak preferred, never >80% sustained for >1h
**Every byte with provenance = latent value (zero egress at 10G LAN)**
**Updated**: Aug 2, 2026 13:15 EDT

---

## COMPLETED (on ZFS with full provenance)

| Dataset | Size | Files | Provenance | Source |
|---------|------|-------|-----------|--------|
| UniProt TrEMBL FASTA + DAT | 110 GB | 1 | FULL | UniProt FTP |
| PDB mmCIF (full mirror) | 88 GB | 257,179 | Manifest + BLAKE3 | RCSB rsync |
| UniRef90 | 68 GB | 2 | FULL | UniProt FTP |
| AlphaFold v6 (10 model species) | 28 GB | 10 | FULL | EBI FTP |
| PDB70 HHsearch profiles | 27 GB | 1 | FULL | MPI Bioinformatics |
| LINCS L1000 Level 5 + metadata | 20 GB | 6 | FULL | NCBI GEO |
| ChEMBL 37 | 15 GB | 2 | FULL | EBI |
| TCGA Pan-Cancer (Xena + GDC) | 15 GB | 9 | FULL | UCSC Xena / GDC |
| InterPro protein-domain annotations | 13 GB | 1 | FULL | EBI FTP |
| PubChem (SMILES + InChI-Key + Synonym + Mass) | 11 GB | 5 | FULL | NCBI FTP |
| PubChem BioAssay | 11 GB | 5 | FULL | NCBI FTP |
| NCBI Gene (Info+GO+Acc) | 7.0 GB | 3 | FULL | NCBI FTP |
| COSMIC v104 (CGC + Genome/Targeted Screens + Breakpoints) | 4.7 GB | 5 | FULL | Sanger Institute |
| NOAA GHCND | 3.5 GB | 3 | FULL | NOAA |
| GEO SOFT (cancer curated original) | 3.0 GB | 11 | FULL | NCBI GEO |
| GTEx V8 expression | 2.4 GB | 4 | FULL | GTEx Portal |
| PhysioNet PTB-XL | 1.8 GB | 1 | FULL | PhysioNet |
| dbSNP common variants (GRCh38) | 1.5 GB | 1 | FULL | NCBI FTP |
| RefSeq Human GRCh38 + GTF | 981 MB | 2 | FULL | NCBI FTP |
| UniProt Swiss-Prot | 764 MB | 3 | FULL | UniProt FTP |
| NF Data Portal — NF1 drug screen + NF2 kinomics | 666 MB | 658 | FULL | Synapse |
| BindingDB (All + Assays + rsid mappings, 202608) | 583 MB | 3 | FULL | BindingDB |
| GEO SOFT expanded (HCC + Renal + IPF + Bladder + Lung) | 564 MB | 9 | FULL | NCBI GEO |
| Pfam-A domain HMM profiles | 399 MB | 1 | FULL | EBI FTP |
| PDB structures (506 individual) | 361 MB | 506 | FULL | RCSB |
| SILVA 138.1 (16S ref) | 188 MB | 1 | FULL | SILVA |
| ClinVar clinical variants (GRCh38) | 184 MB | 1 | FULL | NCBI FTP |
| ZINC20 SMILES (drug-like subset) | 160 MB | 110 | FULL | ZINC20 |
| USDA NASS Census 2017 | 132 MB | 1 | FULL | USDA |
| MONDO disease ontology | 103 MB | 1 | FULL | MONDO |
| Reactome pathways | 96 MB | 3 | FULL | Reactome |
| STRING v12.0 human protein interactions | 80 MB | 1 | FULL | STRING-DB |
| NCBI Taxonomy | 72 MB | 1 | FULL | NCBI FTP |
| MassBank NIST reference spectra | 63 MB | 1 | FULL | MassBank |
| Ensembl GRCh38.113 human GTF | 62 MB | 1 | FULL | Ensembl FTP |
| PDB mmCIF manifests | 35 MB | 3 | FULL | RCSB |
| Reactome pathways | 24 MB | 3 | FULL | Reactome |
| PhysioNet MIT-BIH | 22 MB | 1 | FULL | PhysioNet |
| Gene Ontology (OBO + human annotations) | 20 MB | 2 | FULL | GO Consortium |
| HGNC gene nomenclature | 7.0 MB | 1 | FULL | HGNC (GCS) |
| PDBe SIFTS PDB-UniProt mappings | 5.8 MB | 1 | FULL | EBI FTP |
| LTEE REL606 genome | 5.8 MB | 1 | FULL | NCBI |
| USGS earthquake catalog (monthly) | 2.4 MB | 2 | FULL | USGS |
| KEGG (pathways + compounds + reactions + enzymes) | 1.9 MB | 5 | FULL | KEGG REST |
| Molecular Force Fields (CHARMM36) | 1.1 MB | 2 | FULL | MacKerell Lab |
| AME2020 nuclear masses | 641 KB | 2 | FULL | IAEA/NDS |
| BRENDA enzyme kinetics (Km, kcat, Ki for 20 EC classes) | 633 KB | 74 | FULL | BRENDA SOAP API |
| **TOTAL COMPLETE** | **~435 GB** | **~258K** | | **47 datasets** |

---

## IN PROGRESS

None currently running — all in-flight downloads completed.

---

## REMAINING — Batch 2/3 (this week)

| Dataset | Est. Size | Priority | Spring/Garden | Notes |
|---------|-----------|----------|---------------|-------|
| COSMIC Resistance Mutations + VCF | ~2 GB | P2 | healthSpring | Some paths give 500 |
| EPA CompTox PFAS | ~1 GB | P1 | wetSpring PFAS | Needs browser session |
| NIST PFAS Reference Data | ~500 MB | P1 | wetSpring PFAS | |
| EcoCyc E. coli metabolism | ~1 GB | P2 | hotSpring | Requires license |
| Dryad LTEE fitness data | <1 GB | P1 | wetSpring lithoSpore | DOI changed |
| BRENDA full flat file (remaining enzymes) | ~2 GB | P3 | hotSpring | SOAP API working |
| CCLE/DepMap (expression + CRISPR) | ~5 GB | P1 | healthSpring | Needs browser/figshare |
| HMDB metabolites | ~3 GB | P2 | hotSpring | Cloudflare protection |
| DisGeNET gene-disease | ~1 GB | P2 | healthSpring | Needs registration |
| Open Targets associations | ~5 GB | P2 | healthSpring | Needs parquet URL |
| **Batch 2/3 remaining** | **~21 GB** | | | |

## Batch 4 — Over 2 weeks

| Dataset | Est. Size | Priority | Spring/Garden |
|---------|-----------|----------|---------------|
| AmeriFlux eddy covariance | ~10 GB | P2 | airSpring |
| IRIS FDSN catalogs | ~2 GB | P1 | groundSpring |
| ERA5-Land (Copernicus) | ~100 GB subset | P2 | airSpring | Needs licence accept |
| **Batch 4 total** | **~112 GB** | | |

## Batch 5 — Month-scale

| Dataset | Est. Size | Priority | Spring/Garden |
|---------|-----------|----------|---------------|
| HMP Phase II (gut microbiome) | ~500 GB | P2 | wetSpring |
| Cell x Gene (scRNA-seq) | ~500 GB | P3 | wetSpring |
| Earth Microbiome Project | ~200 GB | P2 | wetSpring |
| MalariaGEN Pf6 | ~50 GB | P2 | wetSpring ABG |
| AlphaFold DB v6 (full — 214M structures) | ~23 TB | P2 | neuralSpring |
| NCBI SRA (curated BioProjects) | ~2 TB | P2 | wetSpring |
| SalmoBase genomes | ~20 GB | P2 | wetSpring ABG |
| ERA5-Land full (Copernicus) | ~3 TB | P3 | airSpring |
| **Batch 5 total** | **~29 TB** | | |

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
| Current (complete) | ~435 GB | 0.86% | Done |
| After Batch 2/3 | ~456 GB | 0.90% | This week |
| After Batch 4 | ~568 GB | 1.12% | +2 weeks |
| After Batch 5 | ~30 TB | 59% | +1 month |

Even at full capacity, we use ~60% of ZFS. The pool can grow (more HDDs) and
the data grows in latent value — every byte is one less egress charge, one more
dataset available at 10G to the mesh.

## Credential Vault

Encrypted API keys stored on golgiBody in `wateringHole/vault/`:
- NCBI, Synapse, Copernicus CDS, COSMIC, BRENDA
- AES-256 encrypted, ecosystem passphrase
- Any gate can clone and decrypt to bootstrap data access
