var center = [0, 0];
var polygon_state = false;
var polyline_state = false;
var rectangle_state = false;
var circleMarker_state = false;
var cizim_etiket_alan_control = false;
var editmode = false;
var dragObjectMove = false;
var drawingState = false;
var drawCounter = 0;
var edited_stroke_width;
var last_property_of_line;
var drawed_objects = [];
var marker_middle_icon = true
var last_selected_drawing;
var drawSplineMapList = [];
var impCrwEditModeStatus = false;
var splineCircleDrag = false;
var polylineCircleDrag = false;


var map = L.map('back-img-frame', {zoomControl: false}).setView(center, 10);
map.dragging.disable();
map.touchZoom.disable();
map.doubleClickZoom.disable();
map.scrollWheelZoom.disable();
map.boxZoom.disable();
map.keyboard.disable();

map.pm.disableGlobalDragMode();
// çizimleri kaydırma muhabbeti

var editableLayers = new L.FeatureGroup();
map.addLayer(editableLayers);
// yukarıdaki iki satır

var delete_sayac = 0;
var createAnno_sayac = 0;
var marking_type_dict = {
    "circlemarker": "point",
    "rectangle": "rectangle",
    "polygon": "polygon",
    "polyline": "polyline",
    "marker": "marker"
}

var myIcon = L.icon({
    iconUrl: '/static/images/anno.png',
    iconSize: [24, 24],
    iconAnchor: [22, 24]
});

var implantIcon = L.icon({
    iconUrl: '/static/img/teeth/tooth_implant_dental_36_1.png',
    iconSize: [100, 100]
});

var crownIcon = L.icon({
    iconUrl: '/static/img/crown-img.png',
    iconSize: [100, 100]
});

function modalOperationForDeleteCrown(crownImg) {
    // bu fonksyion tıklanan çöp kutusundaki crown img i siler
    console.log(crownImg)
    $("#deleteCrownImage").addClass("active").attr("data-crown-slug", crownImg)
    $(".leaflet-pane.leaflet-marker-pane i.delete-icon").remove()
}

function putIconForDeleteCrown(img) {
    let crownXCoord = img.offset().left + img.width() - $("#back-img-frame").offset().left - 15;
    let crownYCoord = img.offset().top + img.height() - $("#back-img-frame").offset().top - 15;

    $('.leaflet-pane.leaflet-marker-pane')
        .append(`<i class="fa-solid fa-trash delete-icon position-fixed cursor-pointer" style="top: ${crownYCoord}px; left: ${crownXCoord}px; z-index: 999;" onclick="modalOperationForDeleteCrown('${img.attr("data-slug")}')"></i>`);
}

$('#deleteCrownImage [data-modal-close="yes"]').click(function() {
    let slug = $("#deleteCrownImage").attr("data-crown-slug");
    let targetImg = $(`img[data-slug="${slug}"]`);
    if (targetImg.length > 0) {
        targetImg.remove();
        deleteImpCrown(slug);
    } else {
        console.error(`No img element found with data-slug "${slug}"`);
    }
})


map.on('draw:created', async function (e) {
    var type = e.layerType,
        layer = e.layer;
    if (type !== 'marker') {
        layer.setStyle({weight: 1});
    }
    e.class = "drawingLayersFor" + drawed_objects.length;
    var points = layer._latlngs;
    var geojson = layer.toGeoJSON();
    if (!$(".tq-butx").hasClass('current')) {
        $('.tq-butx').toggleClass("current");
        var last_selected_element = $('.last_selected_element')[0]
        if (last_selected_element) {
            $('#label-list2').prepend(last_selected_element)
            $('.last_selected_element').removeClass("last_selected_element")
        }
        $('.tq-butx').next(".s-click-dropdown").fadeToggle(100);
    }
    layer.on('mouseover', function () {
        layer.openPopup();
        try {
            layer.getPopup().options.autoPan = false;
            layer.getPopup().update();
        } catch (error) {

        }
    });
    layer.on('mouseout', function () {
        layer.closePopup();
    });
    if (type === 'circlemarker') {
        layer.setStyle({
            color: "#3388ff",
            fill: true,
            fillOpacity: 1,
            opacity: 1,
            radius: 1.5,
            repeatMode: false,
            stroke: true,
            weight: 1
        });
    }
    map.addLayer(layer);
    drawed_objects.push({
        "active_image_id": drawCounter,
        "user_id": 1,
        "marking_type": marking_type_dict[type],
        "cartesian_coordinates": {},
        "is_saved": false,
        "is_deleted": false,
        "is_edited": false,
        "is_move": false,
        "layer": layer,
        "label": {
            "id": NaN,
            "color": NaN,
            "name": NaN,
            "slug": NaN
        }
    })
    
    // cizim_sayac += 1;
    // cizim_etiket_alan_control = true;

    // $("#draw-polygon").hide();


    $(".draw-icon-item img.active").removeClass("active") // ui kodu -- çizim yapıldıktan sonra tıklanan minibar ikonundaki active liği kaldır

    if (type == 'marker') {
        impCrwnTotalEditFunc();
        saveImpCrown(layer);
    } else if (type == 'rectangle') {
        $(layer._path).attr({
            "stroke-dasharray": "5",
            "stroke": "#0057FF",
            "stroke-width": "2",
            "fill": "opacity"
        })
        let cornerXaxisOfPath = $(layer._path).offset().left + $(layer._path).get(0).getBBox().width // svg nin sağ alt köşesini bul x koordinatı
        let cornerYaxisOfPath = $(layer._path).offset().top + $(layer._path).get(0).getBBox().height // svg nin sağ alt köşesini bul y koordinatı
        let newCornerXaxisOfPath = findClosestPoint(cornerXaxisOfPath, cornerYaxisOfPath, parseCoordinates($(layer._path).attr("d")))[0] + $("#back-img-frame").offset().left
        let newCornerYaxisOfPath = findClosestPoint(cornerXaxisOfPath, cornerYaxisOfPath, parseCoordinates($(layer._path).attr("d")))[1] + $("#back-img-frame").offset().top

        let doctorAddCircle =
            `<div class="doctorAddedIllnessCircle" 
                style="left : ${newCornerXaxisOfPath}px; top : ${newCornerYaxisOfPath}px">
                <i class="fa-solid fa-plus text-light"></i>
            </div>`

        $("body").append(doctorAddCircle).css("left", $(layer._path).offset().left)

        $("#labeling-box").removeClass("d-none").addClass("d-inline-flex").css({
            "left": `${newCornerXaxisOfPath + 13}px`,
            "top": `${newCornerYaxisOfPath}px`
        })
        rectangle_state = false;

        $(".leaflet-interactive").last().attr({
            "data-slug": "none",
        });
        $(".leaflet-interactive").last().addClass("drawsElement");

        // doctor_drawings.push(layer);

    }else if (type === 'polygon') {
        // layer.setStyle({
        //     stroke: true,
        //     weight: 2,
        //     fillOpacity: 0.1,
        // });
        $(layer._path).attr({
            "stroke-dasharray": "5",
            "stroke": "#0057FF",
            "stroke-width": "2",
            "fill": "opacity"
        })
        let cornerXaxisOfPath = $(layer._path).offset().left + $(layer._path).get(0).getBBox().width // svg nin sağ alt köşesini bul x koordinatı
        let cornerYaxisOfPath = $(layer._path).offset().top + $(layer._path).get(0).getBBox().height // svg nin sağ alt köşesini bul y koordinatı
        let newCornerXaxisOfPath = findClosestPoint(cornerXaxisOfPath, cornerYaxisOfPath, parseCoordinates($(layer._path).attr("d")))[0] + $("#back-img-frame").offset().left
        let newCornerYaxisOfPath = findClosestPoint(cornerXaxisOfPath, cornerYaxisOfPath, parseCoordinates($(layer._path).attr("d")))[1] + $("#back-img-frame").offset().top

        let doctorAddCircle =
            `<div class="doctorAddedIllnessCircle" 
                style="left : ${newCornerXaxisOfPath}px; top : ${newCornerYaxisOfPath}px">
                <i class="fa-solid fa-plus text-light"></i>
            </div>`

        $("body").append(doctorAddCircle).css("left", $(layer._path).offset().left)
        console.log("d none kalkıyor")
        $("#labeling-box").removeClass("d-none").addClass("d-inline-flex").css({
            "left": `${newCornerXaxisOfPath + 13}px`,
            "top": `${newCornerYaxisOfPath}px`
        })

        polygon_state = false;

        $(".leaflet-interactive").last().attr({
            "data-slug": "none",
        });
        $(".leaflet-interactive").last().addClass("drawsElement");
    }


    if (type === 'marker') {
        // layer._icon.id = "marker" + drawCounter;
    }

    drawingState = true;
    drawCounter += 1;
    // map.pm.enableGlobalDragMode();

    // $("#draw-rectangle").hide();
    $("#draw-circle").hide();
    $("#draw-polyline").hide();
    if (drawCounter % 2 == 0) {
        $("#calibrationTool .dropdown-section").removeClass("d-none");
        $("#calibrationTool .dropdown-section").addClass("d-flex");
    }

});

