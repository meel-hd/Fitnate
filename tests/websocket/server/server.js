/**
 * Simple websocket server
 * Used to send announcements to all clients connected to the server
 *
 * When a client connects, it sends a message to all clients
 * when a client sends a message, it sends the message to all clients
 * we keep track of the number of clients connected to the server
 *
 */

const ws = require("ws");

const wss = new ws.Server({ port: 8080 });

count = 0;

wss.on("connection", (userWs) => {
  count++;
  userWs.on("message", (message) => {
    console.log(message.toString());
    // send message to all clients
    wss.clients.forEach((client) => {
      client.send(message);
    });
  });
});
