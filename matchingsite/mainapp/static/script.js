$(function() {

    // connecting click on profile image with click on upload file remove_button
    $('#profile-img').click(function() {
        $("#img_file").click();
    });


    $("#datepicker").datepicker({
        dateFormat: 'yy-mm-dd',
        changeMonth: true,
        changeYear: true,
        yearRange: "-100:-18",
        maxDate: '-18y',
    });


    $('.option-group-demo').multiselect({
        numberDisplayed: 1


    });



    function progressHandler(event) {
        var percent = (event.loaded / event.total) * 100;
        $('#progressBar').val(Math.round(percent));
    }

    function completeHandler(event) {
        $('#progressBar').val(0);
        $('#progressBar').hide();
    }

    $('#img_file').change(function uploadFile() {
        $('#progressBar').show();
        var formdata = new FormData();
        var file = document.getElementById('img_file').files[0];
        formdata.append('img_file', file);
        formdata.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());


        $.ajax({
            xhr: function() {
                var xhr = new window.XMLHttpRequest();
                xhr.upload.addEventListener('progress', progressHandler, false);
                xhr.addEventListener('load', completeHandler, false);
                return xhr;
            },
            type: 'POST',
            url: 'uploadimage/',
            data: formdata,
            success: function(data) {
                $('#profile-img').attr("src", data);
            },
            error: function() {},
            processData: false,
            contentType: false,
        });
    });


    // shows the selected hobbies in the edit profile page
    $("#option-group-edit").ready(function(e) {
        $.ajax({
            type: "GET",
            url: '/hobby/',
            dataType: 'json',
            success: function(response) {
                var Json = JSON.parse(response)
                for (var i = Json.length - 1; i >= 0; i--) {
                    $('#option-group-edit').multiselect('select', Json[i].fields['name']);
                }
            },
        });


    });



    $("body").on('click', ".match", function(e) {
        var val = $(this).attr('value')
        var element = this;
        $.ajax({
            type: "POST",
            url: 'match/',
            data: {
                'username': val,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function(json) {
                $(element).html("Matched")
            },
            error: function() {
                alert("error")
            },
        });
        return false;
    });


    $("body").on('click', ".unmatch", function(e) {
        var val = $(this).attr('value')
        var element = this;

        $.ajax({
            type: "POST",
            url: 'unmatch/',
            data: {
                'username': val,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function(json) {
                $(element).slideUp(200, function() {

                    $(this).parent().parent().remove();
                });
            },
            error: function() {
                alert("error")
            },
        });
        return false;
    });




    $('#filter_submit').click(function() {
        var val = $('#age').val()
        var gender = $('#gender').val()
        $.ajax({
            type: "POST",
            url: 'filtered/',
            data: {
                'val': val,
                "gender": gender,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),

            },
            success: getFiltered,
            error: function() {
                alert("error")
            }
        });
    });




    function getFiltered(response) {
        $("#tbody_id").empty()
        var Json = JSON.parse(response)
        textlist = ""
        for (var i = 0; i < Json.length; i++) {
            textlist += "<tr> <td class='usernames'>" + Json[i][0] + '</td> <td>' + Json[i][1] + "</td> <td> <button style='width:100px' class='match' id =" + i + " value =" + Json[i][0] + "> Match </button> </td></tr>"
        }
        $("#tbody_id").html(textlist)

    }


    $("body").on('click', ".clickable-row", function() {
        window.location = $(this).data("href");

    });

});