$(function() {

    var image = new Image();
    image.src = '/static/mainapp/robin.gif';
    image.onload = function() {
        gradient = context.createLinearGradient(0, 0, 0, 89);
        gradient.addColorStop(0.00, '#faa');
        gradient.addColorStop(0.66, '#f00');
        context.fillStyle = gradient;
        context.fillText("R  bin's Nest", 0, 0);
        context.strokeText("R  bin's Nest", 0, 0);
        context.drawImage(image, 64, 32)
    };

    // connecting click on profile image with click on upload file remove_button
    $('#profile-img').click(function() {
        $("#img_file").click();
    });


    $("#datepicker").datepicker({
        dateFormat: 'yy-mm-dd',
        changeMonth: true,
        changeYear: true,
        yearRange: "-100:+0"
    });


    $('.option-group-demo').multiselect({
        numberDisplayed: 1


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



    $('.match').click(function(){
        var val = $(this).attr('value')
        var element = this;
        alert(val)
        $.ajax({
            type: "POST",
            url: 'match/',
            async:false,
            data: {
                'username': val,
                'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function(json) {
                $(element).html("Matched")
            },
            error:function() {
                alert("error")
            }
        });
    });



});
