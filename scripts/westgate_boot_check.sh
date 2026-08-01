#!/bin/bash
# westGate Boot Check — run after reboot to verify persistence
# Usage: ./westgate_boot_check.sh
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
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

echo "=========================================="
echo "  westGate Boot Check"
echo "  $(date)"
echo "=========================================="
echo ""

echo "--- ZFS ---"
if sudo zpool status nestgate >/dev/null 2>&1; then
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

ERRORS=$(sudo zpool status nestgate 2>/dev/null | grep -c "No known data errors" || echo 0)
if [ "$ERRORS" -gt 0 ]; then
    check "ZFS zero errors" "PASS"
else
    check "ZFS zero errors" "FAIL"
fi

DATA_DIRS=$(ls -d /mnt/nestgate/cold/zfs/data/*/ 2>/dev/null | wc -l)
check "Data directories ($DATA_DIRS)" "$([ $DATA_DIRS -ge 10 ] && echo PASS || echo WARN)"

CAS=$(find /mnt/nestgate/cold/zfs/cas/ -type f 2>/dev/null | wc -l)
check "CAS objects ($CAS)" "$([ $CAS -ge 4700 ] && echo PASS || echo WARN)"

echo ""
echo "--- NUCLEUS ---"

ACTIVE=$(systemctl --user is-active beardog-tower songbird-tower skunkbat-tower nestgate-tower rhizocrypt-tower loamspine-tower sweetgrass-tower toadstool-tower barracuda-tower coralreef-tower petaltongue-tower squirrel-tower neural-api-tower 2>/dev/null | grep -c active)
check "Services active ($ACTIVE/13)" "$([ $ACTIVE -eq 13 ] && echo PASS || echo WARN)"

SOCKETS=$(ls /run/user/1000/membrane/*.sock 2>/dev/null | wc -l)
check "Sockets ($SOCKETS)" "$([ $SOCKETS -ge 13 ] && echo PASS || echo WARN)"

HEALTH=$(python3 -c "
import json, subprocess, struct
prefix = struct.pack('BB', 0xEC, 0x01)
r = subprocess.run(['socat','-t5','-','UNIX-CONNECT:/run/user/1000/membrane/neural-api-westgate-tower-155f.sock'],
                   input=prefix+json.dumps({'jsonrpc':'2.0','method':'health.check','params':{},'id':1}).encode(),
                   capture_output=True, timeout=10)
if r.stdout:
    h = json.loads(r.stdout).get('result',{})
    print(f'v{h.get(\"version\")} {h.get(\"mode\")} {h.get(\"registered_capabilities\",0)}caps')
else:
    print('UNREACHABLE')
" 2>/dev/null)
check "biomeOS health ($HEALTH)" "$(echo $HEALTH | grep -q 'UNREACHABLE' && echo FAIL || echo PASS)"

echo ""
echo "--- Provenance Pipeline ---"

CAS_TEST=$(python3 -c "
import json, subprocess, struct, base64
PREFIX = struct.pack('BB', 0xEC, 0x01)
req = json.dumps({'jsonrpc':'2.0','method':'content.put','params':{'data': base64.b64encode(b'boot-check').decode(), 'hash_type':'blake3'},'id':1})
r = subprocess.run(['socat','-t10','-','UNIX-CONNECT:/run/user/1000/membrane/nestgate-westgate-tower-155f.sock'],
                   input=PREFIX+req.encode(), capture_output=True, timeout=15)
print('PASS' if r.stdout and b'result' in r.stdout else 'FAIL')
" 2>/dev/null)
check "CAS put roundtrip" "$CAS_TEST"

echo ""
echo "--- Storage ---"
ZFS_USED=$(sudo zfs list nestgate -o used -H 2>/dev/null || echo "?")
ZFS_AVAIL=$(sudo zfs list nestgate -o avail -H 2>/dev/null || echo "?")
echo "  ZFS used:  $ZFS_USED"
echo "  ZFS avail: $ZFS_AVAIL"
echo "  Machine:   $(uptime -p)"

echo ""
echo "=========================================="
echo "  Results: ${GREEN}$PASS PASS${NC}  ${YELLOW}$WARN WARN${NC}  ${RED}$FAIL FAIL${NC}"
echo "=========================================="

if [ $FAIL -gt 0 ]; then
    exit 1
fi
