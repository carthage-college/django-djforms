function sel(num) {
    if (num == 14) {
        $('input[name=session7]:radio').attr('disabled', 'disabled');
        $('input[name=session7]:radio').removeAttr('checked');
        $('input[name=session14]:radio').removeAttr('disabled');
        $('input[name=session7]:radio').attr('checked', false);
    }
    else if (num == 7) {
        $('input[name=session14]:radio').attr('disabled', 'disabled');
        $('input[name=session7]:radio').removeAttr('disabled');
        $('input[name=session14]:radio').attr('checked', false);
    }
}

$(function() {
    /* simulate html5 placeholder feature for broken-ass browsers */
    jQuery.support.placeholder = false;
    test = document.createElement('input');
    // inFieldLabels plugin adds placeholder feature similar to html5.
    if('placeholder' in test) jQuery.support.placeholder = true;
    if(!$.support.placeholder) {
        $("label").inFieldLabels();
        $("input").attr("autocomplete","off");
    } else {
        $(".placeholder").hide();
    }

    /* payment options. hide credit card form if not cc. */
    $('#id_payment_type_0').click(function() {
        $('#payment-details').show();
    });
    $('#id_payment_type_1').click(function() {
        $('#payment-details').hide();
    });
    $('#id_payment_type_2').click(function() {
        $('#payment-details').hide();
    });

    /* control logic for 7/14 week sessions where some things are only
       offered in 14 week session
    */
    $("[id^=id_educationalgoal_]").click(function() {
        num = $(this).val();
        if (num == 1 || num == 6 || num == 7) {
            if ($('input[name=program][value=7]:radio').attr('disabled')) {
                $('input[name=program][value=7]:radio').removeAttr('disabled');
                $('input[name=session7]:radio').removeAttr('disabled')
            }
        }
        else if (num == 2 || num == 3 || num == 4 || num == 5) {
            if (!$('input[name=program][value=7]:radio').attr('disabled')) {
                $('input[name=program][value=7]:radio').attr('disabled', 'disabled');
                $('input[name=session7]:radio').attr('disabled', 'disabled')
                $('input[name=program][value=14]:radio').attr('checked', true)
                sel(14);
            }
        }
    });
    // disable access to the unselected 7/14 week session
    $("[id^=id_program_]").click(function() {
        sel($(this).val());
    });

    /* dynamic selection of schools based on state and city. */
    // state select field populated via ajax which returns HTML
    $("#states").change(function() {
        var id=$(this).val();
        var dataString = 'state='+ id;
        $.ajax ({
            type: "POST",
            url: "/jenzabar/admissions/cities/",
            data: dataString,
            cache: false,
            success: function(html) {
                $("#cities").html(html);
            }
        });
    });
    // city select field populated via ajax based on state selected
    $("#cities").change(function() {
        var dataString = 'city='+ $(this).val() + '&state=' + $("#states").val();
        $.ajax ({
            type: "POST",
            url: "/jenzabar/admissions/schools/",
            data: dataString,
            cache: false,
            success: function(html) {
                $("#schools").html(html);
            }
        });
    });

    /* toggle between manual and dynamic selection of schools */
    $("#toggle_schools").click(function() {
        $('#selectschool, #manualschool').slideToggle();
        $(this).val($(this).val() == 'Return to school listings' ? 'Click here if your school is not listed' : 'Return to school listings');
        return false;
    });

    /* add and remove schools */
    // remove schools
    $(".destroy_school").live('click', function() {
        $(this).parent().remove();
    });
    // add schools
    $("#add_school").click(function () {
        if ($("#toggle_schools").val() == "Return to school listings" ) {
            dynamic = false;
            city = $("#man_city").val();
            state = $("#man_state").val();
            school = $("#man_school").val();
        } else {
            dynamic = true;
            city = $("#cities").val();
            state = $("#states").val();
            school = $("#schools").val(); // used for error handling only
        }
        if (city && state && school) {
            doop++;
            newId = "doop_" + doop;
            // error handling above does not work with .text() in select elements
            // so we use val() for error handling and then reassign here
            if (dynamic) {
                school = $("#schools").text();
            }
            // names and places
            $("#doop_master").find(".school_code").val($("#schools").val());
            $("#doop_master").find("input[name^=school_name]").val(school);
            $("#doop_master").find("input[name^=school_city]").val(city);
            $("#doop_master").find("input[name^=school_state]").val(state);
            // dates
            $("#doop_master").find(".from_month option").filter(function() {
                return $(this).val() == $("#from_month_orig").val();
            }).attr('selected', true);
            $("#doop_master").find(".from_year option").filter(function() {
                return $(this).val() == $("#from_year_orig").val();
            }).attr('selected', true);
            $("#doop_master").find(".to_month option").filter(function() {
                return $(this).val() == $("#to_month_orig").val();
            }).attr('selected', true);
            $("#doop_master").find(".to_year option").filter(function() {
                return $(this).val() == $("#to_year_orig").val();
            }).attr('selected', true);
            $("#doop_master").find(".grad_month option").filter(function() {
                return $(this).val() == $("#grad_month_orig").val();
            }).attr('selected', true);
            $("#doop_master").find(".grad_year option").filter(function() {
                return $(this).val() == $("#grad_year_orig").val();
            }).attr('selected', true);
            // clone the doop
            $("#doop_master").clone().attr("id",newId).appendTo("#selected_schools");
            // clear the doop and dynamic selects
            $("#doop_master").find(".school_code").val("");
            $("#doop_master").find(".school_name").val("");
            $("#doop_master").find(".school_city").val("");
            $("#doop_master").find(".school_state").val("");
            $("#doop_master").find('*').attr('selected', false);
            $("select[name$=_orig]").find('*').attr('selected', false);
            $("#states").children().removeProp('selected');
            $("#cities").empty();
            $("#schools").empty();
            $("#man_state").val('');
            $("#man_city").val('');
            $("#man_school").val('');
        } else {
            error = "Required fields are empty: ";
            if (!city){
                error += "City, "
            }
            if (!state){
                error += "State, "
            }
            if (!school){
                error += "School"
            }
            alert(error);
        }
    });
});
