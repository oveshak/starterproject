// console.log("✅ Purchase Variation JS Loaded");

// document.addEventListener("DOMContentLoaded", function () {
//     const productField = document.getElementById("id_purchase_product");
//     const variationField = document.getElementById("id_purchase_product_variation");

//     if (!productField || !variationField) return;

//     function resetVariation() {
//         variationField.innerHTML = '<option value="">---------</option>';
//     }

//     function loadVariations(productId) {
//         resetVariation();
//         if (!productId) return;

//         fetch(`/_admin/variations/?product=${productId}`)
//             .then(res => res.json())
//             .then(data => {
//                 data.forEach(v => {
//                     const opt = document.createElement("option");
//                     opt.value = v.id;
//                     opt.textContent = v.name;
//                     variationField.appendChild(opt);
//                 });
//             });
//     }

//     productField.addEventListener("change", function () {
//         loadVariations(this.value);
//     });
// });



console.log("✅ Purchase Variation JS Loaded");

document.addEventListener("DOMContentLoaded", function () {
    const productField = document.getElementById("id_purchase_product");
    const variationField = document.getElementById("id_purchase_product_variation");

    if (!productField || !variationField) return;

    function resetVariation() {
        variationField.innerHTML = '<option value="">---------</option>';
    }

    function loadVariations(productId) {
        resetVariation();
        if (!productId) return;

        fetch(`/admin/variations/?product=${productId}`)
            .then(res => res.json())
            .then(data => {
                data.forEach(v => {
                    const opt = document.createElement("option");
                    opt.value = v.id;
                    opt.textContent = v.name + (v.isunck ? " (Unique)" : "");
                    variationField.appendChild(opt);
                });
            });
    }

    productField.addEventListener("change", function () {
        loadVariations(this.value);
    });
});

