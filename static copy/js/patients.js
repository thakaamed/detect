$(document).ready(function () {
    if (window.location.href.includes("/en/")) {
        var lang = "en"
    }
    else if (window.location.href.includes("/fr/")){
        var lang = "fr"
    }
    var hepsiText = lang === 'en' ? 'All' : 'Tous';
    var mydatatable = $('#example').DataTable({
        columnDefs: [
            {orderable: false, targets: [3, 7, 8]}
        ],
        language: {
            lengthMenu: '_MENU_',
            zeroRecords: lang === 'en' ? 'No records available' : 'Aucun document disponible',
            info: '_PAGE_ / _PAGES_ sayfa',
            infoEmpty: 'No records available',
            infoFiltered: '(filtered from _MAX_ total records)',
            "paginate": {
                "next": lang == "fr" ? "Suivant <i class='fa-solid fa-angle-right'></i>" : "Next <i class='fa-solid fa-angle-right'></i>",
                "previous": lang == "fr" ? "<i class='fa-solid fa-angle-left'></i> Précédent" : "<i class='fa-solid fa-angle-left'></i> Previous"
            }

        },
        lengthMenu: [[5, 10, 25, 50, -1], [5, 10, 25, 50, hepsiText]],
        "pageLength": userThemeChoices["page_length"] === hepsiText ? -1 : parseInt(userThemeChoices["page_length"]),
        initComplete: function () {
            // hasta listemedeki değer değiştiğinde veritabanındaki userthemeyi güncelleyen fonksiyon
            $('[name="example_length"]').change(function (e) {
                var csrfmiddlewaretoken= $('input[name=csrfmiddlewaretoken]').val()
                var page_length = $(e.target).val()
                $.ajax({
                    url: "/api/update_page_length",
                    method: "POST",
                    headers: { "X-CSRFToken": csrfmiddlewaretoken },
                    data: {
                        "page_length": page_length,
                    },
                    success: function (response) {
                    },
                    error: function (xhr, errmsg, err) {
                        console.log(xhr.status + ": " + xhr.responseText)
                        // Burada silme işlemi başarısızsa kullanıcıya bir hata mesajı gösterebilirsiniz
                    }
                })
            });
            $('#mySearchBox').on('keyup', function () {
                var value = $(this).val();
                mydatatable.search(value).draw();
                var searchTerm = $(this).val().toLowerCase();
                // Tüm kart öğelerini seçin
                $('.card-item').each(function () {
                    var name = $(this).find('.content-container p:first-child span').text().toLowerCase();
                    // İsim ve soyisim bilgilerinde arama yapın
                    if (name.indexOf(searchTerm) !== -1) {
                        $(this).show(); // Eşleşenleri görünür yapın
                    } else {
                        $(this).hide(); // Eşleşmeyenleri gizleyin
                    }
                });
            });
            $("#example_length").appendTo(".datatable-length-selectbox"); // select in yeri değişti
        }
    });
    
});



function toggleCardView() {
    // patients sayfasındaki itemları tablo yada card tasarımına değiştirir
    $(".view-icon").click(function () {
        var csrfmiddlewaretoken= $('input[name=csrfmiddlewaretoken]').val()
        $(".view-icon").removeClass("active");
        $(this).addClass("active");
        // $(".patient-view-container").hide();
        var card_view = $(this).data("view_type")
        if(card_view === 0) {
            // list view
            $("#example").removeClass("patient-card-view")
            $(".table-name-star-icon").hide()
        } else {
            // 1 gelir buda card view
            $("#example").addClass("patient-card-view")
            $(".table-name-star-icon").show()
        }
        $.ajax({
            url: "/api/change_card_view",
            method: "POST",
            headers: { "X-CSRFToken": csrfmiddlewaretoken },
            data: {
                "card_view": card_view,
            },
            success: function (response) {
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText)
            }
        })
        // $($(this).attr("data-type")).show();
    });
}

// function deletePatient() {
//   // patients sayfasında patient silmek için kullanılan fonksiyon
//   $("[data-btn-operation='delete-patient']").click(function(event) {
//     let patientId = $(event.target).closest(".modal-container").attr("data-patient-id")
//     console.log(`silinecek olan hastanın idsi : ${patientId}`)
//     $(event.target).closest(".modal-container").removeClass("active")
//   })
// }



// function change_favorite_status(patient_slug, e) {
//     $.ajax({
//         url: "/api/change_favorite_status/",
//         method: "GET",
//         data: {'patient_slug': patient_slug},
//         success: function (res) {
//             if (res['status']) {
//                 $(e.target).addClass("d-none")
//                 $(e.target + " + i").removeClass("d-none")
//
//             } else {
//                 alert("Unable to add to favourites.")
//             }
//
//         }
//     })
// }


$(document).ready(function () {
    toggleCardView(); // patients sayfasındaki itemların görünüm türünü değiştir
});

$(document).ready(function () {

    $("#radiography_types").on("change",function() {
        let selectValue = $(this).val()
        if(selectValue === '3') {
            // cbct

            // butonları göster gizle
            $("#CBCTUpload").removeClass("d-none")
            $("#filepondUploadButton").addClass("d-none")

            // formları göster gizle
            $("#dicomDropzone").removeClass("d-none")
            $("#uploadFilepond").addClass("d-none")
        } else {
            // diğerleri

            // butonları göster gizle
            $("#CBCTUpload").addClass("d-none")
            $("#filepondUploadButton").removeClass("d-none")

            // formları göster gizle
            $("#dicomDropzone").addClass("d-none")
            $("#uploadFilepond").removeClass("d-none")
        }
    })
    
})












