import dgram from "node:dgram";

const STATSD_HOST = process.env.STATSD_HOST || "graphite";
const STATSD_PORT = Number(process.env.STATSD_PORT) || 8125;

const socket = dgram.createSocket("udp4");

function logCounter(name, value) {
  const message = Buffer.from(`${name}:${value}|c`);
  socket.send(message, STATSD_PORT, STATSD_HOST);
}

export function logVolume(currency, amount) {
  logCounter(`exchange.volume.${currency}`, amount);
}

export function logNet(currency, amount) {
  logCounter(`exchange.net.${currency}`, amount);
}
