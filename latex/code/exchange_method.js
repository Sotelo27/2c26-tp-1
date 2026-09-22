export async function exchange(exchangeRequest) {
    ...
    //get the exchange rate
    const exchangeRate = rates[baseCurrency][counterCurrency];
    //compute the requested (counter) amount
    const counterAmount = baseAmount * exchangeRate;
    ...
            //all good, update balances
            baseAccount.balance += baseAmount;
            counterAccount.balance -= counterAmount;
    ...
}