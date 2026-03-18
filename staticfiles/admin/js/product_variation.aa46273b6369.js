// // // // console.log(" product_variation.js LOADED (Purchase Admin)");


// // // // document.addEventListener("DOMContentLoaded", function () {
// // // //     const productField = document.getElementById("id_product_name");
// // // //     const variationField = document.getElementById("id_product_variation");

// // // //     if (!productField || !variationField) return;

// // // //     function clearVariation() {
// // // //         variationField.innerHTML = "";
// // // //         const opt = document.createElement("option");
// // // //         opt.value = "";
// // // //         opt.textContent = "---------";
// // // //         variationField.appendChild(opt);
// // // //     }

// // // //     function loadVariations(productId) {
// // // //         clearVariation();

// // // //         if (!productId) return;

// // // //         fetch(`/admin/variations/?product=${productId}`)

// // // //             .then(res => res.json())
// // // //             .then(data => {
// // // //                 data.forEach(v => {
// // // //                     const opt = document.createElement("option");
// // // //                     opt.value = v.id;
// // // //                     opt.textContent = v.name || `Variation #${v.id}`;
// // // //                     variationField.appendChild(opt);
// // // //                 });
// // // //             })
// // // //             .catch(err => {
// // // //                 console.error("Variation load error:", err);
// // // //             });
// // // //     }

// // // //     // initial load (edit page)
// // // //     if (productField.value) {
// // // //         loadVariations(productField.value);
// // // //     }

// // // //     // on product change
// // // //     productField.addEventListener("change", function () {
// // // //         loadVariations(this.value);
// // // //     });
// // // // });


// // // // console.log(" product_variation.js LOADED (BranchProductStock Admin)");

// // // // document.addEventListener("DOMContentLoaded", function () {
// // // //   const productField = document.getElementById("id_product_name");
// // // //   const variationField = document.getElementById("id_product_variation");
// // // //   const branchField = document.getElementById("id_stock_branch");
// // // //   const qtyField = document.getElementById("id_quantity");

// // // //   const unickFrom = document.getElementById("id_unickkey_from");
// // // //   const unickTo = document.getElementById("id_unickkey_to");

// // // //   if (!productField || !variationField) return;

// // // //   let variationMeta = {}; // variationId -> {isunck: bool}

// // // //   function clearSelect(selectEl) {
// // // //     if (!selectEl) return;
// // // //     selectEl.innerHTML = "";
// // // //   }

// // // //   function clearVariation() {
// // // //     variationField.innerHTML = '<option value="">---------</option>';
// // // //   }

// // // //   function setQtyFromSelectedUnick() {
// // // //     if (!unickTo || !qtyField) return;
// // // //     qtyField.value = unickTo.options.length;
// // // //   }

// // // //   function enableQty(enable) {
// // // //     if (!qtyField) return;
// // // //     qtyField.disabled = !enable;
// // // //   }

// // // //   function loadVariations(productId) {
// // // //     clearVariation();
// // // //     variationMeta = {};

// // // //     if (!productId) return;

// // // //     fetch(`/admin/variations/?product=${productId}`)
// // // //       .then(res => res.json())
// // // //       .then(data => {
// // // //         data.forEach(v => {
// // // //           variationMeta[v.id] = { isunck: !!v.isunck };
// // // //           const opt = document.createElement("option");
// // // //           opt.value = v.id;
// // // //           opt.textContent = v.name + (v.isunck ? " (Unique)" : "");
// // // //           variationField.appendChild(opt);
// // // //         });
// // // //       });
// // // //   }

// // // //   function loadAvailableUnicks(variationId) {
// // // //     if (!unickFrom || !unickTo) return;

// // // //     // clear available list only; keep selected as-is
// // // //     clearSelect(unickFrom);

// // // //     const branchId = branchField ? branchField.value : "";
// // // //     // edit page হলে stock_id পাঠাতে পারো (optional), না থাকলেও চলবে
// // // //     const stockId = document.getElementById("id_id") ? document.getElementById("id_id").value : "";

// // // //     const url = `/admin/unickkeys/?variation=${variationId}&branch=${branchId}&stock_id=${stockId}`;

// // // //     fetch(url)
// // // //       .then(res => res.json())
// // // //       .then(data => {
// // // //         data.forEach(u => {
// // // //           const opt = document.createElement("option");
// // // //           opt.value = u.id;
// // // //           opt.textContent = u.text;
// // // //           unickFrom.appendChild(opt);
// // // //         });
// // // //       });
// // // //   }

// // // //   function onVariationChange() {
// // // //     const vid = variationField.value;
// // // //     if (!vid) {
// // // //       enableQty(true);
// // // //       return;
// // // //     }

// // // //     const meta = variationMeta[vid];
// // // //     const isunck = meta ? meta.isunck : false;

// // // //     if (isunck) {
// // // //       // unique হলে qty auto
// // // //       enableQty(false);
// // // //       loadAvailableUnicks(vid);
// // // //       setQtyFromSelectedUnick();
// // // //     } else {
// // // //       // normal হলে qty manual
// // // //       enableQty(true);
// // // //     }
// // // //   }

// // // //   // product change -> variation load
// // // //   productField.addEventListener("change", function () {
// // // //     loadVariations(this.value);
// // // //   });

// // // //   // variation change -> unique logic
// // // //   variationField.addEventListener("change", onVariationChange);

// // // //   // when moving unicks between select boxes, update qty
// // // //   if (unickTo) {
// // // //     unickTo.addEventListener("change", setQtyFromSelectedUnick);
// // // //   }
// // // //   // filter_horizontal uses buttons; easiest: observe DOM changes
// // // //   if (unickTo) {
// // // //     const obs = new MutationObserver(setQtyFromSelectedUnick);
// // // //     obs.observe(unickTo, { childList: true });
// // // //   }

// // // //   // initial load (edit page)
// // // //   if (productField.value) loadVariations(productField.value);
// // // // });








// // // // console.log(" product_variation.js LOADED (BranchProductStock Admin)");

// // // // document.addEventListener("DOMContentLoaded", function () {
// // // //   const productField = document.getElementById("id_product_name");
// // // //   const variationField = document.getElementById("id_product_variation");
// // // //   const branchField = document.getElementById("id_stock_branch");
// // // //   const qtyField = document.getElementById("id_quantity");

// // // //   const unickFrom = document.getElementById("id_unickkey_from");
// // // //   const unickTo = document.getElementById("id_unickkey_to");

// // // //   if (!productField || !variationField) return;

// // // //   let variationMeta = {}; // variationId -> { isunck: bool }

// // // //   /* ----------------- helpers ----------------- */

// // // //   function clearSelect(selectEl) {
// // // //     if (!selectEl) return;
// // // //     selectEl.innerHTML = "";
// // // //   }

// // // //   function clearVariation() {
// // // //     variationField.innerHTML = '<option value="">---------</option>';
// // // //   }

// // // //   function setQtyFromSelectedUnick() {
// // // //     if (!unickTo || !qtyField) return;
// // // //     qtyField.value = unickTo.options.length;
// // // //   }

// // // //   function enableQty(enable) {
// // // //     if (!qtyField) return;
// // // //     qtyField.disabled = !enable;
// // // //   }

// // // //   /* ----------------- load variations by product ----------------- */

// // // //   function loadVariations(productId) {
// // // //     clearVariation();
// // // //     variationMeta = {};

// // // //     if (!productId) return;

// // // //     fetch(`/admin/variations/?product=${productId}`)
// // // //       .then(res => res.json())
// // // //       .then(data => {
// // // //         data.forEach(v => {
// // // //           variationMeta[v.id] = { isunck: !!v.isunck };

// // // //           const opt = document.createElement("option");
// // // //           opt.value = v.id;
// // // //           opt.textContent = v.name + (v.isunck ? " (Unique)" : "");
// // // //           variationField.appendChild(opt);
// // // //         });
// // // //       });
// // // //   }

