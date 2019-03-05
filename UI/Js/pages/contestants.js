const $contestants = document.getElementById("render-posts-&-contestants");
const createofficebuttoncontainer = document.getElementById("createoffice");
let officename, officetype;

let createOfficeButton = {
  type: "button",
  props: { class: "button button-color", onclick: `toggleModal()` },
  children: ["Create Office"]
};

let allofficenames = [];

function getValue(event) {
  return event.target.value;
}
function toggleModal() {
  var modal = document.getElementById("myModal");
  if (modal.style.display === "block") {
    modal.style.display = "none";
  } else {
    modal.style.display = "block";
  }
}

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
        placeholder: "Office Name"
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
        name: "type",
        id: "type",
        placeholder: "Office Type"
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
              children: ["Create a new Office"]
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

function shouldSubmitBeActive() {
  let submitbtn = document.getElementById("submit");

  if (
    doesFieldContainValidValue(officename) &&
    doesFieldContainValidValue(officetype)
  ) {
    if (allofficenames.includes(officename)) {
      submitbtn.setAttribute("value", "Government Office already exists");
      submitbtn.setAttribute("disabled", true);
    } else {
      submitbtn.removeAttribute("disabled");
      submitbtn.setAttribute("value", "Submit");
    }
  }
}

if (isUserAnAdmin()) {
  createofficebuttoncontainer.appendChild(createElement(createOfficeButton));
  document.body.appendChild(createElement(modalvdom));
  var modal = document.getElementById("myModal");
  let submitbtn = document.getElementById("submit");

  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  };

  document.getElementById("name").oninput = function(event) {
    officename = getValue(event);
    shouldSubmitBeActive();
  };

  document.getElementById("type").oninput = function(event) {
    officetype = getValue(event);
    shouldSubmitBeActive();
  };

  // submit name
  document.getElementById("sign-in-form").onsubmit = function(event) {
    event.preventDefault();
    document.getElementById("name").value = "";
    document.getElementById("type").value = "";
    submitbtn.setAttribute("disabled", true);
    submitbtn.setAttribute("value", "Fill in name of position to enter");
    if (isUserAnAdmin()) {
      fetch("https://tevpolitico.herokuapp.com/api/v2/offices", {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          "x-access-token": getToken()
        },
        body: JSON.stringify({
          name: officename,
          type: officetype
        })
      })
        .then(data => data.json())
        .then(({ status, error }) => {
          if (status === 201) {
            callSnackBar("Office Created Successfully", "success");
            toggleModal();
            performFetchOfOffices();
            var scrollingElement = document.scrollingElement || document.body;
            scrollingElement.scrollTop = scrollingElement.scrollHeight;
          } else {
            callSnackBar(error);
          }
        });
    } else {
      callSnackBar("You cannot create a new office since you are not an admin");
    }
    officetype = "";
    officename = "";
  };
}

const performFetchOfOffices = () => {
  $contestants.appendChild(createElement(loadingindicator));

  fetch("https://tevpolitico.herokuapp.com/api/v2/offices/metainfo")
    .then(data => data.json())
    .then(data => {
      allofficenames = data.data.map(({ name }) => name);
      return groupBy(data.data, "type");
    })
    .then(data => {
      destroyNodeChildren("render-posts-&-contestants");
      let officetypelist = Object.keys(data);
      let vdom = {
        type: "div",
        props: {},
        children: officetypelist.map(type => ({
          type: "div",
          props: {},
          children: [
            {
              type: "h1",
              props: { class: "positiontitle" },
              children: [`Office-type: ${type}`]
            },
            {
              type: "div",
              props: {},
              children: data[type].map(office => ({
                type: "div",
                props: {},
                children: [
                  {
                    type: "h3",
                    props: { class: "officename" },
                    children: [office.name]
                  },
                  {
                    type: "div",
                    props: {},
                    children:
                      office.candidates.length > 0
                        ? office.candidates.map(candidate => ({
                            type: "div",
                            props: { class: "votecontainer shadow" },
                            children: [
                              {
                                type: "h3",
                                props: {},
                                children: [candidate.username]
                              },
                              {
                                type: "h3",
                                props: {},
                                children: ["Email"]
                              },
                              {
                                type: "h3",
                                props: {},
                                children: [candidate.email]
                              }
                            ]
                          }))
                        : [
                            {
                              type: "h3",
                              props: { class: "candidatesinfo" },
                              children: [
                                "No One is vying in this post contact the admin if you are interested"
                              ]
                            }
                          ]
                  }
                ]
              }))
            }
          ]
        }))
      };
      return vdom;
    })
    .then(vdom => {
      $contestants.appendChild(createElement(vdom));
    });
};

performFetchOfOffices();
