import { nanoid } from "nanoid";

import { init as stateInit, getAccounts as stateAccounts, getRates as stateRates, getLog as stateLog } from "./state.js";
import { logVolume, logNet } from "./currency_metrics.js";

let accounts;
let rates;
let log;

//reasons why an exchange can be rejected, reported in the obs field of the result
export const REJECTIONS = {
  NOT_ENOUGH_FUNDS: "Not enough funds on counter currency account",
  WITHDRAW_FAILED: "Could not withdraw from clients' account",
  DEPOSIT_FAILED: "Could not transfer to clients' account",
};

//call to initialize the exchange service
export async function init() {
  await stateInit();

  accounts = stateAccounts();
  rates = stateRates();
  log = stateLog();
}

//returns all internal accounts
export function getAccounts() {
  return accounts;
}

//sets balance for an account
export function setAccountBalance(accountId, balance) {
  const account = findAccountById(accountId);

  if (account != null) {
    account.balance = balance;
  }
}

//returns all current exchange rates
export function getRates() {
  return rates;
}

//returns the whole transaction log
export function getLog() {
  return log;
}

//sets the exchange rate for a given pair of currencies, and the reciprocal rate as well
export function setRate(rateRequest) {
  const { baseCurrency, counterCurrency, rate } = rateRequest;

  rates[baseCurrency][counterCurrency] = rate;
  rates[counterCurrency][baseCurrency] = Number((1 / rate).toFixed(5));
}

//executes an exchange operation
export async function exchange(exchangeRequest) {
  const {
    baseCurrency,
    counterCurrency,
    baseAccountId: clientBaseAccountId,
    counterAccountId: clientCounterAccountId,
    baseAmount,
  } = exchangeRequest;

  //get the exchange rate
  const exchangeRate = rates[baseCurrency][counterCurrency];
  //compute the requested (counter) amount
  const counterAmount = baseAmount * exchangeRate;
  //find our account on the provided (base) currency
  const baseAccount = findAccountByCurrency(baseCurrency);
  //find our account on the counter currency
  const counterAccount = findAccountByCurrency(counterCurrency);

  //construct the result object with defaults
  const exchangeResult = {
    id: nanoid(),
    ts: new Date(),
    ok: false,
    request: exchangeRequest,
    exchangeRate: exchangeRate,
    counterAmount: 0.0,
    obs: null,
  };

  //check if we have funds on the counter currency account
  if (counterAccount.balance >= counterAmount) {
    //reserve the funds right after the check, with no await in between, so concurrent
    //exchanges cannot approve themselves against the same balance
    counterAccount.balance -= counterAmount;

    let transferred = false;

    try {
      transferred = await transferFunds(
        exchangeResult,
        clientBaseAccountId,
        clientCounterAccountId,
        baseAccount,
        counterAccount,
        baseAmount,
        counterAmount
      );
    } finally {
      //the exchange did not complete (rejected or failed with an error), release the reservation
      if (!transferred) {
        counterAccount.balance += counterAmount;
      }
    }

    if (transferred) {
      //all good, update the base balance (the counter one was already reserved)
      baseAccount.balance += baseAmount;
      exchangeResult.ok = true;
      exchangeResult.counterAmount = counterAmount;

      const baseAmountUsd = toUsd(baseCurrency, baseAmount);
      const counterAmountUsd = toUsd(counterCurrency, counterAmount);

      logVolume(baseCurrency, baseAmountUsd);
      logVolume(counterCurrency, counterAmountUsd);
      logNet(baseCurrency, baseAmountUsd);
      logNet(counterCurrency, -counterAmountUsd);
    }
  } else {
    //not enough funds on internal counter account
    exchangeResult.obs = REJECTIONS.NOT_ENOUGH_FUNDS;
  }

  //log the transaction and return it
  log.push(exchangeResult);

  return exchangeResult;
}

// internal - move the funds between the clients' accounts and ours, returns true if both transfers succeeded
async function transferFunds(
  exchangeResult,
  clientBaseAccountId,
  clientCounterAccountId,
  baseAccount,
  counterAccount,
  baseAmount,
  counterAmount
) {
  //try to transfer from clients' base account
  if (!(await transfer(clientBaseAccountId, baseAccount.id, baseAmount))) {
    //could not withdraw from clients' account
    exchangeResult.obs = REJECTIONS.WITHDRAW_FAILED;
    return false;
  }

  //try to transfer to clients' counter account
  if (!(await transfer(counterAccount.id, clientCounterAccountId, counterAmount))) {
    //could not transfer to clients' counter account, return base amount to client
    await transfer(baseAccount.id, clientBaseAccountId, baseAmount);
    exchangeResult.obs = REJECTIONS.DEPOSIT_FAILED;
    return false;
  }

  return true;
}

// internal - call transfer service to execute transfer between accounts
async function transfer(fromAccountId, toAccountId, amount) {
  const min = 200;
  const max = 400;
  return new Promise((resolve) =>
    setTimeout(() => resolve(true), Math.random() * (max - min + 1) + min)
  );
}

function toUsd(currency, amount) {
  if (currency == 'USD') {
    return amount;
  }

  const pivotRateToUsd = rates['ARS']?.['USD'];

  if (currency == 'ARS') {
    return amount * pivotRateToUsd;
  }

  return amount * rates[currency]?.['ARS'] * pivotRateToUsd;
}

function findAccountByCurrency(currency) {
  for (let account of accounts) {
    if (account.currency == currency) {
      return account;
    }
  }

  return null;
}

function findAccountById(id) {
  for (let account of accounts) {
    if (account.id == id) {
      return account;
    }
  }

  return null;
}
