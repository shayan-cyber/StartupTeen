//Wizard Init

$("#wizard").steps({
    headerTag: "h3",
    bodyTag: "section",
    transitionEffect: "none",
    stepsOrientation: "vertical",
    titleTemplate: '<span class="number">#index#</span>'
});

//Form control

$('.purpose-radio-input').on('change', function(e) {
    $('#business-type').text(e.target.value);
});

$('#firstName').on('change', function(e) {
    $('#enteredFirstName').text(e.target.value || 'Cha');
});

$('#lastName').on('change', function(e) {
    $('#enteredLastName').text(e.target.value || 'Ji-Hun C');
});

$('#phoneNumber').on('change', function(e) {
    $('#enteredPhoneNumber').text(e.target.value || '+230-582-6609');
});

$('#emailAddress').on('change', function(e) {
    $('#enteredEmailAddress').text(e.target.value || 'willms_abby@gmail.com');
});

