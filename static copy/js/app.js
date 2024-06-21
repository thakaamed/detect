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

function setAdjustableContent() {
    let headerHeight = $("section#header").outerHeight(true) || 55;
    // let userbarHeight = $(".user-bar").outerHeight(true);
    let footerHeight = $("section#footer").outerHeight(true) || 55;
    let marginBottom = 10;
    let totalHeight = `calc(100vh - ${headerHeight + footerHeight + marginBottom
        }px)`;
    $(".adjustable-content").css("height", totalHeight);
}


$(document).ready(function() {
    const pointers = $('.tree-view .slider .pointer-container .pointer');
    const sliders = pointers.parent();
    let isDragging = false;
    let activeSliderIndex = -1;
    let startPointerOffset;
    let initialPointerPosition;
  
    pointers.on('mousedown', function(event) {
      isDragging = true;
      activeSliderIndex = pointers.index($(this));
      const pointer = $(this);
      const slider = $(sliders[activeSliderIndex]);
      const sliderLeft = slider.offset().left;
      const pointerLeft = pointer.offset().left;
      startPointerOffset = event.pageX - pointerLeft;
      initialPointerPosition = parseInt(pointer.css('left'));
    });
  
    $(document).on('mousemove', function(event) {
      if (isDragging) {
        if (activeSliderIndex !== -1) {
          const slider = $(sliders[activeSliderIndex]);
          const pointer = $(pointers[activeSliderIndex]);
          const sliderLeft = slider.offset().left;
          const sliderWidth = slider.width();
          const pointerHalfWidth = pointer.width() / 2;
          const newPosition = event.pageX - sliderLeft - startPointerOffset;
          const newPositionNormalized = Math.max(0, Math.min(newPosition, sliderWidth - pointerHalfWidth));
          pointer.css('left', newPositionNormalized + 'px');
  
          // Update opacity based on position
          let opacityVal;
          if (newPositionNormalized === 0) {
            opacityVal = 0;
          } else if (newPositionNormalized === sliderWidth - pointerHalfWidth) {
            opacityVal = 1;
          } else {
            const positionPercentage = newPositionNormalized / (sliderWidth - pointerHalfWidth);
            if (positionPercentage <= 0.25) {
              opacityVal = positionPercentage * 0.25;
            } else if (positionPercentage <= 0.5) {
              opacityVal = (positionPercentage - 0.25) * 2;
            } else if (positionPercentage <= 0.75) {
              opacityVal = (positionPercentage - 0.5) * 2 + 0.5;
            } else {
              opacityVal = (positionPercentage - 0.75) * 4 + 0.75;
            }
          }
          matlaştır(activeSliderIndex, opacityVal);
          changeOpacityForDiagnosisPage(event, pointer, activeSliderIndex);
        }
      }
    });
    pointers.on('change', function() {
        if (isDragging) {
            if (activeSliderIndex !== -1) {
                const slider = $(sliders[activeSliderIndex]);
                const pointer = $(pointers[activeSliderIndex]);
                const sliderWidth = slider.width();
                const pointerHalfWidth = pointer.width() / 2;
                const currentPosition = parseInt(pointer.css('left'));
                if (currentPosition === 0) {
                    matlaştır(activeSliderIndex, 0);
                } else if (currentPosition === sliderWidth - pointerHalfWidth) {
                    matlaştır(activeSliderIndex, 1); // Maksimum matlık
                }
            }
            isDragging = false;
            activeSliderIndex = -1;
        }
    });
    function matlaştır(index, opacity) {
    //   console.log(`Slider ${index} pozisyonu: ${opacity}`);
    //   let illnessName = $(pointers[index]).attr("data-illness-name");
    //   let currentSvgPath = $(`.leaflet-pane svg path.drawsElement[data-illness-name='${illnessName}']`);
    //   currentSvgPath.attr("fill-opacity", opacity);
    }
  });
  
  

