#!/bin/bash
# westGate Boot Check — verify hardware, data estate, and provenance readiness
# For spring teams: tells you if your data is ready for consumption.
# Usage: ./westgate_boot_check.sh
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m'

PASS=0
FAIL=0
WARN=0

check() {
    local name="$1"
    local result="$2"
    if [ "$result" = "PASS" ]; then
        echo -e "  ${GREEN}PASS${NC}  $name"
        PASS=$((PASS + 1))
    elif [ "$result" = "WARN" ]; then
        echo -e "  ${YELLOW}WARN${NC}  $name"
        WARN=$((WARN + 1))
    else
        echo -e "  ${RED}FAIL${NC}  $name"
        FAIL=$((FAIL + 1))
    fi
}

info() {
    echo -e "  ${CYAN}INFO${NC}  $1"
}

DATA_ROOT="/mnt/nestgate/cold/zfs/data"

echo "=========================================="
echo "  westGate Boot Check"
echo "  $(date)"
echo "=========================================="
echo ""

# ── Hardware ──────────────────────────────────────────────────────

echo "--- Hardware ---"
CPU=$(grep -m1 'model name' /proc/cpuinfo 2>/dev/null | cut -d: -f2 | xargs)
CORES=$(nproc 2>/dev/null || echo "?")
RAM=$(free -h 2>/dev/null | awk '/Mem:/{print $2}')
GPU=$(lspci 2>/dev/null | grep -i 'vga\|3d' | head -1 | sed 's/.*: //')
info "CPU: $CPU ($CORES threads)"
info "RAM: $RAM"
info "GPU: $GPU"

# ── ZFS ───────────────────────────────────────────────────────────

echo ""
echo "--- ZFS Pool ---"
if zpool status nestgate >/dev/null 2>&1; then
    check "ZFS pool imported" "PASS"
else
    check "ZFS pool imported" "FAIL"
    echo "    FIX: sudo zpool import nestgate"
fi

if mountpoint -q /mnt/nestgate/cold/zfs 2>/dev/null; then
    check "ZFS mounted" "PASS"
else
    check "ZFS mounted" "FAIL"
    echo "    FIX: sudo zfs mount -a"
fi

ERRORS=$(zpool status nestgate 2>/dev/null | grep -c "No known data errors" || echo 0)
if [ "$ERRORS" -gt 0 ]; then
    check "ZFS zero errors" "PASS"
else
    check "ZFS zero errors" "FAIL"
fi

ZFS_SIZE=$(zpool list nestgate -o size -H 2>/dev/null || echo "?")
ZFS_ALLOC=$(zpool list nestgate -o alloc -H 2>/dev/null || echo "?")
ZFS_FREE=$(zpool list nestgate -o free -H 2>/dev/null || echo "?")
ZFS_CAP=$(zpool list nestgate -o cap -H 2>/dev/null || echo "?")
ZFS_HEALTH=$(zpool list nestgate -o health -H 2>/dev/null || echo "?")
info "Pool: ${ZFS_SIZE} total, ${ZFS_ALLOC} used, ${ZFS_FREE} free (${ZFS_CAP})"
info "Health: $ZFS_HEALTH"

# ── NUCLEUS ───────────────────────────────────────────────────────

echo ""
echo "--- NUCLEUS Tower ---"

TOWER_SERVICES="beardog-tower nestgate-tower rhizocrypt-tower loamspine-tower sweetgrass-tower toadstool-tower barracuda-tower coralreef-tower petaltongue-tower squirrel-tower"
ACTIVE=0
TOTAL=0
for svc in $TOWER_SERVICES; do
    TOTAL=$((TOTAL + 1))
    if systemctl --user is-active "$svc" >/dev/null 2>&1; then
        ACTIVE=$((ACTIVE + 1))
    fi
done
check "Tower services ($ACTIVE/$TOTAL)" "$([ $ACTIVE -eq $TOTAL ] && echo PASS || echo WARN)"

