$(function() {
  $("#panel-btn").click(function() {
    $("#panel").slideToggle(200);
    $("#panel-btn-icon").toggleClass("close");
    return false;
  });
});

$(document).ready(function () {
    var pagetop = $('.pagetop');
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            pagetop.fadeIn();
        } else {
            pagetop.fadeOut();
        }
    });
    pagetop.click(function () {
        $('body, html').animate({ scrollTop: 0 }, 500);
        return false;
    });
});

// クリックされた画像のsrcを取得しModalに貼り付けるJavaScript
function pop(self) {
    $('#imagepreview').attr('src', $(self).attr('src'));
    $('#imagemodal').modal('show');
}

// フォトライブラリー内の追従するメニュー用
jQuery(document).ready(function($){
	//variables
	var $window = $(window);
	var $menu = $("#photoes_menu");
	var $photoes = $("#photoes");
	var window_min = 0;
	var window_max = 0;
	var threshold_offset = 10;
	/*
	 set the container's maximum and minimum limits as well as movement thresholds
	*/
	function set_limits(){
		//max and min container movements
		var max_move = $photoes.offset().top + $photoes.height() - $menu.height() - 2*parseInt($menu.css("top") );
		var min_move = $photoes.offset().top;
		//save them
		$menu.attr("data-min", min_move).attr("data-max",max_move);
		//window thresholds so the movement isn't called when its not needed!
		//you may wish to adjust the freshhold offset
		window_min = min_move - threshold_offset;
		window_max = max_move + $menu.height() + threshold_offset;
	}
	//sets the limits for the first load
	set_limits();

	function window_scroll(){
		//if the window is within the threshold, begin movements
		if( $window.scrollTop() >= window_min && $window.scrollTop() < window_max ){
			//reset the limits (optional)
			set_limits();
			//move the container
			container_move();
		}
	}
	$window.bind("scroll", window_scroll);

	/**
	 * Handles moving the container if needed.
	**/
	function container_move(){
		var wst = $window.scrollTop();
		//if the window scroll is within the min and max (the container will be "sticky";

  		if( wst >= $menu.attr("data-min") && wst <= $menu.attr("data-max") ){
  			//work out the margin offset
  			var margin_top = $window.scrollTop() - $menu.attr("data-min");
  			//margin it down!
  			$menu.css("margin-top", margin_top);

  		//if the window scroll is below the minimum
  		}else if( wst <= $menu.attr("data-min") ){
  			//fix the container to the top.
  			$menu.css("margin-top",0);

  		//if the window scroll is above the maximum
  		}else if( wst > $menu.attr("data-max") ){
  			//fix the container to the top
  			$menu.css("margin-top", $menu.attr("data-max")-$menu.attr("data-min")+"px" );
  		}
	}
	//do one container move on load
	container_move();
});

// プロジェクトカード
var json_url = 'http://private-c40429-missionforest.apiary-mock.com/missions';
$(window).load(function (){
  // APIからJSONを取得
  $.getJSON(json_url)
  // JSON取得後の処理
  .done(function (data){
    if(data){
      for(var i in data){
        $("#output").append(
          "<div class=\"col-xs-12 col-sm-6 col-md-4 col-lg-3\">\n" +
            "<a href=\"" + data[i].url + "\">\n" +
              "<div class=\"card\">\n" +
                "<img class=\"card-img\" src=\"" + data[i].thumb_url + "\" class=\"out_cover_210x280\">\n" +
                "<div class=\"card-content\">\n" +
                  "<h1 class=\"card-title\">" + data[i].title + "</h1>" +
                  "<div class=\"col-xs-4\">" +
                    "<img src=\"" + data[i].author.thumb_url + "\" class=\"img-responsive img-circle out_cover_50x50\">" +
                  "</div>" +
                  "<div class=\"col-xs-8\">" +
                    "<p class=\"card-name\">" + data[i].author.name + "</p>" +
                  "</div>" +

                  "<div class=\"col-xs-12\">" +
                    "<p class=\"card-text\">" + data[i].summary + "</p>" +
                  "</div>" +

                  "</div>" +
                "</div>" +
              "</a>" +
            "</div>"
          );
      }
    }
  });
});

/*
<div class="col-xs-12 col-sm-6 col-md-4 col-lg-3">
  <a href="">
    <div class="card">
      <img class="card-img" src="images/1.jpg" alt="">
      <div class="card-content">
        <h1 class="card-title">Project1</h1>
        <div class="col-xs-4">
          <img src="images/person.png" class="img-responsive img-circle img-thumbnail">
        </div>
        <div class="col-xs-8">
          <p class="card-text">名工 太郎</p>
        </div>
        <div class="col-xs-12">
          <p class="card-text">プロジェクトの説明</p>
        </div>
      </div>
    </div>
  </a>
</div>
*/
