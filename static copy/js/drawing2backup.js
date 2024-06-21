var center = [0, 0];
var polygon_state = false;
var polyline_state = false;
var rectangle_state = false;
var circleMarker_state = false;
var cizim_etiket_alan_control = false;
var editmode = false;
var dragObjectMove = false;

var drawed_objects = [];


var map = L.map('back-img-frame', {zoomControl: false}).setView(center, 20);
map.dragging.disable();
map.touchZoom.disable();
map.doubleClickZoom.disable();
map.scrollWheelZoom.disable();
map.boxZoom.disable();
map.keyboard.disable();

map.pm.enableGlobalDragMode();


// Set up the OSM layer

// add a marker in the given location

// Initialise the FeatureGroup to store editable layers
var editableLayers = new L.FeatureGroup();
map.addLayer(editableLayers);


// var drawPluginOptions = {
//     position: 'topleft',
//     draw: {
//         polygon: {
//             allowIntersection: false, // Restricts shapes to simple polygons
//             drawError: {
//                 color: '#e1e100', // Color the shape will turn when intersects
//                 message: '<strong>Oh snap!<strong> you can\'t draw that!' // Message that will show when intersect
//             },
//             shapeOptions: {
//                 color: '#97009c'
//             }
//         },
//         rectangle: {
//             drawError: {
//                 color: '#e1e100', // Color the shape will turn when intersects
//                 message: '<strong>Oh snap!<strong> you can\'t draw that!' // Message that will show when intersect
//             },
//             shapeOptions: {
//                 color: '#f4858c'
//             }
//         },
// 		circleMarker: {
//             drawError: {
//                 color: '#e1e100', // Color the shape will turn when intersects
//                 message: '<strong>Oh snap!<strong> you can\'t draw that!' // Message that will show when intersect
//             },
//             shapeOptions: {
//                 color: '#12232b'
//             }
//         },
//         // disable toolbar item by setting it to false
//         polyline: false, // Turns off this drawing tool
//         marker: false, // Turns off this drawing tool
//     },
//     edit: {
//         featureGroup: editableLayers, //REQUIRED!!
//         remove: true
//     }
// };
// var drawControl = new L.Control.Draw(drawPluginOptions);
// map.addControl(drawControl);

var delete_sayac = 0;
var createAnno_sayac = 0;
var marking_type_dict = {"circlemarker": "point", "rectangle": "rectangle", "polygon": "polygon", "polyline": "polyline"}

var myIcon = L.icon({
    iconUrl: '/static/images/anno.png',
    iconSize: [24, 24],
    iconAnchor: [22, 24]
});
map.on('draw:created', function (e) { //TODO: bunu nasıl tetikleyebilirim edit mod olunca drw_obj[right_id-1]["layer"] buraya yolla layer varsa o layer ile çizdir tip ve renk de aynı şekilde
    window.onbeforeunload = function () {
        return "Kaydedilmemiş değişiklikler olabilir. Çıkmak istediğinizden emin misiniz?";
    }
    var cizim_fark = cizim_sayac - delete_sayac - $("#right-lbl-list").children().length;
    if (cizim_fark === 0) {
        var type = e.layerType,
            layer = e.layer;
        layer.setStyle({weight: 1});
        e.class = "cizim" + cizim_sayac;
        var points = layer._latlngs;
        //// console.log("ADDED NEW POINT", points); // zoomed values
        var geojson = layer.toGeoJSON();
        // if (!$(".tq-butx").hasClass('current')) {
        //     $('.tq-butx').toggleClass("current");
        //     $('.tq-butx').next(".s-click-dropdown").fadeToggle(100);
        // }
        //// console.log(layer);
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
        // drawed_objects.push(layer);
        drawed_objects.push({
            // "image_id": active_image_id,
            "image_id": 1, // orjinali üst satır
            // "user_id": user_id,
            "user_id": 1, // orjinali yukarda
            "marking_type": marking_type_dict[type], // Rectangle, polygon, point için dbde kayıtlı olan idler
            "label": {
                "id": NaN,
                "color": NaN,
                "name": NaN,
                // "rigth_label_list_id": cizim_sayac // Sağdaki label listesinde eklediğimiz idsi ne?
                "rigth_label_list_id": 1 // Sağdaki label listesinde eklediğimiz idsi ne?
            },
            "layer": layer,
            // leafletten gelen değerler
            // leafletin her çizim için kendi json formatı var. Bu formatta da ekstra olarak kaydedip o kayıtlardan load edebilir miyiz?
            "cartesian_coordinates": {
                // coordinatların kartezyen coordinatlardaki karşılıkları
            },
            "is_saved": false,
            "is_deleted": false,
            "is_edited": false,
            "is_move": false,
        })
        if (type === 'polygon') {
            drawed_objects[drawed_objects.length - 1]["layer"]["editing"]["latlngs"][0][0].push(drawed_objects[drawed_objects.length - 1]["layer"]["editing"]["latlngs"][0][0][0]);
        }
        editableLayers.addLayer(layer);
        // cizim_sayac += 1;
        cizim_etiket_alan_control = true;
        $("#draw-polygon").hide();
        // $("#draw-rectangle").hide();
        $("#draw-circle").hide();
        $("#draw-polyline").hide();
        /*
            var points = layer._latlngs;
            // console.log("ADDED NEW POINT", points); // zoomed values
            var geojson = layer.toGeoJSON();
            layer.bindPopup('<div><div class="popup-top-text-div"><i class="fas fa-user" style="float: left;margin-right: 5px;font-size: 19px;color: #0190cf;"></i><p class="popup-top-text-p">Student 1</p></div><input type="text" class="popup-input" placeholder="Reply"/></div>');
            editableLayers.addLayer(layer);
            <div class="popup-top-text-div"><i class="fas fa-user" style="float: left;margin-right: 5px;font-size: 19px;color: #0190cf;"></i><p class="popup-top-text-p">Student 1</p></div>
            */
    }
});
/*map.on('pm:globaldragmodetoggled', e => {
  // console.log(e);
});
*/
var cbs;
var loading_status = false