// // // //   /* ----------------- 🔥 NEW: load unickkey by variation ----------------- */

// // // //   function loadAvailableUnicks(variationId) {
// // // //     if (!unickFrom) return;

// // // //     clearSelect(unickFrom);

// // // //     if (!variationId) return;

// // // //     // edit page support
// // // //     const stockIdEl = document.getElementById("id_id");
// // // //     const stockId = stockIdEl ? stockIdEl.value : "";

// // // //     const url = `/admin/unickkeys/?variation=${variationId}&stock_id=${stockId}`;

// // // //     fetch(url)
// // // //       .then(res => res.json())
// // // //       .then(data => {
// // // //         data.forEach(u => {
// // // //           const opt = document.createElement("option");
// // // //           opt.value = u.id;
// // // //           opt.textContent = u.text;
// // // //           unickFrom.appendChild(opt);
// // // //         });
// // // //       })
// // // //       .catch(err => console.error("Unick load error:", err));
// // // //   }

// // // //   /* ----------------- variation change logic ----------------- */

// // // //   function onVariationChange() {
// // // //     const vid = variationField.value;

// // // //     if (!vid) {
// // // //       enableQty(true);
// // // //       return;
// // // //     }

// // // //     const meta = variationMeta[vid];
// // // //     const isunck = meta ? meta.isunck : false;

// // // //     if (isunck) {
// // // //       // unique variation → qty auto + unick filter
// // // //       enableQty(false);
// // // //       loadAvailableUnicks(vid);
// // // //       setQtyFromSelectedUnick();
// // // //     } else {
// // // //       // normal variation
// // // //       enableQty(true);
// // // //     }
// // // //   }

// // // //   /* ----------------- events ----------------- */

// // // //   // product change → reload variations
// // // //   productField.addEventListener("change", function () {
// // // //     loadVariations(this.value);
// // // //   });

// // // //   // variation change → unique logic + unick filter
// // // //   variationField.addEventListener("change", onVariationChange);

// // // //   // when unick selected/removed → update qty
// // // //   if (unickTo) {
// // // //     const obs = new MutationObserver(setQtyFromSelectedUnick);
// // // //     obs.observe(unickTo, { childList: true });
// // // //   }

// // // //   /* ----------------- initial load (edit page) ----------------- */

// // // //   if (productField.value) {
// // // //     loadVariations(productField.value);
// // // //   }

// // // //   if (variationField.value) {
// // // //     onVariationChange();
// // // //   }
// // // // });


















// // // // console.log(" product_variation.js LOADED (BranchProductStock Admin)");

// // // // document.addEventListener("DOMContentLoaded", function () {
// // // //   const productField = document.getElementById("id_product_name");
// // // //   const variationField = document.getElementById("id_product_variation");
// // // //   const branchField = document.getElementById("id_stock_branch");
// // // //   const qtyField = document.getElementById("id_quantity");

// // // //   const unickFrom = document.getElementById("id_unickkey_from"); // Available
// // // //   const unickTo = document.getElementById("id_unickkey_to");     // Chosen

// // // //   if (!productField || !variationField) return;

// // // //   let variationMeta = {}; // variationId -> { isunck: bool }

// // // //   /* ---------------- helpers ---------------- */

// // // //   function clearSelect(selectEl) {
// // // //     if (!selectEl) return;
// // // //     selectEl.innerHTML = "";
// // // //   }

// // // //   function clearVariation() {
// // // //     variationField.innerHTML = '<option value="">---------</option>';
// // // //   }

// // // //   function enableQty(enable) {
// // // //     if (!qtyField) return;
// // // //     qtyField.disabled = !enable;
// // // //   }

// // // //   function setQtyFromSelectedUnick() {
// // // //     if (!unickTo || !qtyField) return;
// // // //     qtyField.value = unickTo.options.length;
// // // //   }

// // // //   function getChosenUnickIds() {
// // // //     if (!unickTo) return [];
// // // //     return Array.from(unickTo.options).map(o => String(o.value));
// // // //   }

// // // //   /* ---------------- load variations by product ---------------- */

// // // //   function loadVariations(productId) {
// // // //     clearVariation();
// // // //     variationMeta = {};

// // // //     if (!productId) return;

// // // //     fetch(`/admin/variations/?product=${productId}`)
// // // //       .then(res => res.json())
// // // //       .then(data => {
// // // //         data.forEach(v => {
// // // //           variationMeta[v.id] = { isunck: !!v.isunck };

// // // //           const opt = document.createElement("option");
// // // //           opt.value = v.id;
// // // //           opt.textContent = v.name + (v.isunck ? " (Unique)" : "");
// // // //           variationField.appendChild(opt);
// // // //         });
// // // //       })
// // // //       .catch(err => console.error("Variation load error:", err));
// // // //   }

// // // //   /* ---------------- 🔥 load unickkey by variation (FIXED) ---------------- */

// // // //   function loadAvailableUnicks(variationId) {
// // // //     if (!unickFrom) return;

// // // //     clearSelect(unickFrom);
// // // //     if (!variationId) return;

// // // //     const stockIdEl = document.getElementById("id_id");
// // // //     const stockId = stockIdEl ? stockIdEl.value : "";

// // // //     fetch(`/admin/unickkeys/?variation=${variationId}&stock_id=${stockId}`)
// // // //       .then(res => res.json())
// // // //       .then(data => {
// // // //         const chosenIds = getChosenUnickIds(); // 🔥 already selected

// // // //         data.forEach(u => {
// // // //           // 🔥 FIX-1: already chosen unick Available এ দেখাবে না
// // // //           if (chosenIds.includes(String(u.id))) return;

// // // //           const opt = document.createElement("option");
// // // //           opt.value = u.id;
// // // //           opt.textContent = u.text;
// // // //           unickFrom.appendChild(opt);
// // // //         });
// // // //       })
// // // //       .catch(err => console.error("Unick load error:", err));
// // // //   }

// // // //   /* ---------------- variation change logic ---------------- */

// // // //   function onVariationChange() {
// // // //     const vid = variationField.value;

// // // //     if (!vid) {
// // // //       enableQty(true);
// // // //       return;
// // // //     }

// // // //     const meta = variationMeta[vid];
// // // //     const isunck = meta ? meta.isunck : false;

// // // //     if (isunck) {
// // // //       // 🔥 unique variation
// // // //       enableQty(false);
// // // //       loadAvailableUnicks(vid);
// // // //       setQtyFromSelectedUnick();
// // // //     } else {
// // // //       // normal variation
// // // //       enableQty(true);
// // // //     }
// // // //   }

// // // //   /* ---------------- events ---------------- */

// // // //   // product change → reload variations
// // // //   productField.addEventListener("change", function () {
// // // //     loadVariations(this.value);
// // // //   });

// // // //   // variation change → unique logic
// // // //   variationField.addEventListener("change", onVariationChange);

// // // //   // 🔥 FIX-2: when unick chosen/removed → qty auto update
// // // //   if (unickTo) {
// // // //     const obs = new MutationObserver(setQtyFromSelectedUnick);
// // // //     obs.observe(unickTo, { childList: true });
// // // //   }

// // // //   /* ---------------- initial load (EDIT PAGE FIX) ---------------- */

// // // //   if (productField.value) {
// // // //     loadVariations(productField.value);
// // // //   }

// // // //   if (variationField.value) {
// // // //     onVariationChange();
// // // //   }

// // // //   // 🔥 FIX-3: filter_horizontal late load issue
// // // //   setTimeout(() => {
// // // //     setQtyFromSelectedUnick();
// // // //   }, 150);
// // // // });




// // // // console.log(" BranchProductStock JS loaded");

// // // // document.addEventListener("DOMContentLoaded", function () {
// // // //   const productField = document.getElementById("id_product_name");
// // // //   const variationField = document.getElementById("id_product_variation");
// // // //   const qtyField = document.getElementById("id_quantity");

// // // //   const unickFrom = document.getElementById("id_unickkey_from");
// // // //   const unickTo = document.getElementById("id_unickkey_to");