function saveImpCrown(layer) {
    var form = new FormData();
    if(layer._icon.src.indexOf("implant") > -1) {
        var item_type = "implant";
        var icon_id = "1";
    }else {
        var item_type = "crown";
        var icon_id = layer._icon.src.split("-")[2].split(".")[0];
    }
    var dimension = Number(layer._icon.style.width.split("px")[0]);
    form.append("item_type", item_type);
    form.append("coordinate", JSON.stringify([map.latLngToLayerPoint([layer._latlng.lat, layer._latlng.lng]).x / g_original_shape.width_rate,map.latLngToLayerPoint([layer._latlng.lat, layer._latlng.lng]).y  / g_original_shape.height_rate]));
    form.append("dimension", dimension);
    form.append("rotate", "0");
    form.append("icon_id", icon_id);
    form.append("image_report_id", image_report_id);
    form.append("original_shape", g_original_shape.width_rate);

    var settings = {
        "url": "/api/save-implant-or-crown",
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
        $(".leaflet-interactive").last().attr({
            "data-slug": JSON.parse(response).response_dict.slug,
        });
    });
}

function deleteImpCrown (slug) {
    var form = new FormData();
    form.append("slug", slug);
    form.append("image_report_id", image_report_id);
    var settings = {
        "url": "/api/delete-implant-or-crown",
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
    });
}

function updateImpCrown(slug) {
    $("#page-loading").show();
    var layer;
    var layerSelect = $.map(map._layers, function(value,key) {
        if(value._icon) {
            if($(value._icon).attr("data-slug") == slug) {
                layer = value;
            }
        }
    });
    var form = new FormData();
    var img = $(`img[data-slug="${slug}"]`);
    var dimension = Number($(img).css("width").split("px")[0]);
    form.append("slug", slug);
    form.append("image_report_id", image_report_id);
    form.append("coordinate", JSON.stringify([map.latLngToLayerPoint([layer._latlng.lat, layer._latlng.lng]).x / g_original_shape.width_rate,map.latLngToLayerPoint([layer._latlng.lat, layer._latlng.lng]).y  / g_original_shape.height_rate]));
    form.append("dimension", dimension);
    form.append("rotate", parseInt($(".active_impcrw_img")[0].style.transform.split("rotate")[1].split("(")[1].split("deg")[0]));
    form.append("original_shape", g_original_shape.width_rate);
    var settings = {
        "url": "/api/save-implant-or-crown",
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
        $("#page-loading").hide();
    });
}

function impCrwnTotalEditFunc() {
    $(".leaflet-marker-pane img").removeClass("active_impcrw_img");
        // $(".leaflet-marker-pane img").last().addClass("active_impcrw_img");
        $(".leaflet-marker-pane img").click(function (event) {
            $(".leaflet-marker-pane img").removeClass("active_impcrw_img");
            $(this).addClass("active_impcrw_img");
            impCrwEditModeStatus = true;
            map.pm.enableGlobalDragMode();

            $(".draw-icon-item img.active") ? $(".draw-icon-item img.active").removeClass("active") : null
            $("#implantCrownDropdown .dropdown-section").addClass("d-flex");

            putIconForDeleteCrown($(event.target)) // delete ikonu yerleştir
            setImpCrwVal(this);          
        });
        $(".leaflet-marker-pane img").mousedown((event)=>{
            if($("#implantCrownDropdown .dropdown-section").hasClass("d-flex")) {
                $("#implantCrownDropdown .dropdown-section").removeClass("d-flex")
            }
            $(".leaflet-pane.leaflet-marker-pane i.delete-icon").remove()
            if($(event.target).attr("src").split("/").pop().includes("implant")) {
                // implant taşıması yapılacak
                $("[data-put-icon-type='implant'] img.moving-img").show()
            } else {
                $("[data-put-icon-type='crown'] img.moving-img").show()
                // crown taşıması yapılacak
            }
            
        })
        $(".leaflet-marker-pane img").mouseup(function () {
            // var thisMarker = drawed_objects[($(this)[0].id.split("marker")[1])];
            $("[data-put-icon-type] img.moving-img").hide()
            if(!$("#implantCrownDropdown .dropdown-section").hasClass("d-flex")) {
                $("#implantCrownDropdown .dropdown-section").addClass("d-flex")
            }
        });
        $(".leaflet-pane.leaflet-marker-pane i.delete-icon").remove()
}

// var dragging = false;
// var target;
var degree = 0;
//
// $(document).mouseup(function () {
//     dragging = false
// })
// $(document).mousemove(function (e) {
//     if (dragging) {
//         var mouse_x = e.pageX;
//         var mouse_y = e.pageY;
//         var radians = Math.atan2(mouse_x - 10, mouse_y - 10);
//         degree = ((radians * (180 / Math.PI) * -1) + 90) * 90;
//         var nowTransform = $(target)[0].style.transform.split("rotate")[0];
//         $(target).css('transform', nowTransform + " rotate(" + degree + "deg)");
//         $(target).css('-moz-transform-origin', '50% 50%');
//         $(target).css('-webkit-transform-origin', '50% 50%');
//         $(target).css('-o-transform-origin', '50% 50%');
//         $(target).css('-ms-transform-origin', '50% 50%');
//     }
// })
//
// var startX, startY, startWidth, startHeight;
//
// function initDrag(e) {
//     startX = e.clientX;
//     startY = e.clientY;
//     startWidth = parseInt(document.defaultView.getComputedStyle($(resizeMarkerElement)[0]).width, 10);
//     startHeight = parseInt(document.defaultView.getComputedStyle($(resizeMarkerElement)[0]).height, 10);
//     document.documentElement.addEventListener('mousemove', doDrag, false);
//     document.documentElement.addEventListener('mouseup', stopDrag, false);
//     let cornerXaxisOfPath = $(resizeMarkerElement).offset().left + $(resizeMarkerElement).width() - 30 // svg nin sağ alt köşesini bul x koordinatı
//     var cornerXaxisOfPathRotate = $(resizeMarkerElement).offset().left + 30
//     let cornerYaxisOfPath = $(resizeMarkerElement).offset().top + $(resizeMarkerElement).height() // svg nin sağ alt köşesini bul y koordinatı
//     var thisIcon = resizeMarkerIcon;
//     $(thisIcon).parent().css("left", cornerXaxisOfPath);
//     $(thisIcon).parent().css("top", cornerYaxisOfPath);
//     $("#rotate" + $(thisIcon)[0].id.split("resize")[1]).parent().css("top", cornerYaxisOfPath);
// }
//
// function doDrag(e) {
//     $(resizeMarkerElement)[0].style.width = (startWidth + e.clientX - startX) + 'px';
//     $(resizeMarkerElement)[0].style.height = (startHeight + e.clientY - startY) + 'px';
//     let cornerXaxisOfPath = $(resizeMarkerElement).offset().left + $(resizeMarkerElement).width() - 30 // svg nin sağ alt köşesini bul x koordinatı
//     var cornerXaxisOfPathRotate = $(resizeMarkerElement).offset().left + 30
//     let cornerYaxisOfPath = $(resizeMarkerElement).offset().top + $(resizeMarkerElement).height() // svg nin sağ alt köşesini bul y koordinatı
//     var thisIcon = resizeMarkerIcon;
//     $(thisIcon).parent().css("left", cornerXaxisOfPath);
//     $(thisIcon).parent().css("top", cornerYaxisOfPath);
//     $("#rotate" + $(thisIcon)[0].id.split("resize")[1]).parent().css("top", cornerYaxisOfPath);
// }
//
// function stopDrag(e) {
//     document.documentElement.removeEventListener('mousemove', doDrag, false);
//     document.documentElement.removeEventListener('mouseup', stopDrag, false);
//     let cornerXaxisOfPath = $(resizeMarkerElement).offset().left + $(resizeMarkerElement).width() - 30 // svg nin sağ alt köşesini bul x koordinatı
//     var cornerXaxisOfPathRotate = $(resizeMarkerElement).offset().left + 30
//     let cornerYaxisOfPath = $(resizeMarkerElement).offset().top + $(resizeMarkerElement).height() // svg nin sağ alt köşesini bul y koordinatı
//     var thisIcon = resizeMarkerIcon;
//     $(thisIcon).parent().css("left", cornerXaxisOfPath);
//     $(thisIcon).parent().css("top", cornerYaxisOfPath);
//     $("#rotate" + $(thisIcon)[0].id.split("resize")[1]).parent().css("top", cornerYaxisOfPath);
// }

