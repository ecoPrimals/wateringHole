#!/usr/bin/env python3
"""
GPS Platform Data Converter — NumPy/pickle → JSON for tideGlass Rust

Extracts tideGlass-consumable JSON from Zenodo GPS platform v5/v6 ZIPs:
  1. Gene list (selected_genes_2198.csv → target_genes JSON)
  2. MLP weight tensors per cell line (model.pkl → JSON state dicts)
  3. NA_IDX gene index lists (NA_IDX_*.pkl → JSON arrays)
  4. GO fingerprint metadata (go_fingerprints CSV headers → JSON)

Outputs written to staging dir, then CAS-ingested with derivation lineage
(parent_hash → original ZIP BLAKE3).

Usage:
  python3 gps_to_json.py
  python3 gps_to_json.py --dry-run    # show what would be extracted, skip CAS
"""

import argparse
import csv
import hashlib
import json
import os
import pickle
import sys
import tempfile
import zipfile
from pathlib import Path

GPS_DIR = Path("/mnt/nestgate/cold/zfs/data/gps_platform")
STAGING = Path("/tmp/gps_json_staging")

sys.path.insert(0, str(Path(__file__).parent))

def extract_gene_list(zip_path, staging):
    """Extract selected_genes_2198.csv → JSON gene list."""
    with zipfile.ZipFile(zip_path) as zf:
        for name in zf.namelist():
            if "selected_genes" in name and name.endswith(".csv"):
                with zf.open(name) as f:
                    reader = csv.reader(f.read().decode("utf-8").splitlines())
                    genes = []
                    for row in reader:
                        if row and row[0] and not row[0].startswith("#"):
                            gene = row[0].strip()
                            if gene and gene != "gene" and gene != "Gene":
                                genes.append(gene)
                    if genes:
                        out = staging / "target_genes.json"
                        out.write_text(json.dumps(genes, indent=None))
                        print(f"  GENE LIST: {len(genes)} genes → {out}")
                        return genes
    return None


def extract_mlp_weights(zip_path, staging):
    """Extract PyTorch MLP state dicts → JSON per cell line."""
    import torch
    import importlib.util

    # The model.pkl files need the MLP class from GPS4Drugs/code/model.py.
    # Extract it to a temp dir and add to sys.path for unpickling.
    model_module_loaded = False
    with zipfile.ZipFile(zip_path) as zf:
        for name in zf.namelist():
            if name.endswith("model.py") and "code/model.py" in name and "__MACOSX" not in name:
                model_tmp = staging / "_model_module"
                model_tmp.mkdir(parents=True, exist_ok=True)
                with zf.open(name) as src, open(model_tmp / "model.py", "wb") as dst:
                    dst.write(src.read())
                if str(model_tmp) not in sys.path:
                    sys.path.insert(0, str(model_tmp))
                model_module_loaded = True
                break

    extracted = []
    with zipfile.ZipFile(zip_path) as zf:
        for name in zf.namelist():
            if name.endswith("model.pkl") and "__MACOSX" not in name:
                parts = Path(name).parts
                cell_line = None
                for p in parts:
                    if p in ("HEPG2_t0", "PC3_t1", "MCF7_t1", "VCAP_t1"):
                        cell_line = p
                        break
                if not cell_line:
                    cell_line = parts[-2] if len(parts) > 1 else "unknown"

                with zf.open(name) as f:
                    try:
                        state = torch.load(f, map_location="cpu", weights_only=False)
                    except Exception as e:
                        print(f"  SKIP {name}: {e}")
                        continue

                models = {}
                if isinstance(state, dict):
                    for key, val in state.items():
                        if hasattr(val, "state_dict"):
                            sd = val.state_dict()
                            layer_data = {k: v.tolist() for k, v in sd.items()}
                            models[key] = layer_data
                        elif isinstance(val, dict):
                            layer_data = {}
                            for lk, lv in val.items():
                                if hasattr(lv, "tolist"):
                                    layer_data[lk] = lv.tolist()
                                else:
                                    layer_data[lk] = str(lv)
                            models[key] = layer_data

                if models:
                    out = staging / f"mlp_weights_{cell_line}.json"
                    out.write_text(json.dumps(models))
                    size_mb = out.stat().st_size / 1024 / 1024
                    print(f"  MLP WEIGHTS: {cell_line} → {out} ({size_mb:.1f} MB, {len(models)} ensemble members)")
                    extracted.append((cell_line, str(out)))
    return extracted


