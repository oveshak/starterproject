// console.log("✅ product_variation.js LOADED (Purchase Admin)");


// document.addEventListener("DOMContentLoaded", function () {
//     const productField = document.getElementById("id_product_name");
//     const variationField = document.getElementById("id_product_variation");

//     if (!productField || !variationField) return;

//     function clearVariation() {
//         variationField.innerHTML = "";
//         const opt = document.createElement("option");
//         opt.value = "";
//         opt.textContent = "---------";
//         variationField.appendChild(opt);
//     }

//     function loadVariations(productId) {
//         clearVariation();

//         if (!productId) return;

//         fetch(`/admin/variations/?product=${productId}`)

//             .then(res => res.json())
//             .then(data => {
//                 data.forEach(v => {
//                     const opt = document.createElement("option");
//                     opt.value = v.id;
//                     opt.textContent = v.name || `Variation #${v.id}`;
//                     variationField.appendChild(opt);
//                 });
//             })
//             .catch(err => {
//                 console.error("Variation load error:", err);
//             });
//     }

//     // initial load (edit page)
//     if (productField.value) {
//         loadVariations(productField.value);
//     }

//     // on product change
//     productField.addEventListener("change", function () {
//         loadVariations(this.value);
//     });
// });


// console.log("✅ product_variation.js LOADED (BranchProductStock Admin)");

// document.addEventListener("DOMContentLoaded", function () {
//   const productField = document.getElementById("id_product_name");
//   const variationField = document.getElementById("id_product_variation");
//   const branchField = document.getElementById("id_stock_branch");
//   const qtyField = document.getElementById("id_quantity");

//   const unickFrom = document.getElementById("id_unickkey_from");
//   const unickTo = document.getElementById("id_unickkey_to");

//   if (!productField || !variationField) return;

//   let variationMeta = {}; // variationId -> {isunck: bool}

//   function clearSelect(selectEl) {
//     if (!selectEl) return;
//     selectEl.innerHTML = "";
//   }

//   function clearVariation() {
//     variationField.innerHTML = '<option value="">---------</option>';
//   }

//   function setQtyFromSelectedUnick() {
//     if (!unickTo || !qtyField) return;
//     qtyField.value = unickTo.options.length;
//   }

//   function enableQty(enable) {
//     if (!qtyField) return;
//     qtyField.disabled = !enable;
//   }

//   function loadVariations(productId) {
//     clearVariation();
//     variationMeta = {};

//     if (!productId) return;

//     fetch(`/admin/variations/?product=${productId}`)
//       .then(res => res.json())
//       .then(data => {
//         data.forEach(v => {
//           variationMeta[v.id] = { isunck: !!v.isunck };
//           const opt = document.createElement("option");
//           opt.value = v.id;
//           opt.textContent = v.name + (v.isunck ? " (Unique)" : "");
//           variationField.appendChild(opt);
//         });
//       });
//   }

//   function loadAvailableUnicks(variationId) {
//     if (!unickFrom || !unickTo) return;

//     // clear available list only; keep selected as-is
//     clearSelect(unickFrom);

//     const branchId = branchField ? branchField.value : "";
//     // edit page হলে stock_id পাঠাতে পারো (optional), না থাকলেও চলবে
//     const stockId = document.getElementById("id_id") ? document.getElementById("id_id").value : "";

//     const url = `/admin/unickkeys/?variation=${variationId}&branch=${branchId}&stock_id=${stockId}`;

//     fetch(url)
//       .then(res => res.json())
//       .then(data => {
//         data.forEach(u => {
//           const opt = document.createElement("option");
//           opt.value = u.id;
//           opt.textContent = u.text;
//           unickFrom.appendChild(opt);
//         });
//       });
//   }

//   function onVariationChange() {
//     const vid = variationField.value;
//     if (!vid) {
//       enableQty(true);
//       return;
//     }

//     const meta = variationMeta[vid];
//     const isunck = meta ? meta.isunck : false;

//     if (isunck) {
//       // unique হলে qty auto
//       enableQty(false);
//       loadAvailableUnicks(vid);
//       setQtyFromSelectedUnick();
//     } else {
//       // normal হলে qty manual
//       enableQty(true);
//     }
//   }

//   // product change -> variation load
//   productField.addEventListener("change", function () {
//     loadVariations(this.value);
//   });

//   // variation change -> unique logic
//   variationField.addEventListener("change", onVariationChange);

//   // when moving unicks between select boxes, update qty
//   if (unickTo) {
//     unickTo.addEventListener("change", setQtyFromSelectedUnick);
//   }
//   // filter_horizontal uses buttons; easiest: observe DOM changes
//   if (unickTo) {
//     const obs = new MutationObserver(setQtyFromSelectedUnick);
//     obs.observe(unickTo, { childList: true });
//   }

//   // initial load (edit page)
//   if (productField.value) loadVariations(productField.value);
// });








// console.log("✅ product_variation.js LOADED (BranchProductStock Admin)");

