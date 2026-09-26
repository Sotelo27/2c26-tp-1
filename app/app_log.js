import express from "express";

import { logEndpoint } from "./endpoint_metrics.js";
import {
  init as logInit,
  stream,
} from "./log.js";

await logInit();

const app = express();
const port = 3001;

app.use(logEndpoint);
app.use(express.json());

// LOG endpoint

app.get("/log", (req, res) => {
  stream(res).catch((err) => {
    console.error("Error streaming log:", err);
    res.destroy();
  });
});

app.listen(port, () => {
  console.log(`Log API listening on port ${port}`);
});

export default app;
