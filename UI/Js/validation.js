function validateEmail(email) {
  var re = /\S+@\S+\.\S+/;
  return re.test(email);
}

function areValuesEqual(val1, val2) {
  return val1 === val2;
}

function doesFieldContainValidValue(value) {
  return /\S/.test(value) && Boolean(value);
}
