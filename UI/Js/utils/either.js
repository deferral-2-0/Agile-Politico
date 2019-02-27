const Right = x => ({
  map: f => Right(f(x)),
  fold: (f, g) => g(x),
  inspect: () => `Right(${x})`
});

const Left = x => ({
  map: f => Left(x),
  fold: (f, g) => f(x),
  inspect: () => `Left(${x})`
});

const fromNullable = x => (x != null ? Right(x) : Left(null));

const getnotifications = fromNullable(
  window.localStorage.getItem("notifications")
).fold(_ => [], notifications => JSON.parse(notifications));

const notification = (notification, i) => ({
  type: "div",
  props: { class: "alert" },
  children: [
    {
      type: "strong",
      props: {},
      children: [notification]
    }
  ]
});

const notifications = {
  type: "div",
  props: {},
  children: getnotifications.map(notification)
};

const $notifications = document.getElementById("notifications");

// append the list of notifications only when the notificcations tab is opens
fromNullable($notifications).fold(
  x => null,
  element => {
    element.appendChild(createElement(notifications));
    setTimeout(() => {
      destroyNodeChildren("notifications");
      window.localStorage.removeItem("notifications");
    }, 3000);
  }
);
