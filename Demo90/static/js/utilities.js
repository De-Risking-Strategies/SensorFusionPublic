
var elem = document.documentElement;
var modal;
var span;

/* View in fullscreen */
function openFullscreen() {
  if (elem.requestFullscreen) {
    elem.requestFullscreen();
  } else if (elem.webkitRequestFullscreen) { /* Safari */
    elem.webkitRequestFullscreen();
  } else if (elem.msRequestFullscreen) { /* IE11 */
    elem.msRequestFullscreen();
  }
}

/* Close fullscreen */
function closeFullscreen() {
  if (document.exitFullscreen) {
    document.exitFullscreen();
  } else if (document.webkitExitFullscreen) { /* Safari */
    document.webkitExitFullscreen();
  } else if (document.msExitFullscreen) { /* IE11 */
    document.msExitFullscreen();
  }
}

function notImplementedYet(){
  alert("Not Yet Implemented");
}
function btn1_click(){
  var hdr = document.getElementById("modal_header");
  var modal1 = document.getElementById("modal_body1");
  var modal2 = document.getElementById("modal_body2");
  var ftr = document.getElementById("modal_footer");
  hdr.innerHTML  = "Toggle Bar";
  modal1.innerHTML = "Toggle the Bars on/off";
  modal2.innerHTML = "Not Implemented Yet!";
  ftr.innerHTML = "Click out to return";
  modal.style.display = "block";
}
function init(){
modal = document.getElementById("sfModal");

// Get the button that opens the modal
var btn = document.getElementsByClassName("myBtn");
var btnLength = btn.length;
// Get the <span> element that closes the modal
span = document.getElementsByClassName("close")[0];

span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}
}

