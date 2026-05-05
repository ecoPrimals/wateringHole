# Deployment Log: ironGate JupyterHub (Phase 1 Prototype)

**Gate**: ironGate
**Date**: May 4, 2026
**Status**: Verified working, not running as persistent service yet

---

## Gate Selection

ironGate was selected as the initial prototype because it was the accessible
development machine. The ideal bioinformatics gate is **strandGate** (dual
EPYC 7452, 256 GB ECC, RTX 3090) — replication there is a follow-up task.

| Gate | CPU | RAM | GPU | Suitability |
|------|-----|-----|-----|-------------|
| **ironGate** (current) | i9-14900K (24c/32t) | 96 GB DDR5 | RTX 5070 12 GB | Good — plenty for notebooks, dev + compute overlap risk |
| **strandGate** (ideal) | Dual EPYC 7452 (64c/128t) | 256 GB ECC | RTX 3090 24 GB | Best — ECC RAM, massive core count, dedicated science machine |
| **biomeGate** | TR 3970X (32c/64t) | 256 GB | Titan V + K80 | Good for HBM2 workloads, but semi-mobile |
| **southGate** | 5800X3D | 128 GB | RTX 4060 (display) | Reasonable, but dual-boot complicates persistence |

The setup script (`setup-jupyterhub.sh`) is portable — run it on any gate
to replicate the full environment.

---

## What Was Installed

### Miniforge3
- Location: `~/miniforge3`
- Provides: conda, mamba, conda-forge channel

### Environments

**jupyterhub** (base hub):
- Python 3.12, JupyterHub 5.4.5, JupyterLab 4.5.7
- configurable-http-proxy, jupyterhub-idle-culler

**bioinfo** (Python bioinformatics kernel):
- scanpy, anndata, pandas, numpy, scipy, matplotlib, seaborn, scikit-learn
- pydeseq2, snakemake-minimal, biom-format (from bioconda)
- Registered as kernel: "Bioinformatics (Python 3.12)"

**r-bioinfo** (R bioinformatics kernel):
- R 4.5, Seurat 5.5, ggplot2, dplyr, tidyverse, IRkernel
- Registered as kernel: "R Bioinformatics (R 4.5)"

### Configuration
- Config: `~/jupyterhub/jupyterhub_config.py`
- Bind: `127.0.0.1:8000` (local only — tunnel required for external)
- Auth: PAM (system users)
- Spawner: LocalProcessSpawner
- Resource limits: 32 GB RAM, 8 CPU cores per user
- Idle culling: 1 hour timeout

### Verified (May 4, 2026)

**Infrastructure**:
- [x] JupyterHub starts and binds to port 8000
- [x] Login page serves (HTTP 200)
- [x] API responds (version 5.4.5)
- [x] Idle culler has correct role scopes
- [x] Three kernels registered and visible (python3, bioinfo, r-bioinfo)
- [x] API token auth works (admin scopes)
- [x] Notebook server spawns via API (HTTP 201) and stops cleanly (HTTP 204)

**Python bioinfo kernel**:
- [x] scanpy 1.12.1 — full pipeline: normalize → log → HVGs → PCA → neighbors → UMAP → Leiden (12 clusters from 500 synthetic cells)
- [x] pydeseq2 0.5.4 — full DE pipeline: size factors → dispersions → LFC → Wald test (12/100 genes significant with spiked fold-change)
- [x] snakemake 9.20.0, biom-format 2.1.17, numpy 2.4.3, scipy 1.17.1, pandas 2.3.3, scikit-learn 1.8.0
- [x] leidenalg + igraph installed (required for scanpy clustering)

**R bioinfo kernel**:
- [x] Seurat 5.5.0 — full pipeline: normalize → variable features → scale → PCA → neighbors → clusters
- [x] ggplot2 4.0.3, dplyr 1.2.1, tidyverse 2.0.0, R 4.5.3

**GPU access**:
- [x] nvidia-smi visible from bioinfo env: RTX 5070, 12 GB, driver 570.153.02
- [x] CUDA_VISIBLE_DEVICES not restricted (full GPU access)
- [ ] PyTorch/JAX not installed in bioinfo env (add per-project when needed)

**Resource limits**:
- [ ] mem_limit/cpu_limit NOT enforced by LocalProcessSpawner (process shows unlimited)
- Acceptable for Phase 1 (human monitors, single trusted user)
- For Phase 2+: use systemd-run cgroups or switch to DockerSpawner

**System headroom** (during test):
- RAM: 7.2 GB used / 94 GB total (79 GB available)
- CPU: 32 threads, <1% utilization from JupyterHub
- Disk: 168 GB used / 3.6 TB (5%)
- GPU: 560 MB / 12 GB VRAM, 1% utilization

---

## To Make Persistent

```bash
# Start manually:
bash ~/jupyterhub/start.sh

# Or create a systemd user service:
# systemctl --user enable jupyterhub
# systemctl --user start jupyterhub
```

Not running as a persistent service yet — Phase 1 doesn't require it until
an ABG member actually needs access.

---

## To Add External Users

1. Create a Linux user: `sudo adduser <username>`
2. Create their notebooks dir: `sudo -u <username> mkdir -p /home/<username>/notebooks`
3. Add to config: edit `allowed_users` in `jupyterhub_config.py`
4. Set up tunnel access (WireGuard/Tailscale) for external connectivity
5. Restart JupyterHub

---

## Replication to Another Gate

```bash
# Copy the setup script and run on any gate:
scp setup-jupyterhub.sh <gate>:~/
ssh <gate> 'bash ~/setup-jupyterhub.sh'
```
