//    在结果详细页面添加随机分配得到的时间和可分配资源
//的可视化拼图

$(document).ready(function(){
    update_time_avaliable();
});

function update_time_avaliable(){
    var experiment_id = parseInt($("#for-get-id").text())
    $.ajax({
        url: "/experiment/update_time_avliable?experiment_id="+experiment_id,
        type: 'GET',
        data: $(this).serialize(),
        cache: false,
        success: function(data){
          if(data['status']=="SUCCESS"){
                time_d = data['time'];
                available_d = data['available'];
                time_d = time_d.map((value,key)=>["第"+(key+1)+"位客户",value]);
                available_d = available_d.map((value,key)=>["第"+(key+1)+"种资源",value])
                var chart = {
                    plotBackgroundColor:null,
                    plotBorderWidth:null,
                    plotShadow:false
                };
                var title_time = {
                    text:'各客户资源最大占用时间'
                };
                var title_avaliable={
                    text:'可分配资源数'
                }
                var tooltip = {
                    pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
                 };
                var plotOptions = {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}</b>: {point.y}',
                        style: {
                            color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                        }
                    }
                }
                };
                var series_time = [{
                    type:'pie',
                    name:'时间',
                    data:time_d
                }];

                var series_avaliable = [{
                    type:'pie',
                    name:'资源',
                    data: available_d,
                }];
                var credits = {
                    enabled: false // 禁用版权信息
               };


                var json = {}
                json.chart = chart;
                json.title = title_time;
                json.tooltip = tooltip;
                json.series = series_time;
                json.plotOptions = plotOptions;
                json.credits = credits;
                
                //添加客户占用时间的饼图
                var chart = Highcharts.chart('chart-time',json);

                //添加可分配资源的饼图
                json.title = title_avaliable;
                json.series = series_avaliable;//改变标题和数据，其他样式不变
                var chart = Highcharts.chart('chart-avaliable',json);     
          }
          else{
                console.log(data['code']+"  "+data['message']);
                if(now-last>=3000){
                    alert(data['code']+"  "+data['message']);
                }
          }
        },
        error: function(xhr){
            console.log(xhr)
        }
    });
}