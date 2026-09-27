import dgram from "dgram"; 
import Docker from "dockerode";

const ID = parseInt(process.env.ID);
const PORT = 4000;
const PEERS = [
    "watchdog-1",
    "watchdog-2",
    "watchdog-3"
];
const API_CONTAINER = "exchange-api-1";
const HEARTBEAT_PERIOD = 1000;
const TIMEOUT = 3000;
const API_TIMEOUT = 3000;

var leader = null;
var lastLeaderHeartbeat = Date.now();
var lastApiHeartbeat = Date.now();
var electing = false;
var answered = false;
var restarting = false;

var docker = new Docker();
var socket = dgram.createSocket("udp4");

function sendMsg(type, destId) {
    var message = type + " " + ID;
    socket.send(message, PORT, PEERS[destId - 1], function(err) {
        // console.log(err);
    });
}

function startElection() {
    if (electing == false) { 
        electing = true;
        answered = false;

        for (var i = 0; i < PEERS.length; i++) {
            var peerId = i + 1;
            if (peerId != ID) {
                if (peerId > ID) {
                    sendMsg("election", peerId);
                }
            }
        }

        setTimeout(function() {
            if (answered == false){
                leader = ID;
                console.log("Watchdog " + ID + " is leader");

                for (var j = 0; j < PEERS.length; j++) {
                    var pId = j + 1;
                    if (pId != ID) {
                        sendMsg("leader", pId);
                    }
                }
            }
            electing = false;
        }, TIMEOUT); 
    }
}

async function checkApi() {
    if (restarting == false) {
        if (Date.now() - lastApiHeartbeat >= API_TIMEOUT) {
            restarting = true;
            console.log("Watchdog " + ID + ": api is down, restarting " + API_CONTAINER);

            try {
                var container = docker.getContainer(API_CONTAINER);
                await container.restart({ t: 0 });
                console.log("Watchdog " + ID + ": " + API_CONTAINER + " restarted ok");
            } catch (error){
                console.log("Watchdog " + ID + ": error restarting " + API_CONTAINER + " " + error.message);
            }

            lastApiHeartbeat = Date.now();
            restarting = false;
        }
    }
}

socket.on("message", function(msg) {
    var content = msg.toString();
    var parts = content.split(" ");
    
    var type = parts[0];
    var sender = parseInt(parts[1]);

    // console.log("message from " + sender + " type " + type);

    if (type == "api") {
        lastApiHeartbeat = Date.now();
    } else if (type == "heartbeat") {
        if (leader == ID) {
            sendMsg("alive", sender);
        }
    } else if (type == "alive") {
        lastLeaderHeartbeat = Date.now();
    } else if (type == "election") {
        sendMsg("answer", sender);
        startElection();
    } else if (type == "answer") {
        answered = true;
    } else if (type =="leader") {
        if (sender < ID) {
            startElection();
        } else {
            leader = sender;
            electing = false;
            lastLeaderHeartbeat = Date.now();
            console.log("Watchdog " + ID + ": new leader is " + leader);
        }
    }
});

setInterval(function() {
    if (leader == ID) {
        checkApi();
    } else { 
        if (leader != null) {
            sendMsg("heartbeat", leader);
        }

        if (Date.now() - lastLeaderHeartbeat > TIMEOUT) { 
            startElection();
        }
    }
},HEARTBEAT_PERIOD); 

socket.bind(PORT, function() {
    console.log("Watchdog " + ID + " listening on port " + PORT);
    startElection();
});