function hexToRgba(hex) {
    hex = hex.startsWith('#') ? hex.substring(1) : hex; 
    hex = hex.length === 3 ? hex.replace(/./g, '$&$&') : hex; 
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16),
        a: 1 
    } : null;
}
function changeColorForDiagnosisPage(event, id) {
    // bu fonksiyon diagnosis sayfaındaki input:color değiştiğinde arkaplan rengini değiştirir
    console.log("You clicked the color box");
    $(
        `.color[data-id='${id}'], .pointer-container .pointer[data-id='${id}']`
    ).css("background-color", event.target.value);
    $(`.gradient[data-id='${id}']`).css(
        "background-image",
        `linear-gradient(90deg, rgba(0, 0, 0, 0) 0%, ${event.target.value} 100%)`
    );
    let diagnosisName = $(event.target).attr("data-illness-name");
    let currentSvgPath = $(`.leaflet-pane svg [data-illness-name='${diagnosisName}']`);
    let currentColor = $(event.target).val();
    currentSvgPath.attr("fill", currentColor);
    currentSvgPath.attr("stroke", currentColor);
}
function changeOpacityForDiagnosisPage(event, pointerTarget, id) {
    // console.log("You changed color opacity");
    // let opacityVal = event.target.value;
    // let illnessName = $(event.target).attr("data-illness-name");
    // let currentSvgPath = $(`.leaflet-pane svg path.drawsElement[data-illness-name='${illnessName}']`);
    // $(pointerTarget).css("left", `${opacityVal}%`);
  
    // // Adjust factor for less transparency in matlaştırma
    // const matlaştırmaFactor = 0.000000000001; // You can adjust this value
  
    // currentSvgPath.attr("fill-opacity", opacityVal * matlaştırmaFactor);
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
    function clickHandlerRemove(event) {
        // $(".tooth-menu").removeClass("active")
        console.log(event.target)
        if (!$(event.target).hasClass("pencil") && !$(event.target).hasClass("tooth-edit")) {
            setTimeout(function () {
                $(".tooth-menu").removeClass("active")
            }, 100)
        }
    }
    if ($(".tooth-menu").hasClass("active")) {
        $("body").on("click", clickHandlerRemove);
    }

}

function changeToothType(toothId, path, element, className = "", toothType) {
    // seçilen dişin tipini değiştirir
    if ($(`.tooth[data-tooth='${toothId}'] img.imgToChange`).hasClass("auto-height")) {
        $(`.tooth[data-tooth='${toothId}'] img.imgToChange`).removeClass("auto-height")
    }
    // $(`.tooth[data-tooth='${toothId}'] img`).addClass("imgToChange");
    var $toothImage = $(`.tooth[data-tooth='${toothId}'] img.imgToChange`);
    if (toothId < 30 && toothType === "Pontic") {
        $toothImage.attr({"src": path, "data-tooth-type": toothType})
        $toothImage.addClass("mt-5"); 
        $toothImage.addClass(className); 

    } else if (toothId > 30 && toothType === "Pontic") {
        $toothImage.attr({"src": path, "data-tooth-type": toothType})
        $toothImage.addClass(className); 
        $toothImage.addClass("mb-5"); 


    }else{
        $toothImage.attr({"src": path, "data-tooth-type": toothType}).addClass(className)
        $toothImage.attr({"src": path, "data-tooth-type": toothType})
        $toothImage.removeClass("mb-5")
        $toothImage.removeClass("mt-5")
    }
    // $(`.tooth[data-tooth='${toothId}'] img.imgToChange`).attr({"src": path, "data-tooth-type": toothType}).addClass(className)
    $(".tooth-menu").removeClass("active") // tekrardan menüyü kapat
    var iconType = element.dataset.iconType;
    if (window.location.href.includes("embeded")) {
        url = "/api/embeded_update_reportTooth"
    } else {
        url = "/api/update_reportTooth"
    }
    $.ajax({
        url: url,
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
            let patientSlug = $(event.target).closest("tr").attr("data-patient-slug")
            openModal.attr("data-patient-slug", patientSlug)
        } else if ($(event.target).attr("data-modal-type") === "patient-delete-with-card") {
            let patientSlug = $(event.target).closest(".card-item").attr("data-patient-slug")
            openModal.attr("data-patient-slug", patientSlug)
        } else if ($(event.target).attr("data-modal-type") === "patient-radiography-upload") {
            var patientSlug = $(event.target).data('patient-slug');
            $("#modal-radyografy-upload").attr("data-patient-slug", patientSlug)
            dropzone_patient_slug = patientSlug
        } else if ($(event.target).attr("data-modal-type") === "patient-show-past-analysis") {
            var patientSlug = $(event.target).data('patient-slug');
            $("#modal-show-past-analysis").attr("data-patient-slug", patientSlug)
            dropzone_patient_slug = patientSlug
        }
    });
}

