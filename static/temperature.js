$(document).ready(function() {
    function createChart_146(containerId) {
        var chart = Highcharts.chart(containerId, {
            chart: {
                type: 'line'
            },
            title: {
                text: '수온 : Tank - 2'
            },
            xAxis: {
                categories: [],
                tickInterval: 3000
            },
            yAxis: {
                title: {
                    text: '온도 (°C)'
                },
                min : 5,
                max : 20,
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
                name: '온도',
                data: []
            }]
        });
        function requestData() {
            $.get('/eq_id_146_t2_temperature', function(response) {
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
    function createChart_133(containerId) {
        var chart = Highcharts.chart(containerId, {
            chart: {
                type: 'line'
            },
            title: {
                text: '수온 : Tank - 1'
            },
            xAxis: {
                categories: [],
                tickInterval: 3000
            },
            yAxis: {
                title: {
                    text: '온도 (°C)'
                },
                min : 9,
                max : 15
            },
            series: [{
                name: '온도',
                data: []
            }]
        });
        
        function requestData() {
    $.get('/eq_id_133_t1_temperature', function(response) {
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

createChart_133('133'); // 첫 번째 그래프 생성
createChart_146('146'); // 두 번째 그래프 생성
});