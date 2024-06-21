$("[data-open-view-analysis]").click(function (event) {
    $(event.target).toggleClass("transparent btn-blue")
    $("#view-analysis").toggleClass("active")
})

$(".report-list[data-collapseble] .input-container input").focus(function () {
    $(".report-items").css("height", "150px")
})

$(".report-list[data-collapseble] .input-container input").blur(function () {
    setTimeout(function () {
        $(".report-list[data-collapseble] .report-items").css("height", "0px")
    }, 500)
})

function getPointCategoryByPoint(point) {
    // bu fonksiyon gelen point noktasının hangi ana kategoriye ait olduğunu döndürür
    // baz aldığı değişken html sayfasındaki var ile tanımlanmış lateral_cephalometric_dict değişkeni
    let currentCategory
    let keysOfMyObject = Object.getOwnPropertyNames(lateral_cephalometric_dict);
    for (let i = 0; i < keysOfMyObject.length; i++) {
        let currentArray = lateral_cephalometric_dict[keysOfMyObject[i]]
        if (currentArray.includes(point)) {
            currentCategory = keysOfMyObject[i]
            break
        }
    }
    return currentCategory
}

function createPointForMap(multiple, target) {
    // bu fonksiyon gelen targeta göre gider nokta oluşturur ve yerleştirir
    $(".point-area").remove() // noktaların hepsinden önce bir kurtul
    if (multiple) {
        // birden çok nokta çizdirilecek
        console.log("gelen noktalar : ", target)
        target.map((index, item) => {
            console.log(index, item, $(item).get(0).getBBox().width)
            let point = item

            let pointWidth = $(item).get(0).getBBox().width
            let pointHeight = $(item).get(0).getBBox().height
            let offsetLeftOfPoint = $(item).offset().left
            let offsetToptOfPoint = $(item).offset().top
            let pointAreaDiv = $("<div>");
            pointAreaDiv.addClass("point-area");
            pointAreaDiv.css({
                "top": `${offsetToptOfPoint + (pointHeight / 2)}px`,
                "left": `${offsetLeftOfPoint + (pointWidth / 2)}px`
            })
            $("body").append(pointAreaDiv);
        })
    } else {
        // yok tek nokta yeterli
        let point = target
        let pointWidth = point.get(0).getBBox().width
        let pointHeight = point.get(0).getBBox().height
        let offsetLeftOfPoint = point.offset().left
        let offsetToptOfPoint = point.offset().top
        let pointAreaDiv = $("<div>");
        pointAreaDiv.addClass("point-area");
        pointAreaDiv.css({
            "top": `${offsetToptOfPoint + (pointHeight / 2)}px`,
            "left": `${offsetLeftOfPoint + (pointWidth / 2)}px`
        })
        $("body").append(pointAreaDiv);
        // console.log("clicked to item")
    }
}

function selectAllMultiInput(event, targetDatalist) {
    if ($(event.target).is(":checked")) {
        targetDatalist.find("option").each((index, item) => {
            targetDatalist.parent().find("input").val()
            let optionItem = document.createElement('div');
            optionItem.classList.add('item');
            optionItem.textContent = $(item).val();
            targetDatalist.parent().append(optionItem)
            targetDatalist.html('')
        })
    } else {
        $(targetDatalist.parent().find(".item")).each((index, item) => {
            let option = document.createElement('option')
            option.value = $(item).text()
            targetDatalist.append(option)
            $(item).remove()
        })
    }
}

function selectAllMultipleSelect(event, targetSelectbox) {
    if ($(event.target).is(":checked")) {
        // hepsini aç
        targetSelectbox.find(".report-item").addClass("active")
    } else {
        // hepsini kapat
        targetSelectbox.find(".report-item.active").removeClass("active")
    }
}

$(".angle-container input").change(function (event) {
    let radioValue = event.target.value
    $(this).closest(".angle-container").find(".section-back-value").css("width", `${20 * radioValue}%`)
    $(this).closest(".angle-container").find(".section-marker").css("left", `${20 * radioValue}%`)
    $(this).closest(".angle-container").find(".current-number").css("left", `${20 * (radioValue - 1)}%`)
})


var scaleVal = -1
$(".flip_span[data-direction]").click(function () {
    let direction = $(this).attr("data-direction")
    if (direction === "vertical") {
        $("#container").css("transform", `scaleX(${scaleVal})`)
    } else {
        $("#container").css("transform", `scaleY(${scaleVal})`)
    }
    scaleVal === -1 ? scaleVal = 1 : scaleVal = -1
    $(".flip_span").removeClass("active")
    $(this).addClass("active")
})

var rotateVal = 0
$(".flip_span[data-rotate-direction]").click(function () {
    let rotateDirection = $(this).attr("data-rotate-direction")
    rotateVal = (rotateVal + parseInt(rotateDirection)) % 360
    $("#rotateInput").val(rotateVal)
    if (rotateVal >= 0) {
        $("#rotate-btn").nextAll('.range-marker').first().css("left", `${rotateVal / 3.6}%`);
        $("#rotate-btn").nextAll('.range-value').first().css("width", `${rotateVal / 3.6}%`);
    }
    $("#rotate-btn").val(rotateVal)
    rotateBackImg()
})

