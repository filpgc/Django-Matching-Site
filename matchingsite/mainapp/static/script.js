$(function() {

    var image = new Image();
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
      xhr: function () {
         var xhr = new window.XMLHttpRequest();
         xhr.upload.addEventListener('progress', progressHandler, false);
         xhr.addEventListener('load', completeHandler, false);
         return xhr;
      },
      type : 'POST',
      url  : 'uploadimage/',
      data : formdata,
      success: function(data) {
         $('#profile-img').attr("src",data);
      },
      error : function(){
      },
      processData : false,
      contentType : false,
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



   $(document). on('click', ".match" ,function() {
        var val = $(this).attr('value')
        var element = this;
        alert(val)
        $.ajax({
            type: "POST",
            url: 'match/',
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




$('#filter_submit').click(function(){
        var val = $('#age').val()
        var gender= $('#gender').val()
        alert(val)
        alert(gender)
        $.ajax({
            type: "POST",
            url: 'filteredage/',
            data: {
                'val': val,
                "gender" : gender,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),

            },
            success: getFiltered,
            error: function () {
                alert("error")
            }
        });
        });




function getFiltered(response) {
    $("#tbody_id").empty()
    var Json = JSON.parse(response)
    alert(Json)
    textlist = ""
    for (var i = 0; i < Json.length; i++) {
        textlist += "<tr> <td class='usernames'>" + Json[i][0] + '</td> <td>' + Json[i][1] +"</td> <td> <button style='width:100px' class='match' id ="  + i + " value =" + Json[i][0] + "> Match </button> </td></tr>"
    }
    $("#tbody_id").html(textlist)

}


$(document).ready(function($) {
    $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });
});

});