function liveSearchingForDiagnosis(event) {
    // diagnosis sayfasındaki hastalıklar için canlı arama fonksiyonu
    const searchQuery = event.target.value.toLowerCase();
    const searchResults = $(".label-element");
    let resultsFound = false;
    let resultsNotFoundMessage = "No disease found in the search criteria";
    const langCode = window.location.pathname.includes("/pt/") ? "pt" : window.location.pathname.includes("/ar/") ? "ar" : window.location.pathname.includes("/tr/") ? "tr" : "default";
    searchResults.each((index, item) => {
        const text = $(item).text().toLowerCase();
        $(item).closest(".child-view").addClass("d-block")
        if (text.includes(searchQuery)) {
            $(item).parent().parent().removeClass("passive");
            resultsFound = true;
            $(".diagnosis-content .items .not-found-messeage").html(null);
            $(".tree-view").css("display","block");
            $(".warning-message").css("display","none");

        } else {
            $(item).parent().parent().addClass("passive");
            // resultsFound = false;
        }

    });
    
    if(searchQuery.length == 0){
        $(".child-view").removeClass("d-block")
     }
    if (!resultsFound) {
        const notFoundMessage = langCode === "pt" ? "Nenhum critério de busca encontrado." : langCode === "ar" ? "لم يتم العثور على معيار البحث." : langCode === "tr" ? "Aranan kriterde hastalık bulunamadı" : langCode === "ru" ? "Не обнаружено ни одного заболевания, соответствующего критериям поиска." : langCode === "uz" ? "Qidiruv mezonlariga mos keladigan kasallik topilmadi" : langCode === "nl" ? "Er is geen ziekte gevonden die voldoet aan de zoekcriteria" : resultsNotFoundMessage;
        $(".warning-message").html(
            notFoundMessage
        );
        $(".tree-view").css("display","none");
        $(".warning-message").css("display","block");
    }
}

