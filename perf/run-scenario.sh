#!/bin/sh
scenario=$1
env=$2
run_dir="runs/${scenario}_$(date +%s)"
mkdir -p "$run_dir"

start=$(date +%s)
npm run artillery -- run "${scenario}.yaml" -e "$env" --output "$run_dir/report.json"
end=$(date +%s)

sleep 2

curl -s "http://localhost:8090/render?target=stats.gauges.artillery-api.*&format=json&from=${start}&until=${end}" -o "$run_dir/artillery.json"

curl -s "http://localhost:8090/render?target=stats.gauges.cadvisor.exchange-*.*&format=json&from=${start}&until=${end}" -o "$run_dir/cadvisor.json"

curl -s "http://localhost:8090/render?target=stats_counts.exchange.*.*&format=json&from=${start}&until=${end}" -o "$run_dir/currency.json"

printf '{"scenario":"%s","start":%s,"end":%s}\n' "$scenario" "$start" "$end" > "$run_dir/meta.json"
