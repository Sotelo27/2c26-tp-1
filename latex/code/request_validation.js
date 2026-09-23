// app/app.js (caso base)
if (
  !baseCurrency ||
  !counterCurrency ||
  !baseAccountId ||
  !counterAccountId ||
  !baseAmount
) {
  return res.status(400).json({ error: "Malformed request" });
}
