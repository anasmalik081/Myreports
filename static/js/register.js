$( document ).ready(function() {
    if ($('#id_user_type').val() === 'doctor') {
        $('#clinic_name').parent().show();
        $('#lab_name').parent().hide();
    }
    else if ($('#id_user_type').val() == 'lab') {
        $('#clinic_name').parent().hide();
        $('#lab_name').parent().show();
    }
    else {
        $('#clinic_name').parent().hide();
        $('#lab_name').parent().hide();
    }
});

$('#id_user_type').on('change', function() {
    if (this.value === 'doctor') {
        $('#clinic_name').parent().show();
        $('label').not('[for!="clinic_name"]').addClass('required');
        $('label').not('[for!="lab_name"]').removeClass('required');
        $('#lab_name').parent().hide();
    }
    else if ($(this).val() == 'lab') {
        $('#clinic_name').parent().hide();
        $('#lab_name').parent().show();
        $('label').not('[for!="clinic_name"]').removeClass('required');
        $('label').not('[for!="lab_name"]').addClass('required');
    }
    else {
        $('#clinic_name').parent().hide();
        $('#lab_name').parent().hide();
        $('label').not('[for!="lab_name"]').removeClass('required');
        $('label').not('[for!="clinic_name"]').removeClass('required');
    }
 });



 $( document ).ready(function() {
    if ($('#id_address').val() === '') {
        $('label').not('[for!="id_address"]').addClass('required');
    }
    else {
        $('label').not('[for!="id_address"]').removeClass('required');
    }
});