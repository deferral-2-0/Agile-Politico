let email, password;
let submitbtn = document.getElementById("submit");

function getValue(event) {
  return event.target.value;
}
function shouldSubmitBeActive() {
  if (
    doesFieldContainValidValue(email) &&
    doesFieldContainValidValue(password)
  ) {
    submitbtn.removeAttribute("disabled");
    submitbtn.setAttribute("value", "Submit");
  } else {
    submitbtn.setAttribute("disabled", true);
  }
}

let isAlreadySignedUp = {
  type: "h3",
  props: {},
  children: ["You are signed in already"]
};

if (window.localStorage.getItem("user")) {
  mynode = destroyNodeChildren("center");
  mynode.appendChild(createElement(isAlreadySignedUp));
} else {
  document.getElementById("email").oninput = function(event) {
    email = getValue(event);
    shouldSubmitBeActive();
  };
  document.getElementById("password").oninput = function(event) {
    password = getValue(event);
    shouldSubmitBeActive();
  };

  document.getElementById("sigin-in-form").onsubmit = function(event) {
    event.preventDefault();
    fetch("https://tevpolitico.herokuapp.com/api/v2/auth/signin", {
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
      .then(res => res.json())
      .then(({ data, status, error }) => {
        if (status === 200) {
          window.localStorage.setItem("user", JSON.stringify(data));
          callSnackBar("Signed in successfully", "success");
          newnotifications = JSON.stringify(["Signed in successfully"]);
          window.localStorage.setItem("notifications", newnotifications);
          // redirect admin to admin dash but user to home page.
          if (email === "admindetails@gmail.com") {
            location.replace("admindash.html");
            return;
          }
          location.replace("index.html");
        } else {
          callSnackBar(error);
        }
      })
      .catch(console.log);
  };
}
