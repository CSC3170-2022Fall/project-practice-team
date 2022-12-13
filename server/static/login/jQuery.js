$('.loginBtn').click(function(){
    $('.login').show();
    $('.signUp').hide();
    /* border bottom on button click */
    $('.loginBtn').css({'border-bottom' : '2px solid #ff4141'});
    /* remove border after click */
    $('.signUpBtn').css({'border-style' : 'none'});
  });
   
   
  /* Show sign Up form on button click */
   
  $('.signUpBtn').click(function(){
    $('.login').hide();
    $('.signUp').show();
    /* border bottom on button click */
    $('.signUpBtn').css({'border-bottom' : '2px solid #ff4141'});
     /* remove border after click */
     $('.loginBtn').css({'border-style' : 'none'});
  });


/* mutual exclusive identity checkbox*/
$('.ex_checkbox').click(function(){
    $(this).siblings().each(function(){
      $(this).prop('checked', false);
    });
});


/* form validation */
$('button[name="register"]').click(function(){
  var username = $('#username').val();
  var password = $('#password').val();
  var confirmPassword = $('#confirmPassword').val();

  if (username.length < 1 || password.length < 1 || confirmPassword.length < 1){
    alert("Form Incomplete");
  }

  if ($('#password').val() != $('#confirmPassword').val()){
    alert("Wrong Confirm Password");
  };

});

// $('button[name="login"]').click(function(){
//   var username = $('#username').val();
//   var password = $('#password').val();

//   if (username.length < 1 || password.length < 1){
//     alert("Form Incomplete");
//   }
// });