$(".flip_span").click(function () {
    $(".flip_span").removeClass("active")
    $(this).addClass("active")
})

$("#resetRotateBtn").click(function () {
    rotateVal = 0
    $("#rotateInput").val(rotateVal)
    $("#rotate-btn").nextAll('.range-marker').first().css("left", "0");
    $("#rotate-btn").nextAll('.range-value').first().css("width", "0");
    rotateBackImg()
})

$("#rotateInput").on("input", function () {
    var inputVal = $(this).val();
    // Check if inputVal is a number
    console.log("değer", rotateVal)


    if (!isNaN(inputVal)) {
        // Convert the input value to a number
        var numValue = parseFloat(inputVal);

        // Check if the number is within the range [0, 360]
        if (numValue >= 0 && numValue <= 360) {
            // Valid number, do nothing
            rotateVal = parseInt(inputVal)
        } else {
            // Number is out of range, reset the input value
            $(this).val('');
            console.log("Please enter a number between 0 and 360.");
        }
    } else {
        // Input is a string, remove the string part and keep the numeric part
        var numPart = inputVal.replace(/[^0-9.-]/g, '');
        $(this).val(numPart);
        if (inputVal === '') {
            rotateVal = 0
        }
    }
    $("#rotate-btn").nextAll('.range-marker').first().css("left", `${inputVal / 3.6}%`);
    $("#rotate-btn").nextAll('.range-value').first().css("width", `${inputVal / 3.6}%`);
    rotateBackImg()

})

$("#rotate-btn").on("input", function () {
    let value = $(this).val()
    rotateVal = parseInt(value)
    $("#rotateInput").val(value)
    rotateBackImg()
})

function rotateBackImg() {
    $("#container").css("transform", `rotate(${rotateVal}deg)`)
}


