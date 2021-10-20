function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');


$(document).ready(function() {
    var rankingList;
    var simpleList = document.getElementById('sortable-blocks');
    var complexList = Sortable.create(simpleList, {
      handle: '.list-group-item',
      animation: 150,
      onEnd : function(evt, item) {
        evt.stopPropagation();
        console.log(complexList);
        indexList = complexList.toArray();
        console.log(indexList);
        $.ajax({
            method: 'post',
            url: '',
            data: JSON.stringify({'data': {'index': indexList}}),
            dataType: 'json',
            headers: {"X-CSRFToken": getCookie('csrftoken')}
        });
      }
    });
    console.log(complexList);

});

$(document).on("mousewheel", function (e) {
    e.preventDefault();
    return false;
});