//           SAYFA RESİZE KAYMA KODLARI SİLME
// map.on('moveend', function(e) {
//     $("#loading").css('opacity', 0.5)
//     $("#loading").show()
//     setTimeout(function (){after_than_resize()}, 500)
//  });
// function after_than_resize() {
//     $(".leaflet-map-pane")[0].style.transform = "translate3d(0px, 0px, 0px)"
//     $("#sli1")[0].style.height = sli1_height
//     $("svg")[0].style.transform = svg_transform
//     $("svg")[0].viewBox.baseVal.x = svg_x
//     $("svg")[0].viewBox.baseVal.y = svg_y
//     $("svg")[0].viewBox.baseVal.width = svg_width
//     $("svg")[0].viewBox.baseVal.height = svg_height
//     $("svg")[0].width.baseVal.value = svg_width
//     $("svg")[0].height.baseVal.value = svg_height
//     for (let index = 0; index < paths_d.length; index++) {
//         const element = paths_d[index];
//         // console.log("BEFORE: ", paths[index].attributes.d.value)
//         paths[index].attributes.d.value = element
//         // console.log("ELEMENT: ", element)
//         // console.log("AFTER: ", paths[index].attributes.d.value)
//     }
//     loading_hide()
// }

var label_indice = 0;
// $(".leaflet-pane").on('mousedown', function (e) {
//     loading_status = false;
//     class_name = ""
//     try {
//         try {
//             label_indice = e.target.attributes.class.value.split('etiketdiv')[1].split(' ')[0];
//             drawed_objects[label_indice - 1]["is_move"] = true;
//             drawed_objects[label_indice - 1]["layer"].closePopup();
//         } catch (_) {
//             // var label_indice = e.originalEvent.currentTarget.lastChild.offsetLeft * -1
//             var paths = e.target.parentElement.parentElement.children[2].children[0].children[0].children;
//             var es = e.target.parentElement.children
//             var x = e.target.style.transform.substr(12).split("px")[0]
//             var y = e.target.style.transform.substr(20).split("px")[0]
//             var point_coord = x + " " + y
//             var k = 0;
//             for (i=0;i<es.length;i++){
//                 var x = es[i]._leaflet_pos.x
//                 var y = es[i]._leaflet_pos.y
//                 var point_coord = x + " " + y
//                 if (drawed_objects[k]["is_move"] === false) {
//                     for (var j = 0; j < paths.length; j++) {
//                         var d_stra = paths[j].attributes.d.value
//                         if (d_stra.includes(point_coord)) {
//                             drawed_objects[j]["is_move"] = true;
//                             k = j
//                             label_indice = k + 1;
//                         }
//                     }
//                 }
//             }
//             drawed_objects[label_indice - 1]["layer"].closePopup();
//         }
//     } catch (_) {
//         console.log("edit yok")
//     }
//     dragObjectMove = true;
//     if (editmode == false) {
//     }
//     $("#big-slider").draggable({disabled: true});
//
//     $("path").on('mousedown', function (e) {
//         loading_status = false
//         cbs = document.getElementsByClassName("etiketdivclass");
//         for (var y = 0; y < cbs.length; y++) {
//             $(cbs[y]).find('label').find('input')[0].checked = false;
//         }
//         for (var k = 0; k < cbs.length; k++) {
//             if ($(this).hasClass($(cbs[k]).attr('id'))) {
//                 $(cbs[k]).find('label').find('input')[0].checked = true;
//             }
//         }
//         try {
//             class_name = ".etiketdiv" + label_indice
//             $(class_name).on('moveend', function() {
//                 label_indice = 0;
//                 if ($('#place').hasClass('active')) {
//                     $("#loading").show();
//                     setTimeout(loading_hide,2500)
//                     $("#loading").css('opacity', 0.5)
//                     //var index = $( "path" ).index( this );
//                     finded_status = false;
//                     if (!loading_status) {
//                         loading_status = true
//                         for (j = 0; j < drawed_objects.length; j++) {
//                             if (drawed_objects[j]["is_move"] === true) {
//                                 drawed_objects[j]["is_move"] = false;
//                                 finded_status = true
//                                 var label_db_id = drawed_objects[j]["label"]["id"];
//                                 a = false;
//
//                                 $.ajax({
//                                     url: "/api/editimagelabel/",
//                                     method: "GET",
//                                     data: {
//                                         'image_label_id': drawed_objects[j]["image_label_id"],
//                                         'i': j,
//                                     },
//                                     success: function (res) {
//                                         var moved_right_id = res["i"]
//                                         kaydet(label_db_id, a, moved_right_id + 1);
//                                         loading_status = false
//                                     }
//                                 })
//                             }
//                         }
//                     }
//                 }
//              });
//         } catch (_) {
//             console.error(_)
//         }
//
//     });
// });
$("#sli1").on('mousedown', function (e) {
    loading_status = false
    if (label_indice == 0) {
        dragObjectMove = false;
    }
});
$("#leaflet-pane").on('mousedown', function (e) {
    loading_status = false
});
$("#sli1").on('mouseup', function (e) {
    label_indice = 0;
	if ($('#place').hasClass('active') && dragObjectMove) {
		dragObjectMove = false;
        $("#loading").show();
        setTimeout(loading_hide,2500)
		$("#loading").css('opacity', 0.5)
		finded_status = false;
		if (!loading_status) {
			loading_status = true
			for (j = 0; j < drawed_objects.length; j++) {
				if (drawed_objects[j]["is_move"] === true) {
					drawed_objects[j]["is_move"] = false;
					finded_status = true
					var label_db_id = drawed_objects[j]["label"]["id"];
					a = false;

					$.ajax({
						url: "/api/editimagelabel/",
						method: "GET",
						data: {
							'image_label_id': drawed_objects[j]["image_label_id"],
							'i': j,
						},
						success: function (res) {
							var moved_right_id = res["i"]
							kaydet(label_db_id, a, moved_right_id + 1);
							loading_status = false
						}
					})
				}
			}
		}
	}
});