// // // //   if (!productField || !variationField) return;

// // // //   let variationMeta = {};

// // // //   function setQty() {
// // // //     if (qtyField && unickTo) qtyField.value = unickTo.options.length;
// // // //   }

// // // //   function loadVariations(pid) {
// // // //     variationField.innerHTML = '<option value="">---------</option>';
// // // //     variationMeta = {};
// // // //     if (!pid) return;

// // // //     fetch(`/admin/variations/?product=${pid}`)
// // // //       .then(r => r.json())
// // // //       .then(data => {
// // // //         data.forEach(v => {
// // // //           variationMeta[v.id] = v.isunck;
// // // //           const o = document.createElement("option");
// // // //           o.value = v.id;
// // // //           o.textContent = v.name + (v.isunck ? " (Unique)" : "");
// // // //           variationField.appendChild(o);
// // // //         });
// // // //       });
// // // //   }

// // // //   function loadUnicks(vid) {
// // // //     if (!unickFrom) return;
// // // //     unickFrom.innerHTML = "";

// // // //     const stockId = document.getElementById("id_id")?.value || "";

// // // //     fetch(`/admin/unickkeys/?variation=${vid}&stock_id=${stockId}`)
// // // //       .then(r => r.json())
// // // //       .then(data => {
// // // //         const chosen = Array.from(unickTo.options).map(o => o.value);
// // // //         data.forEach(u => {
// // // //           if (chosen.includes(String(u.id))) return;
// // // //           const o = document.createElement("option");
// // // //           o.value = u.id;
// // // //           o.textContent = u.text;
// // // //           unickFrom.appendChild(o);
// // // //         });
// // // //       });
// // // //   }

// // // //   productField.addEventListener("change", () => loadVariations(productField.value));

// // // //   variationField.addEventListener("change", () => {
// // // //     const vid = variationField.value;
// // // //     if (!vid) return;

// // // //     if (variationMeta[vid]) {
// // // //       qtyField.disabled = true;
// // // //       loadUnicks(vid);
// // // //       setQty();
// // // //     } else {
// // // //       qtyField.disabled = false;
// // // //     }
// // // //   });

// // // //   if (unickTo) {
// // // //     new MutationObserver(setQty).observe(unickTo, { childList: true });
// // // //   }

// // // //   if (productField.value) loadVariations(productField.value);
// // // // });




// // // // console.log(" BranchProductStock Variation JS Loaded");

// // // // document.addEventListener("DOMContentLoaded", function () {

// // // //   const productField   = document.getElementById("id_product_name");
// // // //   const variationField = document.getElementById("id_product_variation");
// // // //   const qtyField       = document.getElementById("id_quantity");

// // // //   const unickFrom = document.getElementById("id_unickkey_from");
// // // //   const unickTo   = document.getElementById("id_unickkey_to");

// // // //   if (!productField || !variationField) return;

// // // //   let variationMeta = {};

// // // //   function setQtyFromUnicks() {
// // // //     if (qtyField && unickTo) {
// // // //       qtyField.value = unickTo.options.length;
// // // //     }
// // // //   }

// // // //   // 🔹 Load variations by product
// // // //   function loadVariations(productId) {
// // // //     variationField.innerHTML = '<option value="">---------</option>';
// // // //     variationMeta = {};

// // // //     if (!productId) return;

// // // //     fetch(`/admin/variations/?product=${productId}`)
// // // //       .then(r => r.json())
// // // //       .then(data => {
// // // //         data.forEach(v => {
// // // //           variationMeta[v.id] = v.isunck;

// // // //           const opt = document.createElement("option");
// // // //           opt.value = v.id;
// // // //           opt.textContent = v.name + (v.isunck ? " (Unique)" : "");
// // // //           variationField.appendChild(opt);
// // // //         });
// // // //       });
// // // //   }

// // // //   // 🔹 Load unickkeys (exclude already-used ones)
// // // //   function loadUnicks(variationId) {
// // // //     if (!unickFrom) return;

// // // //     unickFrom.innerHTML = "";

// // // //     const stockId = document.getElementById("id_id")?.value || "";

// // // //     fetch(`/admin/unickkeys/?variation=${variationId}&stock_id=${stockId}`)
// // // //       .then(r => r.json())
// // // //       .then(data => {
// // // //         const selected = Array.from(unickTo.options).map(o => o.value);

// // // //         data.forEach(u => {
// // // //           if (selected.includes(String(u.id))) return;

// // // //           const opt = document.createElement("option");
// // // //           opt.value = u.id;
// // // //           opt.textContent = u.text;
// // // //           unickFrom.appendChild(opt);
// // // //         });
// // // //       });
// // // //   }

// // // //   // 🔹 Events
// // // //   productField.addEventListener("change", () => {
// // // //     loadVariations(productField.value);
// // // //   });

// // // //   variationField.addEventListener("change", () => {
// // // //     const vid = variationField.value;
// // // //     if (!vid) return;

// // // //     if (variationMeta[vid]) {
// // // //       qtyField.disabled = true;
// // // //       loadUnicks(vid);
// // // //       setQtyFromUnicks();
// // // //     } else {
// // // //       qtyField.disabled = false;
// // // //     }
// // // //   });

// // // //   // auto update qty when unick changes
// // // //   if (unickTo) {
// // // //     new MutationObserver(setQtyFromUnicks).observe(unickTo, { childList: true });
// // // //   }

// // // //   // edit page support
// // // //   if (productField.value) {
// // // //     loadVariations(productField.value);
// // // //   }
// // // // });


// // // // console.log(" BranchProductStock Variation JS Loaded");

// // // // document.addEventListener("DOMContentLoaded", function () {

// // // //   const productField   = document.getElementById("id_product_name");
// // // //   const variationField = document.getElementById("id_product_variation");
// // // //   const qtyField       = document.getElementById("id_quantity");

// // // //   const unickFrom = document.getElementById("id_unickkey_from");

// // // //   if (!productField || !variationField) return;

// // // //   let variationMeta = {};

// // // //   // Load variations by product
// // // //   function loadVariations(productId) {
// // // //     variationField.innerHTML = '<option value="">---------</option>';
// // // //     variationMeta = {};

// // // //     if (!productId) return;

// // // //     fetch(`/admin/variations/?product=${productId}`)
// // // //       .then(r => r.json())
// // // //       .then(data => {
// // // //         data.forEach(v => {
// // // //           variationMeta[v.id] = v.isunck;
// // // //           const opt = document.createElement("option");
// // // //           opt.value = v.id;
// // // //           opt.textContent = v.name + (v.isunck ? " (Unique)" : "");
// // // //           variationField.appendChild(opt);
// // // //         });
// // // //       });
// // // //   }

// // // //   // Load unickkeys (ONLY left box)
// // // //   function loadUnicks(variationId) {
// // // //     if (!unickFrom) return;

// // // //     unickFrom.innerHTML = "";

// // // //     const stockId = document.getElementById("id_id")?.value || "";

// // // //     fetch(`/admin/unickkeys/?variation=${variationId}&stock_id=${stockId}`)
// // // //       .then(r => r.json())
// // // //       .then(data => {
// // // //         data.forEach(u => {
// // // //           const opt = document.createElement("option");
// // // //           opt.value = u.id;
// // // //           opt.textContent = u.text;
// // // //           unickFrom.appendChild(opt);
// // // //         });
// // // //       });
// // // //   }

// // // //   productField.addEventListener("change", () => {
// // // //     loadVariations(productField.value);
// // // //   });

// // // //   variationField.addEventListener("change", () => {
// // // //     const vid = variationField.value;
// // // //     if (!vid) return;

// // // //     if (variationMeta[vid]) {
// // // //       qtyField.disabled = true;
// // // //       loadUnicks(vid);
// // // //     } else {
// // // //       qtyField.disabled = false;
// // // //     }
// // // //   });