SOCKETS=$(ls /run/user/1000/membrane/*.sock 2>/dev/null | wc -l)
check "Membrane sockets ($SOCKETS)" "$([ $SOCKETS -ge 13 ] && echo PASS || echo WARN)"

HEALTH=$(python3 -c "
import json, subprocess, struct
prefix = struct.pack('BB', 0xEC, 0x01)
r = subprocess.run(['socat','-t5','-','UNIX-CONNECT:/run/user/1000/membrane/neural-api-westgate-tower-155f.sock'],
                   input=prefix+json.dumps({'jsonrpc':'2.0','method':'health.check','params':{},'id':1}).encode(),
                   capture_output=True, timeout=10)
if r.stdout:
    raw = r.stdout[2:] if r.stdout[:2] == prefix else r.stdout
    h = json.loads(raw).get('result',{})
    print(f'v{h.get(\"version\",\"?\")} {h.get(\"mode\",\"?\")} {h.get(\"registered_capabilities\",0)}caps')
else:
    print('UNREACHABLE')
" 2>/dev/null || echo "UNREACHABLE")
check "biomeOS Neural API ($HEALTH)" "$(echo $HEALTH | grep -q 'UNREACHABLE' && echo FAIL || echo PASS)"

# ── Provenance Pipeline ──────────────────────────────────────────

echo ""
echo "--- Provenance Pipeline ---"

for primal in nestgate rhizocrypt loamspine sweetgrass beardog; do
    SOCK="/run/user/1000/membrane/${primal}-westgate-tower-155f.sock"
    if [ -S "$SOCK" ]; then
        check "$primal socket" "PASS"
    else
        check "$primal socket" "FAIL"
    fi
done

CAS_TEST=$(python3 -c "
import json, subprocess, struct, base64
PREFIX = struct.pack('BB', 0xEC, 0x01)
req = json.dumps({'jsonrpc':'2.0','method':'content.put','params':{'data': base64.b64encode(b'boot-check').decode(), 'hash_type':'blake3'},'id':1})
r = subprocess.run(['socat','-t10','-','UNIX-CONNECT:/run/user/1000/membrane/nestgate-westgate-tower-155f.sock'],
                   input=PREFIX+req.encode()+b'\n', capture_output=True, timeout=15)
print('PASS' if r.stdout and b'result' in r.stdout else 'FAIL')
" 2>/dev/null || echo "FAIL")
check "CAS put roundtrip" "$CAS_TEST"

# ── Background Jobs ──────────────────────────────────────────────

echo ""
echo "--- Background Jobs ---"

for svc in alphafold-bulk alphafold-prov alphafold-sync; do
    STATUS=$(systemctl --user is-active "${svc}.service" 2>/dev/null || echo "inactive")
    if [ "$STATUS" = "active" ] || [ "$STATUS" = "activating" ]; then
        check "${svc}.service" "PASS"
    else
        check "${svc}.service ($STATUS)" "WARN"
    fi
done

PROV_STATE="/mnt/nestgate/cold/zfs/data/alphafold_structures/.prov_state"
if [ -f "$PROV_STATE" ]; then
    EVENTS=$(python3 -c "import json; print(json.load(open('$PROV_STATE')).get('event_count',0))" 2>/dev/null || echo "?")
    info "Trailer progress: $EVENTS events braided"
fi

# ── Data Estate ───────────────────────────────────────────────────

echo ""
echo "--- Data Estate ---"
DATA_DIRS=$(ls -d ${DATA_ROOT}/*/ 2>/dev/null | wc -l)
check "Datasets on ZFS ($DATA_DIRS)" "$([ $DATA_DIRS -ge 100 ] && echo PASS || echo WARN)"

# Spring data readiness — check key directories exist and have files
echo ""
echo "--- Spring Data Readiness ---"

check_dataset() {
    local name="$1"
    local path="$2"
    local min_size_mb="$3"
    if [ -d "$path" ]; then
        SIZE=$(du -sm "$path" 2>/dev/null | cut -f1)
        if [ "$SIZE" -ge "$min_size_mb" ]; then
            check "$name (${SIZE} MB)" "PASS"
        else
            check "$name (${SIZE} MB, expected >=${min_size_mb} MB)" "WARN"
        fi
    else
        check "$name (missing)" "FAIL"
    fi
}

echo "  -- tideGlass --"
check_dataset "lincs_l1000" "${DATA_ROOT}/lincs_l1000" 1000
check_dataset "chembl37" "${DATA_ROOT}/chembl37" 1000
check_dataset "gps_platform" "${DATA_ROOT}/gps_platform" 100
check_dataset "tcga_gdc" "${DATA_ROOT}/tcga_gdc" 1000
check_dataset "cosmic" "${DATA_ROOT}/cosmic" 500
check_dataset "nf_data_portal" "${DATA_ROOT}/nf_data_portal" 10
check_dataset "pdb_mmcif" "${DATA_ROOT}/pdb_mmcif" 10000

echo "  -- wetSpring --"
check_dataset "sra_fastq" "${DATA_ROOT}/sra_fastq" 10000
check_dataset "uniprot" "${DATA_ROOT}/uniprot" 100
check_dataset "pfam" "${DATA_ROOT}/pfam" 1000
check_dataset "interpro" "${DATA_ROOT}/interpro" 1000

echo "  -- airSpring / groundSpring --"
check_dataset "noaa_ghcnd" "${DATA_ROOT}/noaa_ghcnd" 100
check_dataset "usda_nass" "${DATA_ROOT}/usda_nass" 10
check_dataset "iris_earthquake" "${DATA_ROOT}/iris_earthquake" 1

echo "  -- neuralSpring (mesh-served) --"
check_dataset "alphafold_structures" "${DATA_ROOT}/alphafold_structures" 1000

# ── Summary ───────────────────────────────────────────────────────

echo ""
echo "=========================================="
echo "  Results: ${GREEN}$PASS PASS${NC}  ${YELLOW}$WARN WARN${NC}  ${RED}$FAIL FAIL${NC}"
echo "  Uptime:  $(uptime -p)"
echo "=========================================="

if [ $FAIL -gt 0 ]; then
    exit 1
fi
