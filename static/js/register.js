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
        $('#lab_name').parent().hide();
    }
    else if ($(this).val() == 'lab') {
        $('#clinic_name').parent().hide();
        $('#lab_name').parent().show();
    }
    else {
        $('#clinic_name').parent().hide();
        $('#lab_name').parent().hide();
    }
 });