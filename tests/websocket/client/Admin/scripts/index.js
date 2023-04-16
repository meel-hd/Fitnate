const WEBSOCKET_URL = "ws://localhost:8080";

const ws = new WebSocket(WEBSOCKET_URL);

const messages = document.getElementById("messages"); // Messages view

// Show connection status
connectingMessage = createStyledMessage("Connecting...", "Server", "green");
messages.innerHTML += connectingMessage;
// Connection opened with the server connect quitely
ws.onopen = function (event) {
  clearMessages(true);
  message = createStyledMessage(
    "You are connected to the server",
    "Server",
    "green"
  );
  messages.innerHTML += message;
};

// Receive messages
ws.onmessage = function (event) {
  event.data
    .text()
    .then((message) => {
      // Add message to the view
      addMessage(message);
    })
    .catch((error) => {
      console.error(error);
    });
};

// Connection closed: disconnect from the server
ws.onclose = function (event) {
  li = createStyledMessage("Connection closed", "Server", "red");
  messages.innerHTML += li;
  retryButton = `<button class="bg-gray-800 text-white px-4 py-1 mt-4 mx-[auto] rounded-md" onclick="location.reload()">Retry</button>`;
  messages.innerHTML += retryButton;
};

// Add message to the messages view
function addMessage(message) {
  let color = "yellow";
  let sender = "Anonymous";
  // Colorize messages
  if (message.startsWith("Admin:")) {
    color = "red";
    sender = "Admin";
    message = message.replace("Admin:", "");
  }
  if (message.startsWith("Announcement:")) {
    color = "violet";
    sender = "Announcement";
    message = message.replace("Announcement:", "");
  }
  // Add message to the view
  let li = createStyledMessage(message, sender, color);
  messages.innerHTML += li;
  // scroll to the bottom of the view
  messages.scrollTop = messages.scrollHeight;
}

// Create styled message
function createStyledMessage(message, sender, color) {
  return `<div class="-m-2 py-2 ">
            <div class="w-full  bg-white/20 leading-none  rounded-md p-2 shadow text-teal text-sm">
            <div class="flex justify-between">
                <div class="text-${color}-600 text-white max-w-fit mb-1 font-semibold h-6 px-3 justify-center items-center">${sender}</div>
                <p class="text-gray-400 text-xs">${new Date().toLocaleTimeString()}</p>
            </div>
                <div class="px-2 ml-2">${message}</div>
          </div>`;
}
// Send message as admin
function sendAdminMessage() {
  const message = document.getElementById("admin-message").value;
  if (message != "") {
    ws.send("Admin: " + message);
    document.getElementById("admin-message").value = "";
  }
}
// Send announcement
function sendAnnouncement() {
  const message = document.getElementById("announcement").value;
  if (message != "") {
    ws.send("Announcement: " + message);
    document.getElementById("announcement").value = "";
  }
}
// Send anonymous message
function sendAnonMessage() {
  const message = document.getElementById("anon-message").value;
  if (message != "") {
    ws.send(message);
    document.getElementById("anon-message").value = "";
  }
}
// Clear messages view
function clearMessages(withoutClearMessage) {
  messages.innerHTML = '<h1 class="font-semibold mb-4 text-xl">Messages</h1>';
  if (!withoutClearMessage) {
    messages.innerHTML +=
      ' <p class="text-xs text-gray-300 mb-2">Messages cleared</p>';
  }
}
