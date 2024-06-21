function liveSearch(event, targetElements, errorMessage, errorTarget, parentDegree) {
    // burada parentdegre değeri gelirse gelen sayısa değer kadar for döngüsün
    // diagnosis sayfasındaki hastalıklar için canlı arama fonksiyonu
    const searchQuery = event.target.value.toLowerCase();
    const searchResults = targetElements;
    let resultsFound = false;
    let resultsNotFoundMessage = errorMessage;
    searchResults.each((index, item) => {
      const text = $(item).text().toLowerCase();
      if (text.includes(searchQuery)) {
        if (parentDegree) {
          let targetelement = $(item)
          console.log("ilk element : ", targetelement)
          for (let i = 0; i < parentDegree; i++) {
            targetelement = targetelement.parent()
          }
          console.log("parent element : ", targetelement)
          targetelement.show()
        } else {
          $(item).show();
        }
        resultsFound = true;
        errorTarget.html(null);
      } else {
        if (parentDegree) {
          let targetelement = $(item)
          for (let i = 0; i < parentDegree; i++) {
            targetelement = targetelement.parent()
          }
          targetelement.hide()
        } else {
          $(item).hide();
        }
      }
    });
    if (!resultsFound) {
      errorTarget.html(resultsNotFoundMessage);
    }
  }
  
  function closeDoctorDrawSection() {
    removeDrawAnimatedLine(document.getElementById("teethDrawSvg-eng"))
    $(".map-hover-popup.doctor-draw").css("display", "none")
    $(".map-hover-popup__root").css("display", "none")
  }
  
  function changeTheme() {
    var csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val()
    var theme_choice
    $("#theme").change(function () {
      if ($(this).is(":checked")) {
        $("body").addClass("dark");
        changeLogoForLoginTheme("light");
        theme_choice = "dark"
        // localStorage.setItem("theme", "dark");
      } else {
        $("body").removeClass("dark");
        theme_choice = "light"
        changeLogoForLoginTheme("dark");
        // localStorage.setItem("theme", null);
      }
      $.ajax({
        url: "/api/change_theme_view",
        headers: { "X-CSRFToken": csrfmiddlewaretoken },
        method: "POST",
        data: { "theme": theme_choice, },
        success: function (response) { },
        error: function (xhr, errmsg, err) { }
      })
    });
  }
  function themeRemember() {
    const excludedURLs = [
      "/tr/update-profile",
      "/en/update-profile",
      "/tr/add-patient/",
      "/en/add-patient/",
      "/tr/update-patient/",
      "/en/update-patient/",
      "/en/patient-form",
      "/tr/patient-form",
      "/tr/patient-form-detail/",
      "/en/patient-form-detail/"
    ];
    // const theme = localStorage.getItem("theme"); // temayı çek
    const currentURL = window.location.pathname;
    if (excludedURLs.some(url => currentURL.includes(url))) {
      $("#theme").prop("checked", false);
      $("body").hasClass("dark") ? $("body").removeClass("dark") : null;
      return;
    }
    const theme = userThemeChoices.color; // temayı çek
    console.log("theme", theme)
    if (theme && theme == "dark") {
      // koyu tema eskiden seçilip kaydedilmişse
      // $("body").addClass("dark"); // koyu temayı ayarla
      $("#theme").prop("checked", true); // inputu seçiliye çevir
      changeLogoForLoginTheme("light");
    }
  }
  
  // function themeRemember() {
  //   const excludedURLs = [
  //     "/tr/update-profile",
  //     "/en/update-profile",
  //     "/tr/add-patient/",
  //     "/en/add-patient/"
  //   ];
  //   const currentURL = window.location.pathname;
  //   console.log("current url",currentURL)
  //   // const theme = localStorage.getItem("theme"); // temayı çek
  //   console.log("test")
  //   if(excludedURLs.includes(currentURL)){
  //     console.log("ifte")
  //     const theme = userThemeChoices.color; // temayı çek
  //     if (theme && theme == "dark") {
  //       // koyu tema eskiden seçilip kaydedilmişse
  //       // $("body").addClass("dark"); // koyu temayı ayarla
  //       $("#theme").prop("checked", true); // inputu seçiliye çevir
  //       changeLogoForLoginTheme("light");
  //     }
  //   }
  
  // }
  
  function changeLogoForLoginTheme(which) {
    // giriş sayfasında iken koyu tema seçilince yada zaten seçili ise logo ile aynı renk kalıyor ve logo kayboluyor, logoyu açık logo ile değiştirme zamanı
    $(".login-logo").attr(
      "src",
      which === "dark"
        ? "./img/craniocatch-dark-logo.svg"
        : "./img/craniocatch-light-logo.svg"
    );
  }
  
  function tooltip() {
    // burada tooltip kullanmak için bu kod gerekli
    var tooltipTriggerList = [].slice.call(
      document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl);
    });
  }
  
  // function swiperForDentalXray() {
  //   // bu fonksiyon dentalxray sayfasındaki slider ları çalıştırır
  //   let swiper = new Swiper(".dentalxrayslider-small", {
  //     direction: "vertical",
  //     spaceBetween: 10,
  //     slidesPerView: 4,
  //     freeMode: true,
  //     grabCursor: true,
  //     mousewheel: true,
  //   });
  //   let swiper2 = new Swiper(".dentalxrayslider-big", {
  //     direction: "vertical",
  //     grabCursor: true,
  //     spaceBetween: 10,
  //     mousewheel: true,
  //     pagination: {
  //       el: ".swiper-pagination",
  //       type: "bullets",
  //       clickable: true,
  //     },
  //     thumbs: {
  //       swiper: swiper,
  //     },
  //   });
  // }
  
  function setAdjustableContent() {
    // bu fonksiyon diagnosis sayfasındaki ana kısmın (dişlerin olduğu) yüksekliği ayarlar
    let headerHeight = $("section#header").outerHeight(true) || 55;
    // let userbarHeight = $(".user-bar").outerHeight(true);
    let footerHeight = $("section#footer").outerHeight(true) || 55;
    let marginBottom = 10;
    let totalHeight = `calc(100vh - ${headerHeight + footerHeight + marginBottom
      }px)`;
    $(".adjustable-content").css("height", totalHeight);
  }
  
  function changeColorForDiagnosisPage(event, id) {
    // bu fonksiyon diagnosis sayfaındaki input:color değiştiğinde arkaplan rengini değiştirir
    console.log("you clicked color box")
    $(
      `.color[data-id='${id}'], .pointer-container .pointer[data-id='${id}']`
    ).css("background-color", event.target.value);
    $(`.gradient[data-id='${id}']`).css(
      "background-image",
      `linear-gradient(90deg, rgba(0, 0, 0, 0) 0%, ${event.target.value} 100%)`
    );
    let diagnosisName = $(event.target).attr("data-illness-name")
    let currentSvgPath = $(`.leaflet-pane svg [data-illness-name='${diagnosisName}']`)
    let currentColor = $(event.target).val()
    currentSvgPath.attr("fill", currentColor)
    currentSvgPath.attr("stroke", currentColor)
  }
  
  function changeOpacityForDiagnosisPage(event, pointerTarget, id) {
    console.log("you changed color opacity")
    let opacityVal = event.target.value
    let illnessName = $(event.target).attr("data-illness-name")
    let currentSvgPath = $(`.leaflet-pane svg   path.drawsElement[data-illness-name='${illnessName}']`)
    $(pointerTarget).css("left", `${opacityVal}%`);
    currentSvgPath.attr("fill-opacity", opacityVal / 100)
  }
  
  function toggleToothDiv(id) {
    // diagnosis sayfasındaki sağ tarafta listelenen dişlere tıklayınca active class ekler kaldırır
    // ve ilgili diş detay divini açar kapar
    if ($(`.tooth-detail[data-tooth-id='${id}']`).length) {
      // böyle bir diş varsa bunu yap
      if ($(".see-all-teeth-detail").attr("data-eye") === "open") {
        // tüm dişler gösteriliyor açık şekilde ise filtreleme tarzı bişey yap
        $(".see-all-teeth-detail").attr("data-eye", "close").removeClass("fa-eye-slash").addClass("fa-eye")
        $(".tooth-detail").css("display", "none")
  
        $(`.tooth-detail[data-tooth-id='${id}']`).css("display", "block")
        $(`.teeth .tooth[data-tooth='${id}'] .item`).addClass("active");
      } else {
        // tüm dişler açık değilse normal işlemi neyse onu yap
        if ($(`.tooth-detail[data-tooth-id='${id}']`).css("display") === "block") {
          // div açıktır o zaman kapat 
          $(`.tooth-detail[data-tooth-id='${id}']`).css("display", "none");
          $(`.teeth .tooth[data-tooth='${id}'] .item`).removeClass("active");
        } else {
          // kapalıdır o zaman aç, ama göz aktifse rengi mavi yapma
          $(`.tooth-detail[data-tooth-id='${id}']`).css("display", "block");
          if ($(".see-all-teeth-detail").attr("data-eye") !== "open") {
            $(`.teeth .tooth[data-tooth='${id}'] .item`).addClass("active");
          }
        }
      }
  
    }
    // $(`.teeth .tooth[data-tooth='${id}'] .item`).toggleClass("active");
    // $(`.tooth-detail[data-tooth-id='${id}']`).toggle();
  }
  
  function changeContrast(event) {
    console.log(event.target.value);
    $("#contrast-value").html(`+${event.target.value}`);
  }
  
  function changeHighlight(event) {
    console.log(event.target.value);
    $("#highlight-value").html(`${event.target.value}%`);
  }
  
  function toggleCommentArea(id) {
    // yorum kısmını açar kapar
    $(`.comment-icon[data-id='${id}']`).toggleClass("active");
    $(`.comment-area[data-id='${id}']`).toggle();
  }
  
  function toggleToothMenu(dataToothMenu) {
    // fonksiyon dişin üzerine gelince sağ üst köşedeki kaleme tıklayınca açılan menüyü açar kapatır
    $(`.tooth-menu:not([data-tooth-menu='${dataToothMenu}'])`).removeClass("active");
    $(`.tooth-menu[data-tooth-menu='${dataToothMenu}']`).toggleClass("active");
    console.clear()
    let box = $(`.tooth-menu[data-tooth-menu='${dataToothMenu}']`)
    let boxWidth = box.width()
    let boxEndPosition = box.offset().left + boxWidth
    let panelEndPosition = $(".tooth-chart-illnesses-by-tooth").offset().left + $(".tooth-chart-illnesses-by-tooth").width()
    // console.log(boxEndPosition > panelEndPosition ? "taşdık reis" : "taşma yok devam")
    if (boxEndPosition > panelEndPosition) {
      // eğer ki açılan küçük tooth-menu panelin dışına taşıyor ise sağ taraftan değilde sol taraftan açtır yeah
      $(`.tooth-menu[data-tooth-menu='${dataToothMenu}']`).css({
        "left": "auto",
        "right": "calc(100% + 6px)"
      }).addClass("left-opened")
    }
  
  }
  
  function changeToothType(toothId, path, element, className = "") {
    // seçilen dişin tipini değiştirir
    if ($(`.tooth[data-tooth='${toothId}'] img.imgToChange`).hasClass("auto-height")) {
      $(`.tooth[data-tooth='${toothId}'] img.imgToChange`).removeClass("auto-height")
    }
    console.log(toothId, path, element)
    $(`.tooth[data-tooth='${toothId}'] img.imgToChange`).attr("src", path).addClass(className)
    var iconType = element.dataset.iconType;
    console.log("icon type", iconType)
  
    $.ajax({
      url: "/api/update_reportTooth",
      headers: { "X-CSRFToken": csrfmiddlewaretoken },
      method: "POST",
      data: {
        "image_report_id": image_report_id,
        "number_prediction": toothId,
        // "tooth_id": toothId,
        "report_path": path,
        "icon_type": iconType
      }
    });
  }
  
  function handleLogin(event) {
    // giriş sayfasındaki form işlemi
    event.preventDefault();
    // herhangi bir hata alındığı hata mesajını bu şekilde göster - opacity 1 yaparak
    $(".handleError").css("opacity", 0);
  }
  
  function customModal() {
    $("[data-modal-close]").click(function (event) {
      $(event.target).closest(".modal-container").removeClass("active");
    });
    $("[data-open-modal-pk]").click(function (event) {
      let modalId = $(event.target).attr("data-open-modal-pk");
      let openModal = $(`.modal-container#${modalId}`).addClass("active")
      if ($(event.target).attr("data-modal-type") === "patient-delete") {
        let patientId = $(event.target).closest("tr").attr("data-patient-id")
        openModal.attr("data-patient-id", patientId)
      } else if ($(event.target).attr("data-modal-type") === "patient-delete-with-card") {
        let patientId = $(event.target).closest(".card-item").attr("data-patient-id")
        openModal.attr("data-patient-id", patientId)
      } else if ($(event.target).attr("data-modal-type") === "patient-radiography-upload") {
        var patientSlug = $(event.target).data('patient-slug');
        console.log("patient-slug", patientSlug)
        $("#modal-radyografy-upload").attr("data-patient-slug", patientSlug)
      }
    });
  }
  
  function liveSearchingForDiagnosis(event) {
    // diagnosis sayfasındaki hastalıklar için canlı arama fonksiyonu
    const searchQuery = event.target.value.toLowerCase();
    const searchResults = $(".diagnosis-content .items .item");
    let resultsFound = false;
    let resultsNotFoundMessage = "Aranan kriterde hasatalık bulunamadı..";
    searchResults.each((index, item) => {
      const text = $(item).find(".checkbox + label").text().toLowerCase();
      if (text.includes(searchQuery)) {
        $(item).show();
        resultsFound = true;
        $(".diagnosis-content .items .not-found-messeage").html(null);
        $(".draw-all-btn").show();
      } else {
        $(item).hide();
      }
    });
    if (!resultsFound) {
      $(".diagnosis-content .items .not-found-messeage").html(
        resultsNotFoundMessage
      );
      $(".draw-all-btn").hide();
    }
  }
  
  function liveSearchingForAddDiagnosis(event) {
    // diagnosis sayfasındaki add-diagnosis modal için canlı arama fonksiyonu
    const searchQuery = event.target.value.toLowerCase();
    const searchResults = $(".add-diagnosis-patient-container .patient-item");
    let resultsFound = false;
    let resultsNotFoundMessage = "Aranan kriterde hasatalık bulunamadı..";
    searchResults.each((index, item) => {
      const text = $(item).find("label.patient-text").text().toLowerCase();
      if (text.includes(searchQuery)) {
        $(item).show();
        resultsFound = true;
        $(".not-found-current-patient").html(null);
      } else {
        $(item).hide();
      }
    });
    if (!resultsFound) {
      $(".add-diagnosis-patient-container .not-found-current-patient").html(
        resultsNotFoundMessage
      );
    }
  }
  
  // function deletePatient() {
  //   // patients sayfasında patient silmek için kullanılan fonksiyon
  //   $("[data-btn-operation='delete-patient']").click(function(event) {
  //     let patientId = $(event.target).closest(".modal-container").attr("data-patient-id")
  //     console.log(`silinecek olan hastanın idsi : ${patientId}`)
  //     $(event.target).closest(".modal-container").removeClass("active")
  //     Swal.fire({
  //       position: 'bottom-end',
  //       icon: 'success',
  //       title: 'Hasta başarılı bir şekilde silindi',
  //       showConfirmButton: false,
  //       timer: 2000
  //       })
  //   })
  // }
  
  $(document).ready(function () {
    // git footera footerı yerleştir
    themeRemember(); // kayıtlı tema varsa ayarla
    changeTheme(); // tema checkbox ının çalışmasını sağla
    tooltip(); // tooltiplerin çalışmasını sağla
    // swiperForDentalXray(); // dentalxray sayfası slider başlatıldı
    setAdjustableContent(); // diagnosis sayfasındaki ana kısmın (dişlerin olduğu) yüksekliği ayarlar
    customModal(); // modalın çalışması için gerekli olan fonksiyon
    //deletePatient(); // patient sayfası için patient silme fonksiyonu
    $(".footer-date").html(new Date().getFullYear()); // footerdaki tarih kısmına mevcut sene yazıldı
    $(".imgToChange").click(function () {
      // dişlere tıklanınca da o dişe ait kutuyu açmasını sağla
      $(this).next().click()
    })
  });
  
  function drawAnimatedLine(x1, y1, x2, y2, duration, svgElement) {
    //animasyonlu olarak panel çizgisi svg oluşturma fonksiyonu
    var svg = svgElement;
    var line;
    line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    line.setAttribute('x1', x1);
    line.setAttribute('y1', y1);
    line.setAttribute('x2', x1);
    line.setAttribute('y2', y1);
    line.setAttribute('stroke', 'white');
    line.setAttribute('stroke-width', '2');
    svg.appendChild(line);
  
    animateLine(x2, y2, duration);
  
    function animateLine(targetX, targetY, duration) {
      var start = performance.now();
  
      function ease(t) {
        return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
      }
  
      requestAnimationFrame(function animate(time) {
        var elapsed = time - start;
        var progress = Math.min(elapsed / duration, 1);
        var easedProgress = ease(progress);
  
        var x = x1 + easedProgress * (targetX - x1);
        var y = y1 + easedProgress * (targetY - y1);
  
        line.setAttribute('x2', x);
        line.setAttribute('y2', y);
  
        if (progress < 1) {
          requestAnimationFrame(animate);
        }
      });
    }
  }
  
  function removeDrawAnimatedLine(svgElement) {
    //animasyonlu olarak panel çizgisi svg oluşturma fonksiyonunu kaldırma fonksiyonu
    var svg = svgElement;
    svg.innerHTML = '';
  }
  
  function toggleMapPopup() {
    $(".drawsElement").on("mouseover", function () {
      closeDoctorDrawSection() // doctor çizimi paneli açıksa kapat
      // svg üzerine gelindiğinde
      $("#deleteDoctorDraw").remove()
      let svgPath = $(this)
      let svgPathWidth = $(this).get(0).getBBox().width;
      let svgPathHeight = $(this).get(0).getBBox().height;
  
      let rootWidth = 5
      $(".map-hover-popup__root").css({
        "top": `${svgPath.offset().top + (svgPathHeight / 2) - (rootWidth / 2)}px`,
        "left": `${svgPath.offset().left + (svgPathWidth / 2) - (rootWidth / 2)}px`,
        "width": `${rootWidth}px`,
        "height": `${rootWidth}px`,
        "z-index": "9999",
        "display": "block"
      })
  
      let rootMiddleX = $(".map-hover-popup__root").offset().left + (rootWidth / 2)
      let rootMiddleY = $(".map-hover-popup__root").offset().top + (rootWidth / 2)
  
      setTimeout(function () {
        drawAnimatedLine(rootMiddleX, rootMiddleY, rootMiddleX + 30, rootMiddleY - 30, 200, document.getElementById('teethDrawSvg-eng'));
      }, 0)
      setTimeout(function () {
        drawAnimatedLine(rootMiddleX + 30, rootMiddleY - 30, rootMiddleX + 60, rootMiddleY - 30, 200, document.getElementById('teethDrawSvg-eng'));
      }, 200)
      setTimeout(function () {
        $(".map-hover-popup.single").css({
          "top": `${rootMiddleY - 30}px`,
          "left": `${rootMiddleX + 60}px`,
          "display": "inline-flex",
          "transform": "translateY(-50%)"
        })
      }, 400)
      $('.illness-name-span').text($(this).attr("data-illness-name"))
      $('.illness-proba-span').text(" (" + $(this).attr("data-proba-val") + "%)")
      $("#single_map_like, #single_map_unlike").attr("data-slug",$(this).attr("data-slug"))
      let approve_status = $(this).attr("data-approve-status")
      if(approve_status === "1") {
        // beğenilmiş
        $("#single_map_like").addClass("text-success-i")
        $("#single_map_unlike").removeClass("text-danger-i")
      } else if(approve_status === "2") {
        // beğenilmemiş
        $("#single_map_like").removeClass("text-success-i")
        $("#single_map_unlike").addClass("text-danger-i")
      } else {
        // 0 hiç bişey yapılmamış
        $("#single_map_like").addClass("text-success-iasd")
        $("#single_map_unlike").addClass("text-danger-iasd")
      }
    });
    $(".drawsElement").mouseleave(function () {
      // svg üzerinden gidince
      $(".drawsElement, .toothCardElement").css("pointer-events", "none")
      setTimeout(function () {
        $(".map-hover-popup.single").hasClass("open") ? null : $(".map-hover-popup.single").css("display", "none")
        $(".map-hover-popup.single").hasClass("open") ? null : $(".map-hover-popup__root").css("display", "none")
        $(".map-hover-popup.single").hasClass("open") ? null : removeDrawAnimatedLine(document.getElementById("teethDrawSvg-eng"))
        $(".drawsElement, .toothCardElement").css("pointer-events", "all")
      }, 1000)
    });
    $(".map-hover-popup.single").on("mouseover", function () {
      // popup üzerine gelince
      $(".map-hover-popup.single").addClass("open")
    });
    $(".map-hover-popup.single").mouseleave(function () {
      // popup üzerinden çıkınca
      $(this).css("display", "none").removeClass("open")
      $(".map-hover-popup__root").css("display", "none")
      removeDrawAnimatedLine(document.getElementById("teethDrawSvg-eng"))
    })
    $(".toothCardElement").mouseenter(function (event) {
      closeDoctorDrawSection() // doctor çizimi paneli açıksa kapat
      $("#deleteDoctorDraw").remove()
      try {
        // svg üzerine gelindiğinde
        let svgPath = $(this)
        svgPath.css("stroke", "white");
        let svgPathWidth = $(this).get(0).getBBox().width;
        let svgPathHeight = $(this).get(0).getBBox().height;
        let rootWidth = 5
        $(".map-hover-popup__root").css({
          "top": `${svgPath.offset().top + (svgPathHeight / 2) - (rootWidth / 2)}px`,
          "left": `${svgPath.offset().left + (svgPathWidth / 2) - (rootWidth / 2)}px`,
          "width": `${rootWidth}px`,
          "height": `${rootWidth}px`,
          "z-index": "9999",
          "display": "block"
        })
        let rootMiddleX = $(".map-hover-popup__root").offset().left + (rootWidth / 2)
        let rootMiddleY = $(".map-hover-popup__root").offset().top + (rootWidth / 2)
        setTimeout(function () {
          drawAnimatedLine(rootMiddleX, rootMiddleY, rootMiddleX + 30, rootMiddleY - 30, 200, document.getElementById('teethDrawSvg-eng'));
        }, 0)
        setTimeout(function () {
          drawAnimatedLine(rootMiddleX + 30, rootMiddleY - 30, rootMiddleX + 60, rootMiddleY - 30, 200, document.getElementById('teethDrawSvg-eng'));
        }, 200)
        setTimeout(function () {
          $(".map-hover-popup.multiple").css({
            "top": `${rootMiddleY - 30}px`,
            "left": `${rootMiddleX + 60}px`,
            "display": "inline-flex",
            "transform": "translateY(-50%)"
          })
        }, 400)
  
  
  
        $('.tooth-name').empty()
        tooth_html = `<i class="fa-solid fa-tooth" style="color: #0dcaf0"></i> Tooth ${$(this).attr("tooth-name")}`
        $('.tooth-name').append(tooth_html)
        // $('.tooth-name').text("Tooth " +  $(this).attr("tooth-name"))
  
        var data_ilness_name_list = $(this).attr("data-illness-name").split("*");
        var data_ilness_proba_list = $(this).attr("data-illness-proba").split("*");
        var data_ilness_slug_list = $(this).attr("data-illness-slug").split("*");
        var data_approve_dissapprove = $(this).attr("data-illness-approve").split("*");
        $("#multiple-card-body").empty();
        for (var i = 0; i < data_ilness_name_list.length; i++) {
          var htmlCode = `<div class="item d-flex justify-content-between">
            <span data-illness-slug="${data_ilness_slug_list[i]}" class="tooth_illness_name">${data_ilness_name_list[i]}
              <span class="text-primary tooth_illness_proba" style="color: #0dcaf0 !important;"> (${data_ilness_proba_list[i]}%)</span></span>
              <span class="ms-4">
                <i class="fa-solid fa-thumbs-up me-2 like ${data_approve_dissapprove[i] === '1' ? 'text-success-i' : ''}" data-slug="${data_ilness_slug_list[i]}" data-tooth-number="${$(this).attr("tooth-name")}"></i>
                <i class="fa-solid fa-thumbs-down unlike ${data_approve_dissapprove[i] === '2' ? 'text-danger-i' : ''}" data-slug="${data_ilness_slug_list[i]}" data-tooth-number="${$(this).attr("tooth-name")}"></i>
              </span>
            </div>`
          $("#multiple-card-body").append(htmlCode)
        }
      } catch (e) {
        console.log(e);
      }
    });
    $(".toothCardElement").mouseleave(function (event) {
      let svgPath = $(this)
      svgPath.css("stroke", "transparent");
      // svg üzerinden gidince
      $(".drawsElement, .toothCardElement").css("pointer-events", "none")
      setTimeout(function () {
        $(".map-hover-popup.multiple").hasClass("open") ? null : $(".map-hover-popup.multiple").css("display", "none")
        $(".map-hover-popup.multiple").hasClass("open") ? null : $(".map-hover-popup__root").css("display", "none")
        $(".map-hover-popup.multiple").hasClass("open") ? null : removeDrawAnimatedLine(document.getElementById("teethDrawSvg-eng"))
        $(".drawsElement, .toothCardElement").css("pointer-events", "all")
      }, 1000)
  
    });
    $(".map-hover-popup.multiple").on("mouseover", function () {
      // popup üzerine gelince
      $(".map-hover-popup.multiple").addClass("open")
    });
    $(".map-hover-popup.multiple").mouseleave(function () {
      // popup üzerinden çıkınca
      $(this).css("display", "none").removeClass("open")
      removeDrawAnimatedLine(document.getElementById("teethDrawSvg-eng"))
    })
  }
  
  $(".map-hover-popup").click(function (event) {
    // $(".map-hover-popup.muultiple").click(function (event) { // bu şekilde idi
    if (event.target.nodeName === "I") {
      // tıklanan bir ikonsa
      var approveStatus, toothNumber, slug
      var imageReportId = image_report_id
      if ($(event.target).attr("class").includes('like') && !$(event.target).attr("class").includes('unlike')) {
        // bu ikon like ise
        $(event.target).closest("span").find("i:nth-child(1)").addClass("text-success-i")
        $(event.target).closest("span").find("i:nth-child(2)").removeClass("text-danger-i")
        console.log("beğenme ikonu", $(event.target))
        approveStatus = 1
        slug = $(event.target).attr("data-slug")
        toothNumber = $(event.target).attr("data-tooth-number")
      } else if ($(event.target).attr("class").includes('unlike')) {
        // bu ikon dislike ise
        $(event.target).closest("span").find("i:nth-child(1)").removeClass("text-success-i")
        $(event.target).closest("span").find("i:nth-child(2)").addClass("text-danger-i")
        approveStatus = 2
        slug = $(event.target).attr("data-slug")
        toothNumber = $(event.target).attr("data-tooth-number")
      }
      console.log("approve-status : " + approveStatus + " - tootht-number : " + toothNumber + " - slug : " + slug + " - image-report-id : " + image_report_id)
      $.ajax({
        url: "/api/change_approve_status", // AJAX isteğinin gönderileceği URL
        type: "GET", // İstek tipi (GET, POST, vb.)
        data: {  // İstek verileri (isteğe bağlı)
          tooth_number: toothNumber,
          approve_status: approveStatus,
          illness_slug: slug,
          image_report_id: image_report_id,
        },
        success: function (response) { // İstek başarılı olduğunda çalışacak işlev
          console.log("gelen yanıt : ", response); // Yanıtı konsola yazdır
        },
        error: function (xhr, status, error) { // İstek başarısız olduğunda çalışacak işlev
          console.error(error); // Hata mesajını konsola yazdır
        }
      });
    }
  })