$(".leaflet-pane").on('mouseup', function (e) {
    label_indice = 0;
    if ($('#place').hasClass('active')) {
        $("#loading").show();
        setTimeout(loading_hide,2500)
        $("#loading").css('opacity', 0.5)
        //var index = $( "path" ).index( this );
        finded_status = false;
        if (!loading_status) {
            loading_status = true
            for (j = 0; j < drawed_objects.length; j++) {
                if (drawed_objects[j]["is_move"] === true) {
                    drawed_objects[j]["is_move"] = false;
                    finded_status = true
                    var label_db_id = drawed_objects[j]["label"]["id"];
                    a = false;

                    $.ajax({
                        url: "/api/editimagelabel/",
                        method: "GET",
                        data: {
                            'image_label_id': drawed_objects[j]["image_label_id"],
                            'i': j,
                        },
                        success: function (res) {
                            var moved_right_id = res["i"]
                            kaydet(label_db_id, a, moved_right_id + 1);
                            loading_status = false
                        }
                    })
                }
            }
            // if (!finded_status){
            //     // console.log("Hiçbir eşleşme bulunamadı")
            //     $("#loading").hide()
            //     loading_status=false
            // }
        }
    }
});




var polygonDrawer = new L.Draw.Polygon(map);
var polylineDrawer = new L.Draw.Polyline(map);
var rectangleDrawer = new L.Draw.Rectangle(map);
var circleMarkerDrawer = new L.Draw.CircleMarker(map, {radius: 4, fillOpacity: 1});

//var markerDrawer = new L.Draw.Marker(map, { icon: myIcon});

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
    circleMarkerDrawer = new L.Draw.CircleMarker(map, {radius: 4, fillOpacity: 1});
    circleMarkerDrawer.enable();
}

var username;


