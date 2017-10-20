$.ajax({
  type: 'GET',
  url: 'http://iwb.jp/s/js/data.json',
  dataType: 'json',
  success: function(json){
    var len = json.length;
    for(var i=0; i < len; i++){
      $("#a").append(json[i].version + ' ' + json[i].codename + '<br>');
    }
  }
});
