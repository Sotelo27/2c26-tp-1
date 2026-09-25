import dgram from "node:dgram";

const STATSD_HOST = process.env.STATSD_HOST || "graphite";
const STATSD_PORT = Number(process.env.STATSD_PORT) || 8125;

const socket = dgram.createSocket("udp4");

function logTimer(name, milliseconds) {
  const message = Buffer.from(`${name}:${milliseconds}|ms`);
  socket.send(message, STATSD_PORT, STATSD_HOST);
}

function endpointName(req) {
  if (req.path == "/exchange") return "exchange";
  if (req.path == "/log") return "log";
  if (req.path == "/accounts") return "accounts";
  if (req.path == "/rates") return req.method == "GET" ? "rates" : "set_rates";
  if (req.path.startsWith("/accounts/")) return "accounts_balance";

  return "unknown";
}

export function logEndpoint(req, res, next) {
  const start = Date.now();

  res.on("finish", () => {
    const duration = Date.now() - start;
    logTimer(`exchange.latency.${endpointName(req)}`, duration);
  });

  next();
}