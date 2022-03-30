<script type="text/javascript">
    $(function() {
        {% if or_form.comments.value == 'Other' %}
        $('#designation-other').slideDown(200);
        {% else %}
        $('#designation-other').slideUp(200);
        {% endif %}
        $('#id_ct-spouse').attr('autocomplete', 'off');
        $('#id_ct-spouse').attr('autocomplete', 'chrome-off');
        var $designation = $('select[name="or-comments"]');
        $designation.on('change', function (e){
          if ($designation.val() == 'Other') {
            $('#designation-other').slideDown(200);
          }else{
            $('#designation-other').slideUp(200);
          }
        });
        // disable submit button after user clicks it
        $('form#profile').bind('submit', function (e) {
          $('form#profile input[type=submit]').prop('disabled', true);
          return true;
        });
    });
</script>
