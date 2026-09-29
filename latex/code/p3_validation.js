// app/validation.js (propuesta 3)
export function validateExchangeRequest(body) {
  const { baseCurrency, counterCurrency, baseAccountId,
          counterAccountId, baseAmount } = body ?? {};

  const currencyError =
    validateCurrency("baseCurrency", baseCurrency) ??
    validateCurrency("counterCurrency", counterCurrency);
  if (currencyError) {
    return currencyError;
  }
  if (baseCurrency == counterCurrency) {
    return "baseCurrency and counterCurrency must be different";
  }
  if (!isPositiveNumber(getRates()[baseCurrency]?.[counterCurrency])) {
    return `No exchange rate for ${baseCurrency}/${counterCurrency}`;
  }
  // ... validacion de baseAccountId y counterAccountId
  if (!isPositiveNumber(baseAmount)) {
    return "baseAmount must be a positive number";
  }
  return null;
}

// app/app.js (propuesta 3)
const validationError = validateExchangeRequest(req.body);
if (validationError) {
  return res.status(400).json({ error: "Malformed request", obs: validationError });
}
