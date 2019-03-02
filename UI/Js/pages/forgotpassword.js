let email;
let submitbtn = document.getElementById("submit");
function getValue(event) {
  return event.target.value;
}
function shouldSubmitBeActive() {
  if (validateEmail(email)) {
    submitbtn.removeAttribute("disabled");
    submitbtn.setAttribute(
      "value",
      "Send password renewal instructions to mail"
    );
  } else {
    submitbtn.setAttribute("disabled", true);
  }
}

// monitor email field
document.getElementById("email").oninput = function(event) {
  email = getValue(event);
  shouldSubmitBeActive();
};

document.getElementById("sigin-in-form").onsubmit = function(event) {
  event.preventDefault();
  //   window.location.href = "login.html";
  sendPasswordMailLink();
};

// send email function.
const sendPasswordMailLink = () => {
  callSnackBar("Sending reset password mail", "success");
  fetch("https://tevpolitico.herokuapp.com/api/v2/auth/reset", {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      email
    })
  })
    .then(data => data.json())
    .then(data => {
      if (data.status === 200) {
        callSnackBar("Check your mail box", "success");
        setTimeout(() => {
          window.location.href = "index.html";
        }, 1600);
      } else {
        callSnackBar(data.error);
      }
    })
    .catch(_err => {
      callSnackBar("something went wrong");
    });
};
