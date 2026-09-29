import express from "express";

import { logEndpoint } from "./endpoint_metrics.js";
import {
  init as exchangeInit,
  getAccounts,
  setAccountBalance,
  getRates,
  setRate,
  getLog,
  exchange,
} from "./exchange.js";
import {
  validateExchangeRequest,
  validateRateRequest,
  validateBalanceRequest,
  accountExists,
} from "./validation.js";

await exchangeInit();

const app = express();
const port = 3000;

app.use(logEndpoint);
app.use(express.json());

// ACCOUNT endpoints

app.get("/accounts", (req, res) => {
  res.json(getAccounts());
});

app.put("/accounts/:id/balance", (req, res) => {
  const accountId = req.params.id;
  const { balance } = req.body;

  const validationError = validateBalanceRequest(req.body);
  if (validationError) {
    return res.status(400).json({ error: "Malformed request", obs: validationError });
  }

  if (!accountExists(accountId)) {
    return res.status(404).json({ error: "Account not found" });
  }

  setAccountBalance(accountId, balance);

  res.json(getAccounts());
});

// RATE endpoints

app.get("/rates", (req, res) => {
  res.json(getRates());
});

app.put("/rates", (req, res) => {
  const validationError = validateRateRequest(req.body);
  if (validationError) {
    return res.status(400).json({ error: "Malformed request", obs: validationError });
  }

  const newRateRequest = { ...req.body };
  setRate(newRateRequest);

  res.json(getRates());
});

// LOG endpoint

app.get("/log", (req, res) => {
  res.json(getLog());
});

// EXCHANGE endpoint

app.post("/exchange", async (req, res) => {
  const validationError = validateExchangeRequest(req.body);
  if (validationError) {
    return res.status(400).json({ error: "Malformed request", obs: validationError });
  }

  const exchangeRequest = { ...req.body };
  const exchangeResult = await exchange(exchangeRequest);

  if (exchangeResult.ok) {
    res.status(200).json(exchangeResult);
  } else {
    res.status(500).json(exchangeResult);
  }
});

app.listen(port, () => {
  console.log(`Exchange API listening on port ${port}`);
});

export default app;
