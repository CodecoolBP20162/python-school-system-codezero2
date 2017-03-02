$(document).on("click", ".reserved", function () {
     var mySlot = $(this).data('applicant');
     $("#slotStart").html( mySlot[0] );
     $("#slotApplicantName").html( mySlot[1] );
     $("#slotApplicantCode").html(mySlot[2]);
});