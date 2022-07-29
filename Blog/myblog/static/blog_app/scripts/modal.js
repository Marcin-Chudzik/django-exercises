// Get the modal
var modal = document.getElementById("modal");

// Get triggering button
var btn = document.getElementById("modal-btn");

// Get the button which close modal
var span = document.getElementsByClassName("close")[0];

// Open modal on click button
btn.onclick = function() {
  modal.style.display = "block";
}

// Close modal on click button
span.onclick = function() {
  modal.style.display = "none";
}

// Close modal if click out of modal box
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}