
function showPassword() {
  var x = document.getElementById("password");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}

function showPassword2() {
  var x = document.getElementById("re-enterPassword");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}

function checkPwMatch() {
  var pw1 = document.getElementById("password");
  var pw2 = document.getElementById("re-enterPassword");
  if (pw1.value === pw2.value) {
    return True;
  } else {
    return False;
  }
}
