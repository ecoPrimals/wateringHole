#!/usr/bin/env python3
"""
AlphaFold DB — Async bulk structure downloader.

Downloads all 214M+ predicted protein structures from the AlphaFold API.
Provenance runs as a companion service (alphafold-prov-trailer) that follows
behind, braiding newly downloaded files without slowing the download pipeline.

Restart-safe: tracks completed accessions in a progress file.
Designed for long-running unattended operation via systemd.

URL pattern: https://alphafold.ebi.ac.uk/files/AF-{ID}-F1-model_v{VER}.cif
"""

import asyncio
import csv
import os
import sys
import time
from pathlib import Path

import aiohttp

DEST = Path("/mnt/nestgate/cold/zfs/data/alphafold_structures")
ACCESSIONS = Path("/mnt/nestgate/cold/zfs/data/alphafold/accession_ids.csv")
PROGRESS_FILE = DEST / ".progress"
PROV_QUEUE_FILE = DEST / ".prov_queue"
BASE_URL = "https://alphafold.ebi.ac.uk/files"

CONCURRENCY = 20
REPORT_INTERVAL = 60
RETRY_LIMIT = 3
TIMEOUT = aiohttp.ClientTimeout(total=30, connect=10)
CONNECTOR_LIMIT = 30


async def download_one(
    session: aiohttp.ClientSession,
    sem: asyncio.Semaphore,
    uniprot_id: str,
    af_id: str,
    version: str,
    progress_fh,
    prov_queue_fh,
    stats: dict,
):
    prefix = uniprot_id[:2]
    subdir = DEST / prefix
    outfile = subdir / f"{af_id}-model_v{version}.cif"

    if outfile.exists():
        stats["skipped"] += 1
        return

    subdir.mkdir(parents=True, exist_ok=True)
    url = f"{BASE_URL}/{af_id}-model_v{version}.cif"

    async with sem:
        for attempt in range(RETRY_LIMIT):
            try:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.read()
                        outfile.write_bytes(data)
                        progress_fh.write(f"{uniprot_id}\n")
                        prov_queue_fh.write(f"{outfile}\t{len(data)}\n")
                        stats["success"] += 1
                        stats["bytes"] += len(data)
                        return
                    elif resp.status == 429:
                        wait = int(resp.headers.get("Retry-After", 5))
                        await asyncio.sleep(wait)
                        continue
                    elif resp.status == 404:
                        stats["not_found"] += 1
                        return
                    else:
                        stats["errors"] += 1
                        if attempt < RETRY_LIMIT - 1:
                            await asyncio.sleep(2 ** attempt)
            except (aiohttp.ClientError, asyncio.TimeoutError):
                stats["errors"] += 1
                if attempt < RETRY_LIMIT - 1:
                    await asyncio.sleep(2 ** attempt)

        stats["failed"] += 1


async def progress_reporter(stats: dict, total: int, start_time: float):
    while True:
        await asyncio.sleep(REPORT_INTERVAL)
        done = stats["success"] + stats["skipped"] + stats["not_found"] + stats["failed"]
        elapsed = time.time() - start_time
        rate = stats["success"] / elapsed if elapsed > 0 else 0
        pct = (done / total * 100) if total > 0 else 0
        gb = stats["bytes"] / (1024 ** 3)
        eta_hrs = ((total - done) / rate / 3600) if rate > 0 else float("inf")

        print(
            f"[{time.strftime('%H:%M:%S')}] "
            f"{done:,}/{total:,} ({pct:.2f}%) | "
            f"OK:{stats['success']:,} skip:{stats['skipped']:,} "
            f"404:{stats['not_found']:,} err:{stats['errors']:,} fail:{stats['failed']:,} | "
            f"{rate:.0f}/s | {gb:.2f} GB | ETA {eta_hrs:.1f}h",
            flush=True,
        )


async def main():
    if not ACCESSIONS.exists():
        print(f"ERROR: {ACCESSIONS} not found. Download it first.", file=sys.stderr)
        sys.exit(1)

    DEST.mkdir(parents=True, exist_ok=True)

    completed: set[str] = set()
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE) as f:
            completed = {line.strip() for line in f if line.strip()}
    print(f"Checkpoint: {len(completed):,} previously completed")

    entries: list[tuple[str, str, str]] = []
    with open(ACCESSIONS) as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 5:
                continue
            uid, _, _, af_id, ver = row[0], row[1], row[2], row[3], row[4]
            if uid not in completed:
                entries.append((uid, af_id, ver))

    total_all = len(entries) + len(completed)
    print(f"Total in manifest: {total_all:,}")
    print(f"Remaining: {len(entries):,}")
    print(f"Concurrency: {CONCURRENCY}")

    print(f"Starting download...\n", flush=True)

    stats = {
        "success": 0,
        "skipped": 0,
        "not_found": 0,
        "errors": 0,
        "failed": 0,
        "bytes": 0,
    }

    sem = asyncio.Semaphore(CONCURRENCY)
    conn = aiohttp.TCPConnector(limit=CONNECTOR_LIMIT, limit_per_host=CONNECTOR_LIMIT)
    start_time = time.time()

    reporter = asyncio.create_task(progress_reporter(stats, total_all, start_time))

    async with aiohttp.ClientSession(connector=conn, timeout=TIMEOUT) as session:
        with open(PROGRESS_FILE, "a") as progress_fh, \
             open(PROV_QUEUE_FILE, "a") as prov_queue_fh:
            batch_size = 5000
            for i in range(0, len(entries), batch_size):
                batch = entries[i : i + batch_size]
                tasks = [
                    download_one(session, sem, uid, af_id, ver, progress_fh, prov_queue_fh, stats)
                    for uid, af_id, ver in batch
                ]
                await asyncio.gather(*tasks)
                progress_fh.flush()
                prov_queue_fh.flush()

    reporter.cancel()

    elapsed = time.time() - start_time
    gb = stats["bytes"] / (1024 ** 3)
    print(f"\n{'='*60}")
    print(f"DOWNLOAD COMPLETE in {elapsed/3600:.1f}h")
    print(f"Downloaded: {stats['success']:,} structures ({gb:.2f} GB)")
    print(f"Skipped (already had): {stats['skipped']:,}")
    print(f"Not found (404): {stats['not_found']:,}")
    print(f"Failed: {stats['failed']:,}")
    print(f"Rate: {stats['success']/elapsed:.0f}/s")
    print(f"{'='*60}")


if __name__ == "__main__":
    asyncio.run(main())
