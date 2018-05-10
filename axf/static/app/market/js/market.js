$(function () {

    $("#all_types").click(function () {

        $("#all_types_container").show();
        $("#all_type_logo").removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up");
        $("#sort_container").hide();
        $("#sort_rule_logo").addClass("glyphicon-chevron-down").removeClass("glyphicon-chevron-up");
    })


    $("#all_types_container").click(function () {
        $(this).hide();
        $("#all_type_logo").addClass("glyphicon-chevron-down").removeClass("glyphicon-chevron-up");

    })


    $("#sort_rule").click(function () {
        $("#sort_container").show();
        $("#sort_rule_logo").addClass("glyphicon-chevron-up").removeClass("glyphicon-chevron-down");
        $("#all_types_container").hide();
        $("#all_type_logo").removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");
    })

    $("#sort_container").click(function () {
        $(this).hide();
        $("#sort_rule_logo").addClass("glyphicon-chevron-down").removeClass("glyphicon-chevron-up");
    });

    $('.addShopping').on('click', function () {


    });


    // // 添加商品到购物车
    // $(".subShopping").click(function () {
    //     //    拿到商品id发送给服务器
    //     // var subShop = $(this);
    //     // var goodsid = $(this).attr("goodsid");
    //     // // console.log(goodsid);
    //     // // console.log($(this).attr("class"));
    //     // // console.log("**************")
    //     // // var goodsid2 = $(this).prop("goodsid");
    //     // // console.log(goodsid2);
    //     // // console.log($(this).prop("class"));
    //     //
    //     // $.getJSON("/axf/subtocart/", {"goodsid": goodsid}, function (data) {
    //     //     console.log(data);
    //     //     if (data["status"] == "901") {
    //     //         window.open("/axf/userlogin/", target = "_self");
    //     //     } else if (data["status"] == "200") {
    //     //         var g_num = data["g_num"];
    //     //         var span_num = subShop.next();
    //     //         span_num.html(g_num);
    //     //     } else if (data["status"] == "902") {
    //     //         alert(data["msg"]);
    //     //     }
    //     // })
    //     alert('点击了这里！')
    // })


});
 //  添加商品到购物车
function addtocart(id){
    var str1 = '#span' + id;
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        type: 'post',
        data: {'goods': id},
        headers: {'X-CSRFToken': csrf},
        dataType: 'json',
        url: '/axf/addcar/',
        error: function (msg) {
            console.log(msg);
            console.log('添加失败！')
        },

        success: function (msg) {
            console.log(msg);
            console.log('添加成功!');
            $(str1).text(msg.c_num);
            $('#total').text(msg.total)
        }
    })
}

function subtocart(id) {
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    var str1 = '#span' + id;
    $.ajax({
        type: 'post',
        data: {'goods': id},
        headers: {'X-CSRFToken': csrf},
        dataType: 'json',
        url: '/axf/subcar/',
        error: function (msg) {
            alert('错误')
        },

        success: function (msg) {
            console.log(msg);
            $(str1).text(msg.c_num);
            $('#total').text(msg.total)
        }
    })
}