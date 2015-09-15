function setRatingWidth(stars){
    $('#rating_votes').width(stars * 17);
}

function setDefaultRatingSettings(userid, taskid){
    $('#rating_votes').width(0);
    $('#rating').hover(function() {
            $('#rating_votes, #rating_hover').toggle();
          },
          function() {
            $('#rating_votes, #rating_hover').toggle();
    });
    $("#rating").mousemove(function(e){
        var margin_doc = $("#rating").offset();
        var width_votes = e.pageX - margin_doc.left;
        if (width_votes < 1)
        {
            width_votes = 1 ;
        }
        user_votes = Math.ceil(width_votes/17);
        $('#rating_hover').width(user_votes*17);
    });
    $('#rating').click(function(){
        $("#rating_votes").width(user_votes*17);
        $('#rating_info h5').remove();
        $("#rating_load").show();
        $("#rating").unbind();
        $('#rating_hover').hide();
        var json = JSON.stringify({
            userid: parseInt(userid),
            taskid: parseInt(taskid),
            mark: user_votes
        });
        console.log(user_votes);
        console.log(json);
        $('#rating_votes, #rating_hover').toggle();
        $.ajax({
            url: "/task/put_mark_for_task/",
            type: 'POST',
            data: json,
            success: function (mess) {
                console.log("asd");
                $('#rating_info').append("<h5> Вы оценили задачу на "+ user_votes + "</h5>");
                $("#rating_load").remove();
                $('#current_task_rating').text("" + mess);
                console.log(mess);
            },
            error: function(mess){

            }
        });

    });
}