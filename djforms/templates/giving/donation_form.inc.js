<script src="//www.carthage.edu/static/vendor/jquery/ui/datepicker/js/jquery-ui-1.10.4.custom.min.js"
  type="text/javascript" charset="utf-8"></script>
<script type="text/javascript">
    $(function() {
        $('#pledge').change(function () {
            $('#pledge-payments').toggle(this.checked);
        }).change(); //ensure visible state matches initially
        {% if or_form.pledge.value %}
        $('#pledge').prop('checked', true);
        $('#id_or-pledge').val(true);
        $('#pledge-payments').show();
        {% else %}
        $('#pledge-payments').hide();
        {% endif %}
        // disable submit button after user clicks it
        $('form#profile').bind('submit', function (e) {
          if ( $('#pledge').prop('checked')) {
            $('#id_or-pledge').val(true);
          }else{
            $('#id_or-pledge').val("");
          }
          $('form#profile input[type=submit]').prop('disabled', true);
          return true;
        });
    });
</script>
