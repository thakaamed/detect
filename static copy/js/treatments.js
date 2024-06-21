function changeImageSource() {
    // .dropzone-x-ray sınıfına sahip elementi seç ve toggle() fonksiyonu ile görünürlüğünü değiştir
    $(".dropzone-x-ray").toggle();
}

$(".navbar-one-img").click(function () {
    $(".navbar-two-img").removeClass("navbar-two-img-light")
    $(".navbar-four-img").removeClass("navbar-four-img-light")
    $(".navbar-tree-img").removeClass("navbar-tree-img-light")
    $(".navbar-one-img").removeClass("navbar-one-img-light")
})
$(".navbar-two-img").click(function () {
    $(".navbar-two-img").addClass("navbar-two-img-light")
    $(".navbar-four-img").removeClass("navbar-four-img-light")
    $(".navbar-tree-img").removeClass("navbar-tree-img-light")
    $(".navbar-one-img").addClass("navbar-one-img-light")
})
$(".navbar-tree-img").click(function () {
    $(".navbar-tree-img").addClass("navbar-tree-img-light")
    $(".navbar-two-img").removeClass("navbar-two-img-light")
    $(".navbar-four-img").removeClass("navbar-four-img-light")
    $(".navbar-one-img").addClass("navbar-one-img-light")
})
$(".navbar-four-img").click(function () {
    $(".navbar-four-img").addClass("navbar-four-img-light")
    $(".navbar-tree-img").removeClass("navbar-tree-img-light")
    $(".navbar-two-img").removeClass("navbar-two-img-light")
    $(".navbar-one-img").addClass("navbar-one-img-light")
})

$('.missing-part').on('click', function () {
    // $(".transparents-Extraction").removeClass("d-none");
    // var activeCount = $('.mising-active').length;
    // var span_values = [...$(".mising-active")]
    // console.log(span_values)
    // var spanValues = span_values.map(item => {
    //     var spanText = $(item).children("span").text();
    //      console.log("Value inside span:", spanValues); 
    //     return spanText;
    // })
    // $('.transparents-armount-text').text(activeCount + " x");
    // spanValues.forEach(function (value) {
    //     $('.diagnosis-container').append(`
    //         <div class="gap-2 treatments-new-span rounded d-flex px-2 justify-content-between align-items-center">${value} <i class="fa-solid fa-xmark treatments-x" style="font-size: 14px; cursor: pointer;"></i></div>
    //     `);
    // });
    //  console.log("Span values:", spanValues);
    //  console.log("activeCount:", activeCount);
    // var unitValue= $(".treatments-unit-price span").text()
    // var multipliedValues = ( activeCount * unitValue);
    // console.log(multipliedValues ,"multipliedValues")
    // $(".treatments-price-table").append(`
    //     <span>${multipliedValues}</span> <i class="fa-solid fa-turkish-lira-sign"></i>
    // `)
});

// Toplam değeri hesaplayan fonksiyon
function updateTotalValue() {
    var totalSpans = $(".treatments-price-total");
    var totalValue = 0;
    totalSpans.each(function() {
        if ($(this).text().trim()!= "-"){
            totalValue += parseFloat($(this).text());
        }
    });
    $('.transparents-total-price-span').fadeOut(300, function() {
        $(this).text(totalValue).fadeIn(300);
    });
}
$(document).ready(function() {
    updateTotalValue();
    $('#exampleButton').on('click', function() {
        updateTotalValue();
    });
});


// $("#myTooltip").on('click', function() {
//     $("#discountInput").prop("readonly", false);
// });
// Discount input alanının değerini her değişiklikte güncelle
$("#discountInput").on('input', function() {
    var inputValue = $(this).val().trim();
    if (inputValue.length > 0) {
        inputValue = inputValue.replace(/[^0-9]/g, ''); 
        inputValue = '-' + inputValue;
    }
    $(this).val(inputValue);
    updateDiscountAndTotalDifference();
});

$("#discountInput").on('keyup', function(event) {
    if (event.keyCode === 8 && $(this).val().trim().length === 1) {
        $(this).val('');
        updateDiscountAndTotalDifference();
    } else if ($(this).val().trim() === '-') {
        $(this).val('');
        updateDiscountAndTotalDifference();
    }
});

function updateDiscountAndTotalDifference() {
    var discountValue = parseInt($("#discountInput").val()) || 0; 
    var totalValue = 100; 
    var difference = totalValue - discountValue;
    $(".discounted-prices").text(difference);
}

// İlk yükleme ve butona tıklandığında güncelleme işlemleri
$(document).ready(function() {
    updateDiscountAndTotalDifference();
    $('#exampleButton').on('click', function() {
        updateDiscountAndTotalDifference();
    });
});

