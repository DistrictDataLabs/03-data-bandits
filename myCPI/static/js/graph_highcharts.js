$(document).ready(function () {
    $('#'+chart_id).highcharts({
        chart: chart,
        title: title,
        tooltip: {
            formatter: function () {
                return '<b>' + this.x + '</b><br/>' + this.series.name + ': ' + Math.round(this.y * 100) + '%' + '<br/>'
            },            
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        xAxis: x_axis,
        yAxis: y_axis,
        plotOptions: {
            column: {
                allowPointSelect: true,
                stacking: 'normal',
                cursor: 'pointer',
                dataLabels: {
                    enabled: false,
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    }
                }                
            }
        },
        series: series
    });
    $('#'+chart_id_cpi).highcharts({
        chart: chart_cpi,
        title: title_cpi,
        tooltip: {
            formatter: function () {
                return '<b>' + this.x + '</b><br/>' + this.series.name + ': ' + Math.round(this.y * 100) + '%' + '<br/>'
            },            
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        xAxis: x_axis_cpi,
        yAxis: y_axis_cpi,
        plotOptions: {
            line: {
                dataLabels: {
                    enabled: true
                },
                enableMouseTracking: false                
            }
        },      
        series: series_cpi
    });
});