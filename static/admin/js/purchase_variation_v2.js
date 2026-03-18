// console.log(" Purchase Variation JS Loaded");

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



// console.log(" Purchase Variation JS Loaded");

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

//         fetch(`/admin/variations/?product=${productId}`)
//             .then(res => res.json())
//             .then(data => {
//                 data.forEach(v => {
//                     const opt = document.createElement("option");
//                     opt.value = v.id;
//                     opt.textContent = v.name + (v.isunck ? " (Unique)" : "");
//                     variationField.appendChild(opt);
//                 });
//             });
//     }

//     productField.addEventListener("change", function () {
//         loadVariations(this.value);
//     });
// });



// console.log("Purchase Variation JS Loaded");

// document.addEventListener("change", function (e) {

//     if (e.target.name.includes("purchase_product")) {

//         const productField = e.target;

//         const row = productField.closest("tr");

//         if (!row) return;

//         const variationField = row.querySelector(
//             "select[name$='purchase_product_variation']"
//         );

//         if (!variationField) return;

//         const productId = productField.value;

//         variationField.innerHTML = '<option value="">---------</option>';

//         if (!productId) return;

//         fetch(`/admin/variations/?product=${productId}`)
//             .then(res => res.json())
//             .then(data => {

//                 data.forEach(v => {

//                     const option = document.createElement("option");

//                     option.value = v.id;
//                     option.textContent = v.name + (v.isunck ? " (Unique)" : "");

//                     variationField.appendChild(option);
//                 });

//             })
//             .catch(err => console.error(err));
//     }

// });



console.log("Purchase Variation JS Loaded");

document.addEventListener("DOMContentLoaded", function () {
    const productField = document.querySelector("#id_purchase_product");
    const variationField = document.querySelector("#id_purchase_product_variation");

    if (!productField || !variationField) return;

    productField.addEventListener("change", function () {
        const productId = this.value;

        variationField.innerHTML = '<option value="">---------</option>';

        if (!productId) return;

        fetch(`/ajax/admin/variations/?product=${productId}`)
            .then((res) => res.json())
            .then((data) => {
                data.forEach((v) => {
                    const option = document.createElement("option");
                    option.value = v.id;
                    option.textContent = v.name + (v.isunck ? " (Unique)" : "");
                    variationField.appendChild(option);
                });
            })
            .catch((err) => console.error("Variation load error:", err));
    });
});