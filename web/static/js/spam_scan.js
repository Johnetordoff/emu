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
    $('.spam-btn').on("click", function (e) {
        $.ajax(
            {
                type: 'post',
                url: '',
                dataType: 'json',
                data: {'guid': $('#user-guid').text(), 'spam': e.target.id},
                headers: {"X-CSRFToken": getCookie('csrftoken')},
            }
        )
    });
});

$(document).ajaxStop(function(){
    window.location.reload();
});
