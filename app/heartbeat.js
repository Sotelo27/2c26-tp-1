import dgram from "node:dgram";

const WATCHDOGS = ["watchdog-1", "watchdog-2", "watchdog-3"];
const WATCHDOG_PORT = 4000;
const HEARTBEAT_PERIOD = 1000;

const socket = dgram.createSocket("udp4");

export function startHeartbeat() {
    setInterval(() => {
        for (const host of WATCHDOGS) {
            socket.send("api", WATCHDOG_PORT, host, () => {});
        }
    }, HEARTBEAT_PERIOD);
}
