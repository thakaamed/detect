var closestSpan
$('.special-input').on("blur", function(){
    if ($(this).val() == ""){
        $(this).addClass("mysr-form-inputError");
        var closestSpan = $(this).closest('.mysr-form-inputGroup').find('.mysr-form-requiredAlert');
        closestSpan.removeClass('mysr-form-requiredAlertHidden');
    }else {
        $(this).removeClass("mysr-form-inputError");
        var closestSpan = $(this).closest('.mysr-form-inputGroup').find('.mysr-form-requiredAlert');
        closestSpan.addClass('mysr-form-requiredAlertHidden');
    }
})


// Tüm .mysr-form-input sınıfına sahip inputları seçin
var inputElements = document.querySelectorAll('.mysr-form-input');

// Gönder düğmesini seçin
var submitButton = document.querySelectorAll('.mysr-form-button')[0];
var passwordInput = document.getElementById('password');
var rePasswordInput = document.getElementById('re-password');
// Tüm inputların doldurulup doldurulmadığını kontrol eden bir işlev oluşturun
function checkInputs() {
    var allInputsFilled = true;
    var passwordValue = passwordInput.value.trim();
    var rePasswordValue = rePasswordInput.value.trim();
    // inputElements.forEach(function(inputElement) {
        // if (inputElement.value.trim() === '' || passwordValue != rePasswordValue) { // tüm inputlar dolu mu ve paswordlar eşleşmiş mi?
            // allInputsFilled = false;
            // return;
        // }
    // });

    // Tüm inputlar doldurulduysa butonu etkinleştirin, aksi takdirde devre dışı bırakın
    if (allInputsFilled) {
        submitButton.removeAttribute('disabled');
    } else {
        submitButton.setAttribute('disabled', 'disabled');
    }
}

// Her bir input için input olaylarını dinleyin (örneğin, input değeri değiştiğinde)
inputElements.forEach(function(inputElement) {
    inputElement.addEventListener('input', checkInputs);
});

// Sayfa yüklendiğinde de kontrolü yapın
window.addEventListener('load', checkInputs);