function liveSearchingForAddDiagnosis(event) {
    // diagnosis sayfasındaki add-diagnosis modal için canlı arama fonksiyonu
    let language = ""; 
    if (window.location.href.includes("/en/")) {
        language = "en";
    } else if (window.location.href.includes("/tr/")) {
        language = "tr";
    } else if (window.location.href.includes("/uz/")) {
        language = "uz";
    } else if (window.location.href.includes("/ru/")) {
        language = "ru";
    }
    else if (window.location.href.includes("/nl/")) {
        language = "nl";
    }
    let resultsNotFoundMessage = language === "en" ? "No disease found matching the criteria." :
                              language === "tr" ? "Aranan kriterde hastalık bulunamadı." :
                              language === "uz" ? "Izlanayotgan shartlarda kasallik topilmadi." :
                              language === "ru" ? "Болезнь, соответствующая критериям, не найдена." :
                              "No disease found matching the criteria."
                              language === "nl" ? "Болезнь, соответствующая критериям, не найдена." :
                              "Er is geen ziekte gevonden die voldoet aan de criteria.";
    const searchQuery = event.target.value.toLowerCase();
    const searchResults = $(".add-diagnosis-patient-container .patient-item");
    let resultsFound = false;
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

function setLikeUnlikeAttrOfPath(item, toothOrIlness) {
    // buraya gelen like yada unlike tuşu ve diş numarasına göre path üzerinde data-approve-status set edilir
    // neden böyle yapılır? çünkü like ve unlike değerlerini path üzerinden alıyor. istek atıldığında değişiyor fakat
    // sayfa yenilenmeden değişiklik gözükmüyor çünkü path deki değer güncellenmiyor, işte bu fonksiyon bunu güncelleyip
    // bu sorunu ortadan kaldırmak için
    let slug = item.attr("data-slug")
    let newApproveStatus = item.hasClass("fa-thumbs-up") ? 1 : 2

    if(toothOrIlness !== undefined) {
        // diş üzerinden like unlike geliyor
        let currentItemContainer = item.closest(".item")
        let itemContainers = $("#multiple-card-body .item")
        let indexWhichItemContainer = itemContainers.index(currentItemContainer) // array mantığı 0 dan başlar
        let toothPath = $(`.toothCardElement[tooth-name="${toothOrIlness}"]`)
        let aproveArrOfPath = toothPath.attr("data-illness-approve").split("*")
        aproveArrOfPath[indexWhichItemContainer] = newApproveStatus.toString()
        let newAproveString = aproveArrOfPath.join("*")
        toothPath.attr("data-illness-approve",newAproveString)
        // console.log("diş güncelleme", item, slug, toothOrIlness)
    } else {
        let targetPath = $(`path.drawsElement[data-slug="${slug}"]`)
        targetPath.attr("data-approve-status", newApproveStatus)
    }
}

$(".map-hover-popup").click(function (event) {
    // eğer ki açılan boxta beğen yada beğenmeye tıklanırsa
    // $(".map-hover-popup.muultiple").click(function (event) { // bu şekilde idi
    if (event.target.nodeName === "I") {
        // tıklanan bir ikonsa
        var approveStatus, toothNumber, slug
        var imageReportId = image_report_id
        if ($(event.target).attr("class").includes('like') && !$(event.target).attr("class").includes('unlike')) {
            // bu ikon like ise
            $(event.target).closest("span").find("i:nth-child(1)").addClass("text-success-i")
            $(event.target).closest("span").find("i:nth-child(2)").removeClass("text-danger-i")
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
        } else if ($(event.target).attr("class").includes('delete')){
            approveStatus = 3
            slug = $(event.target).attr("data-slug")
            toothNumber = $(event.target).attr("data-tooth-number")
            console.log("slug", slug)
        }
        setLikeUnlikeAttrOfPath($(event.target), toothNumber)
        // console.log("approve-status : " + approveStatus + " - tootht-number : " + toothNumber + " - slug : " + slug + " - image-report-id : " + image_report_id)
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
                if (approveStatus === 3){
                    var paths = document.querySelectorAll('path');

                    // Her bir SVG yolu elementi üzerinde döngü yap
                    paths.forEach(function(path) {
                        // Eğer "slug" değeri "d859d817c171414a9dede24ccae8464e" ise bu elementi seç
                        if (path.getAttribute('data-slug') === slug) {
                            var element = path;
                            element.remove()
                            // İstediğiniz işlemi gerçekleştirin
                        }
                    });
                }
            },
            error: function (xhr, status, error) { // İstek başarısız olduğunda çalışacak işlev
            }
        });
    }
})