// // // //   // quantity auto sync when arrows clicked
// // // //   document.addEventListener("click", function (e) {
// // // //     if (e.target.classList.contains("selector-add") ||
// // // //         e.target.classList.contains("selector-remove")) {

// // // //       const to = document.getElementById("id_unickkey_to");
// // // //       if (to && qtyField) {
// // // //         qtyField.value = to.options.length;
// // // //       }
// // // //     }
// // // //   });

// // // //   // edit page support
// // // //   if (productField.value) {
// // // //     loadVariations(productField.value);
// // // //   }
// // // // });



// // // // console.log(" product_variation.js LOADED");

// // // // document.addEventListener("DOMContentLoaded", function () {
// // // //   console.log(" DOMContentLoaded fired");

// // // //   const productField   = document.getElementById("id_product_name");
// // // //   const variationField = document.getElementById("id_product_variation");
// // // //   const qtyField       = document.getElementById("id_quantity");
// // // //   const unickFrom      = document.getElementById("id_unickkey_from");

// // // //   console.log("productField =", productField);
// // // //   console.log("variationField =", variationField);
// // // //   console.log("unickFrom =", unickFrom);

// // // //   if (!productField || !variationField) {
// // // //     console.error(" productField or variationField NOT FOUND");
// // // //     return;
// // // //   }

// // // //   let variationMeta = {};

// // // //   // -----------------------------
// // // //   function loadVariations(productId) {
// // // //     console.log("➡️ loadVariations called, productId =", productId);

// // // //     variationField.innerHTML = '<option value="">---------</option>';
// // // //     variationMeta = {};

// // // //     if (!productId) {
// // // //       console.warn("⚠️ No productId, skipping");
// // // //       return;
// // // //     }

// // // //     const url = `/admin/variations/?product=${productId}`;
// // // //     console.log("🌐 Fetching variations:", url);

// // // //     fetch(url)
// // // //       .then(r => {
// // // //         console.log("⬅️ variation response status:", r.status);
// // // //         return r.json();
// // // //       })
// // // //       .then(data => {
// // // //         console.log(" variation data =", data);

// // // //         data.forEach(v => {
// // // //           variationMeta[v.id] = v.isunck;
// // // //           const opt = document.createElement("option");
// // // //           opt.value = v.id;
// // // //           opt.textContent = v.name + (v.isunck ? " (Unique)" : "");
// // // //           variationField.appendChild(opt);
// // // //         });
// // // //       })
// // // //       .catch(err => {
// // // //         console.error(" variation fetch error:", err);
// // // //       });
// // // //   }

// // // //   // -----------------------------
// // // //   function loadUnicks(variationId) {
// // // //     console.log("➡️ loadUnicks called, variationId =", variationId);

// // // //     if (!unickFrom) {
// // // //       console.error(" unickFrom NOT FOUND");
// // // //       return;
// // // //     }

// // // //     unickFrom.innerHTML = "";

// // // //     const stockId = document.getElementById("id_id")?.value || "";
// // // //     const url = `/admin/unickkeys/?variation=${variationId}&stock_id=${stockId}`;

// // // //     console.log("🌐 Fetching unicks:", url);

// // // //     fetch(url)
// // // //       .then(r => {
// // // //         console.log("⬅️ unick response status:", r.status);
// // // //         return r.json();
// // // //       })
// // // //       .then(data => {
// // // //         console.log(" unick data =", data);

// // // //         if (!data.length) {
// // // //           console.warn("⚠️ No unick returned from backend");
// // // //         }

// // // //         data.forEach(u => {
// // // //           console.log("➕ adding unick:", u);
// // // //           const opt = document.createElement("option");
// // // //           opt.value = u.id;
// // // //           opt.textContent = u.text;
// // // //           unickFrom.appendChild(opt);
// // // //         });
// // // //       })
// // // //       .catch(err => {
// // // //         console.error(" unick fetch error:", err);
// // // //       });
// // // //   }

// // // //   // -----------------------------
// // // //   productField.addEventListener("change", () => {
// // // //     console.log("🟡 product changed:", productField.value);
// // // //     loadVariations(productField.value);
// // // //   });

// // // //   variationField.addEventListener("change", () => {
// // // //     const vid = variationField.value;
// // // //     console.log("🟡 variation changed:", vid);

// // // //     if (!vid) return;

// // // //     console.log("variationMeta =", variationMeta);

// // // //     if (variationMeta[vid]) {
// // // //       console.log("🔐 isunck = TRUE → loading unicks");
// // // //       qtyField.disabled = true;
// // // //       loadUnicks(vid);
// // // //     } else {
// // // //       console.log("🔓 isunck = FALSE");
// // // //       qtyField.disabled = false;
// // // //     }
// // // //   });

// // // //   // -----------------------------
// // // //   if (productField.value) {
// // // //     console.log("🟡 edit page detected, product =", productField.value);
// // // //     loadVariations(productField.value);
// // // //   }
// // // // });



// // // // console.log(" product_variation.js LOADED");

// // // // document.addEventListener("DOMContentLoaded", function () {
// // // //   console.log(" DOMContentLoaded fired");

// // // //   const productField   = document.getElementById("id_product_name");
// // // //   const variationField = document.getElementById("id_product_variation");
// // // //   const qtyField       = document.getElementById("id_quantity");

// // // //   //  M2M field (works even if filter_horizontal not showing from/to)
// // // //   const unickSelect = document.getElementById("id_unickkey");

// // // //   console.log("productField =", productField);
// // // //   console.log("variationField =", variationField);
// // // //   console.log("unickSelect =", unickSelect);

// // // //   if (!productField || !variationField) {
// // // //     console.error(" productField or variationField NOT FOUND");
// // // //     return;
// // // //   }

// // // //   let variationMeta = {};

// // // //   function clearSelect(sel) {
// // // //     if (!sel) return;
// // // //     sel.innerHTML = "";
// // // //   }

// // // //   function syncQtyWithUnicks() {
// // // //     if (!unickSelect) return;
// // // //     qtyField.value = [...unickSelect.options].filter(o => o.selected).length;
// // // //   }

// // // //   function loadVariations(productId) {
// // // //     variationField.innerHTML = '<option value="">---------</option>';
// // // //     variationMeta = {};

// // // //     if (!productId) return;

// // // //     fetch(`/admin/variations/?product=${productId}`)
// // // //       .then(r => r.json())
// // // //       .then(data => {
// // // //         data.forEach(v => {
// // // //           variationMeta[String(v.id)] = v.isunck;
// // // //           const opt = document.createElement("option");
// // // //           opt.value = v.id;
// // // //           opt.textContent = v.name + (v.isunck ? " (Unique)" : "");
// // // //           variationField.appendChild(opt);
// // // //         });
// // // //       })
// // // //       .catch(err => console.error(" variation fetch error:", err));
// // // //   }

// // // //   function loadUnicks(variationId) {
// // // //     if (!unickSelect) {
// // // //       console.error(" id_unickkey NOT FOUND (unick field not rendered?)");
// // // //       return;
// // // //     }

// // // //     clearSelect(unickSelect);
// // // //     syncQtyWithUnicks();

// // // //     const stockId = document.getElementById("id_id")?.value || "";
// // // //     const url = `/admin/unickkeys/?variation=${variationId}&stock_id=${stockId}`;

// // // //     console.log("🌐 Fetching unicks:", url);

// // // //     fetch(url)
// // // //       .then(r => r.json())
// // // //       .then(data => {
// // // //         console.log(" unick data =", data);

// // // //         data.forEach(u => {
// // // //           const opt = document.createElement("option");
// // // //           opt.value = u.id;
// // // //           opt.textContent = u.text;
// // // //           unickSelect.appendChild(opt);
// // // //         });

// // // //         syncQtyWithUnicks();
// // // //       })
// // // //       .catch(err => console.error(" unick fetch error:", err));
// // // //   }

// // // //   productField.addEventListener("change", () => {
// // // //     console.log("🟡 product changed:", productField.value);
// // // //     loadVariations(productField.value);

