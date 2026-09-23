// app/exchange.js (caso base)
log.push(exchangeResult);

// app/app.js (caso base)
app.get("/log", (req, res) => {
  res.json(getLog());
});

// app/state.js (caso base)
scheduleSave(log, LOG, 1000);

function scheduleSave(data, fileName, period) {
  setInterval(async () => {
    await save(data, fileName);
  }, period);
}
