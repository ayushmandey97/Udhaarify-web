Highcharts.chart('rcont', {
    chart: {
        type: 'line'
    },
    title: {
        text: 'Money Habits'
    },
    subtitle: {
        text: 'Month-wise'
    },
    xAxis: {
        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    },
    yAxis: {
        title: {
            text: 'Money Spent(in K)'
        }
    },
    plotOptions: {
        line: {
            dataLabels: {
                enabled: true
            },
            enableMouseTracking: false
        }
    },
    series: [{
        name: 'Movies',
        data: [2.0,4.0,1.0,4.5,8.4,1.5,5.2,6.5,3.3,8.3,3.9,9.6]
    }, {
        name: 'Food',
        data: [3.9, 4.2, 5.7, 8.5,1.9,5.2,7.0,6.6,4.2,0.3,6.6,4.8]
    },
    {
        name: 'Education',
        data: [7.0, 6.9, 9.5,4.5,8.4,1.5,5.2,6.5,3.3,8.3,3.9,9.6]
    }]
});
Highcharts.chart('rcontpie', {
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie'
    },
    title: {
        text: 'Spending Habits'
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: true,
                format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                style: {
                    color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                }
            }
        }
    },
    series: [{
        name: 'Spent',
        colorByPoint: true,
        data: [{
            name: 'Food',
            y: 56.33
        }, {
            name: 'Shopping',
            y: 24.03,
            sliced: true,
            selected: true
        }, {
            name: 'Going Out',
            y: 10.38
        }, {
            name: 'Movies',
            y: 4.77
        }, {
            name: 'Udhaar',
            y: 0.91
        }, {
            name: 'Undetectable',
            y: 0.2
        }]
    }]
});