// // // //     qtyField.disabled = false;
// // // //     if (unickSelect) clearSelect(unickSelect);
// // // //   });

// // // //   variationField.addEventListener("change", () => {
// // // //     const vid = String(variationField.value || "");
// // // //     console.log("🟡 variation changed:", vid);

// // // //     if (!vid) return;

// // // //     if (variationMeta[vid]) {
// // // //       console.log("🔐 isunck = TRUE → loading unicks");
// // // //       qtyField.disabled = true;
// // // //       loadUnicks(vid);

// // // //       if (unickSelect) {
// // // //         unickSelect.addEventListener("change", syncQtyWithUnicks);
// // // //         unickSelect.addEventListener("click", syncQtyWithUnicks);
// // // //       }
// // // //     } else {
// // // //       console.log("🔓 isunck = FALSE");
// // // //       qtyField.disabled = false;
// // // //       if (unickSelect) clearSelect(unickSelect);
// // // //     }
// // // //   });

// // // //   if (productField.value) loadVariations(productField.value);
// // // // });



// // // console.log(" product_variation.js LOADED");

// // // document.addEventListener("DOMContentLoaded", function () {
// // //   console.log(" DOMContentLoaded fired");

// // //   const productField   = document.getElementById("id_product_name");
// // //   const variationField = document.getElementById("id_product_variation");
// // //   const qtyField       = document.getElementById("id_quantity");
// // //   const unickSelect    = document.getElementById("id_unickkey"); //  Unfold compatible

// // //   console.log("productField =", productField);
// // //   console.log("variationField =", variationField);
// // //   console.log("unickSelect =", unickSelect);

// // //   if (!productField || !variationField) {
// // //     console.error(" productField or variationField NOT FOUND");
// // //     return;
// // //   }

// // //   let variationMeta = {};

// // //   function clearSelect(sel) {
// // //     if (!sel) return;
// // //     sel.innerHTML = "";
// // //   }

// // //   function syncQtyWithSelectedUnicks() {
// // //     if (!unickSelect || !qtyField) return;
// // //     const selectedCount = [...unickSelect.options].filter(o => o.selected).length;
// // //     qtyField.value = selectedCount;
// // //   }

// // //   function loadVariations(productId) {
// // //     console.log("➡️ loadVariations called, productId =", productId);

// // //     variationField.innerHTML = '<option value="">---------</option>';
// // //     variationMeta = {};

// // //     if (!productId) return;

// // //     const url = `/admin/variations/?product=${productId}`;
// // //     console.log("🌐 Fetching variations:", url);

// // //     fetch(url)
// // //       .then(r => {
// // //         console.log("⬅️ variation response status:", r.status);
// // //         return r.json();
// // //       })
// // //       .then(data => {
// // //         console.log(" variation data =", data);

// // //         data.forEach(v => {
// // //           variationMeta[String(v.id)] = v.isunck;
// // //           const opt = document.createElement("option");
// // //           opt.value = v.id;
// // //           opt.textContent = v.name + (v.isunck ? " (Unique)" : "");
// // //           variationField.appendChild(opt);
// // //         });
// // //       })
// // //       .catch(err => console.error(" variation fetch error:", err));
// // //   }

// // //   function loadUnicks(variationId) {
// // //     console.log("➡️ loadUnicks called, variationId =", variationId);

// // //     if (!unickSelect) {
// // //       console.error(" id_unickkey NOT FOUND (unick field not rendered?)");
// // //       return;
// // //     }

// // //     clearSelect(unickSelect);
// // //     syncQtyWithSelectedUnicks();

// // //     const stockId = document.getElementById("id_id")?.value || "";
// // //     const url = `/admin/unickkeys/?variation=${variationId}&stock_id=${stockId}`;

// // //     console.log("🌐 Fetching unicks:", url);

// // //     fetch(url)
// // //       .then(r => {
// // //         console.log("⬅️ unick response status:", r.status);
// // //         return r.json();
// // //       })
// // //       .then(data => {
// // //         console.log(" unick data =", data);

// // //         data.forEach(u => {
// // //           const opt = document.createElement("option");
// // //           opt.value = u.id;
// // //           opt.textContent = u.text;
// // //           unickSelect.appendChild(opt);
// // //         });

// // //         // after load, qty should be 0 until user selects
// // //         syncQtyWithSelectedUnicks();
// // //       })
// // //       .catch(err => console.error(" unick fetch error:", err));
// // //   }

// // //   productField.addEventListener("change", () => {
// // //     console.log("🟡 product changed:", productField.value);
// // //     loadVariations(productField.value);

// // //     if (qtyField) qtyField.disabled = false;
// // //     if (unickSelect) clearSelect(unickSelect);
// // //   });

// // //   variationField.addEventListener("change", () => {
// // //     const vid = String(variationField.value || "");
// // //     console.log("🟡 variation changed:", vid);

// // //     if (!vid) return;

// // //     if (variationMeta[vid]) {
// // //       console.log("🔐 isunck = TRUE → loading unicks");
// // //       if (qtyField) qtyField.readOnly = true; //  user type করতে পারবে না, কিন্তু auto-update হবে
// // //       loadUnicks(vid);
// // //     } else {
// // //       console.log("🔓 isunck = FALSE");
// // //       if (qtyField) qtyField.readOnly = false;
// // //       if (unickSelect) clearSelect(unickSelect);
// // //     }
// // //   });

// // //   //  manual select => quantity auto sync
// // //   if (unickSelect) {
// // //     unickSelect.addEventListener("change", syncQtyWithSelectedUnicks);
// // //     unickSelect.addEventListener("click", syncQtyWithSelectedUnicks);
// // //   }

// // //   // edit page support
// // //   if (productField.value) {
// // //     loadVariations(productField.value);
// // //   }
// // // });


// // console.log(" product_variation.js LOADED");

// // document.addEventListener("DOMContentLoaded", function () {
// //   console.log(" DOMContentLoaded fired");

// //   const productField   = document.getElementById("id_product_name");
// //   const variationField = document.getElementById("id_product_variation");
// //   const qtyField       = document.getElementById("id_quantity");

// //   // Base select (Unfold may use this directly)
// //   const unickBase      = document.getElementById("id_unickkey");

// //   // Django admin filter_horizontal (classic)
// //   const unickFrom      = document.getElementById("id_unickkey_from");
// //   const unickTo        = document.getElementById("id_unickkey_to");
// //   const addBtn         = document.getElementById("id_unickkey_add_link");
// //   const removeBtn      = document.getElementById("id_unickkey_remove_link");

// //   const usingFilterHorizontal = !!(unickFrom && unickTo);

// //   console.log("productField =", productField);
// //   console.log("variationField =", variationField);
// //   console.log("unickBase =", unickBase, "usingFilterHorizontal =", usingFilterHorizontal);

// //   if (!productField || !variationField) {
// //     console.error(" productField or variationField NOT FOUND");
// //     return;
// //   }

// //   let variationMeta = {};

// //   function clearSelect(sel) {
// //     if (!sel) return;
// //     sel.innerHTML = "";
// //   }

// //   function getSelectedUnickIds() {
// //     if (usingFilterHorizontal) {
// //       return [...unickTo.options].map(o => String(o.value));
// //     }
// //     if (!unickBase) return [];
// //     return [...unickBase.options].filter(o => o.selected).map(o => String(o.value));
// //   }

// //   function setQtyToSelectedUnickCount() {
// //     if (!qtyField) return;
// //     let cnt = 0;

// //     if (usingFilterHorizontal) cnt = unickTo.options.length;
// //     else if (unickBase) cnt = [...unickBase.options].filter(o => o.selected).length;

// //     qtyField.value = cnt;
// //   }

// //   // filter_horizontal থাকলে hidden/base select sync করে রাখি (safety)
// //   function syncHiddenBaseFromTo() {
// //     if (!usingFilterHorizontal || !unickBase) return;