var cbs;
var loading_status = false;
var resizeMarkerIcon;
var resizeMarkerElement;
var marker_edit_mode = false;
var nowTransformRotate;
var startPutTwoPointState = false;
var calibrationsState = false;
$(".leaflet-map-pane").on('mousedown', function (e) {
    try {
        loading_status = false;
        if (e.target.tagName == 'IMG') {
        } else {
            if (drawSplineMapList.length > 0) {
                for (var i = 0; i < drawSplineMapList.length; i++) {
                    drawSplineMapList[i][0].bringToBack()
                }
            } else {
                leaflet_line = $("path.leaflet-pm-draggable")
                leaflet_line[leaflet_line.length - 1].attributes['stroke-width'].value = edited_stroke_width
                class_name = ""
                var paths = e.target.parentElement.parentElement.children[2].children[0].children[0].children;
                var es = e.target.parentElement.children
                var x = e.target.style.transform.substr(12).split("px")[0]
                var y = e.target.style.transform.substr(20).split("px")[0]
                var point_coord = x + " " + y
                var moveState = false;
                for (i = 0; i < es.length; i++) {
                    var x = es[i]._leaflet_pos.x
                    var y = es[i]._leaflet_pos.y
                    var point_coord = (x - 2) + " " + (y - 2)
                    if (!moveState) {
                        for (var j = 0; j < paths.length; j++) {
                            var d_stra = paths[j].attributes.d.value
                            if (d_stra.includes(point_coord)) {
                                drawed_objects[parseInt(paths[j].classList[1].split("etiketdiv")[1]) - 1]["is_move"] = true;
                                label_indice = parseInt(paths[j].classList[1].split("etiketdiv")[1]);
                                //console.log("2****", drawed_objects[label_indice - 1], "move true oldu *****")
                                drawed_objects[label_indice - 1]["layer"].closePopup();
                                moveState = true;
                                break;
                            }
                        }
                    }
                }
            }

        }

    } catch (_) {
        //console.log(_);
        //console.log("edit yok");
        $("#loading").hide();
        // label_indice = parseInt(e.target.classList[1].split("etiketdiv")[1]);
    }
    // dragObjectMove = true;
    // $("#back-img-frame").draggable({disabled: true});
    $("path").on('mousedown', function (e) {
        if (drawSplineMapList.length > 0) {
            for (var i = 0; i < drawSplineMapList.length; i++) {
                drawSplineMapList[i][0].bringToBack()
            }
        } else {
            if (e.target.className.baseVal) {
                var targetClassList = e.target.className.baseVal.split(" ");
                for (var i = 0; i < targetClassList.length; i++) {
                    if (targetClassList[1].split("etiketdiv").length > 1) {
                        label_indice = targetClassList[1].split("etiketdiv")[1];
                    }
                }
            }
            // drawed_objects[label_indice - 1]["layer"].closePopup();
            loading_status = false;
            $.each($('.etiketdivclass').find('label').find('input'), function (i, item) {
                $(item)[0].checked = false;
            })

            $('#etiketdiv' + label_indice).find('label').find('input')[0].checked = true;
            // try {
            //     class_name = ".etiketdiv" + label_indice
            //     $(class_name).on('moveend', function () {
            //         // label_indice = 0;
            //         if ($('#place').hasClass('active')) {
            //             // finded_status = false;
            //             if (!loading_status) {
            //                 loading_status = true
            //                 if (drawed_objects[label_indice - 1]["is_move"] === true) {
            //                     drawed_objects[label_indice - 1]["is_move"] = false;
            //                     //console.log("3****", drawed_objects[j], "move false oldu *****")
            //                     // finded_status = true
            //                     var label_db_id = drawed_objects[label_indice - 1]["label"]["id"];
            //                     $.ajax({
            //                         url: "/api/editimagelabel/",
            //                         method: "GET",
            //                         data: {
            //                             'image_label_id': drawed_objects[label_indice - 1]["image_label_id"],
            //                             'i': label_indice,
            //                         },
            //                         success: function (res) {
            //                             var moved_right_id = res["i"]
            //                             kaydet(label_db_id, false, moved_right_id);
            //                             loading_status = false
            //                             //console.log("editlendi--------------")
            //                             // loading_hide();
            //                         }
            //                     })
            //                 }
            //             }
            //         }
            //     });
            // } catch (_) {
            //     console.error(_)
            // }
        }
    });
});
$("#sli1").on('mousedown', function (e) {
    loading_status = false
    if (label_indice == 0) {
        dragObjectMove = false;
    }
});
$("#leaflet-pane").on('mousedown', function (e) {
    loading_status = false;
});

$(".leaflet-map-pane").on('mousemove', function (e) {
    loading_status = false;
});
$("#sli1").on('mouseup', function (e) {
    // label_indice = 0;
    if (dragObjectMove) {
        dragObjectMove = false;
        // $("#loading").show();
        // $("#loading").css('opacity', 0.5)
        finded_status = false;
        if (!loading_status) {
            loading_status = true
            if (drawed_objects[label_indice - 1]["is_move"] === true) {
                drawed_objects[label_indice - 1]["is_move"] = false;
                //console.log("4****", drawed_objects[label_indice - 1], "move false oldu *****")
                finded_status = true
                var label_db_id = drawed_objects[label_indice - 1]["label"]["id"];
                $.ajax({
                    url: "/api/editimagelabel/",
                    method: "GET",
                    data: {
                        'image_label_id': drawed_objects[label_indice - 1]["image_label_id"],
                        'i': label_indice,
                    },
                    success: function (res) {
                        var moved_right_id = res["i"]
                        kaydet(label_db_id, false, moved_right_id);
                        //console.log("editlendi1--------------")
                        loading_status = false
                        // loading_hide();
                    }
                })
            }
        }
    }
});

$(".leaflet-map-pane").on('mouseup', function (e) {
    if (startPutTwoPointState) {
        circleMarkerCreate();
        startPutTwoPointState = false;
    }
    if ($("#editMode").prop("checked")) {
        try {
            spline_list_latlng = [];

            var updateCircleMapPath = $.map(map._layers, function(value) {
                if(e.target == value._path) {
                    $("#page-loading").show();
                    updateLateralPoints(e.target.dataset.circleName,JSON.stringify([value._point.x / g_original_shape.width_rate,value._point.y / g_original_shape.height_rate]));
                }
            });

            // for (var i = 0; i < spline_list_name.length; i++) {
            //     for (var j = 0; j < spline_list_name[i].length; j++) {
            //         if (e.target.getAttribute("data-circle-name") == spline_list_name[i][j]) {
            //             for (var k = 0; k < drawSplineMapList.length; k++) {
            //                 for (var p = 0; p < drawSplineMapList[k].length; p++) {
            //                     drawSplineMapList[k][p].removeFrom(map);
            //                 }
            //             }
            //             splineCircleDrag = true;
            //             pushSplines(true);
            //             break;
            //         }
            //     }
            // }
            
        } catch (e) {
            console.log(e);
        }

    }

    if ($("#implantCrownDropdown .dropdown-section").hasClass("d-flex") && $(".active_impcrw_img").length > 0) {
        updateImpCrown($(".active_impcrw_img").attr("data-slug"));
    }
});

try {
    var polygonDrawer = new L.Draw.Polygon(map);
    var polylineDrawer = new L.Draw.Polyline(map);
    var rectangleDrawer = new L.Draw.Rectangle(map);
    var circleMarkerDrawer = new L.Draw.CircleMarker(map, {radius: 4, fillOpacity: 1});
    var markerImplantDrawer = new L.Draw.Marker(map, {icon: implantIcon});
    var markerCrownDrawer = new L.Draw.Marker(map, {icon: crownIcon});
} catch (e) {
    console.log(e)
}

function polygonCreate() {
    map.pm.disableGlobalEditMode();
    polygonDrawer = new L.Draw.Polygon(map);
    polygonDrawer.enable();
}

function polylineCreate() {
    map.pm.disableGlobalEditMode();
    polylineDrawer = new L.Draw.Polyline(map);
    polylineDrawer.enable();
}

function rectangleCreate() {
    map.pm.disableGlobalEditMode();
    rectangleDrawer = new L.Draw.Rectangle(map);
    rectangleDrawer.enable();
}

function circleMarkerCreate() {
    map.pm.disableGlobalEditMode();
    circleMarkerDrawer = new L.Draw.CircleMarker(map, {radius: 1, fillOpacity: 0.4});
    circleMarkerDrawer.enable();
}

function markerImplantCreate() {
    map.pm.disableGlobalEditMode();
    markerImplantDrawer = new L.Draw.Marker(map, {icon: implantIcon});
    markerImplantDrawer.enable();
}

function markerCrownCreate() {
    map.pm.disableGlobalEditMode();
    markerCrownDrawer = new L.Draw.Marker(map, {icon: crownIcon});
    markerCrownDrawer.enable();
}


function get_comment_annotations(force = false) {
    if (active_image_id === -1 || active_image_id === "") {
        setTimeout(get_comment_annotations, 500)
    } else {
        $.ajax({
            url: "/api/getCommentAnnotationsByImage/",
            method: "GET",
            data: {
                'image_id': active_image_id,
                'user_id': user_id,
            },
            success: function (res) {
                results = res['results']
                // // console.log(results)
                for (let i = 0; i < results.length; i++) {
                    //// console.log(results[i])
                    anno.addAnnotation(results[i])
                    createAnno_sayac += 1
                    var last_t = $('g[data-id="' + results[i].id + '"]');
                    var a = parseInt(last_t.children().attr("width")) / 2;
                    var b = parseInt(last_t.children().attr("height")) / 2;
                    var c = parseInt(last_t.children().attr("x")) + a - 12;
                    var d = parseInt(last_t.children().attr("y")) + b - 16;
                    $('.a9s-annotationlayer').append('<svg class="anno-img" data-comment-id="' + results[i].id + '" width="200" height="200" xmlns="http://www.w3.org/2000/svg" x="' + c + '" y="' + d + '"><g><path stroke="#ffffff" d="M12 1.02901C5.38298 1.02901 0 5.50201 0 11C0 13.825 1.44398 16.498 3.97898 18.393L2.052 22.247C1.95 22.45 1.99898 22.696 2.169 22.846C2.26298 22.9291 2.37998 22.9711 2.499 22.9711C2.59598 22.9711 2.69302 22.9431 2.778 22.8861L6.99502 20.0551C8.58403 20.662 10.267 20.9701 12 20.9701C18.617 20.9701 24 16.4971 24 10.999C24 5.50102 18.617 1.02901 12 1.02901V1.02901Z" fill="#FF0000"/></path><text class="deneme-text" x="17" y="26" font-family="Verdana" font-size="15" fill="white"></text></g></svg>');
                }
            }
        })
    }

}

