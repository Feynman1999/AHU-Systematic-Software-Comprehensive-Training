
$(document).ready(function () {
    real_time_usetime()
});

function real_time_usetime() {
    var seq_id = 1;//获取安全序列的编号，初始为0
    //得到实验号
    urlstrs = window.location.href.split("/")
    experiment_id = urlstrs[urlstrs.length-1];

    var mark = 0;//记录获取安全失败的次数如果大于三次，我们就判定结束

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
            data: [0,0,0,0,0,0,0,0,0,0]  //图表初始化数据
        }],
        credits:{
            enabled: false // 禁用版权信息
       }
    });

    function getFrom() {
        mypanel.scrollTop=mypanel.scrollHeight;//将滑动条移到页面的底部
        jQuery.ajax({
            url: "/experiment/update_safe_seq?experiment_id="+experiment_id+"&seq_id="+seq_id,
            type: 'GET',
            data: $(this).serialize(),
            cache: false,
            async: false,
            success: function(data){
                if(data['status']=="SUCCESS"){
                    if(data['safe_seq']=='0'||data['usetime']=='0'){
                        seq_id -=1;
                        mark +=1;
                        if(mark>3)
                            clearInterval(window.setinit)
                    }else{
                        mark=0
                        //添加一个点至图表最后，并使前方点向前挪动
                        chart.series[0].addPoint(data['usetime'],true,true,true);
                        data['safe_seq']
                    // $(".panel-body").append("<span class='label label-info' style='margin-top:1em'> "+
                    // "<button type='button' class='btn btn-default' data-toggle='tooltip' data-placement='bottom' title="+data['safe_seq']+">点击</button>"
                    // +" -----"+data['usetime']+"</span>"+"<br>");
                    $(".panel-body").append("<span class='label label-info btn btn-default' style='margin-bottom:0.2em;width:100%;display: inline-table' data-toggle='tooltip'"+
                    " data-placement='bottom' title="+data['safe_seq']+"> "+
                      "这是第"+seq_id+"条记录"+
                    " --------------------------------------------花费 "+data['usetime']+" 单位时间</span>"+"<br>");
                    }
                }
            }
        });
        seq_id +=1;
    }

$(document).ready(function () {
    //每隔1秒自动调用方法，实现图表的实时更新  
    window.setinit = setInterval(getFrom, 3000);
    var mypanel = document.getElementById('mypanel');
    
});
}