function openToothBox(thisElement) {
    closeDoctorDrawSection() // doctor çizimi paneli açıksa kapat
    $("#deleteDoctorDraw").remove()
    try {
        // svg üzerine gelindiğinde
        let svgPath = thisElement
        // svgPath.css("stroke", "white");
        let svgPathWidth = thisElement.get(0).getBBox().width;
        let svgPathHeight = thisElement.get(0).getBBox().height;
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
        var tooth_text = "Tooth"
        if (window.location.href.includes("/tr/")) {
            tooth_text = "Diş";
        } else if (window.location.href.includes("/uz/")) {
            tooth_text = "Tish";
        } else if (window.location.href.includes("/ru/")) {
            tooth_text = "Зуб";
        }else if (window.location.href.includes("/nl/")) {
            tooth_text = "Tand";
        }else{
            tooth_text = "Tooth";
        }       
        tooth_html = `<i class="fa-solid fa-tooth" style="color: #0dcaf0"></i> ${tooth_text} ${thisElement.attr("tooth-name")}`
        $('.tooth-name').append(tooth_html)
        // $('.tooth-name').text("Tooth " +  $(this).attr("tooth-name"))

        var data_ilness_name_list = thisElement.attr("data-illness-name").split("*");
        var data_ilness_proba_list = thisElement.attr("data-illness-proba").split("*");
        var data_ilness_slug_list = thisElement.attr("data-illness-slug").split("*");
        var data_approve_dissapprove = thisElement.attr("data-illness-approve").split("*");
        $("#multiple-card-body").empty();
        for (var i = 0; i < data_ilness_name_list.length; i++) {
            var htmlCode = `<div class="item d-flex justify-content-between">
          <span data-illness-slug="${data_ilness_slug_list[i]}" class="tooth_illness_name">${data_ilness_name_list[i]}
            <span class="text-primary tooth_illness_proba" style="color: #0dcaf0 !important;"> (${data_ilness_proba_list[i]}%)</span></span>
            <span class="ms-4">
              <i class="fa-solid fa-thumbs-up me-2 like ${data_approve_dissapprove[i] === '1' ? 'text-success-i' : ''}" data-slug="${data_ilness_slug_list[i]}" data-tooth-number="${thisElement.attr("tooth-name")}"></i>
              <i class="fa-solid fa-thumbs-down unlike ${data_approve_dissapprove[i] === '2' ? 'text-danger-i' : ''}" data-slug="${data_ilness_slug_list[i]}" data-tooth-number="${thisElement.attr("tooth-name")}"></i>
            </span>
            <span class="ms-2">
                <i class="fa fa-times-circle delete" data-slug="${data_ilness_slug_list[i]}" data-tooth-number="${thisElement.attr("tooth-name")}" aria-hidden="true"></i>
            </span>
          </div>`
            $("#multiple-card-body").append(htmlCode)
        }
    } catch (e) {
        console.log(e);
    }
}

function parseCoordinates(inputString) {
    // bu fonksiyon M89 174L86 176L86 205L88 206L95 ... şeklinde gelen string coord alır diziye çevirip verir
    // Gelen stringi parçalara bölmek için "L" karakterini kullanıyoruz.
    const points = inputString.split("L");

    // x ve y koordinatlarını tutacak bir dizi oluşturuyoruz.
    const coordinates = [];

    // Her bir parçayı dolaşıyoruz ve x, y ikililerini çıkarıyoruz.
    for (let i = 0; i < points.length; i++) {
        const point = points[i];
        const [x, y] = point.split(" ").map(parseFloat);
        coordinates.push({ x, y });
    }

    return coordinates;
}

