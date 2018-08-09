var newCust = [[0, 8], [1, 7], [2,7], [3, 8], [4, 7], [5, 8], [6, 9], [7, 9], [8, 9], [9, 8], [10, 9], [11, 8], [12, 7], [13,8], [14, 7], [15, 7], [16, 8], [17, 9], [18, 9], [19, 10]];
var retCust = [[0, 1], [1, 2], [2,3], [3, 3], [4, 2], [5, 3], [6, 4], [7, 5], [8, 4], [9, 5], [10, 4], [11, 4], [12, 3], [13,4], [14, 4], [15, 5], [16, 5], [17, 4], [18, 6], [19, 7]];

var plot = $.plot($('#ch5'),[
  {
    data: newCust,
    label: 'Gross Revenue',
    color: '#17A2B8'
  },
  {
    data: retCust,
    label: 'Net Revenue',
    color: '#4E6577'
  }
],{
  series: {
    lines: {
      show: false
    },
    splines: {
      show: true,
      tension: 0.4,
      lineWidth: 0,
      fill: 0.5
    },
    shadowSize: 0
  },
  points: {
    show: false,
  },
  grid: {
    hoverable: true,
    clickable: true,
    borderColor: '#ddd',
    borderWidth: 0,
    labelMargin: 5,
    backgroundColor: '#fff'
  },
  yaxis: {
    min: 0,
    max: 15,
    color: '#eee',
    font: {
      size: 10,
      color: '#999'
    }
  },
  xaxis: {
    color: '#eee',
    font: {
      size: 10,
      color: '#999'
    }
  }
});

var ctx = document.getElementById('chartBar1').getContext('2d');
new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ['Basic NodeJS', 'Blockchain Fundamentals', 'How to pickup Girls', 'HTML5 Advance', 'Erlang for Beginners', 'VTQUIT'],
    datasets: [{
      label: 'Revenue ($)',
      data: [1200, 3900, 2000, 1230, 2300, 3040],
      backgroundColor: '#27AAC8'
    }]
  },
  options: {
    legend: {
      display: false,
        labels: {
          display: false
        }
    },
    scales: {
      yAxes: [{
        ticks: {
          beginAtZero:true,
          fontSize: 10,
          max: 5000
        }
      }],
      xAxes: [{
        ticks: {
          beginAtZero:true,
          fontSize: 11
        }
      }]
    }
  }
});
