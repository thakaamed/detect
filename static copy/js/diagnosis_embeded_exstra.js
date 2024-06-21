var currentDoctorDraw;
var currentDoctorDrawObj;


function resetLabelingBox() {
    $("#labeling-box").addClass("d-none").removeClass("d-inline-flex")
    $(".doctorAddedIllnessCircle").remove()
    $("input[name='diseases-list']").prop("checked", false);
}

function addTrashBtnForDoctorDraw(thisElement) {
    let leftForIconElem = thisElement.offset().left + thisElement.get(0).getBBox().width - 20 + "px"
    let topForIconElem = thisElement.offset().top + thisElement.get(0).getBBox().height - 20 + "px"
    $("#deleteDoctorDraw").remove()
    $("body").append(`
        <i id="deleteDoctorDraw" class="fa-solid fa-trash text-light position-absolute" style="left: ${leftForIconElem}; top: ${topForIconElem};"></i>
    `);

    $("#deleteDoctorDraw").click(function () {
        // doktorun çizdiği çizimi kaldırma
        $("#modal-remove-doctor-draw").addClass("active")
        console.log("delete this draw")
        $("#removeThisDoctorDraw").click(function () {
            currentDoctorDraw.remove()
            removeIlnessFunc($(currentDoctorDraw).attr("data-slug"))
            closeDoctorDrawSection()
            $("#deleteDoctorDraw").remove()
        })
    })
}

$(document).ready(async function () {
    async function getDiagnosisContent() {
        let template = "";
        try {
            const response = await $.ajax({
                url: "/api/embeded-all-diseases",
                method: "GET",
                data: { image_report_id: image_report_id },
            });
            let createContent = await response.disease_list.map((item) => {
                template += `
                <div class="diseases-item align-items-center" style="display: flex;">
                    <div class="check-container position-relative">
                      <input type="radio" name="diseases-list" id="diseases-${item.id}" value="${item.id}" data-color="${item.color}" data-illness="${item.name}">
                      <div class="check-container-bg position-absolute"></div>
                      <i class="fa-solid fa-check"></i>
                    </div>
                    <label for="diseases-${item.id}" class="m-0" style="color: #333;">${item.name}</label>
                </div>
            `;
            });
        } catch (error) {
            console.error("getDiagnosisContent function error : ", error);
        }

        return template;
    }

    let diasesForDraw = await getDiagnosisContent()
    $(".labeling-box_content").html(diasesForDraw)
    $("[name='diseases-list']").click(function (event) {
        setTimeout(() => {
            resetLabelingBox()
        }, 550);
        $("path.leaflet-interactive").last().attr({
            "fill": $(event.target).attr("data-color"),
            "stroke": $(event.target).attr("data-color"),
            "stroke-dasharray": 0,
            "data-illness": $(event.target).attr("data-illness")
        })
        // var leflet = $("path.leaflet-interactive")._layers[i]._parts;
        drawed_objects[drawed_objects.length - 1].label.id = $(event.target)[0].value;
        saveIlnessFunc(drawed_objects[drawed_objects.length - 1].label.id, drawed_objects[drawed_objects.length - 1].layer._parts[0])
    })

    $(document).on("click", function (event) {
        var targetElement = $(event.target);
        var labelingBox = $("#labeling-box");

        if (!targetElement.is(labelingBox) && !labelingBox.hasClass("d-none") && !targetElement.closest("#labeling-box").length) {
            // labeling box açıkken kendisi harici bir yere tıklandı, "d-none" sınıfı yok ve labeling-box içinde tıklanmadı, burada yapılacak işlemi tanımlayabilirsiniz
            resetLabelingBox()
            $("path.leaflet-interactive").last().remove();
        }
    });

    $("#labeling-box").on("click", function (event) {
        event.stopPropagation();
    });

    $(document).on('mouseover', 'svg .leaflet-interactive', function () {
        // sayfaya dinamik eklenen öğenin eventı çalışması için bu şekilde kullanılması gerekir saygılar e.b.
        // doktorun çizdiği kare çizim üzerine gelince (çizime dönüştükten sonra)   
        closeDoctorDrawSection()
        if ($(this).attr("stroke-dasharray") === "0") {
            addTrashBtnForDoctorDraw($(this))
            currentDoctorDraw = $(this)
            // hastalık seçildikten sonra kare çizmin üzerine gelinirse
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
                $(".map-hover-popup.doctor-draw").css({
                    "top": `${rootMiddleY - 30}px`,
                    "left": `${rootMiddleX + 60}px`,
                    "display": "inline-flex",
                    "transform": "translateY(-50%)"
                })
            }, 400)
            $('.illness-name-doctor').text($(this).attr("data-illness"));

        }
    });

    $("[data-close-doctor-draw]").click(function () {
        // doktor hastalık seçipte çizim yapırınca ve o çizimin üzerine gelince kapatma ikonuna tıklanma olayı
        closeDoctorDrawSection()
        $("#deleteDoctorDraw").remove()
    })

})