// document.addEventListener("DOMContentLoaded", function () {
//   const productField = document.getElementById("id_product_name");
//   const variationField = document.getElementById("id_product_variation");
//   const branchField = document.getElementById("id_stock_branch");
//   const qtyField = document.getElementById("id_quantity");

//   const unickFrom = document.getElementById("id_unickkey_from");
//   const unickTo = document.getElementById("id_unickkey_to");

//   if (!productField || !variationField) return;

//   let variationMeta = {}; // variationId -> { isunck: bool }

//   /* ----------------- helpers ----------------- */

//   function clearSelect(selectEl) {
//     if (!selectEl) return;
//     selectEl.innerHTML = "";
//   }

//   function clearVariation() {
//     variationField.innerHTML = '<option value="">---------</option>';
//   }

//   function setQtyFromSelectedUnick() {
//     if (!unickTo || !qtyField) return;
//     qtyField.value = unickTo.options.length;
//   }

//   function enableQty(enable) {
//     if (!qtyField) return;
//     qtyField.disabled = !enable;
//   }

//   /* ----------------- load variations by product ----------------- */

//   function loadVariations(productId) {
//     clearVariation();
//     variationMeta = {};

//     if (!productId) return;

//     fetch(`/admin/variations/?product=${productId}`)
//       .then(res => res.json())
//       .then(data => {
//         data.forEach(v => {
//           variationMeta[v.id] = { isunck: !!v.isunck };

//           const opt = document.createElement("option");
//           opt.value = v.id;
//           opt.textContent = v.name + (v.isunck ? " (Unique)" : "");
//           variationField.appendChild(opt);
//         });
//       });
//   }

//   /* ----------------- 🔥 NEW: load unickkey by variation ----------------- */

//   function loadAvailableUnicks(variationId) {
//     if (!unickFrom) return;

//     clearSelect(unickFrom);

//     if (!variationId) return;

//     // edit page support
//     const stockIdEl = document.getElementById("id_id");
//     const stockId = stockIdEl ? stockIdEl.value : "";

//     const url = `/admin/unickkeys/?variation=${variationId}&stock_id=${stockId}`;

//     fetch(url)
//       .then(res => res.json())
//       .then(data => {
//         data.forEach(u => {
//           const opt = document.createElement("option");
//           opt.value = u.id;
//           opt.textContent = u.text;
//           unickFrom.appendChild(opt);
//         });
//       })
//       .catch(err => console.error("Unick load error:", err));
//   }

//   /* ----------------- variation change logic ----------------- */

//   function onVariationChange() {
//     const vid = variationField.value;

//     if (!vid) {
//       enableQty(true);
//       return;
//     }

//     const meta = variationMeta[vid];
//     const isunck = meta ? meta.isunck : false;

//     if (isunck) {
//       // unique variation → qty auto + unick filter
//       enableQty(false);
//       loadAvailableUnicks(vid);
//       setQtyFromSelectedUnick();
//     } else {
//       // normal variation
//       enableQty(true);
//     }
//   }

//   /* ----------------- events ----------------- */

//   // product change → reload variations
//   productField.addEventListener("change", function () {
//     loadVariations(this.value);
//   });

//   // variation change → unique logic + unick filter
//   variationField.addEventListener("change", onVariationChange);

//   // when unick selected/removed → update qty
//   if (unickTo) {
//     const obs = new MutationObserver(setQtyFromSelectedUnick);
//     obs.observe(unickTo, { childList: true });
//   }

//   /* ----------------- initial load (edit page) ----------------- */

//   if (productField.value) {
//     loadVariations(productField.value);
//   }

//   if (variationField.value) {
//     onVariationChange();
//   }
// });


















// console.log("✅ product_variation.js LOADED (BranchProductStock Admin)");

// document.addEventListener("DOMContentLoaded", function () {
//   const productField = document.getElementById("id_product_name");
//   const variationField = document.getElementById("id_product_variation");
//   const branchField = document.getElementById("id_stock_branch");
//   const qtyField = document.getElementById("id_quantity");

//   const unickFrom = document.getElementById("id_unickkey_from"); // Available
//   const unickTo = document.getElementById("id_unickkey_to");     // Chosen

//   if (!productField || !variationField) return;

//   let variationMeta = {}; // variationId -> { isunck: bool }

//   /* ---------------- helpers ---------------- */

//   function clearSelect(selectEl) {
//     if (!selectEl) return;
//     selectEl.innerHTML = "";
//   }

//   function clearVariation() {
//     variationField.innerHTML = '<option value="">---------</option>';
//   }

//   function enableQty(enable) {
//     if (!qtyField) return;
//     qtyField.disabled = !enable;
//   }

//   function setQtyFromSelectedUnick() {
//     if (!unickTo || !qtyField) return;
//     qtyField.value = unickTo.options.length;
//   }

//   function getChosenUnickIds() {
//     if (!unickTo) return [];
//     return Array.from(unickTo.options).map(o => String(o.value));
//   }

//   /* ---------------- load variations by product ---------------- */

//   function loadVariations(productId) {
//     clearVariation();
//     variationMeta = {};

//     if (!productId) return;

