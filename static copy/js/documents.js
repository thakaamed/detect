//sayfa geçişleri
$(".page-two-left-icon").click(function(){
    $(".page-two").addClass("d-none")
    $(".page-one").removeClass("d-none")
})
$(".page-one-right-icon").click(function(){
    $(".page-two").removeClass("d-none")
    $(".page-one").addClass("d-none")
})


function autoExpand(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}


// textarea için yazıldı  
var textareaName; 
$(".textarea-check-name").click(function(){
    textareaName = $(".textarea-name-one").val();
    console.log(textareaName);
    var documentsTextarea = $(".documents-name");
    documentsTextarea.val(textareaName);
});
var textareaTitle;
$(".textarea-check-title").click(function(){
    textareaTitle = $(".documents-title-text").val();
    console.log(textareaTitle);
    var documentsTitleTextarea = $(".documents-title-one");
    documentsTitleTextarea.val(textareaTitle);
});
var textareaTitleTwo;
$(".textarea-check-title-two").click(function(){
    textareaTitleTwo = $(".documents-title-text-two").val();
    console.log(textareaTitleTwo);
    var documentsTitleTextarea = $(".documents-title-two");
    documentsTitleTextarea.val(textareaTitleTwo);
});
var textareaParagraph;
$(".textarea-check-paragraph").click(function(){
    textareaParagraph = $(".documents-paragraph-text").val();
    console.log(textareaParagraph);
    var documentsTitleTextarea = $(".documents-append-paragraph");
    documentsTitleTextarea.val(textareaParagraph);
});

var textareaNamePage; 
$(".textarea-page-check-one").click(function(){
    textareaNamePage = $(".textarea-page-one").val();
    console.log(textareaNamePage);
    var documentsTextarea = $(".documents-page-one");
    documentsTextarea.val(textareaNamePage);
});
var textareaTitlePage;
$(".textarea-page-two").click(function(){
    textareaTitlePage = $(".documents-page-text-two").val();
    console.log(textareaTitlePage);
    var documentsTitleTextarea = $(".documents-page-two");
    documentsTitleTextarea.val(textareaTitlePage);
});
var textareaPageTwo;
$(".textarea-page-tree").click(function(){
    textareaPageTwo = $(".documents-page-text-tree").val();
    console.log(textareaPageTwo);
    var documentsPageTextarea = $(".documents-page-tree");
    documentsPageTextarea.val(textareaPageTwo);
});
var textareaParagraphPage;
$(".textarea-page-four").click(function(){
    textareaParagraphPage = $(".documents-page-text-four").val();
    console.log(textareaParagraphPage);
    var documentsTitleTextareaPage = $(".documents-page-four");
    documentsTitleTextareaPage.val(textareaParagraphPage);
});


$("#editDocumentTab").on("click", function() {
    $(".edit-documents-none").addClass("d-none")
    console.log("Edit Document tab tıklandı!");
});