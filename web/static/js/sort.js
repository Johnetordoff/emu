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

$(document).on('change', '#compare-schemas', function(ev) {
    var data = {
        env: $(this).find(":selected")[0].attributes.env.value,
        id: $(this).find(":selected")[0].attributes.schema_id.value
    };
    var schema_id = $('#schema-info')[0].attributes.value.value;
    console.log(schema_id);
    $.ajax({
        method: 'post',
        url: '/schema/' + schema_id + '/compare/',
        data: JSON.stringify(data),
        dataType: 'json',
        headers: {"X-CSRFToken": getCookie('csrftoken')}
    }).done(function (data) {
        console.log(data);

        var our_blocks = data.our_schema.blocks;
        var other_blocks = data.other_schema.data;
        var changes = {}

        for (var i = 0; i < our_blocks.length; i++) {
            if (typeof other_blocks[i] == "undefined") {
                break;
            }

            if (typeof our_blocks[i].display_text == "undefined") {
                our_blocks[i].display_text = '';
            }
            if (typeof our_blocks[i].example_text == "undefined") {
                our_blocks[i].example_text = '';
            }
            if (typeof our_blocks[i].help_text == "undefined") {
                our_blocks[i].help_text = '';
            }
            if (our_blocks[i].block_type != other_blocks[i].attributes.block_type) {
                if (changes[i] == undefined) {
                    changes[i] = {};
                }
                changes[i]['block_type'] = {
                    'our_schema': our_blocks[i].block_type,
                    'other_schema': other_blocks[i].attributes.block_type
                };
            }

            if (our_blocks[i].display_text != other_blocks[i].attributes.display_text) {
                if (changes[i] == undefined) {
                    changes[i] = {};
                }
                changes[i]['display_text'] = {
                    'our_schema': our_blocks[i].display_text,
                    'other_schema': other_blocks[i].attributes.display_text
                };
            }
            if (our_blocks[i].example_text != other_blocks[i].attributes.example_text) {
                if (changes[i] == undefined) {
                    changes[i] = {};
                }
                changes[i]['example_text'] = {
                    'our_schema': our_blocks[i].example_text,
                    'other_schema': other_blocks[i].attributes.example_text
                };
            }
            if (our_blocks[i].help_text != other_blocks[i].attributes.help_text) {
                if (changes[i] == undefined) {
                    changes[i] = {};
                }
                changes[i]['help_text'] = {
                    'our_schema': our_blocks[i].help_text,
                    'other_schema': other_blocks[i].attributes.help_text
                };
            }
            if (!!our_blocks[i].required != !!other_blocks[i].attributes.required) {
                if (changes[i] == undefined) {
                    changes[i] = {};
                }
                changes[i]['required'] = {
                    'our_schema': !!our_blocks[i].required,
                    'other_schema': !!other_blocks[i].attributes.required
                };
            }
        }
        $('#compare')[0].innerHTML = JSON.stringify(changes, null, 2);

    });
});
