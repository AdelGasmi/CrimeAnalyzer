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


function forecastChart(records) {
  am4core.useTheme(am4themes_animated);

  var chart = am4core.create("firstForecast", am4charts.XYChart);

  var data = [];

  for (i = 0; i < Object.size(records.crimes); i++) {
    price = getSafe(() => records.crimes[i].y, 0);
    quantity = records.forecast[i].yhat;
    data.push({
      date: new Date(records.forecast[i].ds),
      price: price,
      quantity: quantity
    });
  }

  chart.data = data;

  var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
  dateAxis.renderer.grid.template.location = 0.001;
  dateAxis.renderer.ticks.template.length = 8;
  dateAxis.renderer.ticks.template.strokeOpacity = 0.1;

  var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
  valueAxis.tooltip.disabled = true;

  var series = chart.series.push(new am4charts.LineSeries());
  series.dataFields.dateX = "date";
  series.dataFields.valueY = "price";
  series.tooltipText = "{valueY.value}";
  series.name = "Taux de criminalité";
  series.sequencedInterpolation = true;

  var valueAxis2 = chart.yAxes.push(new am4charts.ValueAxis());
  valueAxis2.tooltip.disabled = true;
  valueAxis2.renderer.opposite = true;
  valueAxis2.renderer.grid.template.disabled = true;

  var series2 = chart.series.push(new am4charts.LineSeries());
  series2.dataFields.dateX = "date";
  series2.dataFields.valueY = "quantity";
  series2.yAxis = valueAxis2;
  series2.tooltipText = "{valueY.value}";
  series2.name = "Series 2";
  series2.sequencedInterpolation = true;

  chart.cursor = new am4charts.XYCursor();
  chart.cursor.xAxis = dateAxis;

  var scrollbarX = new am4charts.XYChartScrollbar();
  scrollbarX.series.push(series);
  chart.scrollbarX = scrollbarX;

  chart.legend = new am4charts.Legend();
  chart.legend.parent = chart.plotContainer;
  chart.legend.zIndex = 100;
  chart.legend.valueLabels.template.text = "{valueY.value.formatNumber('$#.')}";
}

function forecastTrend(records) {
  var chartData = generateChartData(records);

  var chart = AmCharts.makeChart("chartdiv", {
    type: "serial",
    language: "fr",
    theme: "dark",
    legend: {
      useGraphSettings: true
    },
    dataProvider: chartData,
    synchronizeGrid: true,
    valueAxes: [
      {
        id: "v1",
        axisColor: "#FF6600",
        axisThickness: 2,
        axisAlpha: 1,
        position: "left"
      },
      {
        id: "v2",
        axisColor: "#FCD202",
        axisThickness: 2,
        axisAlpha: 1,
        position: "right"
      },
      {
        id: "v3",
        axisColor: "#B0DE09",
        axisThickness: 2,
        gridAlpha: 0,
        offset: 50,
        axisAlpha: 1,
        position: "left"
      }
    ],
    graphs: [
      {
        valueAxis: "v1",
        lineColor: "black",
        bullet: "round",
        bulletBorderThickness: 1,
        hideBulletsCount: 30,
        title: "Taux de criminalité",
        valueField: "visits",
        fillAlphas: 0
      },
      {
        valueAxis: "v2",
        lineColor: "#FCD202",
        bullet: "square",
        bulletBorderThickness: 1,
        hideBulletsCount: 30,
        title: "Taux prédit",
        valueField: "hits",
        fillAlphas: 0
      },
      {
        valueAxis: "v3",
        lineColor: "#B0DE09",
        bullet: "triangleUp",
        bulletBorderThickness: 1,
        hideBulletsCount: 30,
        title: "Tendance",
        valueField: "views",
        fillAlphas: 0
      }
    ],
    chartScrollbar: {},
    chartCursor: {
      cursorPosition: "mouse"
    },
    categoryField: "date",
    categoryAxis: {
      parseDates: true,
      axisColor: "#DADADA",
      minorGridEnabled: true
    },
    export: {
      enabled: true,
      position: "bottom-right"
    }
  });

  chart.addListener("dataUpdated", zoomChart);
  zoomChart();
  function generateChartData(records) {
    var chartData = [];
    var firstDate = new Date();
    firstDate.setDate(firstDate.getDate() - 100);

    var visits = 1600;
    var hits = 2900;
    var views = 8700;

    for (i = 0; i < Object.size(records.crimes); i++) {
      visits = getSafe(() => records.crimes[i].y, 0);
      hits = records.forecast[i].yhat;
      views = records.forecast[i].trend;

      chartData.push({
        date: new Date(records.forecast[i].ds),
        visits: visits,
        hits: hits,
        views: views
      });
    }
    return chartData;
  }
  function zoomChart() {
    chart.zoomToIndexes(
      chart.dataProvider.length - 20,
      chart.dataProvider.length - 1
    );
  }
}