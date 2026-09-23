// app/exchange.js (caso base)
if (counterAccount.balance >= counterAmount) {
  if (await transfer(clientBaseAccountId, baseAccount.id, baseAmount)) {
    if (
      await transfer(counterAccount.id, clientCounterAccountId, counterAmount)
    ) {
      baseAccount.balance += baseAmount;
      counterAccount.balance -= counterAmount;
      exchangeResult.ok = true;
      exchangeResult.counterAmount = counterAmount;
    }
  }
}