// //     const selectedSet = new Set([...unickTo.options].map(o => String(o.value)));
// //     [...unickBase.options].forEach(o => {
// //       o.selected = selectedSet.has(String(o.value));
// //     });
// //   }

// //   function loadVariations(productId) {
// //     console.log("➡️ loadVariations called, productId =", productId);

// //     //  preserve currently selected variation (edit/update support)
// //     const prevVariationId = String(variationField.value || "");

// //     variationField.innerHTML = '<option value="">---------</option>';
// //     variationMeta = {};
// //     if (!productId) return;

// //     const url = `/admin/variations/?product=${productId}`;
// //     console.log("🌐 Fetching variations:", url);

// //     fetch(url)
// //       .then(r => {
// //         console.log("⬅️ variation response status:", r.status);
// //         return r.json();
// //       })
// //       .then(data => {
// //         console.log(" variation data =", data);

// //         data.forEach(v => {
// //           variationMeta[String(v.id)] = !!v.isunck;
// //           const opt = document.createElement("option");
// //           opt.value = v.id;
// //           opt.textContent = v.name + (v.isunck ? " (Unique)" : "");
// //           variationField.appendChild(opt);
// //         });

// //         //  re-select previous variation (edit/update)
// //         if (prevVariationId) {
// //           variationField.value = prevVariationId;

// //           // if unique -> auto load unicks on edit page
// //           if (variationMeta[prevVariationId]) {
// //             console.log(" edit restore: variation is unique → auto load unicks");
// //             if (qtyField) qtyField.readOnly = true;
// //             loadUnicks(prevVariationId);
// //           }
// //         }
// //       })
// //       .catch(err => console.error(" variation fetch error:", err));
// //   }

// //   function renderUnicks(data, selectedIdsSet) {
// //     // Clear UI selects
// //     if (usingFilterHorizontal) {
// //       clearSelect(unickFrom);
// //       clearSelect(unickTo);
// //     }
// //     if (unickBase) clearSelect(unickBase);

// //     data.forEach(u => {
// //       const id = String(u.id);

// //       // base select (actual form field)
// //       if (unickBase) {
// //         const optBase = document.createElement("option");
// //         optBase.value = id;
// //         optBase.textContent = u.text;
// //         optBase.selected = selectedIdsSet.has(id);
// //         unickBase.appendChild(optBase);
// //       }

// //       // filter_horizontal UI
// //       if (usingFilterHorizontal) {
// //         const optUi = document.createElement("option");
// //         optUi.value = id;
// //         optUi.textContent = u.text;

// //         if (selectedIdsSet.has(id)) unickTo.appendChild(optUi);
// //         else unickFrom.appendChild(optUi);
// //       }
// //     });

// //     // final sync
// //     syncHiddenBaseFromTo();
// //     setQtyToSelectedUnickCount();
// //   }

// //   function loadUnicks(variationId) {
// //     console.log("➡️ loadUnicks called, variationId =", variationId);

// //     if (!unickBase && !usingFilterHorizontal) {
// //       console.error(" Unick field not rendered");
// //       return;
// //     }

// //     //  preserve currently selected unicks (edit/update)
// //     const prevSelected = getSelectedUnickIds();
// //     const selectedSet = new Set(prevSelected);

// //     const stockId = document.getElementById("id_id")?.value || "";
// //     const url = `/admin/unickkeys/?variation=${variationId}&stock_id=${stockId}`;
// //     console.log("🌐 Fetching unicks:", url);

// //     fetch(url)
// //       .then(r => {
// //         console.log("⬅️ unick response status:", r.status);
// //         return r.json();
// //       })
// //       .then(data => {
// //         console.log(" unick data =", data);
// //         renderUnicks(data, selectedSet);
// //       })
// //       .catch(err => console.error(" unick fetch error:", err));
// //   }

// //   productField.addEventListener("change", () => {
// //     console.log("🟡 product changed:", productField.value);
// //     loadVariations(productField.value);

// //     if (qtyField) qtyField.readOnly = false;

// //     // clear unicks when product changes
// //     if (usingFilterHorizontal) { clearSelect(unickFrom); clearSelect(unickTo); }
// //     if (unickBase) clearSelect(unickBase);

// //     setQtyToSelectedUnickCount();
// //   });

// //   variationField.addEventListener("change", () => {
// //     const vid = String(variationField.value || "");
// //     console.log("🟡 variation changed:", vid);

// //     if (!vid) return;

// //     if (variationMeta[vid]) {
// //       console.log("🔐 isunck = TRUE → loading unicks");
// //       if (qtyField) qtyField.readOnly = true;
// //       loadUnicks(vid);
// //     } else {
// //       console.log("🔓 isunck = FALSE");
// //       if (qtyField) qtyField.readOnly = false;

// //       if (usingFilterHorizontal) { clearSelect(unickFrom); clearSelect(unickTo); }
// //       if (unickBase) clearSelect(unickBase);

// //       setQtyToSelectedUnickCount();
// //     }
// //   });

// //   //  quantity sync triggers (works for both UI types)
// //   function attachQtySync() {
// //     if (usingFilterHorizontal) {
// //       // when user adds/removes
// //       if (addBtn) addBtn.addEventListener("click", () => setTimeout(() => {
// //         syncHiddenBaseFromTo();
// //         setQtyToSelectedUnickCount();
// //       }, 0));

// //       if (removeBtn) removeBtn.addEventListener("click", () => setTimeout(() => {
// //         syncHiddenBaseFromTo();
// //         setQtyToSelectedUnickCount();
// //       }, 0));

// //       // also watch any DOM changes inside "to" box (safest)
// //       const obs = new MutationObserver(() => {
// //         syncHiddenBaseFromTo();
// //         setQtyToSelectedUnickCount();
// //       });
// //       obs.observe(unickTo, { childList: true });
// //     } else if (unickBase) {
// //       unickBase.addEventListener("change", setQtyToSelectedUnickCount);
// //       unickBase.addEventListener("click", setQtyToSelectedUnickCount);
// //     }
// //   }

// //   attachQtySync();

// //   //  edit page initial load
// //   if (productField.value) {
// //     loadVariations(productField.value);

// //     // If variation already selected in HTML (edit page), ensure qty sync at least once
// //     setTimeout(() => {
// //       setQtyToSelectedUnickCount();
// //     }, 0);
// //   }
// // });



// // admin/js/product_variation.js
// console.log(" product_variation.js LOADED");

// document.addEventListener("DOMContentLoaded", function () {
//   console.log(" DOMContentLoaded fired");

//   const productField   = document.getElementById("id_product_name");
//   const variationField = document.getElementById("id_product_variation");
//   const qtyField       = document.getElementById("id_quantity");

//   // Base select (actual form field; often hidden when filter_horizontal is used)
//   const unickBase = document.getElementById("id_unickkey");

//   // Django admin filter_horizontal UI selects/buttons
//   const unickFrom  = document.getElementById("id_unickkey_from");
//   const unickTo    = document.getElementById("id_unickkey_to");
//   const addBtn     = document.getElementById("id_unickkey_add_link");
//   const removeBtn  = document.getElementById("id_unickkey_remove_link");

//   const usingFilterHorizontal = !!(unickFrom && unickTo);

//   console.log("productField =", productField);
//   console.log("variationField =", variationField);
//   console.log("unickBase =", unickBase);
//   console.log("usingFilterHorizontal =", usingFilterHorizontal);

//   if (!productField || !variationField) {
//     console.error(" productField or variationField NOT FOUND");
//     return;
//   }

//   let variationMeta = {};

//   function clearSelect(sel) {
//     if (!sel) return;
//     sel.innerHTML = "";
//   }

//   /**
//    *  FIX: Always trust the ORIGINAL (hidden) base select first.
//    * Because on edit page, Django already marks the saved unicks as selected there.
//    * filter_horizontal UI may not be initialized yet when our JS runs.
//    */
//   function getSelectedUnickIds() {
//     if (unickBase) {
//       const selected = [...unickBase.options]
//         .filter(o => o.selected)
//         .map(o => String(o.value));
//       if (selected.length) return selected;
//     }

