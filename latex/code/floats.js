const exchangeRate = rates[baseCurrency][counterCurrency];
//compute the requested (counter) amount
const counterAmount = baseAmount * exchangeRate;