function get_comment_annotations(force = false) {
    // console.log(active_image_id)
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
                // $('.a9s-annotationlayer').append('<svg class="anno-img" data-comment-id="' + results[i].id + '" width="200" height="200" xmlns="http://www.w3.org/2000/svg" x="' + c + '" y="' + d + '"><g><path stroke="#ffffff" id="svg_4" d="m21.87347,2.08237c-10.2847,0 -18.62199,8.53321 -18.62199,19.05912c0,3.59701 0.98564,6.95731 2.68166,9.82663l-2.68166,8.02294l7.46605,-2.61592c3.11119,2.39082 6.96598,3.82482 11.15594,3.82482c10.28471,0 18.622,-8.53321 18.622,-19.05847c0,-10.52591 -8.33728,-19.05912 -18.622,-19.05912l0,0l0,0z" fill-opacity="null" stroke-opacity="null" stroke-width="3" fill="#ff0000"></path><text class="deneme-text" x="17" y="26" font-family="Verdana" font-size="15" fill="white">' + createAnno_sayac + '</text></g></svg>');
                $('.a9s-annotationlayer').append('<svg class="anno-img" data-comment-id="' + results[i].id + '" width="200" height="200" xmlns="http://www.w3.org/2000/svg" x="' + c + '" y="' + d + '"><g><path stroke="#ffffff" d="M12 1.02901C5.38298 1.02901 0 5.50201 0 11C0 13.825 1.44398 16.498 3.97898 18.393L2.052 22.247C1.95 22.45 1.99898 22.696 2.169 22.846C2.26298 22.9291 2.37998 22.9711 2.499 22.9711C2.59598 22.9711 2.69302 22.9431 2.778 22.8861L6.99502 20.0551C8.58403 20.662 10.267 20.9701 12 20.9701C18.617 20.9701 24 16.4971 24 10.999C24 5.50102 18.617 1.02901 12 1.02901V1.02901Z" fill="#FF0000"/></path><text class="deneme-text" x="17" y="26" font-family="Verdana" font-size="15" fill="white"></text></g></svg>');
            }

            /*if (force) {
                $("#draw-marker").click();
            } else {
                $("#place").click();
                $("#draw-marker").click();
                $("#place2").click();
            }*/
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
            // $('.a9s-annotationlayer').append('<svg class="anno-img" data-comment-id="' + annotation.id + '" width="200" height="200" xmlns="http://www.w3.org/2000/svg" x="' + c + '" y="' + d + '"><g><path stroke="#ffffff" id="svg_4" d="m21.87347,2.08237c-10.2847,0 -18.62199,8.53321 -18.62199,19.05912c0,3.59701 0.98564,6.95731 2.68166,9.82663l-2.68166,8.02294l7.46605,-2.61592c3.11119,2.39082 6.96598,3.82482 11.15594,3.82482c10.28471,0 18.622,-8.53321 18.622,-19.05847c0,-10.52591 -8.33728,-19.05912 -18.622,-19.05912l0,0l0,0z" fill-opacity="null" stroke-opacity="null" stroke-width="3" fill="#ff0000"></path><text class="deneme-text" x="17" y="26" font-family="Verdana" font-size="15" fill="white">' + createAnno_sayac + '</text></g></svg>');
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
    polygonDrawer = new L.Draw.Polygon(map);
    polylineDrawer = new L.Draw.Polyline(map);
    rectangleDrawer = new L.Draw.Rectangle(map);
    circleMarkerDrawer = new L.Draw.CircleMarker(map, {radius: 4, fillOpacity: 1});
    //markerDrawer = new L.Draw.Marker(map, { icon: myIcon});

    $("#draw-polygon").click(function () {
        last_clicked_tool = $("#draw-polygon")
        annoClose();
        //$("#big-slider").draggable({disabled: true});
        rectangleDrawer.disable();
        circleMarkerDrawer.disable();
        polylineDrawer.disable();
        polygon_state = true;
        polyline_state = false;
        rectangle_state = false;
        circleMarker_state = false;
        polygonDrawer.enable();
    });

    $("#draw-polyline").click(function () {
        last_clicked_tool = $("#draw-polyline")
        annoClose();
        //$("#big-slider").draggable({disabled: true});
        rectangleDrawer.disable();
        circleMarkerDrawer.disable();
        polygonDrawer.disable();
        polyline_state = true;
        polygon_state = false;
        rectangle_state = false;
        circleMarker_state = false;
        polylineDrawer.enable();
    });

    $("#draw-rectangle").click(function () {
        annoClose();
        //$("#big-slider").draggable({disabled: true});
        last_clicked_tool = $("#draw-rectangle")
        polygonDrawer.disable();
        circleMarkerDrawer.disable();
        polylineDrawer.disable();
        polygon_state = false;
        rectangle_state = true;
        polyline_state = false;
        circleMarker_state = false;
        rectangleDrawer.enable();
    });

    $("#draw-circle").click(function () {
        annoClose();
        last_clicked_tool = $("#draw-circle")
        //$("#big-slider").draggable({disabled: true});
        rectangleDrawer.disable();
        polygonDrawer.disable();
        polylineDrawer.disable();
        polygon_state = false;
        rectangle_state = false;
        polyline_state = false;
        circleMarker_state = true;
        circleMarkerDrawer.enable();
    });

    $("#draw-marker").click(function () {
        last_clicked_tool = $("#draw-marker")
        //$("#big-slider").draggable({disabled: true});
        rectangleDrawer.disable();
        polygonDrawer.disable();
        circleMarkerDrawer.disable();
        polylineDrawer.disable();
        polygon_state = false;
        polyline_state = false;
        rectangle_state = false;
        circleMarker_state = false;
        annoCreate();
        $('.ul-fix-2 li:nth-child(3)').click();
        $("#big-slider-image").css("top", "0px");
        $("#big-slider-image").css("left", "0px");
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
        //$("#big-slider").draggable({disabled: false, containment: '.big-slider', scroll: false});
        /*$("#big-slider").draggable({
            start: function () {
                $('#big-slider-image').css('transform', 'scale(1)');
            },
            drag: function () {

            },
            stop: function () {
                $('#big-slider-image').css('transform', 'scale(' + zoom + ')');
            }
        });*/
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

    $(".slider1").slick({
        dots: false,
        autoplay: false,
        infinite: false,
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: false,
        fade: false,
        asNavFor: '.slider1-nav'
    });
    $('.slider1-nav').slick({
        slidesToShow: 8,
        slidesToScroll: 8,
        asNavFor: '.slider1',
        infinite: false,
        dots: false,
        focusOnSelect: true,
        responsive: [
            {
                breakpoint: 1024,
                settings: {
                    slidesToShow: 4,
                    slidesToScroll: 3
                }
            },
            {
                breakpoint: 600,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 2
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1
                }
            }
        ]
    });
});

