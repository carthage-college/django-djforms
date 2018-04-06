<script src="//ajax.googleapis.com/ajax/libs/jqueryui/1.11.4/jquery-ui.min.js"
  type="text/javascript" charset="utf-8"></script>
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
        /*
        $("#id_or-total").on("change", function() {
            var $total = $(this).val();
            if ($total < 5) {
                $message = "Please consider making a gift of at least $5 to offset processing fees.";
            } else if ($total < 66) {
                $message = "Last year, the average gift on Giving Day was $66.";
            } else {
                $message = "";
            }
            if ($message) {
                var $dia =$('<div id="dialog-message">' + $message + '</div>')
                $dia.dialog({
                    modal: true,
                    title: "Donation Tip",
                    closeText: "",
                    draggable: false,
                    resizable: false
                });
            }
        });
        */
    });
</script>
