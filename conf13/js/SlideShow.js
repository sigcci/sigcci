document.addEventListener('DOMContentLoaded',function(){
  addTimeSlideShow();
  addSlideArrow();
},false);

var slideID;//スライドショーのタイマーID

function addTimeSlideShow(){
  slideID = window.setInterval(slideEvent,5000);
}

function slideEvent(){
  var btnList = document.getElementsByName('slideshowButton');
  for(var i = 0, len = btnList.length; i < len; ++i){
    if(btnList.item(i).getAttribute('checked')){
      //console.log(i+' Match!'+(len-1));
      if(i == (len-1)){
        //console.log('reset!');
        btnList.item(0).setAttribute('checked',true);
        btnList.item(i).removeAttribute('checked');
      }
      else{
        btnList.item(i+1).setAttribute('checked',true);
        btnList.item(i).removeAttribute('checked');
      }
      break;
    }
  }//for(var i = 0, len = btnList.length; i < len; ++i)
}

function slideEvent_R(){//逆方向にスライド
  var btnList = document.getElementsByName('slideshowButton');
  for(var i = 0, len = btnList.length; i < len; ++i){
    if(btnList.item(i).getAttribute('checked')){
      //console.log(i+' Match!'+(len-1));
      if(i == 0){
        //console.log('reset!');
        btnList.item(len-1).setAttribute('checked',true);
        btnList.item(0).removeAttribute('checked');
      }
      else{
        btnList.item(i-1).setAttribute('checked',true);
        btnList.item(i).removeAttribute('checked');
      }
      break;
    }
  }//for(var i = 0, len = btnList.length; i < len; ++i)
}

function addSlideArrow() {
  document.getElementById('arrow next').addEventListener('click',nextArrow,false);
  document.getElementById('arrow prev').addEventListener('click',prevArrow,false);
}

function nextArrow() {
    //console.log('Next clicked');
    slideEvent();//現在の次に移る
    window.clearInterval(slideID);//インターバル停止
    slideID = window.setInterval(slideEvent,5000);//インターバルを再設定
    //console.log('Cleared!');
}

function  prevArrow() {
  //console.log('Prev clicked');
  slideEvent_R();
  window.clearInterval(slideID);//インターバル停止
  slideID = window.setInterval(slideEvent,5000);//再設定
}
