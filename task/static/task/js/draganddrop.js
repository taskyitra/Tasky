$(document).ready(function() {
    
    var dropZone = $('.dropZone'),
		dropError = $('.dropError'),
        maxFileSize = 1048576; // максимальный размер файла - 1 мб.
    dropError.hide();
    // Обрабатываем событие Drop
    dropZone[0].ondrop = function(event) {
        event.preventDefault();

        var file = event.dataTransfer.files[0];
        if (!file.type.match('image.*')) {
            return false;
        }
        // Проверяем размер файла
        if (file.size > maxFileSize) {
            dropError.text('Файл слишком большой');
            dropError.show();
            return false;
        }
        var reader = new FileReader();
        $('#progress').show();
        // Closure to capture the file information.
        reader.onload = function(event) {
            var contents = encodeURIComponent(event.target.result);
            $.ajax({
                url: "/task/add_picture/",
                type: 'POST',
                data: contents,
                success: function (mess) {
                    dropZone.val(dropZone.val() + "\n![](" + mess + " \"\")");
                    $('#progress').hide();
                },
                error: function(mess){
                    console.log("Error");
                }
            });
        };
        // Read in the image file as a data URL.
        reader.readAsDataURL(file);

        //$.ajax({
        //    url: "/task/add_picture/",
        //    type: 'POST',
        //    data: file,
        //    success: function (mess) {
        //        dropZone.append("\n![](" + mess + " \"\")");
        //        console.log(mess);
        //    },
        //    error: function(mess){
        //        console.log("Error");
        //    }
        //});
    };

});