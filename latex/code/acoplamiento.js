let accounts;
let rates;
let log;

export async function init() {
    await stateInit();

    accounts = stateAccounts();
    rates = stateRates();
    log = stateLog();
}