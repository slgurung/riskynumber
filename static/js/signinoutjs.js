$(document).ready(function() {
  $("#loginForm").on("submit", function(e){
      e.preventDefault();
      if ($("#id_login_username").val() == ""){
          $("#id_login_username").focus();
      }else if ($("#id_login_password").val() == ""){
          $("#id_login_password").focus();
      }else{
        $.ajax({
            url: "/accounts/signin/",
            type: "POST",
            data: {uname: $("#id_login_username").val(),
                      pword: $("#id_login_password").val()},
            dataType: 'json',
            success: function(data){
                $("#id_login_username").val("");
                $("#id_login_password").val("");

                if (data.result == "success")
                {
                    $('#loginModal').modal('toggle');//close modal
                    // redirect to this url after successful login
                    //when not in about and howto
                    if (data_type != "abouthowto"){
                      window.location.href = "/stocks/" + symbol +"/";
                    }else{ //when in about and howto
                      window.location.href = "/";
                    }
                    $("#tickerForm").focus();
                }else if(data.result == "declined"){
                    $("#id_login_username").focus();
                    document.getElementById("id_login_username").placeholder = "Username & password combination doesn't match. Try again.";
                }else if(data.result == "disabled"){
                    $('#loginModal').modal('toggle');//close modal
                    alert("Your account is disabled. Please contact administrator.")
                    window.location.href = "/";
                }else{
                    $('#loginModal').modal('toggle');//close modal
                    alert("System error! Try again.");
                    window.location.href = "/";
                }
            }
        });
          //instead of calling auth_login();
          // $("#tickerForm").focus();
      }
  });

  $("#signupForm").on("submit", function(e){
      e.preventDefault();
      if ($("#id_username").val() == ""){
          $("#id_username").focus();
      }else if ($("#id_password").val() == ""){
          $("#id_password").focus();
      }else{
        $.ajax({
            url: "/accounts/signup_ajax/",
            type: "POST",
            data: {uname: $("#id_username").val(),
                pword: $("#id_password").val(),
                pword2: $("#id_password2").val(),
                fname: $("#id_first_name").val(),
                lname: $("#id_last_name").val(),
                email: $("#id_email").val() },
            dataType: 'json',
            success: function(data){
                    document.getElementById("signupForm").reset();
                    if (data.result == "success")
                    {
                      $('#signupModal').modal('toggle');//close modal
                      $("#loginModal").modal();
                      $("#id_login_username").focus();
                    }else{
                        alert("Registration failed. Try again.");
                        $("#id_username").focus();
                    }
            }
        });

        // instead of calling signup_ajax();
      }
  });

  $("#signupModal").on("shown.bs.modal", function(){
      $("#id_username").focus();
  });

  $("#loginModal").on("shown.bs.modal", function(){
      $("#id_login_username").focus();
  });

  $("#loginModal").on("hide.bs.modal", function(){
      clearLoginForm();
      //above reset to default & below reset the error message
      document.getElementById("id_login_username").placeholder = "Enter Username";
  });

  $("#signupModal").on("hide.bs.modal", function(){
      clearSignupForm();
      // reset error message to default
      $("#id_username").attr("placeholder", "Enter Username");
  });


  $("#openLogin").click(function(){
      $("#signupModal").on("hidden.bs.modal", function () {
          $("#loginModal").modal();
          $("#signupModal").off("hidden.bs.modal");
      });
  });

  $("#openSignUp").click(function(){
      $("#loginModal").on("hidden.bs.modal", function () {
          $("#signupModal").modal();
          // removes hidden event form loginModal to prevent recursive event
          $("#loginModal").off("hidden.bs.modal");
          //$("#id_first_name").focus();
      });
  });
  // to check username availability
  $("#id_username").change(function () {
      //var uname = $(this).val();
      $.ajax({
          url: "/accounts/validate_username/",
          type: "POST",
          data: {
              uname: $(this).val()
          },
          dataType: 'json',
          success: function(data){
              if(data.is_taken){
                  alert(data.error_message);
                  $("#id_username").val("");
                  $("#id_username").focus();
              }
              else{
                $("#id_password").focus();
              }
          }
      });
  });

  // $("#id_password").change(function(){
  //     var psswd = $("#id_password").val();
  //     if (/[^A-Za-z0-9!@#$&*_]+/.test(psswd) || psswd.length < 5){
  //         // $("#id_password").val(""); // it will trigger empty passward check below
  //         // $("#id_password").focus(); // useless
  //         alert("Invalid password. '5-30 long and any alphabet, number, !@#$&*_are allowed'");
  //     }
  //
  // });

  $("#id_password").focus(function(){
    if($("#id_username").val() == ""){
      //$("#id_username").attr("placeholder", "Username required!");
      $("#id_username").focus();
    }
  });

  $("#id_first_name").focus(function(){
    if($("#id_username").val() == ""){
      $("#id_username").focus();
    }
  });

  $("#id_last_name").focus(function(){
    if($("#id_username").val() == ""){
      $("#id_username").focus();
    }
  });
  $("#id_email").focus(function(){
    if($("#id_username").val() == ""){
      $("#id_username").focus();
    }
  });

  $("#id_password2").focus(function(){
    var psswd = $("#id_password").val();
    if (/[^A-Za-z0-9!@#$&*_]+/.test(psswd) || psswd.length < 5){
        $("#id_password").val("");
        $("#id_password").focus();
        alert("Invalid password! (5-30 long. Any alphabet, number, or !@#$&*_ are allowed)");
    }
  });

  $("#id_password2").change(function(){
      if ($("#id_password").val() != $("#id_password2").val()){
          alert("Don't match the password. Re-enter again.");
          $("#id_password2").val("");
          $("#id_password2").focus();
      }
  });
  // works on class but not on id
  $(".news").click(function(){
      //console.log('hello');
      $("#suggestion").focus();
  });

});  //end of document.ready()


//clear form contents
function clearSignupForm(){
    document.getElementById("signupForm").reset();
}

function clearLoginForm(){
    document.getElementById("loginForm").reset();
}

// instead of calling this paste it where it is called
// function auth_login(){
//     $.ajax({
//         url: "/accounts/signin/",
//         type: "POST",
//         data: {uname: $("#id_login_username").val(),
//                   pword: $("#id_login_password").val()},
//         dataType: 'json',
//         success: function(data){
//                 $("#id_login_username").val("");
//                 $("#id_login_password").val("");
//
//                 if (data.result == "success")
//                 {
//                     $('#loginModal').modal('toggle');//close modal
//                     // redirect to this url after successful login
//                     window.location.href = "/watchlist/"; // + symbol +"/";
//                     $("#tickerForm").focus();
//                 }else if(data.result == "declined"){
//                     $("#id_login_username").focus();
//                     document.getElementById("id_login_username").placeholder = "Username & password combination doesn't match. Try again.";
//                 }else if(data.result == "disabled"){
//                     $('#loginModal').modal('toggle');//close modal
//                     alert("Your account is disabled. Please contact administrator.")
//                     window.location.href = "/";
//                 }else{
//                     $('#loginModal').modal('toggle');//close modal
//                     alert("System error! Try again.");
//                     window.location.href = "/";
//                 }
//         }
//     });
// }

// function signup_ajax(){
//     $.ajax({
//         url: "/accounts/signup_ajax/",
//         type: "POST",
//         data: {uname: $("#id_username").val(),
//             pword: $("#id_password").val(),
//             pword2: $("#id_password2").val(),
//             fname: $("#id_first_name").val(),
//             lname: $("#id_last_name").val(),
//             email: $("#id_email").val() },
//         dataType: 'json',
//         success: function(data){
//                 document.getElementById("signupForm").reset();
//
//                 if (data.result == "success")
//                 {
//                   $('#signupModal').modal('toggle');//close modal
//                   $("#loginModal").modal();
//                   $("#id_login_username").focus();
//                 }else{
//                     alert("Registration failed. Try again.");
//                     $("#id_username").focus();
//                 }
//         }
//     });
// }