//     // fallback (when base select doesn't have selected info)
//     if (usingFilterHorizontal) {
//       return [...unickTo.options].map(o => String(o.value));
//     }

//     return [];
//   }

//   function setQtyToSelectedUnickCount() {
//     if (!qtyField) return;

//     let cnt = 0;

//     if (usingFilterHorizontal) {
//       // "to" box holds chosen items
//       cnt = unickTo?.options?.length || 0;
//     } else if (unickBase) {
//       cnt = [...unickBase.options].filter(o => o.selected).length;
//     }

//     qtyField.value = cnt;
//   }

//   function syncHiddenBaseFromTo() {
//     // sync the hidden/base select selection based on "to" box
//     if (!usingFilterHorizontal || !unickBase) return;

//     const selectedSet = new Set([...unickTo.options].map(o => String(o.value)));
//     [...unickBase.options].forEach(o => {
//       o.selected = selectedSet.has(String(o.value));
//     });
//   }

//   function loadVariations(productId) {
//     console.log("➡️ loadVariations called, productId =", productId);

//     // preserve current selection (edit/update)
//     const prevVariationId = String(variationField.value || "");

//     variationField.innerHTML = '<option value="">---------</option>';
//     variationMeta = {};
//     if (!productId) return;

//     const url = `/admin/variations/?product=${productId}`;
//     console.log("🌐 Fetching variations:", url);

//     fetch(url)
//       .then(r => {
//         console.log("⬅️ variation response status:", r.status);
//         return r.json();
//       })
//       .then(data => {
//         console.log(" variation data =", data);

//         data.forEach(v => {
//           variationMeta[String(v.id)] = !!v.isunck;
//           const opt = document.createElement("option");
//           opt.value = v.id;
//           opt.textContent = v.name + (v.isunck ? " (Unique)" : "");
//           variationField.appendChild(opt);
//         });

//         //  restore previous selection
//         if (prevVariationId) {
//           variationField.value = prevVariationId;

//           // if unique, load unicks
//           if (variationMeta[prevVariationId]) {
//             console.log(" edit restore: unique variation → auto load unicks");
//             if (qtyField) qtyField.readOnly = true;
//             loadUnicks(prevVariationId);
//           }
//         }
//       })
//       .catch(err => console.error(" variation fetch error:", err));
//   }

//   function renderUnicks(data, selectedIdsSet) {
//     // clear UI selects
//     if (usingFilterHorizontal) {
//       clearSelect(unickFrom);
//       clearSelect(unickTo);
//     }
//     if (unickBase) clearSelect(unickBase);

//     data.forEach(u => {
//       const id = String(u.id);

//       // base select (actual form field)
//       if (unickBase) {
//         const optBase = document.createElement("option");
//         optBase.value = id;
//         optBase.textContent = u.text;
//         optBase.selected = selectedIdsSet.has(id);
//         unickBase.appendChild(optBase);
//       }

//       // filter_horizontal UI
//       if (usingFilterHorizontal) {
//         const optUi = document.createElement("option");
//         optUi.value = id;
//         optUi.textContent = u.text;

//         if (selectedIdsSet.has(id)) unickTo.appendChild(optUi);
//         else unickFrom.appendChild(optUi);
//       }
//     });

//     // keep hidden select synced
//     syncHiddenBaseFromTo();
//     setQtyToSelectedUnickCount();
//   }

//   function loadUnicks(variationId) {
//     console.log("➡️ loadUnicks called, variationId =", variationId);

//     if (!unickBase && !usingFilterHorizontal) {
//       console.error(" Unick field not rendered");
//       return;
//     }

//     /**
//      *  FIX: preserve previous selected UNICKS properly
//      * If edit page had 3 saved unicks, we keep them, so when you add 2 new,
//      * qty becomes 5.
//      */
//     const prevSelected = getSelectedUnickIds();
//     const selectedSet = new Set(prevSelected);

//     const stockId = document.getElementById("id_id")?.value || "";
//     const url = `/admin/unickkeys/?variation=${variationId}&stock_id=${stockId}`;
//     console.log("🌐 Fetching unicks:", url);

//     fetch(url)
//       .then(r => {
//         console.log("⬅️ unick response status:", r.status);
//         return r.json();
//       })
//       .then(data => {
//         console.log(" unick data =", data);
//         renderUnicks(data, selectedSet);
//       })
//       .catch(err => console.error(" unick fetch error:", err));
//   }

//   // ===========================
//   // Event listeners
//   // ===========================

//   productField.addEventListener("change", () => {
//     console.log("🟡 product changed:", productField.value);
//     loadVariations(productField.value);

//     if (qtyField) qtyField.readOnly = false;

//     // clear unicks when product changes
//     if (usingFilterHorizontal) { clearSelect(unickFrom); clearSelect(unickTo); }
//     if (unickBase) clearSelect(unickBase);

//     setQtyToSelectedUnickCount();
//   });

//   variationField.addEventListener("change", () => {
//     const vid = String(variationField.value || "");
//     console.log("🟡 variation changed:", vid);

//     if (!vid) return;

//     if (variationMeta[vid]) {
//       console.log("🔐 isunck = TRUE → loading unicks");
//       if (qtyField) qtyField.readOnly = true;
//       loadUnicks(vid);
//     } else {
//       console.log("🔓 isunck = FALSE");
//       if (qtyField) qtyField.readOnly = false;

//       if (usingFilterHorizontal) { clearSelect(unickFrom); clearSelect(unickTo); }
//       if (unickBase) clearSelect(unickBase);

//       setQtyToSelectedUnickCount();
//     }
//   });

//   //  Quantity sync for both widget types
//   function attachQtySync() {
//     if (usingFilterHorizontal) {
//       const doSync = () => setTimeout(() => {
//         syncHiddenBaseFromTo();
//         setQtyToSelectedUnickCount();
//       }, 0);

//       if (addBtn) addBtn.addEventListener("click", doSync);
//       if (removeBtn) removeBtn.addEventListener("click", doSync);

//       // Watch "to" box list changes
//       const obs = new MutationObserver(() => {
//         syncHiddenBaseFromTo();
//         setQtyToSelectedUnickCount();
//       });
//       obs.observe(unickTo, { childList: true });
//     } else if (unickBase) {
//       unickBase.addEventListener("change", setQtyToSelectedUnickCount);
//       unickBase.addEventListener("click", setQtyToSelectedUnickCount);
//     }
//   }

//   attachQtySync();

//   /**
//    *  FIX: Initial load MUST wait until window.load
//    * because filter_horizontal/unfold widgets complete initialization after DOMContentLoaded.
//    * Otherwise your saved 3 unicks may look like 0.
//    */
//   window.addEventListener("load", () => {
//     if (productField.value) {
//       loadVariations(productField.value);

//       // ensure quantity is correct at least once after widgets initialize
//       setTimeout(() => {
//         // for filter_horizontal, keep hidden select synced
//         syncHiddenBaseFromTo();
//         setQtyToSelectedUnickCount();
//       }, 0);
//     }
//   });
// });


// admin/js/product_variation.js
console.log(" product_variation.js LOADED");

