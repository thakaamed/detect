$(".news-carousel").owlCarousel({
  loop: true,
  margin: 0,
  nav: true,
  dots: false,
  responsive: {
    0: {
      items: 1,
    },
    600: {
      items: 3,
    },
    1000: {
      items: 3,
    },
  },
});

$(".client-says-carousel").owlCarousel({
  loop: true,
  margin: 0,
  nav: true,
  dots: false,
  responsive: {
    0: {
      items: 1,
    },
    600: {
      items: 3,
    },
  },
});

// carousel in altındaki ileri geri butonları nın içini font awesome iconu ile değiştirdim
$(".owl-prev").html('<i class="fa-solid fa-arrow-left"></i>');
$(".owl-next").html('<i class="fa-solid fa-arrow-right"></i>');

$("section#tooth-label .glass input").click(function (event) {
  // diş etiketleme bölümü için checkboxlar ile svg ler toggle oluyor
  $($(event.target).attr("data-target-svg")).toggle();
});

function changePriceType(event) {
  if ($(event.target).prop("checked")) {
    // eğerki checkbox seçili ise - yearly seçilmiş
    $("section#ucretSecim .checkbox-mark").css("left", "54px");
    $("section#ucretSecim span.label").removeClass("active");
    $("section#ucretSecim span.label.y").addClass("active");

    $(".ucret-card__fiyat.baslangic").html("<span>₺5000</span>/yıl");
    $(".ucret-card__fiyat.pro").html("<span>₺10000</span>/yıl");
    $(".ucret-card__fiyat.gelismis").html("<span>₺20000</span>/yıl");
  } else {
    // monthly seçilmiş
    $("section#ucretSecim .checkbox-mark").css("left", "4px");
    $("section#ucretSecim span.label").removeClass("active");
    $("section#ucretSecim span.label.m").addClass("active");

    $(".ucret-card__fiyat.baslangic").html("<span>₺500</span>/ay");
    $(".ucret-card__fiyat.pro").html("<span>₺1000</span>/ay");
    $(".ucret-card__fiyat.gelismis").html("<span>₺2000</span>/ay");
  }
}

function changeStep(which) {
  // ödeme sayfasındaki form adımlarını yöneten fonksiyon
  if (which === 1) {
    // birinci ödeme adımına geçiliyor
    $(".step").hide();
    $(".step.step-1").show();
    changeStepFormCount(1);
  } else if (which === 2) {
    // ikinci ödeme adımına geçiliyor
    let validate = form1Validate();
    // önce doğrulama yaptır
    if (validate) {
      $(".step").hide();
      $(".step.step-2").show();
      changeStepFormCount(2);
    }
  } else if (which === 3) {
    // üçüncü ödeme adımına geçiliyor
    satin_al()

    let validate = form2Validate();
    if (validate) {
      $(".step").hide();
      $(".step.step-3").show();
      changeStepFormCount(3);

    }
  }
}

function changeStepFormCount(step) {
  // ödeme sayfasındaki form adımlarının sayılarını yöneten fonksiyon
  $(".step-count .count-item").removeClass("active");
  if (step === 1) {
    // birinci adıma gidiliyor
    $(".step-count").attr("data-step", 1);
    $(".step-count .count-item:eq(0)").addClass("active");
  } else if (step === 2) {
    // ikinci adıma geçiliyor
    $(".step-count").attr("data-step", 2);
    $(".step-count .count-item:eq(1)").addClass("active");
  } else {
    // sonunda ödendi :D
    $(".step-count").attr("data-step", 3);
    $(".step-count .count-item:eq(2)").addClass("active");
    doPayment()
    // Ödeme isteği için ajax
  }
}

