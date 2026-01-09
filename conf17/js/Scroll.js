//ページ内リンク、#非表示。スムーズスクロール
  $(".scroll").click(function(){
    var speed = 800;
    var href= $(this).attr("href");
    var offset = $(this).attr("data-offset");
    var target = $(href == "#" || href == "" ? 'html' : href);
    var windowWidth = window.innerWidth;
    offset2 = 0
    //console.log(windowWidth);
    if(windowWidth > 1024){
      offset2 = 0;
    }
    else if(windowWidth > 768){
      offset2 = 40;
    }
    else if(windowWidth > 414){
      offset2 = 10;
    }

    var position = target.offset().top-offset2;//通常より offset2 ピクセル上がスクロールの目的地
    $("html, body").animate({scrollTop:position}, speed, "swing");
    return false;
  });
