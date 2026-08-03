# Data Federation — Blockers & Issues Log

**Gate**: westGate
**Started**: Aug 2, 2026
**Updated**: Aug 2, 2026 20:45 EDT

Track failures, user-intervention items, and issues to circle back to.

---

## NEEDS USER (registration, browser, licence acceptance)

| # | Dataset | Blocker | Action Required | Priority |
|---|---------|---------|----------------|----------|
| 1 | Copernicus ERA5 | Licence not accepted | Visit [ERA5 licence page](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels?tab=download#manage-licences), click Accept | P2 |
| 2 | DepMap/CCLE | Cloudflare bot protection | Download via browser from [DepMap portal](https://depmap.org/portal/download/all/), grab CCLE_expression.csv + CRISPRGeneEffect.csv | P1 |
| 3 | HMDB metabolites | Cloudflare bot protection | Download via browser from [HMDB downloads](https://hmdb.ca/downloads), grab hmdb_metabolites.zip (~3 GB) | P2 |
| 4 | DisGeNET | Requires free registration | Register at [DisGeNET](https://www.disgenet.org/signup/), then download curated_gene_disease_associations.tsv.gz | P2 |
| 5 | EPA CompTox PFAS | Browser-only download | Download PFAS compound list from [CompTox Dashboard](https://comptox.epa.gov/dashboard/) | P1 |
| 6 | EcoCyc E. coli | Academic licence required | Request at [EcoCyc](https://ecocyc.org/) | P3 |
| 7 | OMIM genemap2 | Requires API key | Register at [OMIM API](https://omim.org/api) for free academic key | P2 |
| 8 | MSigDB full JSON | Requires Broad login | Register at [GSEA-MSigDB](https://www.gsea-msigdb.org/gsea/msigdb/) — we got individual GMT files without auth | P3 |
| 9 | DrugBank | Requires academic registration | Register at [DrugBank](https://go.drugbank.com/releases/latest) for download access | P2 |
| 10 | Bgee expression | Cloudflare bot protection | Download via browser from [Bgee](https://bgee.org/?page=download) | P3 |
| 11 | AmeriFlux BASE | Requires registration | Register at [AmeriFlux](https://ameriflux.lbl.gov/) for BASE data access | P2 |
| 12 | PharmGKB downloads | Requires terms acceptance | Agree to terms at [PharmGKB](https://www.pharmgkb.org/downloads) | P2 |

## DOWNLOAD FAILURES (scripted retry possible)

| # | Dataset | Issue | Error | Retry Strategy | Status |
|---|---------|-------|-------|---------------|--------|
| 1 | GWAS Catalog associations | EBI API returns Tomcat 500 | 992 bytes HTML error | Retry later — EBI service outage | OPEN |
| 2 | GEO GSE62944 (TCGA recount) | NCBI FTP returns tiny stub | 200 OK, 2.5 KB | GEO supplementary files available separately | WONTFIX |
| 3 | NIST PFAS SRD | API endpoint wrong/moved | 154 bytes | Research correct data.nist.gov endpoint | OPEN |
| 4 | Open Targets | FTP path structure changed | 404 on json/ directory | Find current release parquet/json paths | RESOLVED |
| 5 | Dryad LTEE fitness (Wiser 2013) | API returns 401/403 | Auth/redirect broken | Need Dryad API token or manual download | OPEN |
| 6 | HomoloGene | NCBI FTP 404 | Possibly discontinued | Replaced with OrthoDB v11 | RESOLVED |
| 7 | Ensembl regulatory build | Specific file path 404 | 196 bytes | Find current release filename | RESOLVED |
| 8 | PDB validation summary | RCSB URL changed | 323 bytes redirect | Find new reports URL | LOW |
| 9 | SIGNOR signaling | Download requires POST/JS | Returns HTML page | Need API or browser | LOW |
| 10 | CORUM complexes | Download page changed | 0 bytes | Find current release URL | LOW |
| 11 | Pathway Commons | URL structure changed (v12/v13 both 404) | 693 bytes | Research new download location | LOW |
| 12 | dbNSFP | S3 bucket "dbnsfp" no longer exists | NoSuchBucket error | Find current hosting (maybe Google Drive?) | OPEN |
| 13 | BOLD Systems API | API returns partial HTML | 10 KB mixed HTML/TSV | May need smaller taxonomic queries | LOW |
| 14 | BioModels SBML | Download endpoint changed | 0 bytes | Research current EBI BioModels API | LOW |
| 15 | TAIR GO annotations | Requires authentication | 118 byte redirect | Register at arabidopsis.org | LOW |
| 16 | MalariaGEN Pf6 metadata | Site redesigned, all URLs return HTML | 42 KB HTML | Use malariagen Python package or GCS VObs | OPEN |
| 17 | Michigan EGLE PFAS GIS | ArcGIS API returns empty/error | 11-72 bytes | Need correct FeatureServer URL | OPEN |
| 18 | EPA UCMR5 PFAS | URL rotates with each data release | 6.5 KB HTML | Research current year's URL | OPEN |
| 19 | CAZy/dbCAN HMMs | URL structure changed | 18 KB HTML | Research bcb.unl.edu/dbCAN2 current paths | OPEN |
| 20 | HMP gene catalog | NCBI HMPDACC FTP returns XML | 990 bytes | Need correct HMP2 data URL | OPEN |
| 21 | BioGRID chemicals | Download URL returns HTML | 7 KB | Need current version number | LOW |
| 22 | USDA PLANTS | CSV URL changed/requires AJAX | 710 bytes HTML | Use alternative botanical data source | LOW |
| 23 | FEMA NFHL | REST endpoint returns HTML | 1.5 KB | Need current ArcGIS service URL | LOW |
| 24 | Human Cell Atlas | API endpoint changed | 130 bytes | Research current HCA Data Explorer API | LOW |

## TECHNICAL ISSUES

| Issue | Detail | Impact | Resolution |
|-------|--------|--------|------------|
| NCBI FTP rate limiting | Aggressive 403 on parallel requests (>2) | Slows GEO/NCBI bulk downloads | Sequential with 10s delays; NCBI API key helps for Entrez but not FTP |
| Xena Hub S3 bucket access | pancanatlas S3 returns AccessDenied | Some TCGA supplementary files | Used toil-xena-hub S3 as fallback (got expression + mutations) |
| EBI FTP file paths change | Filenames include version numbers that rotate | 404 on specific files | List directory first to find current filenames |
| GEO SOFT vs supplementary | Large GEO series (LINCS) return metadata stubs in SOFT format | Missing embedded data | Use GEO supplementary files or direct data downloads instead |

## SUCCESSFULLY RESOLVED THIS SESSION

| Issue | Resolution |
|-------|------------|
| AlphaFold version mismatch | URLs were v4, current is v6 — fixed and downloaded 10 species |
| ChEBI SDF filename | Was `ChEBI_complete_3star.sdf.gz`, actual is `chebi_3_stars.sdf.gz` |
| COSMIC cell lines API | API path returns ServerError for cell lines product |
| USGS query limit | 20K event limit — split into yearly queries (27 files) |
| Pfam/InterPro downloads | Needed longer timeouts (InterPro = 12 GB) |
| Open Targets path | FTP restructured — data is under `output/` not `output/etl/json/` |
| Ensembl regulatory build | Filename had wrong date — found correct via directory listing |
| Uberon/CL ontology | raw.githubusercontent.com 404 — used purl.obolibrary.org instead |
| MSigDB | Full JSON needs login — individual GMT collections downloadable without auth |
| HomoloGene | Discontinued by NCBI — replaced with OrthoDB v11 |
| Sarkas ZIP 14 bytes | GitHub `main` branch → `master` branch fixed download |
| SRA RunInfo API | Old Trace API returns HTML — switched to Entrez esearch+efetch |
| NCBI gene expansions | Added gene2go (1.3 GB) + gene2pubmed (268 MB) via FTP |
| Tabula Muris data | Found 290 MB FACS + 4 MB annotations on Figshare via API |
| SILVA NR99 expansion | Added 197 MB NR99 SSURef to existing SILVA 138.1 |

---

## SESSION STATS

### Session 2 (Aug 2, 2026 evening — contacts + baseCamp sweep)

- **Source**: Deep scan of `attsi/non-anon/contact/`, baseCamp papers, garden scopes
- **New datasets acquired**: 30+ (GPS Platform, Murillo Plasma+Surrogate, Jones PFAS, Tabula Muris, EMP, PLUMED-NEST, breseq, CQ.AAT1, SEPP/SATe, HotQCD, PhyNetPy, NCBI Assembly, Ensembl Compara, OSM, MIMIC demo, plus expansions to gene_info/gene2go/gene2pubmed, GOA, SILVA NR99, Reactome interactors, Rfam clans, OBO ontologies, and SRA metadata for 12 BioProjects)
- **Data volume added**: ~8 GB new + expansions
- **Provenance**: 100% — all 30+ datasets through full 5-step chain
- **Grand total**: 373 GB, 118 datasets, 473 files

### Session 1 (Aug 2, 2026 — initial sweep)

- **Datasets attempted**: ~50
- **Datasets acquired**: 30+ new
- **Success rate**: ~60% (rest blocked by auth, Cloudflare, URL changes, rate limits)
- **Data volume this session**: ~67 GB new data

### Running Total

- **Grand total**: 373 GB, 118 datasets, 473 files
- **ZFS usage**: 0.74% of 50.7 TB

*Circle back to NEEDS USER items when user has time for registrations.*
*Circle back to OPEN items on next data session — most are URL research tasks.*
*NCBI FTP: wait 10+ minutes between bulk download batches to avoid 403.*
*SRA BioProject FASTQ downloads (Tier B) are the next major data volume opportunity (~1 TB).*