// $(document).ready(function () {
//     $('#tableone').DataTable({
//         "info": false,
//         "searching": false
//     });
//     list_count = $("#s1nav-list").children().children().children();
//     $(list_count[0]).find('div:nth-child(2)').addClass("border-select");
//     $("#place").click();
//     $("#place2").click();
// });

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

function kaydet(label_db_id, a, get_right_id = 0) {
    if (get_right_id == 0) {
        if (!cizim_sayac == 0) {
            $(".list-is-clear").css('background-image', 'none');
            $(".list-is-clear").css('marginTop', '0px');
            $(".lic-text").css('display', 'none');
            $(".es-content").css('display', 'block');
            $(".es-content").append('<div class="row right-lbl-row" id="eklenenEtiket"><div class="col-12 etiketdivclass" id="etiketdiv" onmouseover="hoverOn(this.id)" onmouseout="hoverOff(this.id)"><label class="label-control4"><input class="label-do-' + String(cizim_sayac) + ' label-do-id-' + label_db_id + '" type="checkbox" id="etiket-check" onclick="layerSelect(this.id)"><span class="border-one background-one right-span" id="span-etiket"></span><span class="tq-color" id="right-span"></span><i src="eye.png" id="visibleImage" class="eyeImg" width="25" height="16" onclick="visibleOff(this.parentElement.firstChild.id,$(this).parent().parent().parent(),this)"></i><i src="delete.png" class="deleteImg" id="delImg" width="20" height="20" onclick="removeLayer(this.parentElement.firstChild.id,$(this).parent().parent().parent(),false)"></i><i src="edit.png" id="editImage" class="editImg" width="24" height="24" onclick="editLayer($(this).parent())"></i></label></div></div>');
            var e = document.getElementById("span-etiket");
            e.id = "span-etiket" + cizim_sayac;
            var a_id = a.id;
            e.textContent = $("#color" + label_db_id).parent().html().split('</span>')[1];
            var textcontent = e.textContent;
            var etk = document.getElementById("eklenenEtiket");
            etk.id = "eklenenEtiket" + cizim_sayac;
            var etkdiv = document.getElementById("etiketdiv");
            etkdiv.id = "etiketdiv" + cizim_sayac;
            var g = document.getElementById("etiket-check");
            g.id = "etiket-check" + cizim_sayac;
            var f = document.getElementById("right-span");
            f.id = "right-span" + cizim_sayac;
            $(f).css("left", "4px").css("bottom", "27px").css("padding", "10px 10px 5px 7px").css("background", rgbToHex(colorEl));
            if (a.className.includes('point')) {
                drawed_objects[cizim_sayac - 1]["layer"].setStyle({fillColor: rgbToHex(colorEl), color: "#000000"});
            } else {
                drawed_objects[cizim_sayac - 1]["layer"].setStyle({color: rgbToHex(colorEl)});
            }
            drawed_objects[drawed_objects.length - 1]["label"]["id"] = label_db_id
            drawed_objects[drawed_objects.length - 1]["label"]["color"] = rgbToHex(colorEl)
            drawed_objects[drawed_objects.length - 1]["label"]["name"] = textcontent
            drawed_objects[drawed_objects.length - 1]["label"]["rigth_label_list_id"] = cizim_sayac
            is_save_status = false;
            $("#draw-polygon").show()
            $("#draw-polyline").show()
            $("#draw-rectangle").show()
            $("#draw-circle").show()
            drawed_objects[drawed_objects.length - 1]["layer"].bindPopup(drawed_objects[drawed_objects.length - 1]["label"]["name"]);
            $(".leaflet-zoom-animated g path:last-child").addClass(etkdiv.id);
        } else {
            alert("Çizim Yapmadınız!");
            $('.tq-butx').removeClass("current");
            $('.tq-butx').next(".s-click-dropdown").fadeOut(100);
        }
        save_coordinates()
    } else {
        $(".list-is-clear").css('background-image', 'none');
        $(".list-is-clear").css('marginTop', '0px');
        $(".lic-text").css('display', 'none');
        $(".es-content").css('display', 'block');
        // $(".es-content").append('<div class="row right-lbl-row" id="eklenenEtiket"><div class="col-12 etiketdivclass" id="etiketdiv" onmouseover="hoverOn(this.id)" onmouseout="hoverOff(this.id)"><label class="label-control4"><input class="label-do-' + String(cizim_sayac) + ' label-do-id-' + label_db_id + '" type="checkbox" id="etiket-check" onclick="layerSelect(this.id)"><span class="border-one background-one right-span" id="span-etiket"></span><span class="tq-color" id="right-span"></span><i src="eye.png" id="visibleImage" class="eyeImg" width="25" height="16" onclick="visibleOff(this.parentElement.firstChild.id,$(this).parent().parent().parent(),this)"></i><i src="delete.png" class="deleteImg" id="delImg" width="20" height="20" onclick="removeLayer(this.parentElement.firstChild.id,$(this).parent().parent().parent(),false)"></i><i src="edit.png" id="editImage" class="editImg" width="24" height="24" onclick="editLayer($(this).parent())"></i></label></div></div>');
        // var e = document.getElementById("span-etiket" + right_id);
        // e.id = "span-etiket" + cizim_sayac;
        // var a_id = a.id;
        // e.textContent = $("#color" + label_db_id).parent().html().split('</span>')[1];
        // var textcontent = e.textContent;
        // var etk = document.getElementById("eklenenEtiket" + right_id);
        // etk.id = "eklenenEtiket" + cizim_sayac;
        // var g = document.getElementById("etiket-check" + right_id);
        // g.id = "etiket-check" + cizim_sayac;
        // var f = document.getElementById("right-span" + right_id);
        // f.id = "right-span" + cizim_sayac;
        if (drawed_objects[get_right_id - 1]["is_move"] === false && a !== false) {
            $(f).css("left", "4px").css("bottom", "27px").css("padding", "10px 10px 5px 7px").css("background", rgbToHex(colorEl));
            if (a.className.includes('point')) {
                drawed_objects[get_right_id - 1]["layer"].setStyle({fillColor: rgbToHex(colorEl), color: "#000000"});
            } else {
                drawed_objects[get_right_id - 1]["layer"].setStyle({color: rgbToHex(colorEl)});
            }
            drawed_objects[get_right_id - 1]["label"]["id"] = label_db_id
            drawed_objects[get_right_id - 1]["label"]["color"] = rgbToHex(colorEl)
            drawed_objects[get_right_id - 1]["label"]["name"] = textcontent
            is_save_status = false;
            save_coordinates(false, get_right_id)
            drawed_objects[get_right_id - 1]["layer"].bindPopup(drawed_objects[get_right_id - 1]["label"]["name"]);
            // var etkdiv = document.getElementById("etiketdiv" + get_right_id);
            // etkdiv.id = "etiketdiv" + cizim_sayac;
            // $(".leaflet-zoom-animated g path:last-child").addClass(etkdiv.id);
        } else {
            // var moved_color = drawed_objects[get_right_id-1]["label"]["color"];
            // $(f).css("left", "4px").css("bottom", "27px").css("padding", "10px 10px 5px 7px").css("background", rgbToHex(moved_color));
            // if (drawed_objects[get_right_id - 1]["marking_type"].includes('point')) {
            //     drawed_objects[get_right_id - 1]["layer"].setStyle({fillColor: rgbToHex(moved_color), color: "#000000"});
            // } else {
            //     drawed_objects[get_right_id - 1]["layer"].setStyle({color: rgbToHex(moved_color)});
            // }
            is_save_status = false;
            save_coordinates(false, get_right_id)
            drawed_objects[get_right_id - 1]["layer"].bindPopup(drawed_objects[get_right_id - 1]["label"]["name"]);
            // $(".leaflet-zoom-animated g path:last-child").addClass(etkdiv.id);
        }
        $("#draw-polygon").show()
        $("#draw-polyline").show()
        $("#draw-rectangle").show()
        $("#draw-circle").show()
    }
};

