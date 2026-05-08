# primalSpring — Fresh Remote Deployment Gaps

| Field | Value |
|-------|-------|
| **From** | primalSpring (ironGate — first fresh remote deployment) |
| **To** | plasmidBin maintainers, wateringHole standards |
| **Date** | 2026-05-02 |
| **Gate** | ironGate (i9-14900K, RTX 5070 SM120, 96 GB DDR5, Pop!_OS 22.04) |
| **Context** | First-ever clean bootstrap of the full ecoPrimals ecosystem on a blank machine |
| **Status** | Fixes applied locally, pending upstream merge |

---

## Summary

ironGate is the first gate bootstrapped entirely from zero — no migrated repos,
no pre-existing plasmidBin cache, no prior toolchain. The `bootstrap.sh --fresh`
and `fetch.sh --all` pipeline was run end-to-end, exposing three gaps that
silently break the fetch-then-validate workflow on fresh machines.

All three gaps are in `infra/plasmidBin/` scripts. They are invisible on gates
that evolved in place (where binaries were manually placed or harvested locally),
and invisible in CI (which bypasses `validate_composition.sh` after fetch).

---

## Gap 1: fetch.sh / validate_composition.sh Binary Path Mismatch

**Owner:** plasmidBin
**Priority:** High — blocks all fresh deploys from validating

**Problem:**

`fetch.sh` writes binaries to `primals/{triple}/{name}` (e.g.
`primals/x86_64-unknown-linux-musl/beardog`) via the `target_dir_for()` function
which always appends `$CURRENT_ARCH`.

`validate_composition.sh` (line 159) and `doctor.sh` (line 141) look only at
`primals/{name}` — the flat path. The backward-compat symlinks documented in
both `checksums.toml` and `README.md` ("Legacy symlinks: `primals/{binary}` ->
`x86_64-unknown-linux-musl/{binary}`") are **never created by any script**.

`start_primal.sh` is already resilient (tries triple first, then flat), but the
validation scripts are not.

**Result on fresh machine:** `fetch.sh --all` succeeds (7/13 binaries
downloaded, all BLAKE3 verified), then `validate_composition.sh tower`
immediately fails — "not found in primals/". Manual symlink creation was
required.

**Fix applied:**

`fetch.sh` now creates backward-compat symlinks after the download loop:

```bash
# After download loop, before summary
for bin in "$PRIMALS_DIR/$CURRENT_ARCH"/*; do
    name=$(basename "$bin")
    link="$PRIMALS_DIR/$name"
    if [[ ! -e "$link" ]] || [[ -L "$link" ]]; then
        ln -sf "$CURRENT_ARCH/$name" "$link"
    fi
done
```

**Files changed:** `infra/plasmidBin/fetch.sh`

---

## Gap 2: validate_composition.sh / doctor.sh Checksum Triple Mismatch

**Owner:** plasmidBin
**Priority:** Medium — checksums silently skip instead of verifying

**Problem:**

`validate_composition.sh` (line 190) and `doctor.sh` (line 281) build truncated
triples for checksum lookup:

```bash
# Before (broken)
x86_64)  TRIPLE="x86_64-linux-musl" ;;
aarch64) TRIPLE="aarch64-linux-musl" ;;
```

But `checksums.toml` uses full Rust target triples as keys:

```toml
[primals.beardog]
"x86_64-unknown-linux-musl" = "6ca141..."
```

The `-unknown-` segment is missing, so `grep "\"$TRIPLE\""` never matches. Both
scripts fall through to "no entry in checksums.toml" (WARN) even when the entry
exists and is correct.

**Result on fresh machine:** All checksums show as WARN (unverified) in
`validate_composition.sh`, even though `fetch.sh` successfully verified them
using the correct triple from `detect_target_triple()`.

**Fix applied:**

Both scripts now use full Rust triples:

```bash
# After (fixed)
x86_64)  TRIPLE="x86_64-unknown-linux-musl" ;;
aarch64) TRIPLE="aarch64-unknown-linux-musl" ;;
armv7l)  TRIPLE="armv7-unknown-linux-musleabihf" ;;
```

Additionally, `doctor.sh` aarch64 inventory path was updated from the incorrect
`primals/aarch64/` to `primals/aarch64-unknown-linux-musl/`, and x86_64
inventory now falls back to the arch-qualified path if the flat path is missing.

**Files changed:** `infra/plasmidBin/validate_composition.sh`,
`infra/plasmidBin/doctor.sh`

---

## Gap 3: bootstrap.sh Private Repo Clone Failure

**Owner:** wateringHole
**Priority:** Medium — blocks private repo clone on SSH-only machines

**Problem:**

`bootstrap.sh --fresh` uses `gh repo clone` for all repos. On a fresh machine,
SSH keys are typically configured before `gh auth login` (natural order: generate
key, add to GitHub, then optionally authenticate gh). Private repos (bearDog,
skunkBat) fail with a suppressed WARN because `gh repo clone` stderr is
redirected to `/dev/null`.

The `sources.toml` manifest already marks these repos as `private = true`, but
`clone_repo()` does not use this information.

**Result on fresh machine:** 5 of 33 repos failed to clone. Manual
`git clone git@github.com:...` was required for all private repos after the
bootstrap completed.

**Fix applied:**

`clone_repo()` now falls back to SSH when `gh` fails:

```bash
if ! gh repo clone "$org/$repo" "$dst" 2>/dev/null; then
    if git clone "git@github.com:$org/$repo.git" "$dst" 2>/dev/null; then
        echo "  (cloned via SSH fallback)"
    else
        echo "  WARN: failed to clone $org/$repo (tried gh + SSH)"
        WARNINGS+=("Failed to clone $org/$repo")
        return
    fi
fi
```

**Files changed:** `infra/wateringHole/bootstrap.sh`

---

## CI Gap (Observation)

`.github/workflows/smoke.yml` in plasmidBin runs `fetch.sh` then starts binaries
directly from `primals/x86_64-unknown-linux-musl/$primal` — correctly matching
fetch output but **bypassing** `validate_composition.sh`. The validation workflow
(`validate.yml`) only runs `fetch.sh --dry-run` and metadata checks.

No CI step currently asserts that `fetch.sh --all && validate_composition.sh
tower` passes end-to-end. This is why the symlink gap was invisible.

**Recommendation:** Add a CI step that runs `fetch.sh --all` followed by
`validate_composition.sh tower` (or `--json` for machine-readable output).

---

## Resolution Status

| Gap | Script | Fix | Verified |
|-----|--------|-----|----------|
| 1 — symlink creation | `fetch.sh` | Symlinks created after download | Verified: "Symlinked: 7" on re-run |
| 2 — checksum triple | `validate_composition.sh`, `doctor.sh` | Full Rust triples | Verified: checksums now PASS (were WARN) |
| 3 — SSH fallback | `bootstrap.sh` | `git clone` fallback on `gh` failure | Verified during bootstrap |