function saveIlnessFunc(label_id, drawed_parts) {
    var coordinates = [];
    for (var i = 0; i < drawed_parts.length; i++) {
        coordinates.push([drawed_parts[i].x, drawed_parts[i].y])
    }
    $.ajax({
        url: "/api/embeded-save-drawed-diagnosis",
        type: "POST",
        headers: { 'X-CSRFToken': csrfToken },
        data: {
            label_id: parseInt(label_id),
            coordinates: JSON.stringify(coordinates),
            image_report_id: image_report_id,
            original_shape: JSON.stringify([original_shape.width_rate, original_shape.height_rate])
        },
        dataType: "json",
        success: function (response) {
            console.log("response", response)
            if (response.status) {
                console.log("Veri başarıyla kaydedildi. Slug: " + response.slug);
                drawed_objects[drawed_objects.length - 1].label.slug = response.slug;
                $(".leaflet-interactive").last().attr({
                    "data-slug": response.slug,
                });
            } else {
                console.log("Veri kaydedilemedi.");
            }
        },
        error: function (error) {
            console.log("Hata:", error);
        }
    });
}


function removeIlnessFunc(slug) {

    $.ajax({
        url: "/api/embeded-delete-drawed-illness",
        type: "POST",
        headers: { 'X-CSRFToken': csrfToken },
        data: {
            illness_slug: slug,
            image_report_id: image_report_id
        },
        dataType: "json",
        success: function (response) {
            console.log("response", response)
            if (response.status) {
                console.log("Veri başarıyla silindi.");
            } else {
                console.log("Veri silinemedi.");
            }
        },
        error: function (error) {
            console.log("Hata:", error);
        }
    });
}

function saveImpCrwMarker() {
    var coordinates = [];
    for (var i = 0; i < drawed_parts.length; i++) {
        coordinates.push([drawed_parts[i].x, drawed_parts[i].y])
    }
    $.ajax({
        url: "/api/embeded-save-drawed-diagnosis",
        type: "POST",
        headers: { 'X-CSRFToken': csrfToken },
        data: {
            label_id: parseInt(label_id),
            coordinates: JSON.stringify(coordinates),
            image_report_id: image_report_id,
            original_shape: JSON.stringify([original_shape.width_rate, original_shape.height_rate])
        },
        dataType: "json",
        success: function (response) {
            console.log("response", response)
            if (response.status) {
                console.log("Veri başarıyla kaydedildi. Slug: " + response.slug);
                drawed_objects[drawed_objects.length - 1].label.slug = response.slug;
                $(".leaflet-interactive").last().attr({
                    "data-slug": response.slug,
                });
            } else {
                console.log("Veri kaydedilemedi.");
            }
        },
        error: function (error) {
            console.log("Hata:", error);
        }
    });
}