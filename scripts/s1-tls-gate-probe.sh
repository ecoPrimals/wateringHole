#!/usr/bin/env bash
# s1-tls-gate-probe.sh — S1 TLS 7-day cutover gate measurement
#
# Probes sovereign TLS (Caddy :443) latency every invocation.
# Appended to /var/lib/membrane/telemetry/s1_tls_gate.csv
# Designed to run via systemd timer (every 15 min).
#
# Gate criteria: 7 consecutive days, p95 TTFB < 500ms,
# zero TLS failures over measurement period.

set -euo pipefail

TELEMETRY_DIR="/var/lib/membrane/telemetry"
CSV="$TELEMETRY_DIR/s1_tls_gate.csv"
GATE_START_FILE="$TELEMETRY_DIR/s1_gate_start"
GATE_DAYS=7

mkdir -p "$TELEMETRY_DIR"

if [[ ! -f "$GATE_START_FILE" ]]; then
    date -u +%Y-%m-%dT%H:%M:%SZ > "$GATE_START_FILE"
fi

if [[ ! -f "$CSV" ]]; then
    echo "timestamp,ttfb_ms,total_ms,connect_ms,tls_ok,http_code" > "$CSV"
fi

ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)

result=$(curl -sk -o /dev/null \
    -w "%{time_starttransfer}|%{time_total}|%{time_connect}|%{http_code}" \
    --max-time 10 \
    https://membrane.primals.eco/health 2>&1) || result="0|0|0|000"

IFS='|' read -r ttfb total connect code <<< "$result"

to_ms() { printf '%s' "$1" | awk '{printf "%d", $1 * 1000}'; }
ttfb_ms=$(to_ms "$ttfb")
total_ms=$(to_ms "$total")
connect_ms=$(to_ms "$connect")

tls_ok="true"
if [[ "$code" == "000" ]] || [[ -z "$code" ]]; then
    tls_ok="false"
fi

echo "$ts,$ttfb_ms,$total_ms,$connect_ms,$tls_ok,$code" >> "$CSV"

lines=$(wc -l < "$CSV")
if (( lines > 2 )); then
    failures=$(tail -n +2 "$CSV" | grep -c "false" || true)
    gate_start=$(cat "$GATE_START_FILE")
    echo "S1 TLS gate: started=$gate_start samples=$((lines - 1)) failures=$failures"
fi