function layerSelect(id) {
    var textcontent = $("#" + id).parent().find("span")[0].textContent;
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
            //nokta
            drawed_objects[j - 1]["layer"]['_path'].attributes["stroke-width"].value = "2";
        } else {
            drawed_objects[j - 1]["layer"].setStyle({weight: 3});
            if (visibilityChange == true) {
                drawed_objects[j - 1]["layer"].pm.enable({
                    allowSelfIntersection: true,
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
            });
            editmode = false;
        }
    }
    map.pm.disableGlobalDragMode();
    drawed_objects[j - 1]["layer"].bindPopup(textcontent).openPopup();
}

var currentElement;

function checkColorChange(a) {
    label_db_id = a.id.split('color')[1]
    $(".lbl_checkbox:checkbox").prop("checked", false);
    if (right_id === 0) {
        $(a).prop("checked", true);
        $('.tq-butx').removeClass("current");
        $('.tq-butx').next(".s-click-dropdown").fadeOut(100);
        colorEl = $(a).parent().parent().parent().find('.tq-color')[0].style.background;
        kaydet(label_db_id, a);
    } else {
        if (drawed_objects[right_id - 1]["is_edited"]) {
            colorEl = $(a).parent().parent().parent().find('.tq-color')[0].style.background;
            var thisTextContent = $.trim($(a).parent().text());
            editLayerChange(colorEl, thisTextContent);
            kaydet(label_db_id, a, right_id);
            right_id = 0;
        }
    }
    $(".lbl_checkbox:checkbox").prop("checked", false);
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
        $(id3).addClass("ımgOff");
        $(id3).removeClass("ımgOn");
        visibilityChange = false;
        drawed_objects[j - 1]["layer"].editing.disable();
    } else if (drawed_objects[j - 1]["layer"].options.fillOpacity == "0") {
        if (drawed_objects[j - 1]["layer"].options.color == "#000000") {
            drawed_objects[j - 1]["layer"].setStyle({fillOpacity: 1});
        } else {
            drawed_objects[j - 1]["layer"].setStyle({fillOpacity: 0.2});
        }
        drawed_objects[j - 1]["layer"].setStyle({opacity: 1.0});
        $(id3).addClass("ımgOn");
        $(id3).removeClass("ımgOff");
        visibilityChange = true;
    } else if (drawed_objects[j - 1]["layer"]['_path'].attributes.d.value.length < 20) {
        // console.log("ilk else if")
        if (drawed_objects[j - 1]["layer"]['_path'].attributes["stroke-opacity"].value == 1) {
            // console.log("else-if^if")
            drawed_objects[j - 1]["layer"]['_path'].attributes["stroke-opacity"].value = "0";
            $(id3).addClass("ımgOff");
            $(id3).removeClass("ımgOn");
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
            $(id3).addClass("ımgOn");
            $(id3).removeClass("ımgOff");
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
        $(id3).addClass("ımgOff");
        $(id3).removeClass("ımgOn");
        visibilityChange = false;
    } else {
        for (var x = 0; x < drawed_objects.length; x++) {
            if (drawed_objects[x]["layer"] !== "") {
                if (drawed_objects[x]["layer"].options.color == "#000000") {
                    drawed_objects[x]["layer"].setStyle({fillOpacity: 1});
                } else {
                    drawed_objects[x]["layer"].setStyle({fillOpacity: 0.2});
                }
                drawed_objects[x]["layer"].setStyle({opacity: 1.0});
            }
        }
        $(id3).addClass("ımgOn");
        $(id3).removeClass("ımgOff");
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
                if (drawed_objects[j - 1]["layer"]){
                    drawed_objects[j - 1]["layer"].remove();
                }
                drawed_objects[j - 1]["layer"] = "";
                var etk = document.getElementById("eklenenEtiket" + j);
                etk.remove();
                delete_sayac += 1;
                is_save_status = true;
                right_id = 0;
            }
        })
    } else {
        var i = id.length;
        var j = id.split('check')[1];
        // var j = id.substr(12);
        // var c = $(id2).attr('id')
        // var k = c.length;
        // var l = c[k - 1];
        $("#sureDeleteJ").html(j)
        $("#sureDeleteL").html(label_id)
        $(location).attr('href', '#sureDelete');
    }
}