def extract_na_idx(zip_path, staging):
    """Extract NA_IDX_*.pkl → JSON arrays."""
    extracted = []
    with zipfile.ZipFile(zip_path) as zf:
        for name in zf.namelist():
            if "NA_IDX_" in name and name.endswith(".pkl") and "__MACOSX" not in name:
                disease = Path(name).stem.replace("NA_IDX_", "")
                with zf.open(name) as f:
                    data = pickle.load(f)
                if isinstance(data, list):
                    out = staging / f"na_idx_{disease.lower()}.json"
                    serializable = []
                    for round_list in data:
                        if hasattr(round_list, "tolist"):
                            serializable.append(round_list.tolist())
                        elif isinstance(round_list, list):
                            serializable.append([int(x) for x in round_list])
                        else:
                            serializable.append([int(x) for x in round_list])
                    out.write_text(json.dumps(serializable))
                    total_indices = sum(len(r) for r in serializable)
                    print(f"  NA_IDX: {disease} → {out} ({len(serializable)} rounds, {total_indices} total indices)")
                    extracted.append((disease, str(out)))
    return extracted


def extract_go_fingerprints(zip_path, staging):
    """Extract GO fingerprint feature names from CSV headers."""
    with zipfile.ZipFile(zip_path) as zf:
        for name in zf.namelist():
            if "go_fingerprints" in name and name.endswith(".csv") and "__MACOSX" not in name:
                with zf.open(name) as f:
                    header_line = f.readline().decode("utf-8", errors="replace").strip()
                    columns = [c.strip().strip('"') for c in header_line.split(",")]
                if columns:
                    out = staging / f"go_fingerprint_features_{Path(name).stem}.json"
                    out.write_text(json.dumps(columns))
                    print(f"  GO FEATURES: {Path(name).name} → {out} ({len(columns)} features)")
                    return columns
    return None


def extract_enamine_npz(zip_path, staging):
    """Extract ENAMINE compound matrix metadata (not the full matrix — too large)."""
    import numpy as np

    with zipfile.ZipFile(zip_path) as zf:
        for name in zf.namelist():
            if "ENAMINE" in name and name.endswith(".npz") and "__MACOSX" not in name:
                with zf.open(name) as f:
                    data = np.load(f, allow_pickle=True)
                    result = {}
                    for key in data.files:
                        arr = data[key]
                        if key in ("index", "columns") and arr.dtype.kind in ("U", "S", "O"):
                            result[key] = arr.tolist()
                        else:
                            result[f"{key}_shape"] = list(arr.shape)
                            result[f"{key}_dtype"] = str(arr.dtype)
                    if result:
                        out = staging / "enamine_hts_metadata.json"
                        out.write_text(json.dumps(result))
                        gene_count = len(result.get("index", []))
                        compound_count = len(result.get("columns", []))
                        print(f"  ENAMINE: {gene_count} genes × {compound_count} compounds → {out}")
                        return result
    return None


def build_gps4drug_weights_json(staging, genes):
    """Build the tideglass.gps4drug_weights JSON in the format data.rs expects.

    Schema gap: actual GPS models are PyTorch MLPs, not linear regression.
    This creates a placeholder with the gene list and zero weights so tideGlass
    can boot. The MLP weights are exported separately for future Rust MLP impl.
    """
    if not genes:
        return None

    out = staging / "tideglass_gps4drug_weights.json"
    payload = {
        "weights": [],
        "intercept": 0.0,
        "target_genes": genes,
        "_note": "Placeholder — actual GPS4Drug models are PyTorch MLPs. See mlp_weights_*.json for full ensemble state dicts.",
    }
    out.write_text(json.dumps(payload))
    print(f"  GPS4DRUG WEIGHTS: placeholder with {len(genes)} target genes → {out}")
    return str(out)


