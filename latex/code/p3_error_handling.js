// app/app.js (propuesta 3)
app.post("/exchange", async (req, res, next) => {
  // ... validacion
  try {
    const exchangeResult = await exchange({ ...req.body });
    if (exchangeResult.ok) {
      res.status(200).json(exchangeResult);
    } else {
      res.status(REJECTION_STATUS[exchangeResult.obs] ?? 500).json(exchangeResult);
    }
  } catch (err) {
    next(err);
  }
});

app.use((err, req, res, next) => {
  if (err.status >= 400 && err.status < 500) {
    return res.status(err.status).json({ error: "Malformed request" });
  }
  console.error(`Unexpected error on ${req.method} ${req.path}:`, err);
  res.status(500).json({ error: "Internal server error" });
});