var var_edit_label_id
var right_id = 0

function editLayer(edit_label_id, e) {
    $(e).addClass("editLayerOn");
    right_id = e[0].children[0].id.split('check')[1]
    filter_label(drawed_objects[right_id-1]["marking_type"])
    drawed_objects[right_id - 1]["is_edited"] = true;
    var_edit_label_id = edit_label_id
    if (!$(".tq-butx").hasClass('current')) {
        $('.tq-butx').toggleClass("current");
        $('.tq-butx').next(".s-click-dropdown").fadeToggle(100);
    }
}

function editLayerChange(color, textContent) {
    var textContent = textContent;
    var color = color;
    $.ajax({
        url: "/api/editimagelabel/",
        method: "GET",
        data: {
            'image_label_id': var_edit_label_id,
        },
        success: function (res) {
            if ($(".tq-color").parent().hasClass("editLayerOn")) {
                var tqId = $(".editLayerOn .tq-color").attr('id');
                var j = tqId.replace("right-span", "");
                $(".editLayerOn").children()[1].textContent = textContent;
                $(".editLayerOn .tq-color").css("background", color);
            }
            color = rgbToHex(color);
            if (textContent.includes("Point")) {
                drawed_objects[j - 1]["layer"].setStyle({fillColor: color, color: "#000000"});
            } else {
                drawed_objects[j - 1]["layer"].setStyle({color: color});
            }
            if ($(".tq-butx").hasClass('current')) {
                $('.tq-butx').toggleClass("current");
                $('.tq-butx').next(".s-click-dropdown").fadeToggle(100);
            }
            $(".editLayerOn").removeClass("editLayerOn");
        }
    })
}

// var zoom = 1;
//
// $('.ul-fix-4 li:nth-child(1)').on('click', function () {
//     $("#place").click();
//     $("#place2").click();
//     zoom += 0.1;
//     $('#big-slider-image').css('transform', 'scale(' + zoom + ')');
// });
// $('.ul-fix-2 li:nth-child(2)').on('click', function () {
//     zoom = 1;
//     $(".ul-fix-5")[0].style.display = "none"
//     $(".ul-fix-4")[0].style.display = "none";
//     document.getElementById("sli1").style.filter = "contrast(100%)";
//     $('#big-slider-image').css('transform', 'scale(' + zoom + ')');
//     $("#big-slider-image").css("top", "0px");
//     $("#big-slider-image").css("left", "0px");
// });
// $('.ul-fix-4 li:nth-child(2)').on('click', function () {
//     $("#place").click();
//     $("#place2").click();
//     zoom -= 0.1;
//     $('#big-slider-image').css('transform', 'scale(' + zoom + ')');
// });

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

