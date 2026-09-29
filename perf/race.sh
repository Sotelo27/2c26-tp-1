#!/bin/sh
# Evidencia de la condición de carrera en /exchange.
# Deja la cuenta interna USD con 100, lanza N cambios concurrentes de ~80 USD cada uno y muestra el saldo final.
# Sin condición de carrera se aprueba uno solo y el saldo queda en ~20; con ella se aprueban todos y queda en negativo.
#
# /perf$ ./race.sh [N]    (requiere el sistema levantado con docker compose; por defecto N=2)
# ATENCIÓN: modifica el saldo de la cuenta interna 2 (USD).

n=${1:-2}
url=${API_URL:-http://localhost:5555}
tmp=$(mktemp -d)

usd_balance() {
    curl -s "$url/accounts" | grep -o '"currency":"USD","balance":[-0-9.e]*' | cut -d: -f3
}

curl -sf -o /dev/null -X PUT "$url/accounts/2/balance" -H 'Content-Type: application/json' -d '{"balance":100}' || {
    echo "la api no responde en $url" >&2
    exit 1
}

echo "saldo USD inicial: $(usd_balance)"
echo "lanzando $n cambios concurrentes de 121213 ARS (~80 USD)..."

i=1
while [ "$i" -le "$n" ]; do
    curl -s -o /dev/null -w '%{http_code}\n' -X POST "$url/exchange" -H 'Content-Type: application/json' \
        -d '{"baseCurrency":"ARS","counterCurrency":"USD","baseAccountId":"cli-ARS","counterAccountId":"cli-USD","baseAmount":121213}' \
        > "$tmp/$i" &
    i=$((i + 1))
done
wait

echo "respuestas (cantidad / código HTTP):"
cat "$tmp"/* | sort | uniq -c
echo "saldo USD final: $(usd_balance)"

rm -rf "$tmp"