// Discount ve total değerlerin farkını güncelleme fonksiyonu
function updateDiscountAndTotalDifference() {
    var discountValue = $("#discountInput").val().trim();
    if (discountValue.length > 0) {
        discountValue = discountValue.replace(/[^0-9]/g, ''); 
        discountValue = '-' + discountValue;
    }

    var totalSpans = $(".treatments-price-total");
    var totalValue = 0;
    totalSpans.each(function() {
        if ($(this).text().trim() != "-") {
            totalValue += parseFloat($(this).text());
        }
    });

    if (parseFloat(discountValue) === totalValue) {
        $('.discounted-price').text(totalValue);
    } else {
        var difference = discountValue === '' ? totalValue : totalValue + parseFloat(discountValue);
        $('.discounted-price').text(difference);
    }

    // Eğer discountValue NaN ise discounted-price yerine transparents-total-price-span sınıfının değerini koy
    if (isNaN(parseFloat(discountValue))) {
        $('.discounted-price').text($(".transparents-total-price-span").text());
    }
}



$(document).ready(function() {
    $('#myTooltip').tooltip({
        title: 'Discount',
        placement: 'top',
        trigger: 'hover' 
    });
    $('#myTooltipTwo').tooltip({
        title: 'Healing period',
        placement: 'top',
        trigger: 'hover' 
    });
    $('#myTooltipTree').tooltip({
        title: 'Templates',
        placement: 'top',
        trigger: 'hover' 
    });
    $('#myTooltipFour').tooltip({
        title: 'Phase',
        placement: 'top',
        trigger: 'hover' 
    });
    $('#myTooltipFive').tooltip({
        title: 'Reset',
        placement: 'top',
        trigger: 'hover' 
    });
});



// var priceSpans = $(".treatments-price-table span");
// var totalValue = 0;
// priceSpans.each(function() {
//     totalValue += parseFloat($(this).text());
// });

var counter = 2;

// $(".treatments-tab-plus").click(function () {
//     var newElement = `
//         <div id="treatmentsDiv_${counter}" class="treatments-tab treatments-tab-one d-flex gap-2 align-items-center justify-content-center py-2 " style="background-color: rgba(44, 57, 99, 1); cursor: pointer;">
//         Treatment Plan <span class="treatmentsSpan">${counter}</span>
//         <i class="fa-solid fa-xmark treatments-x" style="font-size: 14px; cursor: pointer;"></i>
//         </div>
//         `;
//     $(".treatments-tab-append").append(newElement);
//     counter++;
// });

$(document).on('click', '.treatments-x', function () {
    $(this).closest('.treatments-tab').remove();
    counter--;
});

$(".treatments-tab-append").on('click', '[id^="treatmentsDiv_"]', function () {
    $(".treatments-tab").removeClass("treatments-tab-menu-active");
    $(this).addClass("treatments-tab-menu-active");
});

$(".treatments-tab-append").click(function () {
    $(this).removeClass("treatments-tab-menu-active");
});

$(".treatments-tab-append").on('click', '[id^="treatmentsDiv_"]', function () {
});

$(".treatments-tab").on("click", function () {
    $(".block-ulti-div").show()
    // $(".none-ulti-div").hide()
})

$("#modalClose").click(function () {
    $("#myModal").modal('hide')
})
var clickedRowId;
$('.trash-icon-container').click(function () {
    clickedRowId = $(this).attr('data-row');
    $('#myModal').modal('show');
});
$("#modalYes").click(function () {
    $('#' + clickedRowId + '.diagnosis-container').removeClass("d-flex").addClass("d-none");
    $('#myModal').modal('hide');
});
$("#modalYesTwo").click(function(){
    $("#myModalTwo").modal('hide');
})
$("#modalCloseTwo").click(function(){
    $("#myModalTwo").modal('hide');
})
$("#modalXTwo").click(function(){
    $("#myModalTwo").modal('hide');
})

$('.trash-icon-container').click(function () {
    var clickedRow = $(this).data('row');
    $('#myModal').modal('show');
});
$("#myTooltipTree").click(function(){
    $("#myModalTwo").modal('show')
})

function appendToDiagnosisContainer(element) {
    var value_at = $(element).text()
    var selectedElement = [...$('.mising-active')];
    selectedElement.map((item) => {
        var id = $(item).attr("data-span");
        $(`#${id}`).append(`
        <div class=" d-flex gap-2 justify-content-between align-items-center px-2 rounded-2">
        <p >${value_at}</p>
        </div>
        `)
        $(".external").removeClass("mising-active")
    })
}

var elements = $('.external-one, .external-two');
elements.on('click', function () {
    elements.removeClass('selected');
    $(this).addClass('selected');
});

