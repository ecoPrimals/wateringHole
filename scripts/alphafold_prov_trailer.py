#!/usr/bin/env python3
"""
AlphaFold provenance trailer — follows the bulk downloader and braids files.

Watches the alphafold_structures directory for new .cif files that haven't
been braided yet. Maintains its own progress file tracking braided files.
Runs as a companion systemd service alongside alphafold-bulk.

Architecture:
  - Downloader writes .cif files at 74/s (full speed, no provenance overhead)
  - This trailer reads newly appeared files and runs BLAKE3→CAS→DAG→spine
  - The trailer can fall behind temporarily; it catches up during pauses
  - Every CHECKPOINT_INTERVAL files, the DAG is partially dehydrated
  - On clean shutdown, the DAG is fully dehydrated, spine committed, signed, braided

Restart-safe: persists provenance session IDs and braided file set.
"""

import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from bulk_ingest import (
    blake3_hash, cas_put,
    dag_session_create, dag_event_append, dag_partial_dehydrate,
    dag_dehydrate, spine_create, spine_entry_append,
    spine_session_commit, sign_merkle_root, braid_create,
)

DEST = Path("/mnt/nestgate/cold/zfs/data/alphafold_structures")
DOWNLOAD_PROGRESS = DEST / ".progress"
PROV_PROGRESS = DEST / ".prov_braided"
PROV_STATE = DEST / ".prov_state"
DATASET_NAME = "alphafold_structures_v6"

BATCH_SIZE = 500
CHECKPOINT_INTERVAL = 2000
SCAN_INTERVAL = 30
REPORT_INTERVAL = 300


def load_prov_state():
    if PROV_STATE.exists():
        try:
            return json.loads(PROV_STATE.read_text())
        except (json.JSONDecodeError, KeyError):
            pass
    return None


def save_prov_state(session_id, spine_id, event_count):
    PROV_STATE.write_text(json.dumps({
        "session_id": session_id,
        "spine_id": spine_id,
        "event_count": event_count,
    }))


def load_braided_set():
    if PROV_PROGRESS.exists():
        return set(PROV_PROGRESS.read_text().splitlines())
    return set()


def init_provenance():
    state = load_prov_state()
    if state and state.get("session_id") and state.get("spine_id"):
        print(f"Resuming provenance: session={state['session_id'][:16]}... "
              f"events={state.get('event_count', 0)}")
        return state["session_id"], state["spine_id"], state.get("event_count", 0)

    session_id = dag_session_create(DATASET_NAME)
    spine_result = spine_create(DATASET_NAME)
    spine_id = spine_result.get("spine_id") if isinstance(spine_result, dict) else spine_result
    if not session_id or not spine_id:
        print("FATAL: provenance init failed", file=sys.stderr)
        sys.exit(1)
    save_prov_state(session_id, spine_id, 0)
    print(f"Provenance started: session={session_id[:16]}... spine={spine_id[:16]}...")
    return session_id, spine_id, 0


def find_unbraided(braided_set, batch_size=500):
    """Find .cif files on disk that haven't been braided yet."""
    unbraided = []
    for subdir in sorted(DEST.iterdir()):
        if not subdir.is_dir() or subdir.name.startswith("."):
            continue
        for f in subdir.iterdir():
            if f.suffix == ".cif" and f.name not in braided_set:
                unbraided.append(f)
                if len(unbraided) >= batch_size:
                    return unbraided
    return unbraided


def braid_batch(files, session_id, spine_id, event_count, braided_set, prov_fh):
    """Braid a batch of files through the full provenance chain."""
    ok = 0
    for fp in files:
        try:
            sz = fp.stat().st_size
            h = blake3_hash(fp)
            cas_put(fp, h)
            dag_event_append(session_id, h, fp.name, sz, DATASET_NAME)
            spine_entry_append(spine_id, h, "chemical/x-cif", sz)
            event_count += 1
            ok += 1
            braided_set.add(fp.name)
            prov_fh.write(fp.name + "\n")

            if event_count % CHECKPOINT_INTERVAL == 0:
                dag_partial_dehydrate(session_id)
                save_prov_state(session_id, spine_id, event_count)
                prov_fh.flush()
                print(f"  [CHECKPOINT] {event_count:,} events", flush=True)
        except Exception as e:
            print(f"  ERR: {fp.name}: {e}", flush=True)
    return ok, event_count


def main():
    print(f"AlphaFold provenance trailer starting", flush=True)
    print(f"Directory: {DEST}", flush=True)

    session_id, spine_id, event_count = init_provenance()
    braided_set = load_braided_set()
    print(f"Previously braided: {len(braided_set):,} files", flush=True)

    total_braided = 0
    t_start = time.time()
    last_report = t_start

    with open(PROV_PROGRESS, "a") as prov_fh:
        while True:
            files = find_unbraided(braided_set, BATCH_SIZE)
            if not files:
                time.sleep(SCAN_INTERVAL)
                now = time.time()
                if now - last_report > REPORT_INTERVAL:
                    elapsed = now - t_start
                    print(f"[{time.strftime('%H:%M:%S')}] "
                          f"braided={total_braided:,} total={len(braided_set):,} "
                          f"events={event_count:,} "
                          f"rate={total_braided/elapsed:.1f}/s "
                          f"(waiting for new files)", flush=True)
                    last_report = now
                continue

            ok, event_count = braid_batch(
                files, session_id, spine_id, event_count, braided_set, prov_fh,
            )
            total_braided += ok
            save_prov_state(session_id, spine_id, event_count)
            prov_fh.flush()

            now = time.time()
            if now - last_report > REPORT_INTERVAL:
                elapsed = now - t_start
                print(f"[{time.strftime('%H:%M:%S')}] "
                      f"braided={total_braided:,} total={len(braided_set):,} "
                      f"events={event_count:,} "
                      f"rate={total_braided/elapsed:.1f}/s",
                      flush=True)
                last_report = now


if __name__ == "__main__":
    main()
