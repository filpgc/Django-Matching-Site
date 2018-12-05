$(function() {
   // draw logo
   var canvas           = document.getElementById('logo');
   var context          = canvas.getContext('2d');
   context.font         = 'bold italic 97px Georgia';
   context.textBaseline = 'top';
   var image            = new Image();
   image.src            = '/static/mainapp/robin.gif';
   image.onload = function() {
     gradient = context.createLinearGradient(0, 0, 0, 89)
     gradient.addColorStop(0.00, '#faa')
     gradient.addColorStop(0.66, '#f00')
     context.fillStyle = gradient
     context.fillText(  "R  bin's Nest", 0, 0)
     context.strokeText("R  bin's Nest", 0, 0)
     context.drawImage(image, 64, 32)
   }
   // check new username is available
   function checkuseranswer(data, textStatus, jqHXR) {
   	$('#info').html(data);
   }
   function f(page) {
		$.ajax({
			type: 'POST',
			url: '/checkuser/',
			data : {
				'username' : $('input[name=username]').val(),
				'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val(),
            'page' : page,
			},
			success: checkuseranswer,
			dataType: 'html',
      });
	}
   function remove_button() {
      $.ajax({
         context: this,
			type: 'POST',
			url: '/erasemessage/',
			data : {
				'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val(),
            'id' : $(this).parent().attr('id'),
			},
			success: function () {
            $(this).parent().fadeOut(150, function() { $(this).remove(); });
         },
         error: function(jqXHR, textStatus, error) {
            console.log(error);
         },
			dataType: 'html',
      });
   }
	$('#regusername').blur(function() { f('register'); });
	$('#logusername').blur(function() { f('login'); });
   $('.remove-btn').click(remove_button);
   // Form for posting a new message
   $("#msg-form").submit(function(event) {
      $.ajax({
         type : $(this).attr('method'),
         url : $(this).attr('action'),
         data: {
				'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val(),
            'recip' : $('input[name=recip]').val(),
            'text' : $('textarea[name=text]').val(),
            'pm' : $(".pm_class:checked").val(),
			},
         success : function(data) {
            $(data).prependTo("#messages-div").hide().fadeIn(400);
            $('.remove-btn').click(remove_button);
         },
         error: function(jqXHR, textStatus, error) {
            console.log(error);
         },
      });
      // prevent normal submission
      event.preventDefault();
   });
   // connecting click on profile image with click on upload file remove_button
   $('#profile-img').click(function() {
       $("#img_file").click();
   });
});

$(document).ready(function() {
        $('#option-group-demo').multiselect({
            numberDisplayed: 1

        });

     });