var anno;

function annoCreate() {
    $(".a9s-annotationlayer").addClass("cursor-cross");
    $(".a9s-annotationlayer").css("display", "");
    $(".r6o-editor").css("display", "");
    (function () {
        anno.on('createAnnotation', function (annotation) {
            createAnno_sayac += 1;
            var last_t = $('g[data-id="' + annotation.id + '"]');
            var a = parseInt(last_t.children().attr("width")) / 2;
            var b = parseInt(last_t.children().attr("height")) / 2;
            var c = parseInt(last_t.children().attr("x")) + a - 12;
            var d = parseInt(last_t.children().attr("y")) + b - 16;
            $('.a9s-annotationlayer').append('<svg class="anno-img" data-comment-id="' + annotation.id + '" width="200" height="200" xmlns="http://www.w3.org/2000/svg" x="' + c + '" y="' + d + '"><g><path stroke="#ffffff" d="M12 1.02901C5.38298 1.02901 0 5.50201 0 11C0 13.825 1.44398 16.498 3.97898 18.393L2.052 22.247C1.95 22.45 1.99898 22.696 2.169 22.846C2.26298 22.9291 2.37998 22.9711 2.499 22.9711C2.59598 22.9711 2.69302 22.9431 2.778 22.8861L6.99502 20.0551C8.58403 20.662 10.267 20.9701 12 20.9701C18.617 20.9701 24 16.4971 24 10.999C24 5.50102 18.617 1.02901 12 1.02901V1.02901Z" fill="#FF0000"/></path><text class="deneme-text" x="17" y="26" font-family="Verdana" font-size="15" fill="white"></text></g></svg>');
            save_comment_annotations();
        });
        anno.on('deleteAnnotation', function (annotation) {
            $('svg[data-comment-id="' + annotation.id + '"]').remove();
            save_comment_annotations();
        });
        anno.on('updateAnnotation', function (annotation) {
            //// console.log("update");
            save_comment_annotations();
        })
        anno.on('addAnnotation', function (annotation) {
            //// console.log("add");
            save_comment_annotations();
        })

    })()
}

function annoClose() {
    $(".a9s-annotationlayer").removeClass("cursor-cross");
    $(".a9s-annotationlayer").css("display", "none");
    $(".r6o-editor").css("display", "none");
}

/* Draw */
$(document).ready(function () {
    try {
        // get_comment_annotations();
        polygonDrawer = new L.Draw.Polygon(map);
        polylineDrawer = new L.Draw.Polyline(map);
        rectangleDrawer = new L.Draw.Rectangle(map);
        circleMarkerDrawer = new L.Draw.CircleMarker(map, {radius: 4, fillOpacity: 1});
        markerDrawer = new L.Draw.Marker(map, {icon: implantIcon});
        markerImplantDrawer = new L.Draw.Marker(map, {icon: implantIcon});
        markerCrownDrawer = new L.Draw.Marker(map, {icon: crownIcon});

        $("#draw-polygon").click(function () {
            last_clicked_tool = $("#draw-polygon")
            //console.log("@@@@@@@@@@@@@@@@@@çizim yapılacak!!")
            annoClose();
            //$("#back-img-frame").draggable({disabled: true});
            rectangleDrawer.disable();
            circleMarkerDrawer.disable();
            polylineDrawer.disable();
            polygon_state = true;
            polyline_state = false;
            rectangle_state = false;
            circleMarker_state = false;
            polygonDrawer.enable();
            $("#back-img-frame").css("cursor", "crosshair!important")
        });

        $("#draw-polyline").click(function () {
            last_clicked_tool = $("#draw-polyline")
            annoClose();
            //$("#back-img-frame").draggable({disabled: true});
            rectangleDrawer.disable();
            circleMarkerDrawer.disable();
            polygonDrawer.disable();
            markerImplantDrawer.disable();
            markerCrownDrawer.disable();
            polyline_state = true;
            polygon_state = false;
            rectangle_state = false;
            circleMarker_state = false;
            polylineDrawer.enable();
        });

        $("#draw-rectangle").click(function () {
            annoClose();
            //$("#back-img-frame").draggable({disabled: true});
            last_clicked_tool = $("#draw-rectangle")
            polygonDrawer.disable();
            circleMarkerDrawer.disable();
            polylineDrawer.disable();
            markerImplantDrawer.disable();
            markerCrownDrawer.disable();
            polygon_state = false;
            rectangle_state = true;
            polyline_state = false;
            circleMarker_state = false;
            rectangleDrawer.enable();
        });

        $("#draw-circle").click(function () {
            annoClose();
            last_clicked_tool = $("#draw-circle")
            //$("#back-img-frame").draggable({disabled: true});
            rectangleDrawer.disable();
            polygonDrawer.disable();
            polylineDrawer.disable();
            markerImplantDrawer.disable();
            markerCrownDrawer.disable();
            polygon_state = false;
            rectangle_state = false;
            polyline_state = false;
            circleMarker_state = true;
            circleMarkerDrawer.enable();
        });

        $("#draw-marker").click(function () {
            last_clicked_tool = $("#draw-marker")
            //$("#back-img-frame").draggable({disabled: true});
            rectangleDrawer.disable();
            polygonDrawer.disable();
            circleMarkerDrawer.disable();
            polylineDrawer.disable();
            markerImplantDrawer.disable();
            markerCrownDrawer.disable();
            polygon_state = false;
            polyline_state = false;
            rectangle_state = false;
            circleMarker_state = false;
            annoCreate();
            $('.ul-fix-2 li:nth-child(3)').click();
            $("#back-img-frame-image").css("top", "0px");
            $("#back-img-frame-image").css("left", "0px");
        });

        $("#draw-implant").click(function () {
            last_clicked_tool = $("#draw-implant")
            //$("#back-img-frame").draggable({disabled: true});
            rectangleDrawer.disable();
            polygonDrawer.disable();
            circleMarkerDrawer.disable();
            polylineDrawer.disable();
            markerCrownDrawer.disable();
            polygon_state = false;
            polyline_state = false;
            rectangle_state = false;
            circleMarker_state = false;
            markerImplantDrawer.enable();
            resetImpCrwVal();
        });

        $(".draw-crown-img").click(function () {
            resetImpCrwVal();
            let targetCrownImgSrc = $(this).find("img").attr("src") //tıklanan crown un src  unu al
            $(".draw-crown-img").removeClass("active") // active olan ı temizle
            $(this).addClass("active") // tıklanana aktif class koy
            $("img#draw-crown").attr("src", targetCrownImgSrc) // implant yanındaki crownun resmini değiştir
            $(".tooth-menu-container").css("display", "none") // paneli kapat
            setTimeout(function() {
                $(".tooth-menu-container").css("display", "") // display none sil ki tekrardan üzerine gelebilsin
            },500)
            $("#implantCrownDropdown .dropdown-section").addClass("d-flex")
            last_clicked_tool = $("#draw-crown")
            crownIcon.options.iconUrl = $("#draw-crown").attr("src");
            crownIcon.options.iconSize[0] = parseInt($("#dimension-btn").attr("value"));
            crownIcon.options.iconSize[1] = parseInt($("#dimension-btn").attr("value"));
            //$("#back-img-frame").draggable({disabled: true});
            rectangleDrawer.disable();
            polygonDrawer.disable();
            circleMarkerDrawer.disable();
            polylineDrawer.disable();
            markerImplantDrawer.disable();
            polygon_state = false;
            polyline_state = false;
            rectangle_state = false;
            circleMarker_state = false;
            markerCrownDrawer.enable();
        });

        $("#place").click(function () {
            annoClose();
            map.pm.disableGlobalEditMode();
            map.pm.enableGlobalDragMode();
            circleMarkerDrawer.enable();
            rectangleDrawer.enable();
            polygonDrawer.enable();
            polylineDrawer.enable();
            rectangleDrawer.disable();
            polygonDrawer.disable();
            polylineDrawer.disable();
            circleMarkerDrawer.disable();
            polygon_state = false;
            polyline_state = false;
            rectangle_state = false;
            circleMarker_state = false;
            cizim_etiket_alan_control = false;
        });

        $("#place2").click(function () {
            annoClose();
            map.pm.disableGlobalEditMode();
            map.pm.enableGlobalDragMode();
            circleMarkerDrawer.enable();
            rectangleDrawer.enable();
            polygonDrawer.enable();
            polylineDrawer.enable();
            rectangleDrawer.disable();
            polygonDrawer.disable();
            polylineDrawer.disable();
            circleMarkerDrawer.disable();
            polygon_state = false;
            polyline_state = false;
            rectangle_state = false;
            circleMarker_state = false;
            cizim_etiket_alan_control = false;
        });
    } catch (e) {
        console.log(e);
    }
});

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})

function rgbToHex(color) {
    color = "" + color;
    if (!color || color.indexOf("rgb") < 0) {
        return;
    }
    if (color.charAt(0) == "#") {
        return color;
    }
    var nums = /(.*?)rgb\((\d+),\s*(\d+),\s*(\d+)\)/i.exec(color),
        r = parseInt(nums[2], 10).toString(16),
        g = parseInt(nums[3], 10).toString(16),
        b = parseInt(nums[4], 10).toString(16);

    return "#" + (
        (r.length == 1 ? "0" + r : r) +
        (g.length == 1 ? "0" + g : g) +
        (b.length == 1 ? "0" + b : b)
    );
}

