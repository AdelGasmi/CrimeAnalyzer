Object.size = function(obj) {
  var size = 0,
    key;
  for (key in obj) {
    if (obj.hasOwnProperty(key)) size++;
  }
  return size;
};
function getSafe(fn, defaultVal) {
  try {
    return fn();
  } catch (e) {
    return defaultVal;
  }
}
function forecastAll(records) {
  var data = [];
  var x1 = [];
  var y1 = [];
  var x2 = [];
  var y2 = [];

  for (i = 0; i < Object.size(records.crimes); i++) {
    number = records.crimes[i].y;
    date = records.crimes[i].ds;
    x1.push(date);
    y1.push(number);
  }
  var trace1 = {
    x: x1,
    y: y1,
    mode: "lines",
    type: "scatter",
    name: "taux réel"
  };

  for (i = 0; i < Object.size(records.forecast); i++) {
    number2 = Math.round(records.forecast[i].yhat);
    console.log(number2);
    date2 = records.forecast[i].ds;
    x2.push(date2);
    y2.push(number2);
  }

  var trace2 = {
    x: x2,
    y: y2,

    mode: "lines+markers",
    type: "scatter",
    name: "Taux prédit",
    marker: {
      color: "rgb(17, 157, 255)",
      size: 5,
      line: {
        color: "#f3cec9",
        width: 1
      }
    }
  };
  var data = [trace1, trace2];
  var layout = {
    xaxis: {
      type: "date",
      title: "Les jours"
    },
    colorway: ["red", "black"],
    title: "Le nombre de crimes par jour"
  };
  Plotly.newPlot("myDiv", data, layout, { showSendToCloud: false });
}
