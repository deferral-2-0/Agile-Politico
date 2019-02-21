let partyname;
let submitbtn = document.getElementById("submit");
let partylistcontainer = document.getElementById("list-of-parties");
let partylist = document.getElementById("partylist");

function getValue(event) {
  return event.target.value;
}

function shouldSubmitBeActive() {
  if (doesFieldContainValidValue(partyname)) {
    if (parties.includes(partyname)) {
      submitbtn.setAttribute("value", "Party name already exists");
      submitbtn.setAttribute("disabled", true);
    } else {
      submitbtn.removeAttribute("disabled");
      submitbtn.setAttribute("value", "Create Party");
    }
  }
}

document.getElementById("name").oninput = function(event) {
  partyname = getValue(event);
  shouldSubmitBeActive();
};

// submit name
document.getElementById("sigin-in-form").onsubmit = function(event) {
  event.preventDefault();
  parties = [...parties, partyname];
  const p = {
    type: "li",
    props: {},
    children: [partyname]
  };
  document.getElementById("render-parties").appendChild(createElement(p));
  document.getElementById("name").value = "";
  submitbtn.setAttribute("disabled", true);
  submitbtn.setAttribute("value", "Enter party name to submit");
};
