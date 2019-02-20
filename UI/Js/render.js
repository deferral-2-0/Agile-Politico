//the createElement function renders the items provided and calls itself recursively
// based on whether children are provided or not
const createElement = node => {
  if (typeof node === "string") {
    return document.createTextNode(node);
  }
  const $el = document.createElement(node.type);
  for (let val in node.props) {
    $el.setAttribute(val, node.props[val]);
  }
  node.children.map(createElement).forEach($el.appendChild.bind($el));
  return $el;
};

const isUserLoggedIn = window.localStorage.getItem("user")
  ? [
      {
        type: "a",
        props: {
          onclick: `(function(){
            alert('Are you sure you want to logout');
            window.localStorage.removeItem("user")
            location.reload();
          })()`
        },
        children: ["Logout"]
      }
    ]
  : [
      {
        type: "a",
        props: { href: "login.html" },
        children: ["Login"]
      },
      {
        type: "a",
        props: { href: "sign-up.html" },
        children: ["Sign Up"]
      }
    ];

const layout = {
  type: "header",
  props: { class: "topnav" },
  children: [
    {
      type: "a",
      props: { href: "index.html" },
      children: ["Politico"]
    },
    {
      type: "div",
      props: { class: "flex" },
      children: []
    },
    {
      type: "a",
      props: { href: "contestants.html" },
      children: ["Contestants"]
    },
    {
      type: "a",
      props: { href: "party-viewership.html" },
      children: ["View Parties"]
    },
    {
      type: "a",
      props: { href: "vote.html" },
      children: ["Vote"]
    },
    ...isUserLoggedIn
  ]
};

/**
 *
 * @param {id} - id of the node to be deleted.
 */
const destroyNodeChildren = id => {
  var myNode = document.getElementById(id);
  while (myNode.firstChild) {
    myNode.removeChild(myNode.firstChild);
  }

  return myNode;
};

if ("serviceWorker" in navigator) {
  console.log("CLIENT: service worker registration in progress.");
  navigator.serviceWorker.register("./Js/service-worker.js").then(
    function() {
      console.log("CLIENT: service worker registration complete.");
    },
    function(e) {
      console.log("CLIENT: service worker registration failure.", e);
    }
  );
} else {
  console.log("CLIENT: service worker is not supported.");
}
