/**
 * TARGET SERVER
 *
 * This is a simple server that returns a random valid HTTP response code.
 * It is used to test the HTTP response code checker.
 * To use it, run `node server.js` in the terminal.
 * Then, in the browser, go to http://localhost:5000
 *
 * You should see a random HTTP response code.
 * You can change the port number by changing the `PORT` variable.
 * You can also change the response code by changing the `responseNumber` variable.
 * You can also change the response message by changing the `res.end()` function.
 *
 */

const http = require("http");

const server = http.createServer((req, res) => {
  // Send a a random valid response number
  const responseNumber = Math.floor(Math.random() * 400) + 100;
  res.statusCode = responseNumber;

  res.setHeader("Content-Type", "text/plain");
  res.end("OK");
});

const PORT = 5000; // Change this to the desired port number
server.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
