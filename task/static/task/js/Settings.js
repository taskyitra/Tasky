var tags = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    remote: {
        url: '/task/getOptionsTypeahead/%QUERY',
        wildcard: '%QUERY'
    }
});
$('.typeahead').typeahead(null, {
    display: 'value',
    source: tags,
    limit: 10
});

$('#create_tag').click(function(e){
    console.log("tag");
    var div = document.createElement("div");
    var span = document.createElement("span");
    var input = document.createElement("input");
    div.className = "row";
    input.className = "typeahead col-xs-6";
    input.maxLength = 30;
    input.type = "text";
    input.placeholder = "Введите тэг";
    input.autocomplete = "off";
    span.className = "glyphicon glyphicon-remove";
    span.onclick = function(e){
        span.parentNode.parentNode.removeChild(span.parentNode);
    };
    div.appendChild(input);
    div.appendChild(span);
    var data = [];
    $('#tags .tt-input').each(function(i, elem) {
        data[i] = elem.value;
        elem.parentNode.parentNode.parentNode.removeChild(elem.parentNode.parentNode);
    });
    for(var i=0;i<data.length;i++){
        var div1 = document.createElement("div");
        var span1 = document.createElement("span");
        var input1 = document.createElement("input");
        div1.className = "row";
        input1.className = "typeahead col-xs-6";
        input1.maxLength = 30;
        input1.type = "text";
        input1.placeholder = "Введите тэг";
        input1.autocomplete = "off";
        input1.value = data[i];
        span1.className = "glyphicon glyphicon-remove";
        span1.onclick = function(e){
            e.target.parentNode.parentNode.removeChild(e.target.parentNode);
        };
        div1.appendChild(input1);
        if (i > 0) {
            div1.appendChild(span1);
        }
        $('#tags').append(div1);
    }
    $('#tags').append(div);
    $('.typeahead').typeahead(null, {
        display: 'value',
        source: tags,
        limit: 10
    });
});

$('#create_answer').click(function(e){
    console.log("answer");
    var div = document.createElement("div");
    var span = document.createElement("span");
    var input = document.createElement("input");
    div.className = "row";
    input.className = "col-xs-6";
    input.maxLength = 30;
    input.type = "text";
    input.placeholder = "Введите ответ";
    input.autocomplete = "off";
    input.style.marginBottom = "5px";
    span.className = "glyphicon glyphicon-remove";
    span.onclick = function(e){
        span.parentNode.parentNode.removeChild(span.parentNode);
    };
    div.appendChild(input);
    div.appendChild(span);
    $('#answers').append(div);
});

$('#create_button').click(function(e){
    var error = false;
    $('#tags_errors').hide();
    $('#answers_errors').hide();
    $('#task_name_errors').hide();
    $('#markdown_errors').hide();
    var tags = [];
    $('#tags .tt-input').each(function(i, elem){
        var text = elem.value;
        console.log(text);
        if (text.length == 0){
            error = true;
            $('#tags_errors').show();
        }
        tags[i] = text;
    });
    var answers = [];
    $('#answers input').each(function(i, elem){
        var text = elem.value;
        if (text.length == 0){
            error = true;
            $('#answers_errors').show();
        }
        answers[i] = text;
    });
    if($('#task_name').val().length==0){
        error = true;
        $('#task_name_errors').show();
    }
    if($('#markdown').val().length==0){
        error = true;
        $('#markdown_errors').show();
    }
    if (error){
        return
    }
    var json = JSON.stringify({
        task_name: $('#task_name').val(),
        tags: tags,
        level: parseInt($('#level').val()),
        markdown: $('#markdown').val(),
        area: parseInt($('#area').val()),
        answers: answers
    });
    console.log(json);
    json  = encodeURIComponent(json);
    console.log(json);
    $.ajax({
        url: "/task/create/",
        type: 'POST',
        data: json,
        success: function (mess) {
            document.location.href = "/task/create_task_success/" + mess + "/";
        },
        error: function(mess){
            console.log("Error");
        }
    });
});

$('#edit_button').click(function(e){
    var error = false;
    $('#tags_errors').hide();
    $('#answers_errors').hide();
    $('#task_name_errors').hide();
    $('#markdown_errors').hide();
    var tags = [];
    $('#tags .tt-input').each(function(i, elem){
        var text = elem.value;
        console.log(text);
        if (text.length == 0){
            error = true;
            $('#tags_errors').show();
        }
        tags[i] = text;
    });
    var answers = [];
    $('#answers input').each(function(i, elem){
        var text = elem.value;
        if (text.length == 0){
            error = true;
            $('#answers_errors').show();
        }
        answers[i] = text;
    });
    if($('#task_name').val().length==0){
        error = true;
        $('#task_name_errors').show();
    }
    if($('#markdown').val().length==0){
        error = true;
        $('#markdown_errors').show();
    }
    if (error){
        return
    }
    var json = JSON.stringify({
        task_name: $('#task_name').val(),
        tags: tags,
        level: parseInt($('#level').val()),
        markdown: $('#markdown').val(),
        area: parseInt($('#area').val()),
        answers: answers
    });
    console.log(json);
    json  = encodeURIComponent(json);
    $.ajax({
        url: "/task/edit/" + $('#pk').val() + "/",
        type: 'POST',
        data: json,
        success: function (mess) {
            console.log("Saved")
        },
        error: function(mess){
            console.log("Error");
        }
    });
});