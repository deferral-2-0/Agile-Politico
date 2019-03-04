const renderVotingActivity = document.getElementById(
  "voting-activity-container"
);

const vote = (office, candidate) => {
  callSnackBar("Registering vote", (status = "Success"));
  fetch("https://tevpolitico.herokuapp.com/api/v2/votes", {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      "x-access-token": getToken()
    },
    body: JSON.stringify({
      office,
      candidate
    })
  })
    .then(({ data, status }) => {
      if (status === 201) {
        callSnackBar("Voted successfully", (status = "success"));
        setTimeout(() => {
          location.reload();
        }, 1600);
      } else {
        callSnackBar("Something went wrong, try again");
      }
    })
    .catch(_ => {
      callSnackBar("Something went wrong, try again");
    });
};

const renderListOfPoliticians = (politicians, officeid) =>
  politicians.length > 0
    ? politicians.map(contestant => ({
        type: "div",
        props: {},
        children: [
          {
            type: "div",
            props: {},
            children: [
              {
                type: "div",
                props: { class: "votecontainer votecontaineranimate" },
                children: [
                  {
                    type: "div",
                    props: {},
                    children: [contestant.username]
                  },
                  {
                    type: "div",
                    props: {},
                    children: [contestant.email]
                  },
                  {
                    type: "button",
                    props: {
                      class: "button button-color",
                      onclick: `vote(${officeid}, ${contestant.id})`
                    },
                    children: [`Vote ☑`]
                  }
                ]
              }
            ]
          }
        ]
      }))
    : [
        {
          type: "div",
          props: {},
          children: [
            "No one is vying in this position, if you are interested, kindly contact the admin"
          ]
        }
      ];

if (window.localStorage.getItem("user")) {
  renderVotingActivity.appendChild(createElement(loadingindicator));
  fetch("https://tevpolitico.herokuapp.com/api/v2/votes/activity", {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      "x-access-token": getToken()
    },
    body: JSON.stringify({})
  })
    .then(data => data.json())
    .then(({ data }) => {
      destroyNodeChildren("voting-activity-container");
      let formateditems = groupBy(data, "type");
      let officetypes = Object.keys(formateditems);
      let vdom = {
        type: "div",
        props: {},
        children: officetypes.map(type => ({
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
              children: formateditems[type].map(position => ({
                type: "div",
                props: {},
                children: [
                  {
                    type: "div",
                    props: {},
                    children: [
                      {
                        type: "h2",
                        props: { class: "officename" },
                        children: [position.name]
                      },
                      {
                        type: "div",
                        props: {},
                        children:
                          typeof position.info == "string"
                            ? [
                                {
                                  type: "h4",
                                  props: {},
                                  children: [position.info]
                                }
                              ]
                            : renderListOfPoliticians(
                                position.info,
                                position.id
                              )
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
      renderVotingActivity.appendChild(createElement(vdom));
    });
} else {
  let loginfirst = {
    type: "h3",
    props: {},
    children: ["You need to login first"]
  };
  renderVotingActivity.appendChild(createElement(loginfirst));
}
