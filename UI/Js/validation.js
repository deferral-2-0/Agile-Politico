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

function formatDate(date) {
  var monthNames = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
  ];

  var day = date.getDate();
  var monthIndex = date.getMonth();
  var year = date.getFullYear();

  return day + " " + monthNames[monthIndex] + " " + year;
}
