function validateEmail(email) {
  var re = /\S+@\S+\.\S+/;
  return re.test(email);
}

function areEqual(val1, val2) {
  return val1 === val2;
}
