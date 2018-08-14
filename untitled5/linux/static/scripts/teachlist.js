$(document).ready(function(){
    window.data = null;
    get_data();
    setdata();
});


function get_data() {
    $.ajax({
        type: "get",
        url: "http://127.0.0.1:8000/linux/teacher/list/",
        async: false,
        success: function (callback) {
            if (callback.msg == 'success') {
                window.data = callback.data;
            }
        }
    });
}
function setdata() {
    $('#table').bootstrapTable({
        contentType: "application/json",//请求内容格式 默认是 application/json 自己根据格式自行服务端处理
        dataType: "json",//期待返回数据类型
        method: "GET",
        toolbar: '#toolbar',
        search: true,
        pagination: true,
        showColumns: true,
        showToggle:true,
        smartDisplay:true,
        striped: true,
        detailView: false,
        showFullscreen:true,
        showRefresh: true,
        columns: [{
            checkbox: true
        }, {
            field: 'name',
            title: '姓名'
        }, {
            field: 'age',
            title: '年龄'
        }, {
            field: 'sex',
            title: '性别'
        }, {
            field: 'subject',
            title: '课程'
        }, {
            field: 'telphone',
            title: '电话'
        }],
        data: window.data,
    });
}