function handleMouseActions(element) {
    var isMouseDown = false;

    $(element).mousedown(function (e) {
        e.preventDefault();
        isMouseDown = true;
        $(this).toggleClass("mising-active");
    });

    $(element).mouseover(function () {
        if (isMouseDown) {
            $(this).addClass("mising-active");
        }
    });

    $(document).mouseup(function () {
        isMouseDown = false;
    });

    $(element).click(function (e) {
        if (!isMouseDown) {
            $(this).toggleClass("mising-active");
        }
    });
}

$(".external-one, .external-two").click(function () {
    $(this).toggleClass("mising-active");
});
handleMouseActions(".external-one, .external-two");


$(".icon-reset").click(function () {
    $(".resettable").each(function () {
        var defaultValue = $(this).data("default-value");
        if ($(this).is("input") || $(this).is("textarea")) {
            $(this).val(defaultValue);
        } else if ($(this).is("div")) {
            $(this).text(defaultValue);
        }
    });
});

$('#icon').click(function () {
    $('.dz-image img').addClass('brighten');
});
var konstrant = 0;
$('#iconTwo').click(function () {
    konstrant++;
    $('.dz-image img').addClass('brightenK');
});
$("#rotateDropzone").click(function () {
    $('.dz-image img').removeClass('brightenK');
    $('.dz-image img').removeClass('brighten');
})

function toggleNestedDropdown(element) {
    $(".dropdown-content").not($(element).find(".dropdown-content")).hide();
    $(element).find(".dropdown-content").toggle();
}
function closeDropdown(element) {
    $(element).closest(".dropdown-content").hide();
}
$(document).on("click", function (event) {
    if (!$(event.target).closest('.missing-part').length) {
        $(".dropdown-content").hide();
    }
});

$(".filler-close").click(function () {
    $(".filled-icon-block").addClass("d-none")
})
$(".implant-close").click(function () {
    $(".Implant-icon-block").addClass("d-none")
})
$(".crown-close").click(function () {
    $(".crown-icon-block").addClass("d-none")
})

$(".filled-icon").click(function () {
    $(".filled-icon-block").toggleClass("d-none")
})
$(".crown-icon").click(function () {
    $(".crown-icon-block").toggleClass("d-none")
})
$(".Implant-icon").click(function () {
    $(".Implant-icon-block").toggleClass("d-none")
})
$(".other-icon").click(function () {
    $(".other-icon-block").toggleClass("d-none")
})



var clickCount = 0;
var maxClicks = 3;
var initialScale = 1.2;
var step = 0.2;
$(".zoom-block").click(function () {
    if (clickCount < maxClicks) {
        var scale = initialScale + (clickCount * step);
        $(".dz-image").css("transform", "scale(" + scale + ")");
    }
});
$(".zoom-none").click(function () {
    if (clickCount < maxClicks && clickCount >= 0) {
        var scale = initialScale + ((maxClicks - clickCount - 1) * step);
        $(".dz-image").css("transform", "scale(" + scale + ")");
        clickCount++;
    } else {
        clickCount = 0;
        $(".dz-image").css("transform", "scale(1.2)");
    }
});

$(".navbar-one-img").click(function () {
    $(".navbar-two-img").removeClass("navbar-two-img-light")
    $(".navbar-four-img").removeClass("navbar-four-img-light")
    $(".navbar-tree-img").removeClass("navbar-tree-img-light")
    $(".navbar-one-img").removeClass("navbar-one-img-light")
})
$(".navbar-two-img").click(function () {
    $(".navbar-two-img").addClass("navbar-two-img-light")
    $(".navbar-four-img").removeClass("navbar-four-img-light")
    $(".navbar-tree-img").removeClass("navbar-tree-img-light")
    $(".navbar-one-img").addClass("navbar-one-img-light")
})
$(".navbar-tree-img").click(function () {
    $(".navbar-tree-img").addClass("navbar-tree-img-light")
    $(".navbar-two-img").removeClass("navbar-two-img-light")
    $(".navbar-four-img").removeClass("navbar-four-img-light")
    $(".navbar-one-img").addClass("navbar-one-img-light")
})
$(".navbar-four-img").click(function () {
    $(".navbar-four-img").addClass("navbar-four-img-light")
    $(".navbar-tree-img").removeClass("navbar-tree-img-light")
    $(".navbar-two-img").removeClass("navbar-two-img-light")
    $(".navbar-one-img").addClass("navbar-one-img-light")
})

$(".missing-intact").click(function () {
    $(".intact-dropdown").slideToggle("d-none")
    $(".intact-dropdown").removeClass("d-none")
})
$(".intact-close").click(function () {
    $(".intact-dropdown").addClass("d-none")
})

