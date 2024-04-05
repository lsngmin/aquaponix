$(document).ready(function() {
    function createChart_143(containerId) {
        var chart = Highcharts.chart(containerId, {
            chart: {
                type: 'line'
            },
            title: {
                text: 'DO : Tank - 2'
            },
            xAxis: {
                categories: [],
                tickInterval: 3000
            },
            yAxis: {
                title: {
                    text: 'do'
                },
                min : 0,
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
                name: 'DO',
                data: []
            }]
        });
        function requestData() {
            $.get('/eq_id_143_t2_do', function(response) {
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
    function createChart_131(containerId) {
        var chart = Highcharts.chart(containerId, {
            chart: {
                type: 'line'
            },
            title: {
                text: 'DO : Tank - 1'
            },
            xAxis: {
                categories: [],
                tickInterval: 3000
            },
            yAxis: {
                title: {
                    text: 'do'
                },
                min : 0,
                max : 20
            },
            series: [{
                name: 'DO',
                data: []
            }]
        });
        
        function requestData() {
    $.get('/eq_id_131_t1_do', function(response) {
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

createChart_131('131'); // 첫 번째 그래프 생성
createChart_143('143'); // 두 번째 그래프 생성
});