function findClosestPoint(x, y, points) {
    // bu fonksiyon gelen x ve y değerine en yakın olan x ve y noktalarını pointsten bulur ve bunu döndürür
    let closestPoint = null;
    let closestDistance = Number.MAX_VALUE;
  
    // İkinci parametredeki her bir noktayı dolaşarak en yakın olanı buluyoruz.
    for (const point of points) {
      const [pointX, pointY] = point;
      const distance = Math.sqrt((x - pointX) ** 2 + (y - pointY) ** 2);
  
      if (distance < closestDistance) {
        closestDistance = distance;
        closestPoint = [pointX, pointY];
      }
    }
  
    return closestPoint;
  }

  function toggleMapPopup() {
    var toothCardBoxIsOpen = false
    $(".drawsElement").on("click", function () {
        toothCardBoxIsOpen = false
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

        if ($(this).attr("data-illness-name") === "Mandibular Canal") {
            // eğer ki üzerine gelinen Mandibular Canal ise en yakın noktayı al ve root elementini orada belirt
            let svg = $(this).closest("svg")
            console.log(svg.width())
            let centerPointsOfSvg = [svgPath.offset().top + (svgPathHeight / 2) - (rootWidth / 2), svgPath.offset().left + (svgPathWidth / 2) - (rootWidth / 2)]
            let coordsString = $(this).attr("d")
            console.log("this buna denk gelir : ",$(this))
            let coordsArr = parseCoordinates(coordsString)
            // coordsArr.map(item=>{
            //     console.log("sıralı ikililer : ", item)
            //     $("body").append(`<div style="background-color:lime;position:absolute;width:2px;height:2px;border-radius:50%;left:${item[0] + $("#back-img-frame").offset().left}px;top:${item[1] + $("#back-img-frame").offset().top}px;z-index:99999999999999999999999;"></div>`)
            // })
            let closestPoints = findClosestPoint(centerPointsOfSvg[0], centerPointsOfSvg[1], coordsArr)
            $(".map-hover-popup__root").css({
                "left" : `${closestPoints[0] + $("#back-img-frame").offset().left}px`,
                "top" : `${closestPoints[1] + $("#back-img-frame").offset().top}px`
            })
        }

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
        $("#single_map_like, #single_map_unlike, #single_map_delete").attr("data-slug", $(this).attr("data-slug"))
        let approve_status = $(this).attr("data-approve-status")
        if (approve_status === "1") {
            // beğenilmiş
            $("#single_map_like").addClass("text-success-i")
            $("#single_map_unlike").removeClass("text-danger-i")
        } else if (approve_status === "2") {
            // beğenilmemiş
            $("#single_map_like").removeClass("text-success-i")
            $("#single_map_unlike").addClass("text-danger-i")
        } else {
            // 0 hiç bişey yapılmamış
            $("#single_map_like").addClass("text-success-iasd")
            $("#single_map_unlike").addClass("text-danger-iasd")
        }
    });

    $(document).click(function(event) {
        if (!$(event.target).closest('.drawsElement').length) {
            // If the click is not within the drawsElement
            console.log("Clicked outside drawsElement");
            $(".map-hover-popup.single").css("display", "none")
            $(".map-hover-popup__root").css("display", "none")
            removeDrawAnimatedLine(document.getElementById("teethDrawSvg-eng"))
        }
    });

    /*
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
    */
    $(".map-hover-popup.single").on("mouseover", function () {
        // popup üzerine gelince
        $(".map-hover-popup.single").addClass("open")
    });
    /**$(".map-hover-popup.single").mouseleave(function () {
        // popup üzerinden çıkınca
        $(this).css("display", "none").removeClass("open")
        $(".map-hover-popup__root").css("display", "none")
        removeDrawAnimatedLine(document.getElementById("teethDrawSvg-eng"))
    })**/




    $(".toothCardElement").mouseenter(function (event) {
        $(this).css("stroke", "white");
    });
    $(".toothCardElement").mouseleave(function (event) {
        $(this).css("stroke", "transparent");
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
        }, 500)

    });
    

    $(".toothCardElement").mousemove(function (event) {
        $(".map-hover-popup.single").hide()
        let percent = 25
        let boxWidth = this.getBBox().width;
        let boxHeight = this.getBBox().height;
        let boxOffset = $(this).offset();
        let mouseX = event.pageX - boxOffset.left;
        let mouseY = event.pageY - boxOffset.top;
        let percentFirstWidth = boxWidth * (percent / 100)
        let percentLastWidth = boxWidth - percentFirstWidth
        let percentFirstHeight = boxHeight * (percent / 100)
        let percentLastHeight = boxHeight - percentFirstHeight

        //console.log("Mouse position inside the box: X=" + mouseX + ", Y=" + mouseY);
        //console.log("Box dimensions: Width=" + boxWidth + ", Height=" + boxHeight);
        //console.log("percentFirst10Width, percentLast10Width", percentFirst10Width ,percentLast10Width, percentFirst10Height, percentLast10Height)

        if ((mouseX > percentFirstWidth && mouseX < percentLastWidth) && (mouseY > percentFirstHeight && mouseY < percentLastHeight)) {
            // kutunun tam ortasına geldi
            // müsait artık kutu açılabilir
            if (!toothCardBoxIsOpen) {
                openToothBox($(this))
            }
            toothCardBoxIsOpen = true
        } else {
            // kutunun ortasından çıktı
            if (toothCardBoxIsOpen === true) { toothCardBoxIsOpen = false }
        }
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




