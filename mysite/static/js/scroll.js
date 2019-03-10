window.onscroll=function(){
        
    scrollFunction();
    
};


function scrollFunction(){
    if(document.body.scrollTop > 160 || document.documentElement.scrollTop > 160){
        document.getElementById("btnScroll").style.display = "block";
    }else{
        document.getElementById("btnScroll").style.display = "none";
    }
    // console.log($(document).scrollTop(),$(document).height(),$(window).height())
    // 向后端发送渲染请求得到两个  先得到当前div下最后一个div的id值 看是否<n
    var myDate = new Date();
    var now = myDate.getTime();
    var last = getCookie("last_time")
    if (last==""){last = 0}
    else {last = parseInt(last)}
    if ($(document).scrollTop()+120>= $(document).height() - $(window).height() && now-last>=300 && $("#chart-n").length > 0 ){//最后一项判断在detail页面
        $('body').css('overflow','hidden');
        document.cookie="last_time="+myDate.getTime();
        var experiment_id = parseInt($("#for-get-id").text())
        var nnn = parseInt($("#n-number").text()); //得到顾客数目
        var last_obj_id = $("#chart-n").children("div").length;//得到目前最后渲染出的顾客id
        var options = {
            chart: {
                type: 'column'
            },
            xAxis: {
                title: {
                    text: '资源号'
                },
                crosshair: true
            },
            yAxis: {
                min: 0,
                title: {
                    text: '数量'
                }
            },
            tooltip: {
                // head + 每个 point + footer 拼接成完整的 table
                headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f}</b></td></tr>',
                footerFormat: '</table>',
                shared: true,
                useHTML: true
            },
            plotOptions: {
                column: {
                    borderWidth: 0
                }
            },
            credits: {enabled: false},
        };
        $.ajax({
            url: "/experiment/update_n?lastn="+last_obj_id+"&experiment_id="+experiment_id+"&nnn="+nnn,
            type: 'GET',
            data: $(this).serialize(),
            cache: false,
            success: function(data){
              if(data['status']=="SUCCESS"){
                    var id = "chart-n-"+(last_obj_id+1)
                    var chart_html = "<div id=\"" + id + "\"></div><br>"
                    $("#chart-n").append(chart_html);
                    console.log((last_obj_id+1)+"已插入")
                    options.title = new Object();
                    options.title.text = (last_obj_id+1)+'号顾客';
                    options.xAxis = new Object();
                    options.xAxis.categories = data['m_id'];
                    options.series = new Array();
                    options.series[0] = new Object();
                    options.series[0].name = 'need';
                    options.series[0].data = data['need'];
                    options.series[1] = new Object();
                    options.series[1].name = 'allocation';
                    options.series[1].data = data['allocation'];
                    var chart = Highcharts.chart(id, options);
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
        $('body').css('overflow','auto');
    };
};

function getCookie(cname)
{
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) 
    {
        var c = ca[i].trim();
        if (c.indexOf(name)==0) return c.substring(name.length,c.length);
    }
    return "";
}

function toUp(){
    timer=setInterval(function(){   
        var scrollTop=document.documentElement.scrollTop||document.body.scrollTop;
        var ispeed=Math.floor(-scrollTop/6);
        // console.log(ispeed);
        if(scrollTop==0){
            clearInterval(timer);
        }
        document.documentElement.scrollTop=document.body.scrollTop=scrollTop+ispeed;
    }, 15)
    // document.body.scrollTop = 0;
    // document.documentElement.scrollTop = 0;
};