var cizim_sayac = 0;
var popupErrorId;

function kaydet(label_db_id, a, saveId = 0) {
    if (saveId == 0) {
        if (drawingState) {
            //console.log("603")
            $(".list-is-clear").css('background-image', 'none');
            $(".list-is-clear").css('marginTop', '0px');
            $(".lic-text").css('display', 'none');
            $(".es-content").css('display', 'block');
            $(".es-content").append('<div class="row right-lbl-row" id="eklenenEtiket"><div class="col-12 etiketdivclass" id="etiketdiv" onmouseover="hoverOn(this.id)" onmouseout="hoverOff(this.id)"><label class="label-control4"><input class="label-do-' + String(drawCounter) + ' label-do-id-' + label_db_id + '" type="checkbox" id="etiket-check" onclick="layerSelect(this.id)"><span class="border-one background-one right-span" id="span-etiket"></span><span onclick="delete_selected_labeled(this,this.parentElement.firstChild.id,this.parentElement.firstChild.id,$(this).parent().parent().parent())" class="tq-color" id="right-span"></span><i src="eye.png" id="visibleImage" class="eyeImg" width="25" height="16" onclick="visibleOff(this.parentElement.firstChild.id,$(this).parent().parent().parent(),this)"></i><i src="delete.png" class="deleteImg" id="delImg" width="20" height="20" onclick="removeLayer(this.parentElement.firstChild.id,$(this).parent().parent().parent(),false)"></i><i src="edit.png" id="editImage" class="editImg" width="24" height="24" onclick="editLayer($(this).parent())"></i></label></div></div>');
            var e = document.getElementById("span-etiket");
            e.id = "span-etiket" + drawCounter;
            var a_id = a.id;
            e.textContent = $("#color" + label_db_id).parent().html().split('</span>')[1];
            var textcontent = e.textContent;
            var etk = document.getElementById("eklenenEtiket");
            etk.id = "eklenenEtiket" + drawCounter;
            var etkdiv = document.getElementById("etiketdiv");
            etkdiv.id = "etiketdiv" + drawCounter;
            var g = document.getElementById("etiket-check");
            g.id = "etiket-check" + drawCounter;
            var f = document.getElementById("right-span");
            f.id = "right-span" + drawCounter;
            $(f).css("left", "4px").css("bottom", "27px").css("padding", "10px 10px 5px 7px").css("background", rgbToHex(colorEl));
            if (a.className.includes('point')) {
                drawed_objects[drawCounter - 1]["layer"].setStyle({
                    fillColor: rgbToHex(colorEl),
                    color: "#000000"
                });
            } else {
                drawed_objects[drawCounter - 1]["layer"].setStyle({color: rgbToHex(colorEl)});
            }
            drawed_objects[drawCounter - 1]["label"]["id"] = label_db_id
            drawed_objects[drawCounter - 1]["label"]["color"] = rgbToHex(colorEl)
            drawed_objects[drawCounter - 1]["label"]["name"] = textcontent
            is_save_status = false;
            $("#draw-polygon").show()
            $("#draw-polyline").show()
            $("#draw-rectangle").show()
            $("#draw-circle").show()
            //console.log("test1------------------------------------------------------")
            drawed_objects[drawCounter - 1]["layer"].bindPopup(drawed_objects[drawCounter - 1]["label"]["name"]);
            //console.log("test2------------------------------------------------------")
            $(".leaflet-zoom-animated g path:last-child").addClass(etkdiv.id);
            drawingState = false;
            save_coordinates();
        } else {
            //console.log("646")
            alert("Ã‡izim YapmadÄ±nÄ±z!");
            $('.tq-butx').removeClass("current");
            $('.tq-butx').next(".s-click-dropdown").fadeOut(100);
        }
    } else {
        //console.log("652")
        $(".list-is-clear").css('background-image', 'none');
        $(".list-is-clear").css('marginTop', '0px');
        $(".lic-text").css('display', 'none');
        $(".es-content").css('display', 'block');
        if (drawed_objects[saveId - 1]["is_move"] === false && a !== false) {
            $(f).css("left", "4px").css("bottom", "27px").css("padding", "10px 10px 5px 7px").css("background", rgbToHex(colorEl));
            if (a.className.includes('point')) {
                drawed_objects[saveId - 1]["layer"].setStyle({fillColor: rgbToHex(colorEl), color: "#000000"});
            } else {
                drawed_objects[saveId - 1]["layer"].setStyle({color: rgbToHex(colorEl)});
            }
            drawed_objects[saveId - 1]["label"]["id"] = label_db_id
            drawed_objects[saveId - 1]["label"]["color"] = rgbToHex(colorEl)
            drawed_objects[saveId - 1]["label"]["name"] = $(a).parent()[0].textContent.split(/\n/)[2].split("  ")[22];
            is_save_status = false;
            save_coordinates(false, saveId)
            //console.log("test3------------------------------------------------------")
            drawed_objects[saveId - 1]["layer"].bindPopup(drawed_objects[saveId - 1]["label"]["name"]);
            //console.log("test4------------------------------------------------------")
            popupErrorId = saveId;
        } else {
            is_save_status = false;
            save_coordinates(false, saveId)
            //console.log("test4------------------------------------------------------")
            //console.log(drawed_objects)
            //console.log(saveId)
            //console.log(drawed_objects[saveId - 1])
            //console.log(drawed_objects[saveId - 1]["layer"])
            try {
                drawed_objects[saveId - 1]["layer"].bindPopup(drawed_objects[saveId - 1]["label"]["name"]);
            } catch (exceptionVar) {
                console.log(exceptionVar)
            }
            //console.log("test5------------------------------------------------------")
        }
        $("#draw-polygon").show()
        $("#draw-polyline").show()
        $("#draw-rectangle").show()
        $("#draw-circle").show()
    }
};

var popupErrorContent;

function layerSelect(id) {
    //console.log("698")
    var textcontent = $("#" + id).parent().find("span")[0].textContent;
    popupErrorContent = textcontent;
    var i = id.length;
    var j = id.split('check')[1];
    var curEl = document.getElementById(id);
    var curColor = $(curEl).parent().find('.tq-color')[0].style.background;
    var cbs = document.getElementsByClassName("etiketdivclass");
    $("#place").click();
    $("#place2").click();
    for (var y = 0; y < cbs.length; y++) {
        $(cbs[y]).find('label').find('input')[0].checked = false;
    }
    for (var x = 0; x < drawed_objects.length; x++) {
        if (drawed_objects[x]["layer"] !== "") { // TODO: is_deleted == false olacak
            drawed_objects[x]["layer"].setStyle({weight: 1});
            drawed_objects[x]["layer"].pm.disable();
            editmode = false;
        }
    }
    curEl.checked = true;
    if (curEl.checked == true) {
        if (drawed_objects[j - 1]["layer"].options.color == "#000000") {
            drawed_objects[j - 1]["layer"]['_path'].attributes["stroke-width"].value = "2";
        } else {
            last_selected_drawing = drawed_objects[j - 1]["layer"]
            //console.log(last_selected_drawing)
            drawed_objects[j - 1]["layer"].setStyle({weight: 3});
            if (visibilityChange == true) {
                drawed_objects[j - 1]["layer"].pm.enable({
                    allowSelfIntersection: true,
                    snappable: false
                });
                editmode = true;
            }
        }
    } else {
        drawed_objects[j - 1]["layer"].setStyle({weight: 1});
        drawed_objects[j - 1]["layer"].pm.disable();
        if (visibilityChange == true) {
            drawed_objects[j - 1]["layer"].pm.enable({
                allowSelfIntersection: true,
                snappable: false
            });
            editmode = false;
        }
    }
    if (drawed_objects[j - 1].marking_type == 'point') {
        map.pm.enableGlobalDragMode();
    } else {
        map.pm.disableGlobalDragMode();
    }
    drawed_objects[j - 1]["layer"].bindPopup(textcontent).openPopup();
    selectedObjectCount = j;
    right_id = j;
    label_indice = j;
}

var currentElement;

function checkColorChange(a) {
    label_db_id = a.id.split('color')[1]
    $(".lbl_checkbox:checkbox").prop("checked", false);
    if (drawingState) {
        $(a).prop("checked", true);
        $('.tq-butx').removeClass("current");
        $('.tq-butx').next(".s-click-dropdown").fadeOut(100);
        is_fav = a.id.split('color')[0]
        if (!is_fav) {
            a.parentElement.parentElement.parentElement.classList.add("last_selected_element");
        }
        colorEl = $(a).parent().parent().parent().find('.tq-color')[0].style.background;
        kaydet(label_db_id, a);
    } else {
        if (label_indice === 0) {
            $(a).prop("checked", true);
            $('.tq-butx').removeClass("current");
            $('.tq-butx').next(".s-click-dropdown").fadeOut(100);
            colorEl = $(a).parent().parent().parent().find('.tq-color')[0].style.background;
            kaydet(label_db_id, a, label_indice);
        } else {
            // if (drawed_objects[right_id - 1]["is_edited"]) {
            colorEl = $(a).parent().parent().parent().find('.tq-color')[0].style.background;
            var thisTextContent = $.trim($(a).parent().text());
            $.ajax({
                url: "/api/deleteStudentResult/",
                method: "GET",
                data: {
                    'label_id': drawed_objects[label_indice - 1].image_label_id,
                    'j': label_indice
                },
                success: function (res) {
                    //console.log(res);
                }
            });
            editLayerChange(colorEl, thisTextContent, label_db_id, a, label_indice);
        }
    }
    $(".lbl_checkbox:checkbox").prop("checked", false);
    try {
        drawed_objects[popupErrorId - 1]["layer"].bindPopup(thisTextContent);
    } catch (e) {
        console.log(e);
    }
    if (polygon_state == true) {
        polygonCreate();
    } else if (rectangle_state == true) {
        rectangleCreate();
    } else if (circleMarker_state == true) {
        circleMarkerCreate();
    } else if (polyline_state == true) {
        polylineCreate();
    }

}

