//中国地图的配置

var echarts_center = echarts.init(document.getElementById('c1')) //创建一个ec对象

//var mydata = [{'name': '上海','values':36}]

var echarts_center_option = {
    title: {
       // text: '各省情况',
        left: 'center',
        textStyle: {
            color: 'white',
            fontSize: 30,
        },
    },
    tooltip: {
        trigger: 'item'
    },
    visualMap: {
        show: true,
        x: 'left',
        y: 'bottom',
        textStyle: {
            fontSize: 8,
            //color:'white',
        },
        splitList: [{start:0,end:0},
            {start: 1, end: 9},
            {start: 10, end: 50},
            {start: 51, end: 99},
            {start: 100}],
        color: ['#110000','#FF6666','#FFFF00','#33CCFF','#00CC33']
    },
    series: [{
        name: '现存确诊人数',
        type: 'map',
        mapType: 'china',
        roam: false,
        itemStyle: {
            normal: {
                borderwidth: .5,
                borderColor: '#009fe8',
                areaColor: '#ffefd5',
            },
            emphasis: {
                borderwidth: .5,
                borderColor: '#4b0082',
                areaColor: '#fff2',
            }
        },
        lable: {
            normal: {
                show: true,
                fontSize: 8,
            },
            emphasis: {
                show: true,
                fontSize: 8,
            }
        },
        data: [] //key

    }]
};
echarts_center.setOption(echarts_center_option)