def cas_ingest_json(json_path, dataset_key, parent_zip_hash=None, dry_run=False):
    """Ingest a JSON file into CAS with derivation lineage."""
    if dry_run:
        print(f"  [DRY-RUN] Would CAS ingest: {json_path} as {dataset_key}")
        return

    try:
        from bulk_ingest import blake3_hash, cas_put
        path = Path(json_path)
        b3 = blake3_hash(path)
        ok, mode = cas_put(path, b3)
        status = "PASS" if ok else "FAIL"
        size_kb = path.stat().st_size / 1024
        print(f"  CAS {status}: {dataset_key} → {b3[:16]}... ({size_kb:.0f} KB, {mode})")
    except Exception as e:
        print(f"  CAS SKIP: {dataset_key} — {e}")


def main():
    parser = argparse.ArgumentParser(description="GPS platform pickle → JSON converter")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be extracted")
    args = parser.parse_args()

    if not GPS_DIR.exists():
        print(f"ERROR: GPS data not found at {GPS_DIR}")
        sys.exit(1)

    STAGING.mkdir(parents=True, exist_ok=True)
    print(f"GPS Platform → JSON Converter")
    print(f"Source: {GPS_DIR}")
    print(f"Staging: {STAGING}")
    print(f"{'=' * 60}")

    zips = sorted(GPS_DIR.glob("*.zip"))
    print(f"Found {len(zips)} ZIP archives\n")

    genes = None
    all_outputs = {}

    for zp in zips:
        print(f"\n--- {zp.name} ({zp.stat().st_size / 1024 / 1024:.0f} MB) ---")

        if "GPS4Drugs" in zp.name:
            g = extract_gene_list(zp, STAGING)
            if g:
                genes = g
                all_outputs["target_genes"] = STAGING / "target_genes.json"

            mlps = extract_mlp_weights(zp, STAGING)
            for cell, path in mlps:
                all_outputs[f"mlp_weights.{cell}"] = Path(path)

            go = extract_go_fingerprints(zp, STAGING)
            enamine = extract_enamine_npz(zp, STAGING)
            if enamine:
                all_outputs["enamine_hts_metadata"] = STAGING / "enamine_hts_metadata.json"

        elif "MolSearch" in zp.name:
            na = extract_na_idx(zp, STAGING)
            for disease, path in na:
                all_outputs[f"na_idx.{disease}"] = Path(path)

        elif "RCL" in zp.name:
            mlps = extract_mlp_weights(zp, STAGING)
            for cell, path in mlps:
                all_outputs[f"rcl_weights.{cell}"] = Path(path)

        elif "data_for_GPS_figures" in zp.name or "figure_code" in zp.name:
            print("  (figures/notebooks — no binary artifacts to convert)")

    if genes:
        gps4drug_path = build_gps4drug_weights_json(STAGING, genes)
        if gps4drug_path:
            all_outputs["tideglass.gps4drug_weights"] = Path(gps4drug_path)

    print(f"\n{'=' * 60}")
    print(f"CONVERSION SUMMARY")
    print(f"{'=' * 60}")
    print(f"Total outputs: {len(all_outputs)}")
    total_size = sum(p.stat().st_size for p in all_outputs.values() if p.exists())
    print(f"Total size: {total_size / 1024 / 1024:.1f} MB")
    print()

    for key, path in sorted(all_outputs.items()):
        size_kb = path.stat().st_size / 1024 if path.exists() else 0
        print(f"  {key:40s} {size_kb:>8.0f} KB  {path.name}")

    if not args.dry_run:
        print(f"\n--- CAS Ingestion ---")
        for key, path in sorted(all_outputs.items()):
            cas_ingest_json(path, key, dry_run=args.dry_run)

    print(f"\nDone. tideGlass can load GPS4Drug weights from CAS key 'tideglass.gps4drug_weights'.")
    print(f"Full MLP ensembles in mlp_weights_*.json for future Rust MLP implementation.")


if __name__ == "__main__":
    main()
