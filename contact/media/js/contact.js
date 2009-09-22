$(document).ready(function(){
  var form = $("form#contact");
  var form_parent = form.parent();
  $("button[type=submit]").click(function(event){
    $.ajax({
      type: form.attr("method"),
      url: ".",
      data: form.serialize(),
      dataType: "json",
      success: function(data){
        if (data.valid) {
          form.fadeOut("slow");
          form.parent().append('<p class="lonely">' + gettext('message sent') + '</p>'); // ¿No se podrá hacer de otra forma?
        } else {
          $('form#contact ul.errorlist').remove();
          for (var id in data.errors) {
            var label = $('label[for='+id+']');
            label.before('<ul class="errorlist"></ul>');
            for (var i in data.errors[id])
              label.prev('ul.errorlist').append('<li>' + data.errors[id][i] +'</li>');
          }
        }
      },
      error: function(xhr, textStatus, error) {
        alert(gettext('an error ocurred while attempting to send the message') + '\n' + textStatus + '\n' + error);
      }
    });
    return false;
  });
});
