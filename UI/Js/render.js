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

const isUserAnAdminObject = isUserAnAdmin()
  ? {
      type: "a",
      props: { href: "admindash.html" },
      children: ["Admin Dash"]
    }
  : {
      type: "div",
      props: {},
      children: [""]
    };

const isUserLoggedIn = window.localStorage.getItem("user")
  ? [
      isUserAnAdminObject,
      {
        type: "a",
        props: {
          onclick: `(function(){
            window.localStorage.removeItem("user")
            location.replace("index.html")
            callSnackBar("Logged out User")
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
  props: { class: "topnav", id: "myTopnav" },
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
    {
      type: "a",
      props: { href: "results.html" },
      children: ["Results"]
    },
    ...isUserLoggedIn,
    {
      type: "a",
      props: { href: "#", onclick: `dropDownMenu()`, class: "icon" },
      children: [
        {
          type: "img",
          props: { src: "./images/menu.svg" },
          children: [""]
        }
      ]
    }
  ]
};

function dropDownMenu() {
  var x = document.getElementById("myTopnav");
  if (x.className === "topnav") {
    x.className += " responsive";
  } else {
    x.className = "topnav";
  }
}

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

/**
 *
 * THis function removes an element
 * by id.
 */
function removeElementById(id) {
  var elem = document.getElementById(id);
  return elem.parentNode.removeChild(elem);
}

const callSnackBar = (message, status = "error") => {
  const colorToPick = status === "error" ? "#b42121" : "#48b427";
  let snackbarcomponent = {
    type: "div",
    props: {
      id: "snackbar",
      class: "show",
      style: `background-color: ${colorToPick}`
    },
    children: [message]
  };
  const $body = document.getElementsByTagName("body")[0];
  $body.appendChild(createElement(snackbarcomponent));
  // remove the snackbar after a few seconds.
  setTimeout(function() {
    removeElementById("snackbar");
  }, 5500);
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

const loadingindicator = {
  type: "div",
  props: { class: "sk-cube-grid" },
  children: Array.from({ length: 9 }, (v, k) => k + 1).map((cube, idx) => ({
    type: "div",
    props: { class: `sk-cube sk-cube${cube}` },
    children: [""]
  }))
};

const groupBy = (items, key) =>
  items.reduce(
    (result, item) => ({
      ...result,
      [item[key]]: [...(result[item[key]] || []), item]
    }),
    {}
  );
