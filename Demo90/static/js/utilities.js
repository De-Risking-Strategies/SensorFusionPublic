
var elem = document.documentElement;
 
/* View in fullscreen */
function openFullscreen() {
  var openFullScreen = document.getElementById("open_fullscreen");
  var closeFullScreen = document.getElementById("close_fullscreen");
 
  openFullScreen.style.display = "none";
  closeFullScreen.style.display = "block";
  
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
  var openFullScreen = document.getElementById("open_fullscreen");
  var closeFullScreen = document.getElementById("close_fullscreen");
 
  openFullScreen.style.display = "block";
  closeFullScreen.style.display = "none";
  
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