$('.x-ray-block-icon').on('click', function () {
    var currentSrc = $(this).attr('src');
    if (currentSrc === "{% static 'img/diagnosis-x-ray-dark-icon.png' %}") {
        $(this).attr('src', "{% static 'img/diagnosis-x-ray-light-icon.png' %}");
        $(".dropzone-x-ray").addClass("d-block")
    } else {
        $(this).attr('src', "{% static 'img/diagnosis-x-ray-dark-icon.png' %}");
        $(".dropzone-x-ray").removeClass("d-block")
    }
});

function removeDiv(element) {
    element.parentElement.remove();
}
$(".other-dropdown").click(function () {
    $("#myDropdown").toggle();
});

$(document).on("click", function (event) {
    if (!$(event.target).closest(".other-dropdown").length) {
        $("#myDropdown").hide();
    }
});

function toggleNestedDropdown(element) {
    $(".dropdown-content").not($(element).find(".dropdown-content")).hide();
    $(element).find(".dropdown-content").toggle();
}
$(document).on("click", function (event) {
    if (!$(event.target).closest(".missing-part").length) {
        $(".dropdown-content").hide();
    }
});

// $(".table-add").click(function () {
//     var currentRow = $(this).closest(".row");
//     var diagnosisContainer = currentRow.find(".diagnosis-container");
//     var newTextAreaId = "textarea-" + Date.now();
//     diagnosisContainer.append(`
//         <div class="diagnosis-general-child append-div-textarea tratmens-textarea d-flex justify-content-between align-items-center px-2 rounded-2">
//         <input id="${newTextAreaId}" placeholder="..." class="append-textarea" style="width: 21px;  font-size: 14px; height: 20px; color: white; background: transparent; border: none;">
//         <i class="fa-solid fa-plus plus-icon-general" onclick="plusDiv(this)"></i>
//         <i class="fa-solid fa-xmark general-none d-none" onclick="removeDiv('${newTextAreaId}')"></i>
//         </div>
//         `);
// });
function plusDiv(clickedIcon) {
    var currentRowIcons = $(clickedIcon).closest(".diagnosis-general-child");
    var plusIcon = currentRowIcons.find(".plus-icon-general");
    var noneIcon = currentRowIcons.find(".general-none");

    noneIcon.removeClass("d-none");
    plusIcon.hide();

    if (!noneIcon.hasClass("d-none")) {
        var inputField = currentRowIcons.find(".append-textarea");
        inputField.prop('disabled', true);
        currentRowIcons.css('background-color', 'rgba(80, 113, 200, 1)');
        inputField.addClass("input-light-color");
        noneIcon.addClass("input-light-color");
    }
}

function removeDiv(textAreaId) {
    $("#" + textAreaId).closest('.diagnosis-general-child').remove();
}

$(".table-add-general").click(function () {
    var currentRow = $(this).closest(".row");
    var diagnosisContainer = currentRow.find(".general-append");
    var newTextAreaId = "textarea-" + Date.now();
    diagnosisContainer.append(`
        <div class="diagnosis-general-child append-div-textarea d-flex justify-content-between align-items-center px-2 rounded-2">
        <input id="${newTextAreaId}" placeholder="..." class="append-textarea" style="max-width: 80px; font-size: 14px; height: 20px; color: white; background: transparent; border: none;">
        <i class="fa-solid fa-plus plus-icon-general" onclick="plusDiv(this)"></i>
        <i class="fa-solid fa-xmark general-none d-none" onclick="removeDiv('${newTextAreaId}')"></i>
        </div>
        `);
});
function plusDiv(clickedIcon) {
    var currentRowIcons = $(clickedIcon).closest(".diagnosis-general-child");
    var plusIcon = currentRowIcons.find(".plus-icon-general");
    var noneIcon = currentRowIcons.find(".general-none");
    noneIcon.removeClass("d-none");
    plusIcon.hide();
    if (!noneIcon.hasClass("d-none")) {
        var inputField = currentRowIcons.find(".append-textarea");
        inputField.prop('disabled', true);
        currentRowIcons.css('background-color', 'rgba(80, 113, 200, 1)');
        inputField.addClass("input-light-color");
        noneIcon.addClass("input-light-color");
    }
}
function removeDiv(textAreaId) {
    $("#" + textAreaId).closest('.diagnosis-general-child').remove();
}


$('.treatments-unit-price input').on('input', function() {
    var inputValuee = $(this).val().trim();
    inputValuee = inputValuee.replace(/[^0-9]/g, '');
    $(this).val(inputValuee);

});


// Sayfa yüklendiğinde çalışacak JavaScript kodları
function closeDropdown() {
    // Get the dropdown menu element
    const dropdownMenu = document.querySelector('.dropdown-menu');
  
    // Close the dropdown menu
    dropdownMenu.classList.remove('show');
  }
  
  // Prevent default behavior on click inside dropdown menu
  document.querySelector('.dropdown-menu').addEventListener('click', (event) => {
    event.stopPropagation();
  });
  


