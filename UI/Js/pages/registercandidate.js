function arrayDifference(candidates, users) {
  function find(user) {
    if (
      candidates.map(({ username }) => username).indexOf(user.username) === -1
    ) {
      return user;
    }
  }

  let searchterm = localStorage.getItem("searchuser");
  if (searchterm) {
    return users.filter(user => user.username === searchterm).filter(find);
  }
  return users.filter(find);
}

const getUsers = fetch("https://tevpolitico.herokuapp.com/api/v2/users").then(
  data => data.json()
);
const getMetaInfo = fetch(
  "https://tevpolitico.herokuapp.com/api/v2/offices/metainfo"
).then(data => data.json());

const container = document.getElementById("container");

const setSearchTerm = username => {
  localStorage.setItem("searchuser", username);
};

const clearItem = () => {
  localStorage.removeItem("searchuser");
};

const search = () => {
  const searchbox = document.getElementById("searchbox");
  setSearchTerm(searchbox.value);
  renderFn();
};

// the main reason we are here

const registerCandidate = (user, office_id) => {
  callSnackBar("Registering vote", (status = "Success"));
  fetch(
    `https://tevpolitico.herokuapp.com/api/v2/offices/${office_id}/register`,
    {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        "x-access-token": getToken()
      },
      body: JSON.stringify({
        user
      })
    }
  )
    .then(data => {
      if (data.status === 201) {
        callSnackBar("Registered Candidate", (status = "Success"));
        setTimeout(() => {
          location.reload();
        }, 1600);
      } else {
        callSnackBar("Something went wrong");
      }
    })
    .catch(_err => {
      callSnackBar("Something went wrong, try again later");
    });
};

function renderFn() {
  if (isUserAnAdmin()) {
    container.appendChild(createElement(loadingindicator));

    Promise.all([getUsers, getMetaInfo])
      .then(function(values) {
        destroyNodeChildren("container");
        const allusers = values[0];
        const alloffices = groupBy(values[1].data, "type");
        let officetypelist = Object.keys(alloffices);
        let vdom = {
          type: "div",
          props: {},
          children: [
            {
              type: "input",
              props: { placeholder: "search by username", id: "searchbox" },
              children: ["Search"]
            },
            {
              type: "button",
              props: { class: "button button-color", onclick: `search()` },
              children: ["Search 🔍"]
            },
            {
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
                    children: alloffices[type].map(office => ({
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
                          children: arrayDifference(
                            office.candidates,
                            allusers.data
                          ).map(candidate => ({
                            type: "div",
                            props: { class: "votecontainer" },
                            children: [
                              `${candidate.username} - Email: ${
                                candidate.email
                              }`
                            ],
                            children: [
                              {
                                type: "div",
                                props: {},
                                children: [candidate.username]
                              },
                              {
                                type: "div",
                                props: {},
                                children: [` 🗲  ${candidate.email} 🗲`]
                              },
                              {
                                type: "button",
                                props: {
                                  class: "button button-color",
                                  onclick: `registerCandidate(${
                                    candidate.id
                                  }, ${office.id})`
                                },
                                children: [`Register Candidate ®️`]
                              }
                            ]
                          }))
                        }
                      ]
                    }))
                  }
                ]
              }))
            }
          ]
        };
        return vdom;
      })
      .then(vdom => {
        clearItem();
        container.appendChild(createElement(vdom));
      });
  } else {
    container.appendChild(
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
  }
}

renderFn();
