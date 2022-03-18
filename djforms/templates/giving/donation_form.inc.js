<script type="text/javascript">
    $(function() {
        $('#id_ct-spouse').attr('autocomplete', 'off');
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
          if ($designation.val() == 'Other') {
              $designation.val() = $('#id_or-comments-other').val();
          }
          $('form#profile input[type=submit]').prop('disabled', true);
          return true;
        });
    });
</script>