function paymentCreditCard() {
  // kredi kartı görseline yazılan datalar işlenir
  const cardNumber = $("input#kartnumarasi");
  const cardHolder = $("input#kkkadi");
  const cardValid = $("input#sonkullanimtarihi");
  const cardCVV = $("input#cvvkod");

  const cardNumberText = $(".card-number");
  const cardHolderText = $(".card-name");
  const cardValidText = $(".valid-value");
  const cardCVVText = $(".cvvkod");

  cardNumber.on("keyup", (e) => {
    // kart numarası yazılmaya başlandığında
    if (!e.target.value) {
      cardNumberText.text("**** **** **** ****");
    } else {
      const valuesOfInput = e.target.value.replaceAll(" ", "");

      if (e.target.value.length > 14) {
        e.target.value = valuesOfInput.replace(
          /(\d{4})(\d{4})(\d{4})(\d{0,4})/,
          "$1 $2 $3 $4"
        );
        cardNumberText.html(
          valuesOfInput.replace(/(\d{4})(\d{4})(\d{4})(\d{0,4})/, "$1 $2 $3 $4")
        );
      } else if (e.target.value.length > 9) {
        e.target.value = valuesOfInput.replace(
          /(\d{4})(\d{4})(\d{0,4})/,
          "$1 $2 $3"
        );
        cardNumberText.html(
          valuesOfInput.replace(/(\d{4})(\d{4})(\d{0,4})/, "$1 $2 $3")
        );
      } else if (e.target.value.length > 4) {
        e.target.value = valuesOfInput.replace(/(\d{4})(\d{0,4})/, "$1 $2");
        cardNumberText.html(valuesOfInput.replace(/(\d{4})(\d{0,4})/, "$1 $2"));
      } else {
        cardNumberText.html(valuesOfInput);
      }
    }
  });

  cardHolder.on("keyup", (e) => {
    if (!e.target.value) {
      cardHolderText.html("***** ****");
    } else {
      cardHolderText.html(e.target.value);
    }
  });

  cardValid.on("keyup", (e) => {
    if (!e.target.value) {
      cardValidText.html("xx/xx");
    } else {
      const valuesOfInput = e.target.value.replace("/", "");

      if (e.target.value.length > 2) {
        e.target.value = valuesOfInput.replace(/^(\d{2})(\d{0,2})/, "$1/$2");
        cardValidText.html(valuesOfInput.replace(/^(\d{2})(\d{0,2})/, "$1/$2"));
      } else {
        cardValidText.html(valuesOfInput);
      }
    }
  });

  cardCVV.on("focus", () => {
    $(".the-card").css("transform", "rotateY(180deg)");
  });

  cardCVV.on("blur", () => {
    $(".the-card").css("transform", "rotateY(0deg)");
  });

  cardCVV.on("keyup", (e) => {
    if (!e.target.value) {
      cardCVVText.html("***");
    } else {
      cardCVVText.html(e.target.value);
    }
  });
}

paymentCreditCard();

function form1Validate() {
  const animate = "animate__animated animate__shakeX";
  const mailregex = /\S+@\S+\.\S+/;
  if ($("input[name='isimsoyisim']").val() === "") {
    let element = $("input[name='isimsoyisim']");
    element.addClass(animate);
    element.focus();
    setTimeout(() => element.removeClass(animate), 1000);
    return false;
  } else if ($("input[name='firmaismi']").val() === "") {
    let element = $("input[name='firmaismi']");
    element.addClass(animate);
    element.focus();
    setTimeout(() => element.removeClass(animate), 1000);
    return false;
  } else if ($("input[name='eposta']").val() === "") {
    let element = $("input[name='eposta']");
    element.addClass(animate);
    element.focus();
    setTimeout(() => element.removeClass(animate), 1000);
    return false;
  } else if (!mailregex.test($("input[name='eposta']").val())) {
    let element = $("input[name='eposta']");
    element.addClass(animate);
    element.focus();
    setTimeout(() => element.removeClass(animate), 1000);
    return false;
  } else if ($("input[name='telefon']").val() === "") {
    let element = $("input[name='telefon']");
    element.addClass(animate);
    element.focus();
    setTimeout(() => element.removeClass(animate), 1000);
    return false;
  } else if ($("#telefon").val().length !== 23) {
    let element = $("input[name='telefon']");
    element.addClass(animate);
    element.focus();
    setTimeout(() => element.removeClass(animate), 1000);
    return false;
  }
  return true;
}

function form2Validate() {
  const animate = "animate__animated animate__shakeX";
  if ($("input[name='kredikartikullaniciadi']").val() === "") {
    let element = $("input[name='kredikartikullaniciadi']");
    element.addClass(animate);
    element.focus();
    setTimeout(() => element.removeClass(animate), 1000);
    return false;
  } else if ($("input[name='kartnumarasi']").val() === "") {
    let element = $("input[name='kartnumarasi']");
    element.addClass(animate);
    element.focus();
    setTimeout(() => element.removeClass(animate), 1000);
    return false;
  } else if ($("input[name='kartnumarasi']").val().length !== 19) {
    let element = $("input[name='kartnumarasi']");
    element.addClass(animate);
    element.focus();
    setTimeout(() => element.removeClass(animate), 1000);
    return false;
  } else if ($("input[name='cvvkodu']").val() === "") {
    let element = $("input[name='cvvkodu']");
    element.addClass(animate);
    element.focus();
    setTimeout(() => element.removeClass(animate), 1000);
    return false;
  } else if ($("input[name='cvvkodu']").val().length !== 3) {
    let element = $("input[name='cvvkodu']");
    element.addClass(animate);
    element.focus();
    setTimeout(() => element.removeClass(animate), 1000);
    return false;
  } else if ($("input[name='sonkullanimtarihi']").val() === "") {
    let element = $("input[name='sonkullanimtarihi']");
    element.addClass(animate);
    element.focus();
    setTimeout(() => element.removeClass(animate), 1000);
    return false;
  } else if ($("input[name='sonkullanimtarihi']").val().length !== 5) {
    let element = $("input[name='sonkullanimtarihi']");
    element.addClass(animate);
    element.focus();
    setTimeout(() => element.removeClass(animate), 1000);
    return false;
  }
  return true
}

function doPayment() {
  console.log("artık bilgileri alıp buradan istek mi atacan nabacaksan yap resul");
}
