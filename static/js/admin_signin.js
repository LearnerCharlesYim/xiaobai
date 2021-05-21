$(function () {
   $("#submit").click(function (event) {
       event.preventDefault();
       var usernameE = $("input[name='username']");
       var passwordE = $("input[name='password']");
       var rememberE = $("input[name='remember']");

       var username = usernameE.val();
       var password = passwordE.val();
       var remember = rememberE.checked ? 1:0;

       $.ajax({
           'url':'/cms/signin/',
           'type':'POST',
           'data':{
               'username':username,
               'password':password,
               'remember':remember
           },
           'success':function (res) {
               if(res['code'] === 200){
                   window.location = '/cms/';
               }else{
                   var message = res['message'];
                   $("#message-p").html(message);
                   $("#message-p").show();
                   passwordE.val("");
                   if(message === '请输入正确邮箱格式'){
                       usernameE.val("");
                   }
                }
           },
       })
   })
});