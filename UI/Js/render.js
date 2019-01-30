const a = {
  type: "ul",
  props: { class: "list" },
  children: [
    {
      type: "li",
      props: {},
      children: ["item 1"]
    },
    {
      type: "li",
      props: {},
      children: ["Item 2"]
    }
  ]
};

//the createElement function renders the items provided and calls itself recursively
// based on whether children are provided or not
function createElement(node) {
  if (typeof node === "string") {
    return document.createTextNode(node);
  }
  const $el = document.createElement(node.type);
  for (let val in node.props) {
    $el.setAttribute(val, node.props[val]);
  }
  node.children.map(createElement).forEach($el.appendChild.bind($el));
  return $el;
}

const $root = document.getElementById("root");
$root.appendChild(createElement(a));
