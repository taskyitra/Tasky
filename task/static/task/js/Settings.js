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
    div.className = "container col-sm-10";
    input.className = "typeahead col-sm-6";
    input.id = "qwe";
    input.maxLength = 30;
    input.type = "text";
    input.placeholder = "Введите тэг";
    input.autocomplete = "off";
    span.className = "glyphicon glyphicon-remove col-sm-1";
    span.onclick = function(e){
        span.parentNode.parentNode.removeChild(span.parentNode);
    };
    div.appendChild(input);
    div.appendChild(span);
    $('#tags').append(div);
    $('#qwe').typeahead(null, {
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
    div.className = "container";
    input.className = "col-sm-6";
    input.maxLength = 30;
    input.type = "text";
    input.placeholder = "Введите ответ";
    input.autocomplete = "off";
    input.style.marginBottom = "5px";
    span.className = "glyphicon glyphicon-remove col-sm-1";
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