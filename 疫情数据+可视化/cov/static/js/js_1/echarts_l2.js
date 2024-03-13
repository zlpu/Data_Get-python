var echarts_l2 = echarts.init(document.getElementById('l2'));//初始化
var echarts_l2_option = {//折线图属性
    title: {
        text: '现有确诊&',
        textStyle:{
            color: '#EA0000',
        },
    },
    tooltip: {
        trigger: 'axis'
    },
    legend: {
        data: ['现有确诊']
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    toolbox: {
        feature: {
            //  saveAsImage: {}
        }
    },
    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: []
    },
    yAxis: {
        type: 'value'
    },
    series: [
        {
            name: '现有确诊',
            type: 'line',
            //stack: '总量',
            data: []
        }
    ]
};

echarts_l2.setOption(echarts_l2_option);