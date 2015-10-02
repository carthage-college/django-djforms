    <script src="//www.carthage.edu/static/vendor/jquery/ui/datepicker/js/jquery-ui-1.10.4.custom.min.js"
        type="text/javascript" charset="utf-8"></script>
    <script type="text/javascript">
        $(function() {
            function monthDiff(d1, d2) {
                var months;
                months = (d2.getFullYear() - d1.getFullYear()) * 12;
                months -= d1.getMonth() + 1;
                months += d2.getMonth();
                return months <= 0 ? 0 : months;
            }
            $("#id_or-start_date").datepicker({
                firstDay:1,appendText:"(format yyyy-mm-dd)",
                changeFirstDay:false,dateFormat:"yy-mm-dd",
                showOn:"both",
                buttonImage:"//www.carthage.edu/themes/shared/img/ico/calendar.gif",
                buttonImageOnly:true
            });
            function calculatePayments(amount) {
                today = new Date();
                year = today.getFullYear();
                if (today.getMonth() > 6) {
                    year = year + 1;
                }
                fiscal = new Date(year, 6, 30);
                months = monthDiff(today, fiscal) + 1;
                $('#id_or-payments').val(months);
                donation = Math.round((amount / months) * 1000) / 1000;
                message = "That will be $" + donation + " a month for ";
                message += months + " months for a total of $" + amount + ".";
                $('#pledge-payments').text(message);
            }
            {% if or_form.pledge.value and or_form.total.value %}
            calculatePayments({{or_form.total.value}});
            {% endif %}
            $('#id_or-total').blur(function() {
                $(this).val($(this).val().replace(/[^\d\.]/g, ''));
                calculatePayments($(this).val());
            });

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
            $('form#profile').submit(function(){
                if ( $('#pledge').prop('checked')) {
                    $('#id_or-pledge').val(true);
                }else{
                    $('#id_or-pledge').val("");
                }
                $(this).children('input[type=submit]').attr('disabled', 'disabled');
            });
        });
    </script>
