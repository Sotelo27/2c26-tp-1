#!/bin/sh
scenario=$1
env=$2
services="api nginx"
branch=$(git -C "$(dirname "$0")" rev-parse --abbrev-ref HEAD | tr '/' '-')
data_dir="graficos/data/${branch}_${scenario}_$(date +%s)"
mkdir -p "$data_dir"

# /perf$ ./run-scenario.sh rates api

(cd "$(dirname "$0")/.." && docker compose up -d --build --force-recreate --remove-orphans $services) || exit 1

i=0
until curl -sf -o /dev/null http://localhost:5555/rates; do
    i=$((i + 1))
    if [ "$i" -ge 30 ]; then
        echo "la api no responde en http://localhost:5555" >&2
        exit 1
    fi
    sleep 1
done

start=$(date +%s)
npm run artillery -- run "${scenario}.yaml" -e "$env" --output "$data_dir/report.json"
end=$(date +%s)

sleep 10

curl -s "http://localhost:8090/render?target=stats.gauges.artillery-api.**&format=json&from=${start}&until=${end}" -o "$data_dir/artillery.json"

curl -s "http://localhost:8090/render?target=stats.gauges.cadvisor.exchange-*.**&format=json&from=${start}&until=${end}" -o "$data_dir/cadvisor.json"

curl -s "http://localhost:8090/render?target=stats_counts.exchange.**&format=json&from=${start}&until=${end}" -o "$data_dir/currency.json"

curl -s "http://localhost:8090/render?target=stats.timers.exchange.**&format=json&from=${start}&until=${end}" -o "$data_dir/latency.json"

printf '{"scenario":"%s","branch":"%s","start":%s,"end":%s}\n' "$scenario" "$branch" "$start" "$end" > "$data_dir/meta.json"