var visibilityChange = true;
var selectChange = true;

function visibleOff(id, id2, id3) {
    var i = id.length;
    var j = id.split('check')[1];
    var c = $(id2).attr('id')
    var k = c.length;
    var l = c[k - 1];
    if (drawed_objects[j - 1]["layer"].options.fillOpacity) {
        // console.log("ilk if")
        drawed_objects[j - 1]["layer"].setStyle({opacity: 0});
        drawed_objects[j - 1]["layer"].setStyle({fillOpacity: 0});
        $(id3).addClass("Ä±mgOff");
        $(id3).removeClass("Ä±mgOn");
        visibilityChange = false;
        drawed_objects[j - 1]["layer"].editing.disable();
    } else if (drawed_objects[j - 1]["layer"].options.fillOpacity == "0") {
        if (drawed_objects[j - 1]["layer"].options.color == "#000000") {
            drawed_objects[j - 1]["layer"].setStyle({fillOpacity: 1});
        } else {
            drawed_objects[j - 1]["layer"].setStyle({fillOpacity: 0.1});
        }
        drawed_objects[j - 1]["layer"].setStyle({opacity: 1.0});
        $(id3).addClass("Ä±mgOn");
        $(id3).removeClass("Ä±mgOff");
        visibilityChange = true;
    } else if (drawed_objects[j - 1]["layer"]['_path'].attributes.d.value.length < 20) {
        // console.log("ilk else if")
        if (drawed_objects[j - 1]["layer"]['_path'].attributes["stroke-opacity"].value == 1) {
            // console.log("else-if^if")
            drawed_objects[j - 1]["layer"]['_path'].attributes["stroke-opacity"].value = "0";
            $(id3).addClass("Ä±mgOff");
            $(id3).removeClass("Ä±mgOn");
            visibilityChange = false;
            drawed_objects[j - 1]["layer"].editing.disable();
            for (var i = 0; i < drawed_objects.length; i++) {
                if (drawed_objects[i]["layer"] !== drawed_objects[j - 1]) {
                    drawed_objects[i]["layer"]['_path'].attributes["stroke-width"].value = "8";
                    drawed_objects[i]["layer"]['_path'].attributes["stroke-opacity"].value = "1";
                }
            }
        } else if (drawed_objects[j - 1]["layer"]['_path'].attributes["stroke-opacity"].value == 0) {
            // console.log("else-if^else-if")
            drawed_objects[j - 1]["layer"]['_path'].attributes["stroke-opacity"].value = "1";
            $(id3).addClass("Ä±mgOn");
            $(id3).removeClass("Ä±mgOff");
            visibilityChange = true;
        }
    }
}

function visibleOffAll(id3) {
    if (visibilityChange) {
        for (var x = 0; x < drawed_objects.length; x++) {
            if (drawed_objects[x]["layer"] !== "") {
                drawed_objects[x]["layer"].setStyle({opacity: 0});
                drawed_objects[x]["layer"].setStyle({fillOpacity: 0});
                drawed_objects[x]["layer"].pm.disable();
                drawed_objects[x]["layer"].editing.disable();
                drawed_objects[x]["layer"].closePopup();
            }
        }
        $(id3).addClass("Ä±mgOff");
        $(id3).removeClass("Ä±mgOn");
        visibilityChange = false;
    } else {
        for (var x = 0; x < drawed_objects.length; x++) {
            if (drawed_objects[x]["layer"] !== "") {
                if (drawed_objects[x]["layer"].options.color == "#000000") {
                    drawed_objects[x]["layer"].setStyle({fillOpacity: 1});
                } else {
                    drawed_objects[x]["layer"].setStyle({fillOpacity: 0.1});
                }
                drawed_objects[x]["layer"].setStyle({opacity: 1.0});
            }
        }
        $(id3).addClass("Ä±mgOn");
        $(id3).removeClass("Ä±mgOff");
        visibilityChange = true;
    }
}

function visibleOffAllPopup(id) {
    if (selectChange) {
        for (var x = 0; x < drawed_objects.length; x++) {
            if (drawed_objects[x]["layer"] !== "") {
                drawed_objects[x]["layer"].closePopup();
            }
            $(id).addClass("selectOff");
            $(id).removeClass("selectOn");
            selectChange = false;
        }
    } else {
        for (var x = 0; x < drawed_objects.length; x++) {
            if (drawed_objects[x]["layer"] !== "") {
                drawed_objects[x]["layer"].openPopup();
            }
            $(id).removeClass("selectOff");
            $(id).addClass("selectOn");
            selectChange = true;
        }
    }
}

function removeLayer(label_id, id, id2, delete_sure) {
    if (delete_sure) {
        $.ajax({
            url: "/api/deleteStudentResult/",
            method: "GET",
            data: {
                'label_id': label_id,
                'j': id
            },
            success: function (res) {
                j = res['j']
                if (drawed_objects[j - 1]["layer"]) {
                    drawed_objects[j - 1]["layer"].remove();
                }
                drawed_objects[j - 1]["layer"] = "";
                var etk = document.getElementById("eklenenEtiket" + j);
                etk.remove();
                // drawed_objects.splice(j - 1, 1);
                // cizim_sayac -= 1;
                // delete_sayac += 1;
                is_save_status = true;
                right_id = 0;
            }
        })
    } else {
        var i = id.length;
        var j = id.split('check')[1];
        $("#sureDeleteJ").html(j)
        $("#sureDeleteL").html(label_id)
        $(location).attr('href', '#sureDelete');
    }
}


function removeAllLayer(delete_sure) {
    if (delete_sure) {
        for (var i = 0; i < drawed_objects.length; i++) {
            if (drawed_objects[i]["layer"]) {
                var j = drawed_objects[i]["layer"]._path.classList[1].split("etiketdiv")[1];
                $.ajax({
                    url: "/api/deleteStudentResult/",
                    method: "GET",
                    data: {
                        'label_id': drawed_objects[i].image_label_id,
                        'j': j
                    },
                })
                try {
                    if (drawed_objects[i]["layer"]) {
                        drawed_objects[i]["layer"].remove();
                    }
                    drawed_objects[i]["layer"] = "";
                    var etk = document.getElementById("eklenenEtiket" + j);
                    etk.remove();
                } catch (e) {
                    console.log(e);
                }
                is_save_status = true;
                right_id = 0;
                delete_sayac += 1;
            }
        }
        $('.tq-butx').removeClass("current");
        $('.tq-butx').next(".s-click-dropdown").fadeOut(100);
    } else {
        $(location).attr('href', '#sureAllDelete');
    }
}

var selectedObjectCount;

function removeLayerSelected(delete_sure) {
    if (delete_sure) {
        $.ajax({
            url: "/api/deleteStudentResult/",
            method: "GET",
            data: {
                'label_id': drawed_objects[selectedObjectCount - 1].image_label_id,
                'j': selectedObjectCount
            },
            success: function (res) {
                try {
                    j = res['j'];
                    var etk = document.getElementById("eklenenEtiket" + j);
                    etk.remove();
                    if (drawed_objects[j - 1]["layer"]) {
                        drawed_objects[j - 1]["layer"].remove();
                    }
                    drawed_objects[j - 1]["layer"] = "";
                    //console.log("Deletec Layers: ", drawed_objects[j - 1], " deleted count: ", selectedObjectCount);
                } catch (e) {
                    console.log(e);
                }
                delete_sayac += 1;
                is_save_status = true;
                right_id = 0;
            }
        })
    } else {
        if (!drawed_objects[selectedObjectCount - 1]["layer"]) {

        } else {
            $(location).attr('href', '#sureSelectedDelete');
        }
    }
}

var var_edit_label_id;
var right_id = 0
var edit_label_state = false;

function editLayer(edit_label_id, e) {
    $(e).addClass("editLayerOn");
    var thisId = parseInt(e.parent().attr("id").split("etiketdiv")[1]);
    drawed_objects[thisId - 1]["is_edited"] = true;
    var_edit_label_id = edit_label_id
    if (!$(".tq-butx").hasClass('current')) {
        $('.tq-butx').toggleClass("current");
        $('.tq-butx').next(".s-click-dropdown").fadeToggle(100);
    } else {
        $('.tq-butx').toggleClass("current");
        $('.tq-butx').next(".s-click-dropdown").fadeToggle(100);
    }
}

function editLayerChange(color, textContent, label_db_id, a, editId) {
    var textContent = textContent;
    var color = color;
    var editedElement = $("#etiketdiv" + editId).children();
    $.ajax({
        url: "/api/editimagelabel/",
        method: "GET",
        data: {
            'image_label_id': var_edit_label_id,
        },
        success: function (res) {

            $(editedElement).find("#span-etiket" + label_indice)[0].textContent = textContent;
            $(editedElement).find(".tq-color").css("background", color);
            color = rgbToHex(color);
            if (textContent.includes("Point")) {
                drawed_objects[label_indice - 1]["layer"].setStyle({fillColor: color, color: "#000000"});
            } else {
                drawed_objects[label_indice - 1]["layer"].setStyle({color: color});
            }
            if ($(".tq-butx").hasClass('current')) {
                $('.tq-butx').toggleClass("current");
                $('.tq-butx').next(".s-click-dropdown").fadeToggle(100);
            }
            $(".editLayerOn").removeClass("editLayerOn");

            kaydet(label_db_id, a, label_indice);
        }
    })
}

