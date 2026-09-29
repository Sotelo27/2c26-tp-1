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
  REJECTIONS,
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

//HTTP status for each business rejection: lack of funds is a client error, transfer failures are dependency failures
const REJECTION_STATUS = {
  [REJECTIONS.NOT_ENOUGH_FUNDS]: 409,
  [REJECTIONS.WITHDRAW_FAILED]: 502,
  [REJECTIONS.DEPOSIT_FAILED]: 502,
};

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

app.post("/exchange", async (req, res, next) => {
  const validationError = validateExchangeRequest(req.body);
  if (validationError) {
    return res.status(400).json({ error: "Malformed request", obs: validationError });
  }

  //express 4 does not catch rejected promises, so errors must be forwarded to the error handler explicitly
  try {
    const exchangeRequest = { ...req.body };
    const exchangeResult = await exchange(exchangeRequest);

    if (exchangeResult.ok) {
      res.status(200).json(exchangeResult);
    } else {
      res.status(REJECTION_STATUS[exchangeResult.obs] ?? 500).json(exchangeResult);
    }
  } catch (err) {
    next(err);
  }
});

// ERROR handler

//contains any unexpected error to the request that produced it, instead of terminating the process
app.use((err, req, res, next) => {
  //errors raised by express itself (e.g. an unparseable JSON body) carry a 4xx status
  if (err.status >= 400 && err.status < 500) {
    return res.status(err.status).json({ error: "Malformed request" });
  }

  console.error(`Unexpected error on ${req.method} ${req.path}:`, err);

  if (res.headersSent) {
    return next(err);
  }

  res.status(500).json({ error: "Internal server error" });
});

app.listen(port, () => {
  console.log(`Exchange API listening on port ${port}`);
});

export default app;
