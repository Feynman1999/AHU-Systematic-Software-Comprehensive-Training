
$(document).ready(function () {
    real_time_usetime()
});

function real_time_usetime() {
    var seq_id = 0;//获取安全序列的编号，初始为0
    var chart = {
        plotBackgroundColor:null,
        plotBorderWidth:null,
        plotShadow:false
    };
    var chart = Highcharts.chart('real_time_usetime', {
        title :{
            text:"实时耗费时间"
        },
        xAxis: {//X轴数据

            title:{
                text:'安全序列序号'
            }
        },
        yAxis:{
            title:{
                text:'花费时间'
            }
        },
        legend: {                                                                    
            enabled: false                                                           
        },
        tooltip: {
            enabled: false
        },
        series: [{
            data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,]  //图表初始化数据
        }]
    });

    function getFrom() {
        mypanel.scrollTop=mypanel.scrollHeight;//将滑动条移到页面的底部
        jQuery.ajax({
            url: "/experiment/update_safe_seq?seq_id="+seq_id,
            type: 'GET',
            data: $(this).serialize(),
            cache: false,
            async: false,
            success: function(data){
                if(data['status']=="SUCCESS"){
                //添加一个点至图表最后，并使前方点向前挪动
               chart.series[0].addPoint(data['usetime'],true,true,true); 
               $(".panel-body").append("<span class='label label-info'>{{ "+data['safe_seq']+" }}-----"+data['usetime']+"</span>"+"<br>");
                }
            }
        });
        seq_id +=1;
    }

$(document).ready(function () {
    //每隔1秒自动调用方法，实现图表的实时更新  
    window.setInterval(getFrom, 1000);
    var mypanel = document.getElementById('mypanel');
    
});
}