// $('.ul-fix-3 li:nth-child(3)').click(function () {
//     list_count = $("#s1nav-list").children().children().children();
//     label_count = $('#right-lbl-list').children();
//     //// console.log(!is_save_status, label_count.length);
//     // if (!is_save_status && label_count.length !== 0) {
//     //     go_after_delete = $(list_count[list_count_sayac + 1]).children().find('div');
//     //     setTimeout(function () {
//     //         document.location.href = "#want_save"
//         // }, 10);
//     // } else {
//     if (list_count.length - 1 > list_count_sayac) {
//         list_count_sayac += 1;
//         document.getElementsByClassName("ul-fix-input")[0].innerHTML = list_count_sayac + 1;
//         is_save_status = true;
//         clear_all()
//         set_background(_this = $(list_count[list_count_sayac]).children().find('div'));
//         for (var i = 0; i < list_count.length; i++) {
//             $(list_count[i]).find('div:nth-child(2)').removeClass("border-select");
//         }
//         for (var i = 0; i < drawed_objects.length; i++) {
//             if (drawed_objects[i]["layer"]) {
//                 drawed_objects[i]["layer"].remove();
//             }
//         }
//         for (var i = 0; i < drawed_objects.length; i++) {
//             drawed_objects.splice(drawed_objects.indexOf(0), 1);
//         }
//         var es_content = $('#right-lbl-list').children();
//         for (let i = 0; i < es_content.length; i++) {
//             es_content[i].remove();
//         }
//         $(list_count[list_count_sayac]).find('div:nth-child(2)').addClass("border-select");
//         cizim_sayac = 0;
//     }
//     // }
// })

function clear_all() {
    for (let i = 0; i < drawed_objects.length; i++) {
        if (drawed_objects[i]["layer"]){
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
        if (drawed_objects[i]["layer"]){
            drawed_objects[i]["layer"].remove();
        }
    }
    for (var i = 0; i < drawed_objects.length; i++) {
        drawed_objects.splice(drawed_objects.indexOf(0), 1);
    }
    drawed_objects = []
    createAnno_sayac = 0;
    cizim_sayac = 0;
    delete_sayac = 0;
    drawCounter = 1;
    annotations = anno.getAnnotations()
    for (let anno_index = 0; anno_index < annotations.length; anno_index++) {
        anno.removeAnnotation(annotations[anno_index]);
        $('svg[data-comment-id="' + annotations[anno_index].id + '"]').remove();
        $('g[data-id="' + annotations[anno_index].id + '"]').remove();
    }
}

// $('.ul-fix-3 li:nth-child(1)').click(function () {
//     list_count = $("#s1nav-list").children().children().children();
//     label_count = $('#right-lbl-list').children();
//
//     // if (!is_save_status && label_count.length !== 0) {
//     //     go_after_delete = $(list_count[list_count_sayac - 1]).children().find('div');
//     //     setTimeout(function () {
//     //         // document.location.href = "#want_save"
//     //     }, 10);
//     //
//     // } else {
//     if (list_count_sayac > 0) {
//         list_count_sayac -= 1;
//         document.getElementsByClassName("ul-fix-input")[0].innerHTML = list_count_sayac + 1;
//         is_save_status = true;
//         clear_all()
//         set_background(_this = $(list_count[list_count_sayac]).children().find('div'));
//         for (var i = 0; i < list_count.length; i++) {
//             $(list_count[i]).find('div:nth-child(2)').removeClass("border-select");
//         }
//         $(list_count[list_count_sayac]).find('div:nth-child(2)').addClass("border-select");
//         for (var i = 0; i < drawed_objects.length; i++) {
//             if (drawed_objects[i]["layer"]){
//                 drawed_objects[i]["layer"].remove();
//             }
//         }
//         for (var i = 0; i < drawed_objects.length; i++) {
//             drawed_objects.splice(drawed_objects.indexOf(0), 1);
//         }
//         var es_content = $('#right-lbl-list').children();
//         for (let i = 0; i < es_content.length; i++) {
//             es_content[i].remove();
//         }
//         cizim_sayac = 0;
//     }
//     // }
// })

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
    if (drawed_objects.length > $("#right-lbl-list").children().length + delete_sayac) {
        var i = drawed_objects.length;
        if (drawed_objects[i - 1]["layer"]){
            drawed_objects[i - 1]["layer"].remove();
        }
        drawed_objects.splice(drawed_objects.indexOf(0), 1);
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
        $("#place").click();
        $(".outline").click();
        right_id = 0;
        if ($(".tq-butx").hasClass('current')) {
            $(".tq-butx").click()
        }
    }
});
//var demo = wheelzoom(document.querySelector('img#sli1'));