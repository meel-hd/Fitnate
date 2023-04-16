function openModal() {
  // Add code to open the modal
  document.getElementById("modal").classList.remove("hidden");
  document.body.classList.add("modal-open");
}

function closeModal() {
  // Add code to close the modal
  document.getElementById("modal").classList.add("hidden");
  document.body.classList.remove("modal-open");
}

let time = 5 * 1000; // Default time is 5 seconds

function sendAfterTime() {
  // inform the user that the message will be sent after time
  addMessage(
    "Anouncemt will be sent after " +
      time / 1000 +
      " seconds time after time, to stop it reload the page"
  );
  closeModal();
  // Add code to send a message after time repeatedly
  setInterval(() => {
    content = document.getElementById("auto-announcement").value;
    if (content != "") {
      ws.send("Announcement: " + content);
    }
  }, time);
}

function changeTime() {
  time = document.getElementById("auto-announcement-time").value * 1000;
}

function cancelSendAfterTime() {
  location.reload();
}

function toggleFullscreen() {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen();
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen();
    }
  }
}
