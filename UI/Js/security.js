const parseJwt = token => {
  var base64Url = token.split(".")[1];
  var base64 = base64Url.replace("-", "+").replace("_", "/");
  return JSON.parse(window.atob(base64));
};

const getToken = () => {
  const userobj = JSON.parse(window.localStorage.getItem("user"));

  return userobj ? userobj.token : null;
};

const isUserAnAdmin = () => {
  const userobj = getToken();
  if (userobj) {
    const token = userobj;
    return (
      parseJwt(token).email === "admindetails@gmail.com" ||
      parseJwt(token).isAdmin === true
    );
  } else {
    return false;
  }
};
