
function showPassword1() {
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
  var subBtn = document.getElementById("submit-btn");
  if (pw1.value === pw2.value) {
    // return message saying passwords match
    subBtn.disabled = true;
    //return true;
  } else {
    // return message saying don't passwords match
    subBtn.disabled = false;
    //return false;
  }
}

function verifyPswd() {
  var pw1 = document.getElementById("password");
  var pw2 = document.getElementById("re-enterPassword");
  console.log(pw1.value);
  console.log(pw2.value);
  if (pw1.value === pw2.value) {
    // return message saying passwords match
    console.log("passwords match!")
    console.log(pw1.value === pw2.value)
    return true;
  } else {
    // return message saying don't passwords match
    console.log("passwords do not match!")
    return false;
  }
}
