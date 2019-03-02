let email,
  username,
  password,
  reenterpassword,
  firstname,
  lastname,
  phonenumber;
let submitbtn = document.getElementById("submit");
let politicianBoolean = document.getElementById("politician");
let isAlreadySignedUp = {
  type: "h3",
  props: {},
  children: ["You are signed in already"]
};
if (window.localStorage.getItem("user")) {
  mynode = destroyNodeChildren("center");
  mynode.appendChild(createElement(isAlreadySignedUp));
} else {
  /**
   * register every event in the app
   *
   */

  function getValue(event) {
    return event.target.value;
  }

  //pred function for making sure the SUBMIT BUTTON IS disabled or active
  function shouldSubmitBeActive() {
    if (
      validateEmail(email) &&
      doesFieldContainValidValue(username) &&
      doesFieldContainValidValue(password) &&
      doesFieldContainValidValue(reenterpassword) &&
      doesFieldContainValidValue(firstname) &&
      doesFieldContainValidValue(lastname) &&
      doesFieldContainValidValue(phonenumber) &&
      areValuesEqual(password, reenterpassword)
    ) {
      submitbtn.removeAttribute("disabled");
      submitbtn.setAttribute("value", "Submit");
    } else {
      submitbtn.setAttribute("disabled", true);
    }
  }

  // monitor email field
  document.getElementById("email").oninput = function(event) {
    email = getValue(event);
    shouldSubmitBeActive();
  };
  // monitor username field
  document.getElementById("username").oninput = function(event) {
    username = getValue(event);
    shouldSubmitBeActive();
  };

  // monitor firstname field
  document.getElementById("firstname").oninput = function(event) {
    firstname = getValue(event);
    shouldSubmitBeActive();
  };

  document.getElementById("lastname").oninput = function(event) {
    lastname = getValue(event);
    shouldSubmitBeActive();
  };

  //monitor password field
  document.getElementById("password").oninput = function(event) {
    password = getValue(event);
    shouldSubmitBeActive();
  };

  // monitor re-enter password field
  document.getElementById("reenter-password").oninput = function(event) {
    reenterpassword = getValue(event);
    shouldSubmitBeActive();
  };

  // monitor phonenumber
  document.getElementById("phonenumber").oninput = function(event) {
    phonenumber = getValue(event);
    shouldSubmitBeActive();
  };
  document.getElementById("sigin-in-form").onsubmit = function(event) {
    event.preventDefault();
    // get all fields.
    allfields = {
      email,
      username,
      password,
      retypedpassword: reenterpassword,
      passportUrl: "",
      phone: phonenumber,
      firstname,
      lastname
    };
    fetch("https://tevpolitico.herokuapp.com/api/v2/auth/signup", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json"
      },
      body: JSON.stringify(allfields)
    })
      .then(res => res.json())
      .then(({ data, status, error }) => {
        if (status === 201) {
          window.localStorage.setItem("user", JSON.stringify(data[0]));
          newnotifications = JSON.stringify(["Signed up successfully"]);
          window.localStorage.setItem("notifications", newnotifications);
          location.replace("index.html");
        } else {
          callSnackBar(error.replace("Error.", ""));
        }
      })
      .catch(_err => {
        callSnackBar("Something went wrong");
      });
  };
}
