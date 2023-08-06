require([
  'tributejs',
  'jquery',
], function(Tribute, $){
  'use strict';

  function remoteSearch(text, cb) {
    var URL = $('body').attr('data-portal-url') + '/search_for_principals';
    xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function ()
    {
      if (xhr.readyState === 4) {
        if (xhr.status === 200) {
          var data = JSON.parse(xhr.responseText);
          cb(data);
        } else if (xhr.status === 403) {
          cb([]);
        }
      }
    };
    xhr.open("GET", URL + '?search=' + text, true);
    xhr.send();
  }

  $(document).ready(function(){
    if ($('#form-widgets-comment-text').length > 0) {
      var tribute = new Tribute({
        menuItemTemplate: function (item) {
          return '<img style="max-width: 20px;" src="'+ item.original.image + '">' + item.string;
        },
        values: function (text, cb) {
          remoteSearch(
            text, 
            function(users){
                cb(users);
            }
          )
        },
      })
      tribute.attach(document.getElementById('form-widgets-comment-text'));
    }
  });

});
