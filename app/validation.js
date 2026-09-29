import { getAccounts, getRates } from "./exchange.js";

//each validator returns null if the request is valid, or a message describing the first error found

export function validateExchangeRequest(body) {
  const {
    baseCurrency,
    counterCurrency,
    baseAccountId,
    counterAccountId,
    baseAmount,
  } = body ?? {};

  const currencyError =
    validateCurrency("baseCurrency", baseCurrency) ??
    validateCurrency("counterCurrency", counterCurrency);
  if (currencyError) {
    return currencyError;
  }

  if (baseCurrency == counterCurrency) {
    return "baseCurrency and counterCurrency must be different";
  }

  //a rate must exist for the requested pair, otherwise the exchange cannot be computed
  if (!isPositiveNumber(getRates()[baseCurrency]?.[counterCurrency])) {
    return `No exchange rate for ${baseCurrency}/${counterCurrency}`;
  }

  const accountError =
    validateAccountId("baseAccountId", baseAccountId) ??
    validateAccountId("counterAccountId", counterAccountId);
  if (accountError) {
    return accountError;
  }

  if (!isPositiveNumber(baseAmount)) {
    return "baseAmount must be a positive number";
  }

  return null;
}

export function validateRateRequest(body) {
  const { baseCurrency, counterCurrency, rate } = body ?? {};

  const currencyError =
    validateCurrency("baseCurrency", baseCurrency) ??
    validateCurrency("counterCurrency", counterCurrency);
  if (currencyError) {
    return currencyError;
  }

  if (baseCurrency == counterCurrency) {
    return "baseCurrency and counterCurrency must be different";
  }

  if (!isPositiveNumber(rate)) {
    return "rate must be a positive number";
  }

  return null;
}

export function validateBalanceRequest(body) {
  const { balance } = body ?? {};

  if (!isNonNegativeNumber(balance)) {
    return "balance must be a non negative number";
  }

  return null;
}

export function accountExists(accountId) {
  return getAccounts().some((account) => account.id == accountId);
}

//a currency is supported only if we have an internal account on it
export function isSupportedCurrency(currency) {
  return getAccounts().some((account) => account.currency == currency);
}

function validateCurrency(field, currency) {
  if (typeof currency != "string") {
    return `${field} must be a string`;
  }

  if (!isSupportedCurrency(currency)) {
    return `Unsupported currency ${currency}`;
  }

  return null;
}

//client accounts belong to the transfer service, so we can only check the format
function validateAccountId(field, accountId) {
  if (typeof accountId != "string" || accountId.trim() == "") {
    return `${field} must be a non empty string`;
  }

  return null;
}

function isPositiveNumber(value) {
  return typeof value == "number" && Number.isFinite(value) && value > 0;
}

function isNonNegativeNumber(value) {
  return typeof value == "number" && Number.isFinite(value) && value >= 0;
}
