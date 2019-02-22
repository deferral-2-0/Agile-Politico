let partyname, partyhqAddress;
let submitbtn = document.getElementById("submit");
let partylistcontainer = document.getElementById("list-of-parties");
let partylist = document.getElementById("partylist");

function getValue(event) {
  return event.target.value;
}

function shouldSubmitBeActive() {
  if (
    doesFieldContainValidValue(partyname) &&
    doesFieldContainValidValue(partyhqAddress)
  ) {
    submitbtn.removeAttribute("disabled");
    submitbtn.setAttribute("value", "Create Party");
  } else {
    submitbtn.setAttribute("value", "Some Values are missing");
    submitbtn.setAttribute("disabled", true);
  }
}

document.getElementById("name").oninput = function(event) {
  partyname = getValue(event);
  shouldSubmitBeActive();
};

document.getElementById("hqAddress").oninput = function(event) {
  partyhqAddress = getValue(event);
  shouldSubmitBeActive();
};

// submit name
document.getElementById("sigin-in-form").onsubmit = function(event) {
  event.preventDefault();

  const p = {
    type: "li",
    props: {},
    children: [
      {
        type: "span",
        props: {},
        children: [``]
      },
      {
        type: "p",
        props: {},
        children: [` ${partyname} `]
      },
      {
        type: "p",
        props: {},
        children: [`Party HQ ${partyhqAddress}`]
      }
    ]
  };

  document.getElementById("render-parties").appendChild(createElement(p));
  document.getElementById("name").value = "";
  document.getElementById("hqAddress").value = "";
  submitbtn.setAttribute("disabled", true);
  submitbtn.setAttribute("value", "Enter party name to submit");
  if (isUserAnAdmin()) {
    fetch("https://tevpolitico.herokuapp.com/api/v2/parties", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        "x-access-token": getToken()
      },
      body: JSON.stringify({
        name: partyname,
        hqAddress: partyhqAddress
      })
    })
      .then(data => data.json())
      .then(({ status, error }) => {
        if (status === 201) {
          callSnackBar("Party Created Successfully", "success");
        } else {
          callSnackBar(error);
        }
      });
  } else {
    callSnackBar("You cannot create a new party since you are not an admin");
  }

  partyname = "";
  partyhqAddress = "";
};
