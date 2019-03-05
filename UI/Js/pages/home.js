let homeaccounts = document.querySelectorAll("#homeaccounticons");
console.log(localStorage.getItem("user"));

let login = {
  type: "div",
  props: { class: "space-evenly" },
  children: [
    {
      type: "a",
      props: { href: "login.html", class: "button button-color" },
      children: ["Login"]
    },
    {
      type: "a",
      props: { href: "sign-up.html", class: "button button-color" },
      children: ["Sign Up"]
    }
  ]
};

fromNullable(JSON.parse(localStorage.getItem("user"))).fold(
  _ => {
    homeaccounts.forEach(element => {
      element.appendChild(createElement(login));
    });
  },
  user => {
    let userinfo = {
      type: "div",
      props: { class: "space-evenly" },
      children: [
        {
          type: "div",
          props: { class: "paralax-header" },
          children: [user.user.username]
        },
        {
          type: "a",
          props: { href: "vote.html", class: "button button-color" },
          children: ["View Your Voting activity"]
        }
      ]
    };
    homeaccounts.forEach(element => {
      element.appendChild(createElement(userinfo));
    });
  }
);
