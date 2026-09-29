// app/exchange.js (propuesta 3)
if (counterAccount.balance >= counterAmount) {
  counterAccount.balance -= counterAmount; // reserva, sin await intermedio

  let transferred = false;
  try {
    transferred = await transferFunds(/* ... */);
  } finally {
    if (!transferred) {
      counterAccount.balance += counterAmount; // libera la reserva
    }
  }

  if (transferred) {
    baseAccount.balance += baseAmount;
    exchangeResult.ok = true;
    exchangeResult.counterAmount = counterAmount;
  }
}
