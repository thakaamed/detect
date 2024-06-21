document.addEventListener("DOMContentLoaded", function() {
    const subStarterItems = document.querySelectorAll(".table-sub-starter");
    const priceStarterItems = document.querySelectorAll(".table-price-starter");
    const getDemoItems = document.querySelectorAll(".get-demo");

    setEqualHeight(subStarterItems);
    setEqualHeight(priceStarterItems);
    setEqualHeight(getDemoItems);
});

function setEqualHeight(elements) {
    let maxHeight = 0;

    elements.forEach(function(item) {
        const itemHeight = item.clientHeight;
        if (itemHeight > maxHeight) {
            maxHeight = itemHeight;
        }
    });

    elements.forEach(function(item) {
        item.style.height = maxHeight + "px";
    });
}