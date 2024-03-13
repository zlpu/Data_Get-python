var echarts_r3 = echarts.init(document.getElementById('r3'));
var echarts_r3_option= {
    title:{
        text:"确诊病例多的地区",
        textStyle:{
            color:'#EA0000',
        },
        left:'left'
    },
    color:["#ff6688"],
        tooltip:{
           trigger:"aAxis",
           axisPointer: {
               type:"shadow"
            }
        },
    xAxis: {
        type: 'category',
        data:[]
    },
    yAxis: {
        type: 'value'
    },
    series: [{
        data:[],
        type: 'bar',
        showBackground: true,
        backgroundStyle: {
            color: 'rgba(180, 180, 180, 0.2)'
        }
    }]
};

echarts_r3.setOption(echarts_r3_option);
