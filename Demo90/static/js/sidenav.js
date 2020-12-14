/* Set the width of the side navigation to 250px and the left margin of the page content to 250px */
function openNav() {
  document.getElementById("sfSidenav").style.width = "20%";
  document.getElementById("main").style.marginLeft = "20%";
}

/* Set the width of the side navigation to 0 and the left margin of the page content to 0 */
function closeNav() {
  document.getElementById("sfSidenav").style.width = "0";
  document.getElementById("main").style.marginLeft = "0";
}
function openSettings() {
  document.getElementById("sfSettings").style.width = "18%";
  document.getElementById("main").style.marginRight = "18%";
}

function closeSettings() {
  document.getElementById("sfSettings").style.width = "0";
  document.getElementById("main").style.marginRight = "0";
}