document.addEventListener("DOMContentLoaded", function () {
  console.log(" DOMContentLoaded fired");

  const productField   = document.getElementById("id_product_name");
  const variationField = document.getElementById("id_product_variation");
  const qtyField       = document.getElementById("id_quantity");

  // Base select (actual form field; often hidden when filter_horizontal is used)
  const unickBase = document.getElementById("id_unickkey");

  // Django admin filter_horizontal UI selects/buttons
  const unickFrom  = document.getElementById("id_unickkey_from");
  const unickTo    = document.getElementById("id_unickkey_to");
  const addBtn     = document.getElementById("id_unickkey_add_link");
  const removeBtn  = document.getElementById("id_unickkey_remove_link");

  const usingFilterHorizontal = !!(unickFrom && unickTo);

  console.log("productField =", productField);
  console.log("variationField =", variationField);
  console.log("unickBase =", unickBase);
  console.log("usingFilterHorizontal =", usingFilterHorizontal);

  if (!productField || !variationField) {
    console.error(" productField or variationField NOT FOUND");
    return;
  }

  let variationMeta = {};

  function clearSelect(sel) {
    if (!sel) return;
    sel.innerHTML = "";
  }

  //  Hint / warning UI
  let qtyHint = null;
  function ensureQtyHint() {
    if (!qtyField) return null;
    if (qtyHint) return qtyHint;

    qtyHint = document.createElement("div");
    qtyHint.style.marginTop = "6px";
    qtyHint.style.fontSize = "12px";
    qtyHint.style.opacity = "0.9";
    qtyField.insertAdjacentElement("afterend", qtyHint);
    return qtyHint;
  }

  function getChosenUnickCount() {
    if (usingFilterHorizontal) {
      return unickTo?.options?.length || 0;
    }
    if (unickBase) {
      return [...unickBase.options].filter(o => o.selected).length;
    }
    return 0;
  }

  //  only CHECK (manual qty stays)
  function checkQtyMatch() {
    const vid = String(variationField.value || "");
    const isUnique = !!variationMeta[vid];

    const hint = ensureQtyHint();
    if (!hint) return;

    if (!vid) {
      hint.textContent = "";
      hint.style.color = "";
      return;
    }

    if (!isUnique) {
      hint.textContent = "Non-unique: Quantity manually দিন (Unickkey লাগবে না)।";
      hint.style.color = "";
      return;
    }

    const cnt = getChosenUnickCount();
    const qty = parseInt(qtyField?.value || "0", 10) || 0;

    hint.textContent = `Unique: Chosen Unickkey = ${cnt}. Quantity অবশ্যই ${cnt} হতে হবে (save এ validate হবে)।`;

    // mismatch highlight only
    if (qty !== cnt) hint.style.color = "#ff6b6b";
    else hint.style.color = "#7CFC98";
  }

  /**
   *  Always trust the ORIGINAL (hidden) base select first.
   * Because on edit page, Django already marks the saved unicks as selected there.
   */
  function getSelectedUnickIds() {
    if (unickBase) {
      const selected = [...unickBase.options]
        .filter(o => o.selected)
        .map(o => String(o.value));
      if (selected.length) return selected;
    }
    if (usingFilterHorizontal) {
      return [...unickTo.options].map(o => String(o.value));
    }
    return [];
  }

  //  OLD: qty auto set (removed behaviour)
  //  now only check
  function setQtyToSelectedUnickCount() {
    checkQtyMatch(); // keep function name to avoid changing other parts
  }

  function syncHiddenBaseFromTo() {
    if (!usingFilterHorizontal || !unickBase) return;

    const selectedSet = new Set([...unickTo.options].map(o => String(o.value)));
    [...unickBase.options].forEach(o => {
      o.selected = selectedSet.has(String(o.value));
    });
  }

  function loadVariations(productId) {
    console.log(" loadVariations called, productId =", productId);

    const prevVariationId = String(variationField.value || "");

    variationField.innerHTML = '<option value="">---------</option>';
    variationMeta = {};
    if (!productId) return;

    const url = `/admin/variations/?product=${productId}`;
    console.log(" Fetching variations:", url);

    fetch(url)
      .then(r => {
        console.log("⬅ variation response status:", r.status);
        return r.json();
      })
      .then(data => {
        console.log(" variation data =", data);

        data.forEach(v => {
          variationMeta[String(v.id)] = !!v.isunck;
          const opt = document.createElement("option");
          opt.value = v.id;
          opt.textContent = v.name + (v.isunck ? " (Unique)" : "");
          variationField.appendChild(opt);
        });

        if (prevVariationId) {
          variationField.value = prevVariationId;

          //  keep auto-load unicks (as before) BUT no readonly qty
          if (variationMeta[prevVariationId]) {
            console.log(" edit restore: unique variation → auto load unicks");
            loadUnicks(prevVariationId);
          }
        }

        checkQtyMatch();
      })
      .catch(err => console.error(" variation fetch error:", err));
  }

  function renderUnicks(data, selectedIdsSet) {
    if (usingFilterHorizontal) {
      clearSelect(unickFrom);
      clearSelect(unickTo);
    }
    if (unickBase) clearSelect(unickBase);

    data.forEach(u => {
      const id = String(u.id);

      if (unickBase) {
        const optBase = document.createElement("option");
        optBase.value = id;
        optBase.textContent = u.text;
        optBase.selected = selectedIdsSet.has(id);
        unickBase.appendChild(optBase);
      }

      if (usingFilterHorizontal) {
        const optUi = document.createElement("option");
        optUi.value = id;
        optUi.textContent = u.text;

        if (selectedIdsSet.has(id)) unickTo.appendChild(optUi);
        else unickFrom.appendChild(optUi);
      }
    });

    syncHiddenBaseFromTo();
    checkQtyMatch();
  }

  function loadUnicks(variationId) {
    console.log(" loadUnicks called, variationId =", variationId);

    if (!unickBase && !usingFilterHorizontal) {
      console.error(" Unick field not rendered");
      return;
    }

    const prevSelected = getSelectedUnickIds();
    const selectedSet = new Set(prevSelected);

    const stockId = document.getElementById("id_id")?.value || "";
    const url = `/admin/unickkeys/?variation=${variationId}&stock_id=${stockId}`;
    console.log(" Fetching unicks:", url);

    fetch(url)
      .then(r => {
        console.log("⬅ unick response status:", r.status);
        return r.json();
      })
      .then(data => {
        console.log(" unick data =", data);
        renderUnicks(data, selectedSet);
      })
      .catch(err => console.error(" unick fetch error:", err));
  }

  // ===========================
  // Event listeners
  // ===========================

  productField.addEventListener("change", () => {
    console.log(" product changed:", productField.value);
    loadVariations(productField.value);

    //  keep qty manual always
    if (qtyField) qtyField.readOnly = false;

    if (usingFilterHorizontal) { clearSelect(unickFrom); clearSelect(unickTo); }
    if (unickBase) clearSelect(unickBase);

    checkQtyMatch();
  });

  variationField.addEventListener("change", () => {
    const vid = String(variationField.value || "");
    console.log(" variation changed:", vid);

    if (!vid) return;

    if (variationMeta[vid]) {
      console.log(" isunck = TRUE → loading unicks");
      if (qtyField) qtyField.readOnly = false; //  manual always
      loadUnicks(vid);
    } else {
      console.log(" isunck = FALSE");
      if (qtyField) qtyField.readOnly = false;

      if (usingFilterHorizontal) { clearSelect(unickFrom); clearSelect(unickTo); }
      if (unickBase) clearSelect(unickBase);

      checkQtyMatch();
    }
  });

  //  sync base select + check only (no qty auto set)
  function attachQtySync() {
    if (usingFilterHorizontal) {
      const doSync = () => setTimeout(() => {
        syncHiddenBaseFromTo();
        checkQtyMatch();
      }, 0);

      if (addBtn) addBtn.addEventListener("click", doSync);
      if (removeBtn) removeBtn.addEventListener("click", doSync);

      const obs = new MutationObserver(() => {
        syncHiddenBaseFromTo();
        checkQtyMatch();
      });
      obs.observe(unickTo, { childList: true });
    } else if (unickBase) {
      unickBase.addEventListener("change", checkQtyMatch);
      unickBase.addEventListener("click", checkQtyMatch);
    }
  }

  attachQtySync();

  //  when user types qty manually -> live check
  if (qtyField) qtyField.addEventListener("input", checkQtyMatch);

  window.addEventListener("load", () => {
    if (productField.value) {
      loadVariations(productField.value);
      setTimeout(() => {
        syncHiddenBaseFromTo();
        checkQtyMatch();
      }, 0);
    }
  });
});
