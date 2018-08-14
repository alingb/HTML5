

function main() {
    hidetext();
    test();
    textalert();
    testadd();
    $("#yes").wordLimit();
    // $("#selecttestinput").hide();
    $("#selecttest").append("<option value='1'>1</option>");
    $("#selecttest").append("<option>2</option>");
    $("#selecttest").append("<option>3</option>");
    $("#selecttest").append("<option value='4'>other</option>");

}

function hidetext() {
    $("[type=button]").click(function(){
      var a = "test";
      var b = "test1";
      console.log("a = " + a + b);

    debugger;
    $("#test").toggle(100);
  });
}

function test() {
    $("input").focus(function(){
      var a = "test";
      console.log("a = " + a);
    debugger;
    $("#test").hide();
  });
}

function textalert() {
    $("#textalert").click(function () {
         var text = $("#test").text("aaabbbccc");
         debugger;
         alert("text: " + $("#test").text());
         $("#test").addClass("test");
         $("#test").css({"font-size": "50px"});

    });

}
function testadd() {
    $("#selecttest").change(function () {
        var text = $("#test").text("112233")
        debugger;
        var msg = $("#selecttest  option:selected").val();
        alert(msg);
        if (msg =="4")
        {
            $("#selecttestinput").prop("type", "text");
        }

    })
}
main();