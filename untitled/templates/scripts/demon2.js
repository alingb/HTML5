$(document).ready(function(){
    main();
});
function main() {
    show("fru");
    show("sel");
    show("smart");
}

function show(id) {
    var num = 500
    var box = document.getElementById(id);
    var text = box.innerHTML;
    var newBox = document.createElement("div");
    var btn = document.createElement("button");

    newBox.innerHTML = text.substring(0, num);
    btn.innerHTML = text.length > num ? "...显示全部" : "";
    btn.href = "###";
    btn.onclick = function () {
        if (btn.innerHTML == "...显示全部") {
            btn.innerHTML = "收起";
            newBox.innerHTML = text;
        } else {
            btn.innerHTML = "...显示全部";
            newBox.innerHTML = text.substring(0, num);
        }
    };
    box.innerHTML = "";
    box.appendChild(newBox);
    box.appendChild(btn);
}

    // $(function(){
    //     $("#sel").each(function(){
    //         var maxwidth=200;//设置最多显示的字数
    //         var text=$(this).text();
    //         if($(this).text().length>maxwidth){
    //             $(this).text($(this).text().substring(0,maxwidth));
    //             $(this).html($(this).html()+"..."+"<a href='###'> 点击展开</a>");//如果字数超过最大字数，超出部分用...代替，并且在后面加上点击展开的链接；
    //
    //         };
    //         $(this).find("a").click(function(){
    //             $(this).parent().text(text);//点击“点击展开”，展开全文
    //         })
    //     })
    // })