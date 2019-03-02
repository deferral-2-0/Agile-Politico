let token = location.search.replace("?token=", "");
const secretmail = parseJwt(token).email;
let submitbtn = document.getElementById("submit");

//inputs

function getValue(event) {
  return event.target.value;
}
let email, password, retypedpassword;

document.getElementById("email").oninput = function(event) {
  email = getValue(event);
  shouldSubmitBeActive();
};
// monitor password field
document.getElementById("password").oninput = function(event) {
  password = getValue(event);
  shouldSubmitBeActive();
};

// monitor retypedpassword field
document.getElementById("retypedpassword").oninput = function(event) {
  retypedpassword = getValue(event);
  shouldSubmitBeActive();
};

function shouldSubmitBeActive() {
  submitbtn.setAttribute("value", "Fill in the form to submit");

  if (
    validateEmail(email) &&
    doesFieldContainValidValue(password) &&
    doesFieldContainValidValue(retypedpassword) &&
    areValuesEqual(password, retypedpassword)
  ) {
    if (email === secretmail) {
      submitbtn.removeAttribute("disabled");
      submitbtn.setAttribute("value", "Set new Password");
    } else {
      submitbtn.setAttribute(
        "value",
        "Sorry, but this this not your reset page"
      );
    }
  } else {
    submitbtn.setAttribute("disabled", true);
  }
}

const resetPassword = () => {
  callSnackBar("Reseting password", "success");

  fetch("https://tevpolitico.herokuapp.com/api/v2/auth/newpassword", {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      email,
      password
    })
  })
    .then(data => data.json())
    .then(data => {
      if (data.status === 200) {
        callSnackBar(data.data.message, "success");
        setTimeout(() => {
          location.replace("login.html");
        }, 1600);
      } else {
        callSnackBar("Something went wrong");
      }
    })
    .catch(_err => {
      callSnackBar("Something went wrong");
    });
};

document.getElementById("forgot-password-form").onsubmit = function(event) {
  event.preventDefault();
  resetPassword();
};
