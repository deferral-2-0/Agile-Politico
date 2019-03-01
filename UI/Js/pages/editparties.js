const partiescontainer = document.getElementById("render-parties");
partiescontainer.appendChild(createElement(loadingindicator));

const getElementValue = id => {
  const input = document.getElementById(`editparty-${id}`);
  const a = fromNullable(input).fold(x => "emprt", element => element.value);
  return a;
};

const editParty = party_id => {
  fetch(`https://tevpolitico.herokuapp.com/api/v2/parties/${party_id}/name`, {
    method: "PATCH",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      "x-access-token": getToken()
    },
    body: JSON.stringify({
      name: getElementValue(party_id)
    })
  }).then(data => {
    if (data.status === 200) {
      callSnackBar("Party Updated Successfully", "success");
      setTimeout(() => {
        location.reload();
      }, 1600);
    } else {
      callSnackBar("Something went wrong");
    }
  });
};

const deleteParty = party_id => {
  fetch(`https://tevpolitico.herokuapp.com/api/v2/parties/${party_id}`, {
    method: "DELETE",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      "x-access-token": getToken()
    },
    body: JSON.stringify({})
  }).then(data => {
    if (data.status === 200) {
      callSnackBar("Party Deleted Successfully", "success");
      setTimeout(() => {
        location.reload();
      }, 1600);
    } else {
      callSnackBar("Something went wrong");
    }
  });
};

if (isUserAnAdmin()) {
  fetch("https://tevpolitico.herokuapp.com/api/v2/parties")
    .then(data => data.json())
    .then(data => data.data)
    .then(parties => {
      destroyNodeChildren("render-parties");

      let vdomparties = {
        type: "div",
        props: {},
        children: parties.map(party => ({
          type: "div",
          props: { style: "display: flex " },
          children: [
            {
              type: "input",
              props: { value: party.name, id: `editparty-${party.id}` },
              children: [""]
            },
            {
              type: "button",
              props: {
                class: "button button-color",
                style: "align-self: center",
                onclick: `return editParty(${party.id})`
              },
              children: ["\u{2714}"]
            },
            {
              type: "button",
              props: {
                class: "button button-color",
                style: "align-self: center",
                onclick: `return deleteParty(${party.id})`
              },
              children: ["\u{274C}"]
            }
          ]
        }))
      };
      return vdomparties;
    })
    .then(vdom => {
      partiescontainer.appendChild(createElement(vdom));
    });
} else {
  destroyNodeChildren("render-parties");

  const renderalternative = {
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
  };

  partiescontainer.appendChild(createElement(renderalternative));
}
