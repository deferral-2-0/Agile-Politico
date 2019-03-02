let ordinarydom = document.getElementById("ordinary-users");
let admindom = document.getElementById("admin-users");
let container = document.getElementById("container");

const elevateUser = user_id => {
  callSnackBar("Elevating User", (status = "Success"));
  fetch(`https://tevpolitico.herokuapp.com/api/v2/authorize/${user_id}`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      "x-access-token": getToken()
    },
    body: JSON.stringify({})
  }).then(data => {
    if (data.status === 200) {
      callSnackBar("User elevated to admin successfully", (status = "Success"));
      setTimeout(() => {
        location.reload();
      }, 1600);
    } else {
      callSnackBar("Something went wrong");
    }
  });
};

if (isUserAnAdmin()) {
  admindom.appendChild(createElement(loadingindicator));
  ordinarydom.appendChild(createElement(loadingindicator));
  fetch("https://tevpolitico.herokuapp.com/api/v2/users")
    .then(data => data.json())
    .then(({ data }) => {
      destroyNodeChildren("admin-users");
      destroyNodeChildren("ordinary-users");
      let ordinaryusers = data.filter(user => !user.isAdmin);
      let adminusers = data.filter(user => user.isAdmin);
      let ordinaryusersvdom = {
        type: "div",
        props: {},
        children: ordinaryusers.map(user => ({
          type: "div",
          props: { class: "votecontainer" },
          children: [
            {
              type: "div",
              props: {},
              children: [user.username]
            },
            {
              type: "div",
              props: {},
              children: [user.email]
            },
            {
              type: "div",
              props: {},
              children: [
                {
                  type: "button",
                  props: {
                    class: "button button-color",
                    onclick: `elevateUser(${user.id})`
                  },
                  children: ["Elevate 👍"]
                }
              ]
            }
          ]
        }))
      };

      let adminusersvdom = {
        type: "div",
        props: {},
        children: adminusers.map(user => ({
          type: "div",
          props: { class: "votecontainer" },
          children: [
            {
              type: "div",
              props: {},
              children: ["👑"]
            },
            {
              type: "div",
              props: {},
              children: [user.username]
            },
            {
              type: "div",
              props: {},
              children: [user.email]
            }
          ]
        }))
      };

      // ordinary users
      ordinarydom.appendChild(createElement(ordinaryusersvdom));
      // admin users.
      admindom.appendChild(createElement(adminusersvdom));
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