//     fetch(`/admin/variations/?product=${productId}`)
//       .then(res => res.json())
//       .then(data => {
//         data.forEach(v => {
//           variationMeta[v.id] = { isunck: !!v.isunck };

//           const opt = document.createElement("option");
//           opt.value = v.id;
//           opt.textContent = v.name + (v.isunck ? " (Unique)" : "");
//           variationField.appendChild(opt);
//         });
//       })
//       .catch(err => console.error("Variation load error:", err));
//   }

//   /* ---------------- 🔥 load unickkey by variation (FIXED) ---------------- */

//   function loadAvailableUnicks(variationId) {
//     if (!unickFrom) return;

//     clearSelect(unickFrom);
//     if (!variationId) return;

//     const stockIdEl = document.getElementById("id_id");
//     const stockId = stockIdEl ? stockIdEl.value : "";

//     fetch(`/admin/unickkeys/?variation=${variationId}&stock_id=${stockId}`)
//       .then(res => res.json())
//       .then(data => {
//         const chosenIds = getChosenUnickIds(); // 🔥 already selected

//         data.forEach(u => {
//           // 🔥 FIX-1: already chosen unick Available এ দেখাবে না
//           if (chosenIds.includes(String(u.id))) return;

//           const opt = document.createElement("option");
//           opt.value = u.id;
//           opt.textContent = u.text;
//           unickFrom.appendChild(opt);
//         });
//       })
//       .catch(err => console.error("Unick load error:", err));
//   }

//   /* ---------------- variation change logic ---------------- */

//   function onVariationChange() {
//     const vid = variationField.value;

//     if (!vid) {
//       enableQty(true);
//       return;
//     }

//     const meta = variationMeta[vid];
//     const isunck = meta ? meta.isunck : false;

//     if (isunck) {
//       // 🔥 unique variation
//       enableQty(false);
//       loadAvailableUnicks(vid);
//       setQtyFromSelectedUnick();
//     } else {
//       // normal variation
//       enableQty(true);
//     }
//   }

//   /* ---------------- events ---------------- */

//   // product change → reload variations
//   productField.addEventListener("change", function () {
//     loadVariations(this.value);
//   });

//   // variation change → unique logic
//   variationField.addEventListener("change", onVariationChange);

//   // 🔥 FIX-2: when unick chosen/removed → qty auto update
//   if (unickTo) {
//     const obs = new MutationObserver(setQtyFromSelectedUnick);
//     obs.observe(unickTo, { childList: true });
//   }

//   /* ---------------- initial load (EDIT PAGE FIX) ---------------- */

//   if (productField.value) {
//     loadVariations(productField.value);
//   }

//   if (variationField.value) {
//     onVariationChange();
//   }

//   // 🔥 FIX-3: filter_horizontal late load issue
//   setTimeout(() => {
//     setQtyFromSelectedUnick();
//   }, 150);
// });




console.log("✅ BranchProductStock JS loaded");

document.addEventListener("DOMContentLoaded", function () {
  const productField = document.getElementById("id_product_name");
  const variationField = document.getElementById("id_product_variation");
  const qtyField = document.getElementById("id_quantity");

  const unickFrom = document.getElementById("id_unickkey_from");
  const unickTo = document.getElementById("id_unickkey_to");

  if (!productField || !variationField) return;

  let variationMeta = {};

  function setQty() {
    if (qtyField && unickTo) qtyField.value = unickTo.options.length;
  }

  function loadVariations(pid) {
    variationField.innerHTML = '<option value="">---------</option>';
    variationMeta = {};
    if (!pid) return;

    fetch(`/admin/variations/?product=${pid}`)
      .then(r => r.json())
      .then(data => {
        data.forEach(v => {
          variationMeta[v.id] = v.isunck;
          const o = document.createElement("option");
          o.value = v.id;
          o.textContent = v.name + (v.isunck ? " (Unique)" : "");
          variationField.appendChild(o);
        });
      });
  }

  function loadUnicks(vid) {
    if (!unickFrom) return;
    unickFrom.innerHTML = "";

    const stockId = document.getElementById("id_id")?.value || "";

    fetch(`/admin/unickkeys/?variation=${vid}&stock_id=${stockId}`)
      .then(r => r.json())
      .then(data => {
        const chosen = Array.from(unickTo.options).map(o => o.value);
        data.forEach(u => {
          if (chosen.includes(String(u.id))) return;
          const o = document.createElement("option");
          o.value = u.id;
          o.textContent = u.text;
          unickFrom.appendChild(o);
        });
      });
  }

  productField.addEventListener("change", () => loadVariations(productField.value));

  variationField.addEventListener("change", () => {
    const vid = variationField.value;
    if (!vid) return;

    if (variationMeta[vid]) {
      qtyField.disabled = true;
      loadUnicks(vid);
      setQty();
    } else {
      qtyField.disabled = false;
    }
  });

  if (unickTo) {
    new MutationObserver(setQty).observe(unickTo, { childList: true });
  }

  if (productField.value) loadVariations(productField.value);
});
