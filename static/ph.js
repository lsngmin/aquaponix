$(document).ready(function() {
    function createChart_142(containerId) {
        var chart = Highcharts.chart(containerId, {
            chart: {
                type: 'line'
            },
            title: {
                text: 'PH : Tank - 2'
            },
            xAxis: {
                categories: [],
                tickInterval: 3000
            },
            yAxis: {
                title: {
                    text: 'ph'
                },
                min : 5,
                max : 8,
                gridLineColor : '#e0e0e0',
                plotLines: [{
                    color: 'red',
                    width:2,
                    value:20,
                    zIndex:4,
                    label: {
                        text: 'WARNING',
                        align: 'left',
                        x: -10,
                        y: 10
                    }
                }]
            },
            series: [{
                name: 'PH',
                data: []
            }]
        });
        function requestData() {
            $.get('/eq_id_142_t2_ph', function(response) {
                var data = response;
                var categories = data.map(function(item) {
                    return item.mea_dt;
                });
                var temperatures = data.map(function(item) {
                    return parseFloat(item.value);
                });
        
                chart.update({
                    xAxis: {
                        categories: categories
                    },
                    series: [{
                        data: temperatures
                    }]
                });
                setTimeout(requestData, 15000); // 5초마다 업데이트
            });                                       
        }

        requestData(); // 초기 데이터 요청
    }
    function createChart_130(containerId) {
        var chart = Highcharts.chart(containerId, {
            chart: {
                type: 'line'
            },
            title: {
                text: 'PH : Tank - 1'
            },
            xAxis: {
                categories: [],
                tickInterval: 3000
            },
            yAxis: {
                title: {
                    text: 'ph'
                },
                min : 5,
                max : 8
            },
            series: [{
                name: 'PH',
                data: []
            }]
        });
        
        function requestData() {
    $.get('/eq_id_130_t1_ph', function(response) {
        var data = response;
        var categories = data.map(function(item) {
            return item.mea_dt;
        });
        var temperatures = data.map(function(item) {
            return parseFloat(item.value);
        });

        chart.update({
            xAxis: {
                categories: categories
            },
            series: [{
                data: temperatures
            }]
        });

        setTimeout(requestData, 15000); // 5초마다 업데이트
    });                                       
}

requestData(); // 초기 데이터 요청
}

createChart_130('130'); // 첫 번째 그래프 생성
createChart_142('142'); // 두 번째 그래프 생성
});