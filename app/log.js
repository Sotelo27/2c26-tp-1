import net from "net";
import path from "path";
import fs from "fs";
import { fileURLToPath } from "url";
import { Transform, pipeline } from "stream";

let logs = null;

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const LOGS = "./state/log.ndjson";

//call to initialize the log service
export async function init() {
    logs = await load(LOGS);

    const serverLogSocket = net.createServer(appendToLog);
    serverLogSocket.listen(3002, 'log-api', () => {
        console.log(`Log listening on port 3002`);
    });
}

function load(fileName) {
    const filePath = path.join(__dirname, fileName);
    const fileDescriptor = fs.createWriteStream(filePath, { flags: "a" });

    fileDescriptor.on("error", (err) => {
        console.error(`Error writing to ${filePath}:`, err);
    });

    return fileDescriptor;
}


//returns the whole transaction log
export async function stream(res) {
    const filePath = path.join(__dirname, LOGS);
    const { size } = await fs.promises.stat(filePath);

    if (res.destroyed) {
        return;
    }

    res.type("application/json");

    if (size == 0) {
        res.end("[]");
        return;
    }

    pipeline(
        fs.createReadStream(filePath, { start: 0, end: size - 1, encoding: "utf8" }),
        toJsonArray(),
        res,
        (err) => {
            if (err && err.code != "ERR_STREAM_PREMATURE_CLOSE") {
                console.error("Error streaming log:", err);
            }
        }
    );
}

function toJsonArray() {
    let pending = "";
    let first = true;

    return new Transform({
        transform(chunk, encoding, callback) {
            pending += chunk;
            const lines = pending.split("\n");
            pending = lines.pop();

            let out = "";
            for (const line of lines) {
                if (line.length > 0) {
                    out += (first ? "[" : ",") + line;
                    first = false;
                }
            }
            callback(null, out);
        },
        flush(callback) {
            callback(null, first ? "[]" : "]");
        },
    });
}

function appendToLog(socket) {
    let pending = "";

    socket.setEncoding("utf8");

    socket.on("data", (chunk) => {
        pending += chunk;
        const lines = pending.split("\n");
        pending = lines.pop();

        const complete = lines.filter((line) => line.length > 0);
        if (complete.length > 0) {
            logs.write(complete.join("\n") + "\n");
        }
    });

    socket.on("error", (err) => {
        console.error("Error appending to log:", err);
    });
}