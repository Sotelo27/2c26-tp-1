#!/bin/sh
scenario=$1
env=$2
data_dir="graficos/data/${scenario}_$(date +%s)"
mkdir -p "$data_dir"

# /perf$ ./run-scenario.sh rates api
start=$(date +%s)
npm run artillery -- run "${scenario}.yaml" -e "$env" --output "$data_dir/report.json"
end=$(date +%s)

sleep 2

curl -s "http://localhost:8090/render?target=stats.gauges.artillery-api.**&format=json&from=${start}&until=${end}" -o "$data_dir/artillery.json"

curl -s "http://localhost:8090/render?target=stats.gauges.cadvisor.exchange-*.**&format=json&from=${start}&until=${end}" -o "$data_dir/cadvisor.json"

curl -s "http://localhost:8090/render?target=stats_counts.exchange.**&format=json&from=${start}&until=${end}" -o "$data_dir/currency.json"

printf '{"scenario":"%s","start":%s,"end":%s}\n' "$scenario" "$start" "$end" > "$data_dir/meta.json"
