// app/heartbeat.js (propuesta 2): la API notifica a los tres watchdogs
const WATCHDOGS = ["watchdog-1", "watchdog-2", "watchdog-3"];
setInterval(() => {
  for (const host of WATCHDOGS) {
    socket.send("api", WATCHDOG_PORT, host, () => {});
  }
}, HEARTBEAT_PERIOD);

// app/watchdog.js (propuesta 2): todos registran el heartbeat...
if (type == "api") {
  lastApiHeartbeat = Date.now();
}

// ...pero solo el lider actua sobre la API
setInterval(function() {
  if (leader == ID) {
    checkApi();
  } else {
    // seguidor: heartbeat al lider y nueva eleccion si no responde
  }
}, HEARTBEAT_PERIOD);
