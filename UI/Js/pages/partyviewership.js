const partiescontainer = document.getElementById("render-parties");
const createPartyDiv = document.getElementById("createparty");

let partyname, partyhqAddress;

/* logic for creating a party */

function toggleModal() {
  var modal = document.getElementById("myModal");
  if (modal.style.display === "block") {
    modal.style.display = "none";
  } else {
    modal.style.display = "block";
  }
}

let createPartyButton = {
  type: "button",
  props: { class: "button button-color", onclick: `toggleModal()` },
  children: ["Create Party"]
};

let form = {
  type: "form",
  props: { id: "sign-in-form" },
  children: [
    {
      type: "input",
      props: {
        type: "text",
        name: "name",
        id: "name",
        placeholder: "Party Name"
      },
      children: ["h"]
    },
    {
      type: "br",
      props: {},
      children: ["h"]
    },
    {
      type: "br",
      props: {},
      children: ["j"]
    },
    {
      type: "br",
      props: {},
      children: ["j"]
    },
    {
      type: "input",
      props: {
        type: "text",
        name: "hqAddress",
        id: "hqAddress",
        placeholder: "Party hqAddress"
      },
      children: ["h"]
    },
    {
      type: "br",
      props: {},
      children: ["h"]
    },
    {
      type: "br",
      props: {},
      children: ["h"]
    },
    {
      type: "input",
      props: {
        type: "submit",
        id: "submit",
        disabled: "true",
        value: "Enter party to submit"
      },
      children: [""]
    }
  ]
};

let modalvdom = {
  type: "div",
  props: { id: "myModal", class: "modal" },
  children: [
    {
      type: "div",
      props: { class: "modal-content" },
      children: [
        {
          type: "div",
          props: { class: "modal-header" },
          children: [
            {
              type: "div",
              props: {},
              children: ["Create a new party"]
            }
          ]
        },
        {
          type: "div",
          props: { class: "modal-body" },
          children: [
            {
              type: "div",
              props: {},
              children: [form]
            }
          ]
        },
        {
          type: "div",
          props: { class: "modal-footer" },
          children: [
            {
              type: "div",
              props: {},
              children: [
                {
                  type: "button",
                  props: {
                    onclick: `toggleModal()`,
                    class: "button button-color"
                  },
                  children: ["Close"]
                }
              ]
            }
          ]
        }
      ]
    }
  ]
};

if (isUserAnAdmin()) {
  createPartyDiv.appendChild(createElement(createPartyButton));
  document.body.appendChild(createElement(modalvdom));
  var modal = document.getElementById("myModal");
  let submitbtn = document.getElementById("submit");

  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  };

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

  // submit function
  document.getElementById("sign-in-form").onsubmit = function(event) {
    event.preventDefault();

    const p = {
      type: "li",
      props: {},
      children: [
        {
          type: "span",
          props: {},
          children: [
            `${document.getElementsByClassName("partiesindb").length + 1}.`
          ]
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

    document
      .getElementById("orderedlistofparties")
      .appendChild(createElement(p));
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
            var scrollingElement = document.scrollingElement || document.body;
            scrollingElement.scrollTop = scrollingElement.scrollHeight;
            toggleModal();
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
}

partiescontainer.appendChild(createElement(loadingindicator));

fetch("https://tevpolitico.herokuapp.com/api/v2/parties")
  .then(data => data.json())
  .then(({ status, data }) => {
    destroyNodeChildren("render-parties");
    if (status === 200) {
      const partiestoBeRendered = {
        type: "ol",
        props: { id: "orderedlistofparties" },
        children: data.map((party, idx) => ({
          type: "li",
          props: { class: "partiesindb" },
          children: [
            {
              type: "span",
              props: {},
              children: [`${idx + 1}.`]
            },
            {
              type: "p",
              props: {},
              children: [`Party Name:  ${party.name}`]
            },
            {
              type: "p",
              props: {},
              children: [`Party Head Quaters:  ${party.hqAddress}`]
            }
          ]
        }))
      };
      partiescontainer.appendChild(createElement(partiestoBeRendered));
    }
  });
