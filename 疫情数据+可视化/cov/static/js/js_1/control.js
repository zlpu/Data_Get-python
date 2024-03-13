///获取数据

//<scrips>函数，传递本地时间-到html相应的模块
function gettime() {
    $.ajax({
        url: '/time',
        timeout: 100,
        async: false,
        success: function (data) {

            $("#time").html(data)
        },
        error: function (xhr, type, errorthrom) {

        }
    });
}


//传递l1需要的的数据，-到html相应的模块
function get_l1_data() {
    $.ajax({
        url: "/l1",
        success: function (data) {
            echarts_l1_option.xAxis.data = data.day_1;
            echarts_l1_option.series[0].data = data.confirm;
            echarts_l1_option.series[1].data = data.heal;
            echarts_l1_option.series[2].data = data.dead;

            echarts_l1.setOption(echarts_l1_option);

        },
        error: function (xhr, type, errorThrown) {

        }

    })
}


//传递l2需要的的数据，-到html相应的模块
function get_l2_data() {
    $.ajax({
        url: "/l2",
        success: function (data) {
            echarts_l2_option.xAxis.data = data.day_1;
            echarts_l2_option.series[0].data = data.nowconfirm;
            echarts_l2.setOption(echarts_l2_option);

        },
        error: function (xhr, type, errorThrown) {

        }

    })
}


//传递地图需要的的数据，-到html相应的模块
function get_c1_data() {
    $.ajax({
        url: "/c1",
        success: function (data) {
            echarts_center_option.series[0].data = data.data
            echarts_center.setOption(echarts_center_option)

        },
        error: function (xhr, type, errorThrown) {

        }

    })
}


//传递r1的数据，-到html相应的模块
function get_r1_data() {
    $.ajax({
        url: "/r1",
        success: function (data) {
            $(".num2 h1").eq(0).text(data.confirm);
            $(".num2 h1").eq(1).text(data.heal);
            $(".num2 h1").eq(2).text(data.dead);
            $(".num2 h1").eq(3).text(data.nowConfirm);

        },
        error: function (xhr, type, errorThrown) {

        }
    })

}

//传递r2的数据，-到html相应的模块
function get_r2_data() {
    $.ajax({
        url: "/r2",
        success: function (data) {
            $(".num1 h1").eq(0).text(data.confirm_add);
            $(".num1 h1").eq(1).text(data.heal_add);
            $(".num1 h1").eq(2).text(data.dead_add);
            $(".num1 h1").eq(3).text(data.nowConfirm_add);

        },
        error: function (xhr, type, errorThrown) {

        }
    })

}


//传递r3需要的的数据，-到html相应的模块
function get_r3_data() {
    $.ajax({
        url: "/r3",
        success: function (data) {
            echarts_r3_option.xAxis.data = data.city;
            echarts_r3_option.series[0].data = data.confirm;
            echarts_r3.setOption(echarts_r3_option);

        },
        error: function (xhr, type, errorThrown) {

        }

    })
}

//定时刷新数据
setInterval(gettime, 1000)
setInterval(get_l1_data, 1000)
setInterval(get_l2_data, 1000)
setInterval(get_c1_data, 1000)
setInterval(get_r1_data, 1000)
setInterval(get_r2_data, 1000)
setInterval(get_r3_data, 1000)