var zoom = 1;

$('.ul-fix-4 li:nth-child(1)').on('click', function () {
    $("#place").click();
    $("#place2").click();
    zoom += 0.1;
    $('#back-img-frame-image').css('transform', 'scale(' + zoom + ')');
});
$('.ul-fix-2 li:nth-child(2)').on('click', function () {
    zoom = 1;
    $(".ul-fix-5")[0].style.display = "none"
    $(".ul-fix-4")[0].style.display = "none";
    document.getElementById("sli1").style.filter = "contrast(100%)";
    $('#back-img-frame-image').css('transform', 'scale(' + zoom + ')');
    $("#back-img-frame-image").css("top", "0px");
    $("#back-img-frame-image").css("left", "0px");
});
$('.ul-fix-4 li:nth-child(2)').on('click', function () {
    $("#place").click();
    $("#place2").click();
    zoom -= 0.1;
    $('#back-img-frame-image').css('transform', 'scale(' + zoom + ')');
});

function hoverOn(x) {
    $("#" + x).children().find(".eyeImg").show();
    $("#" + x).children().find(".deleteImg").show();
    $("#" + x).children().find(".newdeleteImg").show();
    $("#" + x).children().find(".editImg").show();
    x = $("#" + x).find('label').find('input')[0].id;
    var j = x.split('check')[1];
    var curEl = document.getElementById(x);
    if (curEl.checked == true) {
        //// console.log($("#" + x).checked);
    } else {
        if (drawed_objects[j - 1]["layer"]['_path'].attributes.d.value.length < 20) {
            if (visibilityChange == true) {
                drawed_objects[j - 1]["layer"]['_path'].attributes["stroke-width"].value = "2";
            }
        } else if (drawed_objects[j - 1]["layer"]['_path'].attributes.d.value.length == 39) {
            drawed_objects[j - 1]["layer"]['_path'].attributes["fill-opacity"].value = "1"
            drawed_objects[j - 1]["layer"]['_path'].attributes["stroke-width"].value = "2"
            drawed_objects[j - 1]["layer"]['_path'].attributes["stroke-opacity"].value = "1";
        } else {
            drawed_objects[j - 1]["layer"].setStyle({weight: 3});
        }
    }
}

function hoverOff(x) {
    $("#" + x).children().find(".eyeImg").hide();
    $("#" + x).children().find(".deleteImg").hide();
    $("#" + x).children().find(".newdeleteImg").hide();
    $("#" + x).children().find(".editImg").hide();
    x = $("#" + x).find('label').find('input')[0].id;
    var j = x.split('check')[1];
    var curEl = document.getElementById(x);
    if (curEl.checked == true) {
    } else {
        if (drawed_objects[j - 1]["layer"]['_path'].attributes.d.value.length < 20) {
            if (visibilityChange == true) {
                drawed_objects[j - 1]["layer"]['_path'].attributes["stroke-width"].value = "1";
            }
        } else if (drawed_objects[j - 1]["layer"]['_path'].attributes.d.value.length == 39) {
            drawed_objects[j - 1]["layer"]['_path'].attributes["fill-opacity"].value = "1"
            drawed_objects[j - 1]["layer"]['_path'].attributes["stroke-width"].value = "1"
            drawed_objects[j - 1]["layer"]['_path'].attributes["stroke-opacity"].value = "1";
        } else {
            drawed_objects[j - 1]["layer"].setStyle({weight: 1});
        }
    }
}


var list_count;
var list_count_sayac = 0;

function clear_all() {
    for (let i = 0; i < drawed_objects.length; i++) {
        if (drawed_objects[i]["layer"]) {
            drawed_objects[i]["layer"].remove();
        }
    }
    var es_content = $('#right-lbl-list').children();
    var matched_list = $('#matched-list').children();
    var unmatched_list = $('#unmatched-list').children();
    var wrond_list = $('#wrong-list').children();
    for (let i = 0; i < es_content.length; i++) {
        es_content[i].remove();
    }
    for (let i = 0; i < wrond_list.length; i++) {
        wrond_list[i].remove();
    }
    for (let i = 0; i < matched_list.length; i++) {
        matched_list[i].remove();
    }
    for (let i = 0; i < unmatched_list.length; i++) {
        unmatched_list[i].remove();
    }
    for (var i = 0; i < list_count.length; i++) {
        $(list_count[i]).find('div:nth-child(2)').removeClass("border-select");
    }
    $(this).parent().addClass('border-select');
    for (var i = 0; i < drawed_objects.length; i++) {
        if (drawed_objects[i]["layer"]) {
            drawed_objects[i]["layer"].remove();
        }
    }
    for (var i = 0; i < drawed_objects.length; i++) {
        drawed_objects.splice(drawed_objects.indexOf(0), 1);
    }
    drawed_objects = [];
    createAnno_sayac = 0;
    drawCounter = 0;
    label_indice = 0;
    // cizim_sayac = 0;
    // delete_sayac = 0;
    // drawCounter = 1;
    annotations = anno.getAnnotations()
    for (let anno_index = 0; anno_index < annotations.length; anno_index++) {
        anno.removeAnnotation(annotations[anno_index]);
        $('svg[data-comment-id="' + annotations[anno_index].id + '"]').remove();
        $('g[data-id="' + annotations[anno_index].id + '"]').remove();
    }
}

$(".ul-fix").children().click(function () {
    if ($(this).children().hasClass("pasive-left-icon")) {

    } else {
        $(".ul-fix").children().children().removeClass("active");
        $(this).children().addClass("active");
    }
});

function matchClick() {
    $("#unmatched-list").parent().parent().hide();
    $("#wrong-list").parent().parent().hide();
    $("#matched-list").parent().parent().show();
}

function wrongClick() {
    $("#matched-list").parent().parent().hide();
    $("#unmatched-list").parent().parent().hide();
    $("#wrong-list").parent().parent().show();
}

function unmatchedClick() {
    $("#matched-list").parent().parent().hide();
    $("#wrong-list").parent().parent().hide();
    $("#unmatched-list").parent().parent().show();
}

$("#place").mouseover(function () {
    $(".lightmode .icon30").css("background", "url('/static/images/icon50_1.png') no-repeat center center");
});
$("#place").mouseout(function () {
    $(".lightmode .icon30").css("background", "url('/static/images/icon50.png') no-repeat center center");
});

$("#draw-rectangle").mouseover(function () {
    $(".lightmode .icon34").css("background", "url('/static/images/icon54_1.png') no-repeat center center");
});
$("#draw-rectangle").mouseout(function () {
    $(".lightmode .icon34").css("background", "url('/static/images/icon54.png') no-repeat center center");
});

$("#draw-polygon").mouseover(function () {
    $(".lightmode .icon35").css("background", "url('/static/images/icon55_1.png') no-repeat center center");
});
$("#draw-polyline").mouseover(function () {
    $(".lightmode .icon35").css("background", "url('/static/images/icon55_1.png') no-repeat center center");
});
$("#draw-polygon").mouseout(function () {
    $(".lightmode .icon35").css("background", "url('/static/images/icon55.png') no-repeat center center");
});
$("#draw-polyline").mouseout(function () {
    $(".lightmode .icon35").css("background", "url('/static/images/icon55.png') no-repeat center center");
});

$("#draw-circle").mouseover(function () {
    $(".lightmode .icon36").css("background", "url('/static/images/icon56_1.png') no-repeat center center");
});
$("#draw-circle").mouseout(function () {
    $(".lightmode .icon36").css("background", "url('/static/images/icon56.png') no-repeat center center");
});

$("#zoom-in").mouseover(function () {
    $(".lightmode .icon41").css("background", "url('/static/images/icon61_1.png') no-repeat center center");
});
$("#zoom-in").mouseout(function () {
    $(".lightmode .icon41").css("background", "url('/static/images/icon61.png') no-repeat center center");
});

$("#zoom-out").mouseover(function () {
    $(".lightmode .icon42").css("background", "url('/static/images/icon62_1.png') no-repeat center center");
});
$("#zoom-out").mouseout(function () {
    $(".lightmode .icon42").css("background", "url('/static/images/icon62.png') no-repeat center center");
});

$("#zoom-reset").mouseover(function () {
    $(".lightmode .icon67").css("background", "url('/static/images/icon67_1.png') no-repeat center center");
});
$("#zoom-reset").mouseout(function () {
    $(".lightmode .icon67").css("background", "url('/static/images/icon67.png') no-repeat center center");
});

$("#place").click(function () {
    if (drawed_objects.length < $("#right-lbl-list").children().length) {
        // var i = drawed_objects.length;
        // if (drawed_objects[i - 1]["layer"]) {
        //     drawed_objects[i - 1]["layer"].remove();
        // }
        // drawed_objects.splice(drawed_objects.indexOf(0), 1);
        $("#draw-polygon").show();
        $("#draw-polyline").show();
        $("#draw-rectangle").show();
        $("#draw-circle").show();
        $('.tq-butx').removeClass("current");
        $('.tq-butx').next(".s-click-dropdown").fadeOut(100);
        cizim_etiket_alan_control = false;
        $("#place").click();
        cizim_sayac -= 1;
        editmode = false;
    }
});

