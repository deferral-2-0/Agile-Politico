let officename, officetype;
let submitbtn = document.getElementById("submit");
let positionscontainer = document.getElementById("list-of-offices");
let positionslist = document.getElementById("positionslist");
let allofficenames = [];

positionscontainer.appendChild(createElement(loadingindicator));

function getValue(event) {
  return event.target.value;
}

if (!isUserAnAdmin()) {
  mynode = destroyNodeChildren("center");
  mynode.appendChild(
    createElement({
      type: "div",
      props: {},
      children: [
        {
          type: "h3",
          props: { style: "margin-bottom: 20px" },
          children: ["You are not an admin"]
        },
        {
          type: "a",
          props: { class: "button button-color", href: "index.html" },
          children: ["Kindly Navigate back to the home page"]
        }
      ]
    })
  );
} else {
  // get the list of offices from the db
  fetch("https://tevpolitico.herokuapp.com/api/v2/offices")
    .then(data => data.json())
    .then(({ status, data }) => {
      destroyNodeChildren("list-of-offices");
      if (status === 200) {
        allofficenames = data.map(({ name }) => name);
        const renderingList = {
          type: "ol",
          props: { id: "positionslist" },
          children: data.map((office, idx) => ({
            type: "li",
            props: {},
            children: [
              {
                type: "span",
                props: {},
                children: [`${idx + 1}.`]
              },
              {
                type: "p",
                props: {},
                children: [` ${office.name} `]
              },
              {
                type: "p",
                props: {},
                children: [`Office type ${office.type}`]
              }
            ]
          }))
        };
        positionscontainer.appendChild(createElement(renderingList));
      }
    });

  function shouldSubmitBeActive() {
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

  document.getElementById("name").oninput = function(event) {
    officename = getValue(event);
    shouldSubmitBeActive();
  };

  document.getElementById("type").oninput = function(event) {
    officetype = getValue(event);
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
          children: [`${allofficenames.length + 1}.`]
        },
        {
          type: "p",
          props: {},
          children: [` ${officename} `]
        },
        {
          type: "p",
          props: {},
          children: [`Office type ${officetype}`]
        }
      ]
    };
    allofficenames = [...allofficenames, officename];
    document.getElementById("positionslist").appendChild(createElement(p));
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
    //   setTimeout(() => {
    //     location.replace("admindash.html");
    //   }, 1000);
  };
}
