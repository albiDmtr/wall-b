import { createServer } from "node:http";
import next from "next";
import { Server } from "socket.io";

const dev = process.env.NODE_ENV !== "production";
const hostname = "localhost";
const port = 3000;
// when using middleware `hostname` and `port` must be provided below
const app = next({ dev, hostname, port });
const handler = app.getRequestHandler();

let users = new Map();

app.prepare().then(() => {
  const httpServer = createServer(handler);

  const io = new Server(httpServer);

  io.on("connection", (socket) => {
    console.log("a user connected");

    socket.on("auth", (msg) => {
      users.set(socket.id, msg);
    });

    socket.on("disconnect", () => {
      console.log(`user disconnected, user id: ${users.get(socket.id)}`);
      users.delete(socket.id);
    });

    socket.emit("status", `{"wallB": ${Array.from(users.values()).includes("wallB")}}`);
  });

  httpServer
    .once("error", (err) => {
      console.error(err);
      process.exit(1);
    })
    .listen(port, () => {
      console.log(`> Ready on http://${hostname}:${port}`);
    });
});