$(document).keyup(function (e) {
    if (e.key === "Escape") { // escape key maps to keycode `27`
        $(".leaflet-pane.leaflet-marker-pane i.delete-icon").remove()
        // if (drawingState) {
        //     drawingState = false;
        //     drawed_objects[drawed_objects.length - 1]["layer"].remove();
        //     drawed_objects.splice(drawed_objects.length - 1, 1);
        //     drawCounter -= 1;
        // }
        // if ($(".tq-butx").hasClass('current')) {
        //     $('.tq-butx').toggleClass("current");
        //     $('.tq-butx').next(".s-click-dropdown").fadeToggle(100);
        // }
        // $("#place").click();
        // $(".outline").click();
        // $("#draw-polygon").show();
        // $("#draw-polyline").show();
        // $("#draw-rectangle").show();
        // $("#draw-circle").show();
    }
});


function parseCoordinates(inputString) {
    // made e.b.
    var processedString = inputString.replace(/[Mz]/g, ''); // M ve z harflerini kaldır
    var coordinatePairs = processedString.split('L');
    var result = [];

    for (var i = 0; i < coordinatePairs.length; i++) {
        var coordinate = coordinatePairs[i].trim();
        var [x, y] = coordinate.split(/\s+/); // Aradaki boşluklara göre böl
        result.push([Number(x), Number(y)]);
    }

    return result;
}

function findClosestPoint(x1, y1, coords) {
    var points = coords;
    var closestPoint = points[0];
    var closestDistance = getDistance(x1, y1, closestPoint[0], closestPoint[1]);

    for (var i = 1; i < points.length; i++) {
        var currentPoint = points[i];
        var currentDistance = getDistance(x1, y1, currentPoint[0], currentPoint[1]);

        if (currentDistance < closestDistance) {
            closestPoint = currentPoint;
            closestDistance = currentDistance;
        }
    }

    return closestPoint;
}

function getDistance(x1, y1, x2, y2) {
    return Math.sqrt(Math.pow((x2 - x1), 2) + Math.pow((y2 - y1), 2));
}

function marker_icon_middle_displaychange(element) {
    el = element.children[0]
    if (marker_middle_icon === false) {
        marker_icon_middle = $('.marker-icon-middle-none')
        $.each(marker_icon_middle, function (index) {
            marker_icon_middle[index].classList.add("marker-icon-middle")
            marker_icon_middle[index].classList.remove("marker-icon-middle-none")
        });
        // $('.marker-icon-middle').attr("style","display: block !important")
        marker_middle_icon = true
        el.classList.add("minus_dot")
        el.classList.remove("plus_dot")
    } else {
        marker_icon_middle = $('.marker-icon-middle')
        // $('.marker-icon-middle').attr("style","display: none !important")
        $.each(marker_icon_middle, function (index) {
            marker_icon_middle[index].classList.add("marker-icon-middle-none")
            marker_icon_middle[index].classList.remove("marker-icon-middle")
        });
        marker_middle_icon = false
        el.classList.add("plus_dot")
        el.classList.remove("minus_dot")
    }
}

$(document).ready(function () {
    edited_stroke_width = 1.5
});

function thinner_line() {
    leaflet_line = $(".leaflet-pm-draggable")
    edited_stroke_width -= 0.4
    if (edited_stroke_width < 0) {
        edited_stroke_width = 0.1
    }
    for (let i = 0; i < leaflet_line.length; i++) {
        $(".leaflet-pm-draggable")[i].attributes["stroke-width"].value = edited_stroke_width
    }
    leaflet_line2 = $("path.leaflet-pm-draggable")
    leaflet_line2[leaflet_line2.length - 1].attributes["stroke-width"].value = edited_stroke_width
    if (editmode == false) {
        leaflet_line2 = $("path.leaflet-pm-draggable")
        leaflet_line2[leaflet_line2.length - 1].attributes["stroke-width"].value = edited_stroke_width
    } else {
        last_selected_drawing.setStyle({weight: edited_stroke_width});
    }

}

function thicker_line() {
    leaflet_line = $(".leaflet-pm-draggable")
    edited_stroke_width += 0.4
    if (edited_stroke_width > 8) {
        edited_stroke_width = 8
    }
    for (let i = 0; i < leaflet_line.length; i++) {
        $(".leaflet-pm-draggable")[i].attributes["stroke-width"].value = edited_stroke_width
    }
    if (editmode == false) {
        leaflet_line2 = $("path.leaflet-pm-draggable")
        leaflet_line2[leaflet_line2.length - 1].attributes["stroke-width"].value = edited_stroke_width
    } else {
        last_selected_drawing.setStyle({weight: edited_stroke_width});
    }
}

var rulerControl = null;
var rulerState = false;

function activateRuler() {
    rulerControl = L.control.ruler({
        position: 'topleft',
        lengthUnit: {
            display: 'mm',
            decimal: 2,
            factor: 0.135,
            label: 'Distance:'
        },
        angleUnit: {
            display: '&deg;',           // This is the display value will be shown on the screen. Example: 'Gradian'
            decimal: 2,                 // Bearing result will be fixed to this value.
            factor: null,                // This option is required to customize angle unit. Specify solid angle value for angle unit. Example: 400 (for gradian).
            label: 'Degree:'
        }
    });
    rulerControl.addTo(map);
}

$("#measure-btn").click(function () {
    if (!rulerState) {
        activateRuler();
        if ($(".leaflet-bar.leaflet-ruler.leaflet-control").css("display") == 'none') {
            $(".leaflet-bar.leaflet-ruler.leaflet-control").css("display", "");
        }
        $(".leaflet-bar.leaflet-ruler.leaflet-control").click();
        $(".leaflet-bar.leaflet-ruler.leaflet-control").css("display", "none");
        rulerState = true;
    } else {
        rulerControl.closeRulerManuel();
        rulerControl.closeRulerManuel();
        rulerState = false;
    }
});

$(document).keyup(function (e) {
    if (e.keyCode === 27 && rulerControl !== null) {
        rulerControl.closeRulerManuel();
    }
});

function resetImpCrwVal() {
    var dimensionValue = 100;
    $("#dimension-btn").nextAll('.range-marker').first().css("left", `${dimensionValue / 3}%`);
    $("#dimension-btn").nextAll('.range-value').first().css("width", `${dimensionValue / 3}%`);
    $("#dimensionValue").text(dimensionValue)
    $("#dimension-btn").attr('value', dimensionValue);
    var implantRotateValue = 0;
    $("#rotate-implant-btn").nextAll('.range-marker').first().css("left", `${implantRotateValue / 3.6}%`);
    $("#rotate-implant-btn").nextAll('.range-value').first().css("width", `${implantRotateValue / 3.6}%`);
    $("#rotateImplantValue").text(implantRotateValue)
    $("#rotate-implant-btn").attr('value', implantRotateValue);

    implantIcon.options.iconSize[0] = dimensionValue;
    implantIcon.options.iconSize[1] = dimensionValue;
    crownIcon.options.iconSize[0] = dimensionValue;
    crownIcon.options.iconSize[1] = dimensionValue;
    degree = 0;
}

function setImpCrwVal(elem) {
    var dimensionValue = $(elem).width();
    $("#dimension-btn").nextAll('.range-marker').first().css("left", `${dimensionValue / 3}%`);
    $("#dimension-btn").nextAll('.range-value').first().css("width", `${dimensionValue / 3}%`);
    $("#dimensionValue").text(dimensionValue)
    $("#dimension-btn").attr('value', dimensionValue);
    var implantRotateValue = parseInt($(elem)[0].style["transform"].split("rotate(")[1].split("deg)")[0]);
    $("#rotate-implant-btn").nextAll('.range-marker').first().css("left", `${implantRotateValue / 3.6}%`);
    $("#rotate-implant-btn").nextAll('.range-value').first().css("width", `${implantRotateValue / 3.6}%`);
    $("#rotateImplantValue").text(implantRotateValue)
    $("#rotate-implant-btn").attr('value', implantRotateValue);
    degree = implantRotateValue;
}

function latLngToCoordFunc(e) {
    const sonuc = [];
    for (let i = 0; i < e.length; i++) {
        const d = e[i];
        const x = d.x;
        const y = d.y;
        sonuc.push([x, y]);
    }
    return sonuc;
}


function disableAllTools() {
    // annoClose();
    map.pm.disableGlobalEditMode();
    map.pm.enableGlobalDragMode();
    rectangleDrawer.enable();
    polygonDrawer.enable();
    polylineDrawer.enable();
    rectangleDrawer.disable();
    polygonDrawer.disable();
    polylineDrawer.disable();
    circleMarkerDrawer.disable();
    editmode = false;
    polygon_state = false;
    polyline_state = false;
    rectangle_state = false;
    circleMarker_state = false;
    cizim_etiket_alan_control = false;
    createDrawState = false;
}

window.onresize = function (event) {
    disableAllTools();
    annoClose()
    $("svg.leaflet-zoom-animated").remove()
    $("#back-img-frame .loading").removeClass("d-none")
    Swal.fire({
        position: 'top-end',
        icon: 'warning',
        title: "You have resized the page. Page is refreshing",
        showConfirmButton: false,
        timer: 2000
    }).then(function () {
        $("#page-loading").show();
        window.location.reload();
    }, 1000)
};