// çizdirme fonksiyonları başlıyor - panel
function mapPopup() {
    $("#back-img-frame svg path.path_circle").on("mouseover", function () {
        // if (!$("#editMode").prop("checked")) {
        let svgPath = $(this)
        let svgPathWidth = $(this).get(0).getBBox().width;
        let svgPathHeight = $(this).get(0).getBBox().height;

        let rootWidth = 10
        $(".map-hover-popup__root").css({
            "top": `${svgPath.offset().top + (svgPathHeight / 2) - (rootWidth / 2)}px`,
            "left": `${svgPath.offset().left + (svgPathWidth / 2) - (rootWidth / 2)}px`,
            "width": `${rootWidth}px`,
            "height": `${rootWidth}px`,
            "z-index": "9999",
            "display": "block",
            "border-radius": "50%"
        })

        let rootMiddleX = $(".map-hover-popup__root").offset().left + (rootWidth / 2)
        let rootMiddleY = $(".map-hover-popup__root").offset().top + (rootWidth / 2)

        setTimeout(function () {
            removeDrawAnimatedLine(document.getElementById('teethDrawSvg-eng'))
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
        $('.illness-name-span').text($(this).attr("data-circle-name"))
        // }

    })
    $("#back-img-frame svg path.path_circle").mouseleave(function () {
        $(".map-hover-popup.single").css("display", "none")
        $(".map-hover-popup__root").css("display", "none")
        removeDrawAnimatedLine(document.getElementById("teethDrawSvg-eng"))
    });
}

// çizdirme fonksiyonları bitiyor - panel

$("#view-analysis-selectbox").change(function (event) {
    doReportTable(event.target.value)

})

function doReportTable(val, state= false) {
    console.log("view_analysis_dict", view_analysis_dict)
    let myObject = view_analysis_dict[val]
    let keysOfMyObject = Object.getOwnPropertyNames(myObject);
    let template = ''
    for (let i = 0; i < keysOfMyObject.length; i++) {
        let keysOfMyObject2 = Object.getOwnPropertyNames(myObject[keysOfMyObject[i]]);
        keysOfMyObject2.map((item, index) => {
            template += `
            <tr>
                <td>${item}</td>
                <td>${myObject[keysOfMyObject[i]][item][0]}</td>
                <td>${myObject[keysOfMyObject[i]][item][1]}</td>
                <td>${myObject[keysOfMyObject[i]][item][2]}</td>
                <td>±${myObject[keysOfMyObject[i]][item][3]}</td>
                <td>${typeof myObject[keysOfMyObject[i]][item][4] === 'number' ? myObject[keysOfMyObject[i]][item][4].toFixed(2) : myObject[keysOfMyObject[i]][item][4]}</td>
            </tr>
            `
        })
    }
    if(!state) {
        try {
            if (res_tooth_cephalometric_coords) {
                map.eachLayer((layer) => {
                    layer.remove();
                });
                spline_list_name = [];
                spline_circleMarker_list = [];
                drawPolylineMapList = [];
                draw_leaflet();
            }
            drawAngleChangeFunc(Object.getOwnPropertyNames(view_analysis_dict[val].angles));
        } catch (error) {
            console.log(error)
        }
    }
    $("#report-table tbody").html(template)
}

function updateLateralPoints(label_name,coordinates) {
    var form = new FormData();
    form.append("label_name", label_name);
    form.append("image_report_id", image_report_id);
    form.append("coordinates", coordinates);

    var settings = {
        "url": "/api/update-lateral-points",
        "method": "POST",
        "timeout": 0,
        "headers": {
            "X-CSRFToken": $('input[name=csrfmiddlewaretoken]').val()
        },
        "processData": false,
        "mimeType": "multipart/form-data",
        "contentType": false,
        "data": form
    };

    $.ajax(settings).done(function (response) {
        console.log(response);
        map.eachLayer((layer) => {
            layer.remove();
        });
        spline_list_name = [];
        spline_circleMarker_list = [];
        drawPolylineMapList = [];
        view_analysis_dict = [];
        draw_leaflet();
        startCheckingAnalysisDict();
    });
}

function startCheckingAnalysisDict() {
    var intervalId = setInterval(function () {
        if (view_analysis_dict) {
            drawAngleChangeFunc(Object.getOwnPropertyNames(view_analysis_dict[$("#view-analysis-selectbox").val()].angles));
            if (drawPolylineMapList.length > 0) {
                for (var i = 0; i < drawPolylineMapList.length; i++) {
                    drawPolylineMapList[i][0].bringToBack()
                }
            }
            doReportTable($("#view-analysis-selectbox").val(), true);
            clearInterval(intervalId);
        }
    }, 500); 
}

function doGroupSelectBox() {
    // burası cephalometric kısmındaki yukarıda sol ve sağ tarafta group ve point kısmının initini yükler sayfa ilk yüklendiğinde itemları onun içine sıkar
    let myObject = lateral_cephalometric_dict
    let keysOfMyObject = Object.getOwnPropertyNames(myObject);
    template = `
        <div class="report-item justify-content-between align-items-center active" data-item-name="all">
            All
            <i class="fa-solid fa-check text-white"></i>
        </div>`
    keysOfMyObject.map((item, index) => {

        template += `
        <div class="report-item justify-content-between align-items-center" data-item-name="${item}">
            ${item}
            <i class="fa-solid fa-check text-white"></i>
        </div>`
    })
    $("#group_report_item.report-items").html(template)
}
function doPointSelectbox(datas) {
    let myObject = lateral_cephalometric_dict
    let keysOfMyObject = Object.getOwnPropertyNames(myObject);
    let template = ''
    var excepts_from_list = ["A processed point", "B processed point", "Li processed point", "Ls processed point", "Mx1c processed point"]

    datas.map(item => {
        if(!excepts_from_list.includes(item)){
            template += `
            <div class="report-item justify-content-between align-items-center" data-item-name="${item}">
                ${item}
                <i class="fa-solid fa-check text-white"></i>
            </div>`
        }
        
    })
    $("#point_report_item.report-items").html(template)
}

$(function () {
    doReportTable("Bjork-Jarabak Analysis")
    doGroupSelectBox()
    $(".report-list .report-items .report-item").click(function (event) {
        if ($(event.target).attr("data-multiple-selectbox") === "true") {
            // console.log("çoklu seim")
            $(event.target).toggleClass("active")
        } else {
            // console.log("çoksuz seçim")
            $(event.target).parent().find(".report-item").removeClass("active")
            $(event.target).addClass("active")
        }
    })
    $("#group_report_item.report-items .report-item").click(function (event) {
        console.log("buraya girdin")
        if ($(this).attr("data-item-name") === "all") {
            // hepsi seçeneği seçilmiş
            doPointSelectbox(allPoints) // tüm noktalar kutuya konuldu
        } else {
            doPointSelectbox(lateral_cephalometric_dict[$(this).attr("data-item-name")])
        }
        $(".report-list .report-items .report-item").click(function (event) {
            if ($(event.target).attr("data-multiple-selectbox") === "true") {
                // console.log("çoklu seim")
                $(event.target).toggleClass("active")
            } else {
                // console.log("çoksuz seçim")
                $(event.target).parent().find(".report-item").removeClass("active")
                $(event.target).addClass("active")
            }
        })
    })
    $("[data-point-items]").click(function (event) {
        // group noktaları ve tekli bir nokta için açık olan menüye tıklandığında harita üzerinde o noktalar belirgin olacak
        let whichSide = $(event.target).closest("[data-point-items]").attr("data-point-items")
        let itemName = $(event.target).attr("data-item-name")
        if (whichSide === "group") {
            createPointForMap(true, $(`path.path_circle[data-point-category="${itemName}"]`))
        } else if (whichSide === "item") {
            createPointForMap(false, $(`path.path_circle[data-circle-name="${itemName}"]`))
        }
    })
})



$(".icon .dropdown-section input[type='color']").focus(function (event) {
    // buradaki sorun toolların içindeki boya kutusuna tıklayınca açılan renk paletine gelince fare .icon dışına çıktığı için komple kapanıyordu onu çözdüm
    $(this).closest(".dropdown-section").addClass("d-flex")
})

$(".icon .dropdown-section input[type='color']").blur(function (event) {
    // buradaki sorun toolların içindeki boya kutusuna tıklayınca açılan renk paletine gelince fare .icon dışına çıktığı için komple kapanıyordu onu çözdüm
    $(this).closest(".dropdown-section").removeClass("d-flex")
})

// tollarda filter toolundaki değişiklikler
$("input[name='filter-tool']").change(function (event) {
    let deadpool = event.target.value
    let cssStatement
    switch (deadpool) {
        case 'invert':
            cssStatement = "invert(100%)"
            break;
        case 'blur':
            cssStatement = "blur(3px)"
            break;
        case 'grayscale':
            cssStatement = "grayscale(100%)"
            break;
        case 'sepia':
            cssStatement = "sepia(100%)"
            break;
    }

    $("#container").css("filter", cssStatement)

})

$("#editMode").click(function () {
    if ($("#editMode").prop("checked")) {
        map.pm.enableGlobalDragMode();
        if ($(".map-hover-popup").css("display") !== 'none') {
            removeDrawAnimatedLine(document.getElementById('teethDrawSvg-eng'));
        }
        try {
            for (var i = 0; i < drawSplineMapList.length; i++) {
                drawSplineMapList[i][0].pm.disable()
            }
        } catch (e) {
            console.log(e);
        }

    } else {
        map.pm.disableGlobalDragMode();
        dragObjectMove = false;
    }
});

$("#editPicture").change(function () {
    // tollar içindeki edit picture checkboxına tıklayınca
    if ($(this).is(":checked")) {
        $("#reset-btn").click();
        $("#cropButton").show()
        $("#rotate_tool").show()
        $("#flip-tool").show()
        $("#draw-tool").show()
        $("#font-tool").show()
        $("#contrast-tool").hide()
        $("#brightness-tool").hide()
        $("#shape-tool").hide()
        $("#zoomin-btn").hide()
        $("#zoomout-btn").hide()
        $("#reset-btn").hide()
        $("#bar_length_tool").hide()
        $("#scale-bar-tool").hide()
        $("#editmode-tool").hide()
        $(".leaflet-pane").addClass("d-none")
        $("#back-img").css("display", "none");
        $("#container").css("display", "")
        $("#save-tool").show()
        $(".point-area").hide()
        $("#shape-tool").show()
        $("#filter-tool").show()
        $("#img-reset-tool").show()
    } else {
        $("#cropButton").hide()
        $("#rotate_tool").hide()
        $("#flip-tool").hide()
        $("#draw-tool").hide()
        $("#font-tool").hide()
        $("#contrast-tool").show()
        $("#brightness-tool").show()
        $("#shape-tool").show()
        $("#zoomin-btn").show()
        $("#zoomout-btn").show()
        $("#reset-btn").show()
        $("#bar_length_tool").show()
        $("#scale-bar-tool").show()
        $("#editmode-tool").show()
        $(".leaflet-pane").removeClass("d-none")
        $("#back-img").css("display", "");
        $("#container").css("display", "none")
        $("#save-tool").hide()
        $(".point-area").show()
        $("#shape-tool").hide()
        $("#filter-tool").hide()
        $("#img-reset-tool").hide()
    }
})

if (window.addEventListener) {
    window.addEventListener('load', function () {
        var canvas, context, canvaso, contexto;

        var backgroundImage = new Image();
        backgroundImage.src = $("#back-img")[0].getAttribute("src");

        'lelele';

        // The active tool instance.
        var tool;
        var tool_default = 'none';

        function init() {
            // Find the canvas element.
            canvaso = document.getElementById('canvas');
            if (!canvaso) {
                alert('Error: I cannot find the canvas element!');
                return;
            }

            if (!canvaso.getContext) {
                alert('Error: no canvas.getContext!');
                return;
            }

            // Get the 2D canvas context.
            contexto = canvaso.getContext('2d');
            if (!contexto) {
                alert('Error: failed to getContext!');
                return;
            }

            // Add the temporary canvas.
            var container = canvaso.parentNode;
            canvas = document.createElement('canvas');
            if (!canvas) {
                alert('Error: I cannot create a new canvas element!');
                return;
            }

            $("#cropButton").on("click", function () {
                tool = new tools.crop();
                tool_select = 'crop';
                canvas.style.cursor = 'crosshair';
                // Uncheck the fontCheckbox
                $("#fontCheckbox").prop("checked", false);
            });

            var ww = $("#back-img").width();
            var wh = $("#back-img").height();
            canvaso.width = ww;
            canvaso.height = wh;

            canvas.id = 'imageTemp';
            canvas.width = canvaso.width;
            canvas.height = canvaso.height;
            container.appendChild(canvas);

            context = canvas.getContext('2d');

            $("input[name='draw_tool_type']").change(closeTextInput);
            $("input[name='shape_tool_type']").change(closeTextInput);

            function closeTextInput() {
                var textInput = document.getElementById('textInput');
                textInput.style.display = 'none';
                textInput.value = '';
                textInputActive = false;
            }

            $("input[name='draw_tool_type']").change(ev_tool_change);
            $("input[name='shape_tool_type']").change(ev_tool_change);
            canvas.addEventListener('mousedown', ev_canvas, false);
            canvas.addEventListener('mousemove', ev_canvas, false);
            canvas.addEventListener('mouseup', ev_canvas, false);

            backgroundImage.onload = function () {
                contexto.drawImage(backgroundImage, 0, 0, canvaso.width, canvaso.height);
            };

            var textInputActive = false; // Metin girişinin aktif olup olmadığını takip etmek için bir bayrak

            function addText(e) {
                if ($("#fontCheckbox").prop("checked")) {
                    if (!textInputActive) {
                        var textInput = document.getElementById('textInput');
                        var rect = canvas.getBoundingClientRect();
                        var x = e.clientX - rect.left + window.pageXOffset;
                        var y = e.clientY - rect.top + window.pageYOffset;

                        textInput.style.left = x + 'px';
                        textInput.style.top = y + 'px';
                        textInput.style.display = 'block';
                        textInput.focus();

                        textInputActive = true; // Metin girişi aktif hale getirildi
                    }
                }
            }

            canvas.addEventListener('click', addText);

            // Textarea'da Enter tuşuna basıldığında metni çizin ve textarea'yı gizleyin
            textInput.addEventListener('keydown', function (e) {
                if (e.key === 'Enter') {
                    var text = textInput.value;
                    var x = parseInt(textInput.style.left);
                    var y = parseInt(textInput.style.top);

                    context.font = $("#fontTypeSize").val() + "px " + $("#fontTypeName").val();
                    context.fillStyle = canvasTextColorCode;
                    context.fillText(text, x, y);

                    textInput.value = '';
                    textInput.style.display = 'none';

                    textInputActive = false; // Metin girişi pasif hale getirildi

                    img_update();
                }
            });
        }

        // The general-purpose event handler. This function just determines the mouse
        // position relative to the canvas element.
        function ev_canvas(ev) {
            if (ev.layerX || ev.layerX == 0) {// Firefox
                ev._x = ev.layerX;
                ev._y = ev.layerY;
            } else if (ev.offsetX || ev.offsetX == 0) {// Opera
                ev._x = ev.offsetX;
                ev._y = ev.offsetY;
            }

            // Call the event handler of the tool.
            try {
                var func = tool[ev.type];
                if (func) {
                    func(ev);
                }
            } catch (e) {
            }

        }

        var tool_select;

        // The event handler for any changes made to the tool selector.
        function ev_tool_change(ev) {
            if (tools[this.value]) {
                tool = new tools[this.value]();
                tool_select = this.value;
                // Uncheck the fontCheckbox
                $("#fontCheckbox").prop("checked", false);
            } else {
                tool = new tools.none(); // Aktif olmayan bir araç atanır
                tool_select = 'none';
            }
        }

        // completes a drawing operation.
        function img_update() {
            contexto.drawImage(canvas, 0, 0);
            context.clearRect(0, 0, canvas.width, canvas.height);
        }

        // This object holds the implementation of each drawing tool.
        var tools = {};

        tools.none = function () {
            this.mousedown = function (ev) {
            };
            this.mousemove = function (ev) {
            };
            this.mouseup = function (ev) {
            };
        };

        // Crop tool
        tools.crop = function () {
            var tool = this;
            this.started = false;
            var startX, startY, endX, endY;
            var canvasCursor = canvas.style.cursor; // Store the original cursor style

            this.mousedown = function (ev) {
                tool.started = true;
                startX = ev._x;
                startY = ev._y;
                endX = ev._x;
                endY = ev._y;

                // Change the cursor to a plus sign
                canvas.style.cursor = 'crosshair';
            };

            this.mousemove = function (ev) {
                if (!tool.started) {
                    return;
                }

                endX = ev._x;
                endY = ev._y;

                // Clear the canvas
                context.clearRect(0, 0, canvas.width, canvas.height);

                // Draw the original image
                contexto.drawImage(backgroundImage, 0, 0, canvaso.width, canvaso.height);

                // Draw the cropped image as background
                context.fillStyle = 'rgba(0, 0, 0, 0.5)';
                context.fillRect(0, 0, canvas.width, canvas.height);

                // Draw the crop area
                context.clearRect(startX, startY, endX - startX, endY - startY);
            };

            this.mouseup = function (ev) {
                if (tool.started) {
                    tool.mousemove(ev);
                    tool.started = false;

                    // Calculate the crop dimensions
                    var width = Math.abs(endX - startX);
                    var height = Math.abs(endY - startY);
                    var left = Math.min(startX, endX);
                    var top = Math.min(startY, endY);

                    // Create a temporary canvas to hold the cropped image
                    var tempCanvas = document.createElement('canvas');
                    tempCanvas.width = width;
                    tempCanvas.height = height;
                    var tempContext = tempCanvas.getContext('2d');

                    // Crop the image
                    tempContext.drawImage(canvaso, left, top, width, height, 0, 0, width, height);

                    // Clear the canvas
                    contexto.clearRect(0, 0, canvas.width, canvas.height);

                    // Draw the cropped image on the canvas
                    contexto.drawImage(tempCanvas, 0, 0, canvaso.width, canvaso.height);

                    // Reset the tool selection
                    tool = new tools.none();
                    tool_select = 'none';

                    // Clear the crop selection
                    context.clearRect(0, 0, canvas.width, canvas.height);

                    // Update the display
                    img_update();

                    // Restore the cursor to the default style
                    canvas.style.cursor = canvasCursor;
                }
            };
        };

        // The drawing pencil.
        tools.pencil = function () {
            var tool = this;
            this.started = false;

            // This is called when you start holding down the mouse button.
            // This starts the pencil drawing.
            this.mousedown = function (ev) {
                context.beginPath();
                context.moveTo(ev._x, ev._y);
                tool.started = true;
                context.strokeStyle = canvasDrawColorCode;
                context.lineWidth = canvasDrawBorderValue;
            };

            // This function is called every time you move the mouse. Obviously, it only
            // draws if the tool.started state is set to true (when you are holding down
            // the mouse button).
            this.mousemove = function (ev) {
                if (tool.started) {
                    context.lineTo(ev._x, ev._y);
                    context.stroke();
                    context.strokeStyle = canvasDrawColorCode;
                    context.lineWidth = canvasDrawBorderValue;
                }
            };

            // This is called when you release the mouse button.
            this.mouseup = function (ev) {
                if (tool.started) {
                    tool.mousemove(ev);
                    tool.started = false;
                    img_update();
                    context.strokeStyle = canvasDrawColorCode;
                    context.lineWidth = canvasDrawBorderValue;
                }
            };
        };

        // The rectangle tool.
        tools.rect = function () {
            var tool = this;
            this.started = false;
            var startX, startY;

            this.mousedown = function (ev) {
                tool.started = true;
                startX = ev._x;
                startY = ev._y;
                context.strokeStyle = canvasDrawShapeBorderColorCode;
                context.lineWidth = canvasDrawShapeBorderValue;
            };

            this.mousemove = function (ev) {
                if (!tool.started) {
                    return;
                }

                var currentX = Math.min(ev._x, startX);
                var currentY = Math.min(ev._y, startY);
                var width = Math.abs(ev._x - startX);
                var height = Math.abs(ev._y - startY);

                context.clearRect(0, 0, canvas.width, canvas.height);

                context.beginPath();
                context.rect(currentX, currentY, width, height);
                context.closePath();
                context.stroke();
                if (canvasDrawShapeFillColorCode !== "") {
                    context.fillStyle = canvasDrawShapeFillColorCode; // İç dolgu rengini ayarla
                    context.fill();
                }
                context.strokeStyle = canvasDrawShapeBorderColorCode;
                context.lineWidth = canvasDrawShapeBorderValue;

                if (!width || !height) {
                    return;
                }

                context.strokeRect(currentX, currentY, width, height);
                context.strokeStyle = canvasDrawColorCode;
                context.lineWidth = canvasDrawShapeBorderValue;
            };

            this.mouseup = function (ev) {
                if (tool.started) {
                    tool.mousemove(ev);
                    tool.started = false;
                    img_update();
                    context.strokeStyle = canvasDrawShapeBorderColorCode;
                    context.lineWidth = canvasDrawShapeBorderValue;
                }
            };
        };

        // The circle tool.
        tools.circle = function () {
            var tool = this;
            this.started = false;
            var startX, startY;

            this.mousedown = function (ev) {
                tool.started = true;
                startX = ev._x;
                startY = ev._y;
                context.strokeStyle = canvasDrawShapeBorderColorCode;
                context.lineWidth = canvasDrawShapeBorderValue;
            };

            this.mousemove = function (ev) {
                if (!tool.started) {
                    return;
                }

                var currentX = startX;
                var currentY = startY;
                var radius = Math.sqrt(Math.pow(ev._x - startX, 2) + Math.pow(ev._y - startY, 2));

                context.clearRect(0, 0, canvas.width, canvas.height);

                context.beginPath();
                context.arc(currentX, currentY, radius, 0, 2 * Math.PI);
                context.stroke();
                context.closePath();
                if (canvasDrawShapeFillColorCode !== "") {
                    context.fillStyle = canvasDrawShapeFillColorCode; // İç dolgu rengini ayarla
                    context.fill();
                }
                context.strokeStyle = canvasDrawShapeBorderColorCode;
                context.lineWidth = canvasDrawShapeBorderValue;
            };

            this.mouseup = function (ev) {
                if (tool.started) {
                    tool.mousemove(ev);
                    tool.started = false;
                    img_update();
                    context.strokeStyle = canvasDrawShapeBorderColorCode;
                    context.lineWidth = canvasDrawShapeBorderValue;
                }
            };
        };

        // The triangle tool.
        tools.triangle = function () {
            var tool = this;
            this.started = false;
            var startX, startY;

            this.mousedown = function (ev) {
                tool.started = true;
                startX = ev._x;
                startY = ev._y;
                context.strokeStyle = canvasDrawShapeBorderColorCode;
                context.lineWidth = canvasDrawShapeBorderValue;
            };

            this.mousemove = function (ev) {
                if (!tool.started) {
                    return;
                }

                var currentX = startX;
                var currentY = startY;
                var endX = ev._x;
                var endY = ev._y;

                context.clearRect(0, 0, canvas.width, canvas.height);

                context.beginPath();
                context.moveTo(currentX, currentY);
                context.lineTo(endX, endY);
                context.lineTo(startX - (endX - startX), endY);
                context.closePath();
                context.stroke();
                if (canvasDrawShapeFillColorCode !== "") {
                    context.fillStyle = canvasDrawShapeFillColorCode; // İç dolgu rengini ayarla
                    context.fill();
                }
                context.strokeStyle = canvasDrawShapeBorderColorCode;
                context.lineWidth = canvasDrawShapeBorderValue;
            };

            this.mouseup = function (ev) {
                if (tool.started) {
                    tool.mousemove(ev);
                    tool.started = false;
                    img_update();
                    context.strokeStyle = canvasDrawShapeBorderColorCode;
                    context.lineWidth = canvasDrawShapeBorderValue;
                }
            };
        };

        // The line tool.
        tools.line = function () {
            var tool = this;
            this.started = false;

            this.mousedown = function (ev) {
                tool.started = true;
                tool.x0 = ev._x;
                tool.y0 = ev._y;
                context.strokeStyle = canvasDrawColorCode;
                context.lineWidth = canvasDrawBorderValue;
            };

            this.mousemove = function (ev) {
                if (!tool.started) {
                    return;
                }

                context.clearRect(0, 0, canvas.width, canvas.height);

                context.beginPath();
                context.moveTo(tool.x0, tool.y0);
                context.lineTo(ev._x, ev._y);
                context.stroke();
                context.closePath();
                context.strokeStyle = canvasDrawColorCode;
                context.lineWidth = canvasDrawBorderValue;
            };

            this.mouseup = function (ev) {
                if (tool.started) {
                    tool.mousemove(ev);
                    tool.started = false;
                    img_update();
                    context.strokeStyle = canvasDrawColorCode;
                    context.lineWidth = canvasDrawBorderValue;
                }
            };
        };

        // The arrow tool.
        tools.arrow = function () {
            var tool = this;
            this.started = false;

            this.mousedown = function (ev) {
                tool.started = true;
                tool.x0 = ev._x;
                tool.y0 = ev._y;
                context.strokeStyle = canvasDrawColorCode;
                context.lineWidth = canvasDrawBorderValue;
            };

            this.mousemove = function (ev) {
                if (!tool.started) {
                    return;
                }

                // Clear the canvas
                context.clearRect(0, 0, canvas.width, canvas.height);

                // Draw the line
                context.beginPath();
                context.moveTo(tool.x0, tool.y0);
                context.lineTo(ev._x, ev._y);
                context.stroke();
                context.strokeStyle = canvasDrawColorCode;
                context.lineWidth = canvasDrawBorderValue;

                // Calculate the angle of the line
                var angle = Math.atan2(ev._y - tool.y0, ev._x - tool.x0);

                // Calculate the arrow size based on the line length
                var lineLength = Math.sqrt(Math.pow(ev._x - tool.x0, 2) + Math.pow(ev._y - tool.y0, 2));
                var arrowSize = lineLength / 10;

                // Draw the arrowhead at the end point
                context.beginPath();
                context.moveTo(ev._x, ev._y);
                context.lineTo(
                    ev._x - arrowSize * Math.cos(angle - Math.PI / 6),
                    ev._y - arrowSize * Math.sin(angle - Math.PI / 6)
                );
                context.moveTo(ev._x, ev._y);
                context.lineTo(
                    ev._x - arrowSize * Math.cos(angle + Math.PI / 6),
                    ev._y - arrowSize * Math.sin(angle + Math.PI / 6)
                );
                context.closePath();
                context.stroke();
            };

            this.mouseup = function (ev) {
                if (tool.started) {
                    tool.mousemove(ev);
                    tool.started = false;

                    // Draw the line
                    context.beginPath();
                    context.moveTo(tool.x0, tool.y0);
                    context.lineTo(ev._x, ev._y);
                    context.stroke();
                    context.strokeStyle = canvasDrawColorCode;
                    context.lineWidth = canvasDrawBorderValue;

                    // Calculate the angle of the line
                    var angle = Math.atan2(ev._y - tool.y0, ev._x - tool.x0);

                    // Calculate the arrow size based on the line length
                    var lineLength = Math.sqrt(Math.pow(ev._x - tool.x0, 2) + Math.pow(ev._y - tool.y0, 2));
                    var arrowSize = lineLength / 10;

                    // Draw the arrowhead at the end point
                    context.beginPath();
                    context.moveTo(ev._x, ev._y);
                    context.lineTo(
                        ev._x - arrowSize * Math.cos(angle - Math.PI / 6),
                        ev._y - arrowSize * Math.sin(angle - Math.PI / 6)
                    );
                    context.moveTo(ev._x, ev._y);
                    context.lineTo(
                        ev._x - arrowSize * Math.cos(angle + Math.PI / 6),
                        ev._y - arrowSize * Math.sin(angle + Math.PI / 6)
                    );
                    context.closePath();
                    context.stroke();

                    img_update();
                    context.strokeStyle = canvasDrawColorCode;
                    context.lineWidth = canvasDrawBorderValue;
                }
            };
        };

        tools.text = function () {
            var tool = this;
            this.started = false;

            this.mousedown = function (ev) {
                if ($("#fontCheckbox").prop("checked")) {
                    var textInput = document.getElementById('textInput');
                    var rect = canvas.getBoundingClientRect();
                    var x = ev.clientX - rect.left + window.pageXOffset;
                    var y = ev.clientY - rect.top + window.pageYOffset;

                    textInput.style.left = x + 'px';
                    textInput.style.top = y + 'px';
                    textInput.style.display = 'block';
                    textInput.focus();

                    // Deactivate other tools
                    $("input[name='draw_tool_type']").prop("checked", false);
                    $("input[name='shape_tool_type']").prop("checked", false);
                    tool_select = 'text';
                    canvas.style.cursor = 'text';
                }
            };

            this.mousemove = function (ev) {
                // No action needed for mouse movement for the text tool.
            };

            this.mouseup = function (ev) {
                // No action needed for mouse release for the text tool.
            };
        };

        init();

        function resetDrawingsOfCanvas() {
            var canvasCursor = canvas.style.cursor; // Store the original cursor style

            contexto.clearRect(0, 0, canvas.width, canvas.height);
            contexto.drawImage(backgroundImage, 0, 0, canvaso.width, canvaso.height);
            tool = new tools.none(); // Assign an inactive tool
            tool_select = 'none';

            // Reset the selection of active tools
            $("input[name='draw_tool_type']").prop("checked", false);
            $("input[name='shape_tool_type']").prop("checked", false);
            canvas.style.cursor = canvasCursor;
        }

        // Event listener for the reset button
        document.querySelector("#img-reset-tool").addEventListener("click", resetDrawingsOfCanvas);
    }, false);
}

var canvasDrawColorCode = "#679BFF";
var canvasDrawShapeFillColorCode = "";
var canvasDrawShapeBorderColorCode = "#679BFF";
var canvasTextColorCode = "#679BFF";
var canvasDrawBorderValue = 1;
var canvasDrawShapeBorderValue = 1;
$("#canvasDrawColorChange").change(function () {
    console.log($(this).val());
    canvasDrawColorCode = $(this).val();
})

$("#canvasDrawShapeFillColorChange").change(function () {
    console.log($(this).val());
    canvasDrawShapeFillColorCode = $(this).val();
})

$("#canvasDrawShapeBorderColorChange").change(function () {
    console.log($(this).val());
    canvasDrawShapeBorderColorCode = $(this).val();
})

$("#canvasTextColorInput").change(function () {
    console.log($(this).val());
    canvasTextColorCode = $(this).val();
})

$("#draw-btn-border").change(function () {
    console.log($(this).val());
    canvasDrawBorderValue = parseInt($(this).val());
})

$("#draw-shape-border").change(function () {
    console.log($(this).val());
    canvasDrawShapeBorderValue = parseInt($(this).val());
})

function resetPointSpecify() {
    // bu fonksiyon zoom yapıldığında kırmızı noktaları temizlemek için oluşturuldu
    $(".point-area").remove()
    $(".report-item").hasClass("active") ? $(".report-item").removeClass("active") : null
    $(".report-item[data-item-name='all']").hasClass("active") ? null : $(".report-item[data-item-name='all']").addClass("active")
}

$("#calibrationTool img").click(function () {
    // mini toollarda calibration ikonuna tıklayınca modal açtırma
    $("#modalCalibration").addClass("active")
})

$("#startPutTwoPoint").click(function () {
    startPutTwoPointState = true;
    calibrationsState = true;
    circleMarkerCreate();
})

$("#calibrationSaveBtn").click(function () {
    $("#page-loading").show()
    if (drawed_objects.length > 0) {
        var ratio = $("#back-img").prop("naturalWidth") / $("#back-img").innerWidth();
        var coordinateFirst = [(drawed_objects[drawCounter - 2].layer._point.x * ratio), (drawed_objects[drawCounter - 2].layer._point.y * ratio)];
        var coordinateLast = [(drawed_objects[drawCounter - 1].layer._point.x * ratio), (drawed_objects[drawCounter - 1].layer._point.y * ratio)];
        let csrfToken = $('input[name=csrfmiddlewaretoken]').val()
        $.ajax({
            url: "/api/get-manuel-calibration",
            method: "POST",
            headers: {'X-CSRFToken': csrfToken},
            data: {
                'measure': parseInt($("#calibrationRange").val()),
                'first_coord': JSON.stringify(coordinateFirst),
                'second_coord': JSON.stringify(coordinateLast),
                'image_report_id': image_report_id,
            },
            success: function (res) {
                //kaydedildi popup yapılacak
                Swal.fire({
                    position: 'top-end',
                    icon: 'success',
                    title: 'Operation is success',
                    showConfirmButton: false,
                    timer: 1500
                  })
                $("#calibrationTool .dropdown-section").addClass("d-none");
                $("#calibrationTool .dropdown-section").removeClass("d-flex");
                drawed_objects[drawCounter - 1]["layer"].remove();
                drawed_objects[drawCounter - 1]["layer"] = "";
                drawed_objects[drawCounter - 2]["layer"].remove();
                drawed_objects[drawCounter - 2]["layer"] = "";
                calibrationsState = false;

                window.location.reload()
            }
        })
    }
})

$("#calibrationWarning .warning-close").click(()=>$("#calibrationWarning").remove())



