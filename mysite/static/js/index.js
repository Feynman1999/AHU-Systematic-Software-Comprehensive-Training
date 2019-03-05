$(document).ready(function(){
    $("#submit_button").click(function(){
        var title = $('#title').val();
        var nnn = $('#nnn').val();
        var mmm = $('#mmm').val();
        if (title == '') {
            alert("实验标题不能为空！");
            return false;
        }
        if (nnn == '') {
            alert("客户数不能为空！");
            return false;
        }
        if (mmm == '') {                
            alert("资源种类数不能为空！");                
            return false;
        }
    });
});