var echarts_l1 = echarts.init(document.getElementById('l1'));//初始化
var echarts_l1_option = {//折线图属性
    title: {
        text: '累计&趋势',
        textStyle:{
            color: '#EA0000',
        },
    },
    tooltip: {
        trigger: 'axis'
    },
    legend: {
        data: ['累计确诊', '累计治愈','累计死亡']
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    toolbox: {
        feature: {
           // saveAsImage: {}
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
            name: '累计确诊',
            type: 'line',
            //stack: '总量',
            data: []
        },
        {
            name: '累计治愈',
            type: 'line',
            //stack: '总量',
            data: []
        },
        {
            name: '累计死亡',
            type: 'line',
            //stack: '总量',
            data: []
        }

    ]
};

echarts_l1.setOption(echarts_l1_option);
