// function handleLogin(event) {

//     // herhangi bir hata alındığı hata mesajını bu şekilde göster - opacity 1 yaparak

//     event.preventDefault();
//     // Form verilerini toplayın ve dizeye dönüştürün.
//     const xhr = new XMLHttpRequest();
//     xhr.open('GET', 'https://icanhazip.com/', true);
//     xhr.onload = function () {
//       if (this.status === 200) {
//         // HTTP isteği başarılı olduğunda, yanıt IP adresi olarak gelir
//         ipAddress = this.responseText.trim();
//         var terms = $('#accept-term').is(":checked")
//         formData = $('#loginform').serialize() + '&key=' + ipAddress + '&terms=' + terms;
//           // AJAX isteği yapın.
//           $.ajax({
//             method: "POST",
//             url: '/',
//             data: formData,
//             success: function(data) {
//                 if (data["status"] == false){
//                     $(".handleError").css("opacity",1).html(`<i class="fa-solid fa-circle-exclamation me-2"></i>` + data["message_tr"])
//                 }
//                 if (data["status"] == true){
//                     window.location.href = "/patients"
//                 }
//             },
//             error: function(xhr, errmsg, err) {
//               // Hata durumunda işlem burada yapılır.
//                 $(".handleError").css("opacity",1)
//             }
//           });

//       }
//     };
//     xhr.send();
// }


function getCookie(name) {
    var cookieValue = null;
    console.log("get cookie'ye geldi.")
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    console.log("cookie val func",cookieValue)
    return cookieValue;
}