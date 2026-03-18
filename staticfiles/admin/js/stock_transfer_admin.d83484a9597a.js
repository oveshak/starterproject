// // // // (function () {
// // // //   function $(sel, root) { return (root || document).querySelector(sel); }
// // // //   function $all(sel, root) { return Array.from((root || document).querySelectorAll(sel)); }

// // // //   function getFromBranchId() {
// // // //     const el = $("#id_from_branch_name");
// // // //     return el ? el.value : "";
// // // //   }

// // // //   async function fetchJSON(url) {
// // // //     const res = await fetch(url, { credentials: "same-origin" });
// // // //     return await res.json();
// // // //   }

// // // //   function clearOptions(selectEl, placeholder) {
// // // //     if (!selectEl) return;
// // // //     selectEl.innerHTML = "";
// // // //     const opt = document.createElement("option");
// // // //     opt.value = "";
// // // //     opt.textContent = placeholder || "---------";
// // // //     selectEl.appendChild(opt);
// // // //   }

// // // //   function addOptions(selectEl, items, valueKey, labelKey) {
// // // //     items.forEach((it) => {
// // // //       const opt = document.createElement("option");
// // // //       opt.value = it[valueKey];
// // // //       opt.textContent = it[labelKey];
// // // //       selectEl.appendChild(opt);
// // // //     });
// // // //   }

// // // //   function getAdminBaseAjaxUrl() {
// // // //     // current page: .../admin/transfers/stocktransfer/<id>/change/
// // // //     // our endpoints: .../admin/transfers/stocktransfer/ajax/...
// // // //     const parts = window.location.pathname.split("/");
// // // //     const idx = parts.indexOf("stocktransfer");
// // // //     if (idx === -1) return "";
// // // //     const base = parts.slice(0, idx + 1).join("/");
// // // //     return base + "/ajax";
// // // //   }

// // // //   async function loadProductsForAllRows() {
// // // //     const fromBranchId = getFromBranchId();
// // // //     const baseAjax = getAdminBaseAjaxUrl();
// // // //     if (!fromBranchId || !baseAjax) return;

// // // //     const data = await fetchJSON(`${baseAjax}/products/?from_branch_id=${fromBranchId}`);
// // // //     const products = data.results || [];

// // // //     // inline rows: each row has select with id like id_lines-0-product (depends on related_name)
// // // //     // Django inline prefix usually: <related_name>-0-...
// // // //     const productSelects = $all('select[id$="-product"]');

// // // //     productSelects.forEach((sel) => {
// // // //       const current = sel.value;
// // // //       clearOptions(sel, "Select product");
// // // //       addOptions(sel, products, "product_name_id", "product_name__name");
// // // //       if (current) sel.value = current;
// // // //     });
// // // //   }

// // // //   async function loadVariationsForRow(rowRoot) {
// // // //     const fromBranchId = getFromBranchId();
// // // //     const baseAjax = getAdminBaseAjaxUrl();
// // // //     if (!fromBranchId || !baseAjax) return;

// // // //     const productSel = $('select[id$="-product"]', rowRoot);
// // // //     const variationSel = $('select[id$="-variation"]', rowRoot);
// // // //     const unickSel = $('select[id$="-unickkeys"]', rowRoot);

// // // //     clearOptions(variationSel, "Select variation");
// // // //     if (unickSel) { unickSel.innerHTML = ""; }

// // // //     if (!productSel || !productSel.value) return;

// // // //     const data = await fetchJSON(`${baseAjax}/variations/?from_branch_id=${fromBranchId}&product_id=${productSel.value}`);
// // // //     const vars = data.results || [];

// // // //     addOptions(variationSel, vars, "product_variation_id", "product_variation__name");
// // // //   }

// // // //   async function loadUnickForRow(rowRoot) {
// // // //     const fromBranchId = getFromBranchId();
// // // //     const baseAjax = getAdminBaseAjaxUrl();
// // // //     if (!fromBranchId || !baseAjax) return;

// // // //     const variationSel = $('select[id$="-variation"]', rowRoot);
// // // //     const unickSel = $('select[id$="-unickkeys"]', rowRoot);
// // // //     if (!variationSel || !unickSel) return;

// // // //     unickSel.innerHTML = "";
// // // //     if (!variationSel.value) return;

// // // //     const data = await fetchJSON(`${baseAjax}/unickkeys/?from_branch_id=${fromBranchId}&variation_id=${variationSel.value}`);
// // // //     const keys = data.results || [];

// // // //     // M2M select box
// // // //     keys.forEach((k) => {
// // // //       const opt = document.createElement("option");
// // // //       opt.value = k.id;
// // // //       opt.textContent = k.label;
// // // //       unickSel.appendChild(opt);
// // // //     });
// // // //   }

// // // //   function bindRowEvents(rowRoot) {
// // // //     const productSel = $('select[id$="-product"]', rowRoot);
// // // //     const variationSel = $('select[id$="-variation"]', rowRoot);

// // // //     if (productSel) {
// // // //       productSel.addEventListener("change", async () => {
// // // //         await loadVariationsForRow(rowRoot);
// // // //       });
// // // //     }
// // // //     if (variationSel) {
// // // //       variationSel.addEventListener("change", async () => {
// // // //         await loadUnickForRow(rowRoot);
// // // //       });
// // // //     }
// // // //   }

// // // //   function bindAllRows() {
// // // //     // inline rows
// // // //     const rows = $all('tr[class*="dynamic-"]');// related_name=lines হলে সাধারণত dynamic-lines class থাকে
// // // //     rows.forEach(bindRowEvents);
// // // //   }

// // // //   async function init() {
// // // //     const fromBranch = $("#id_from_branch_name");
// // // //     if (!fromBranch) return;

// // // //     fromBranch.addEventListener("change", async () => {
// // // //       await loadProductsForAllRows();

// // // //       // from branch change হলে সব row reset
// // // //       $all(".dynamic-lines").forEach((row) => {
// // // //         const variationSel = $('select[id$="-variation"]', row);
// // // //         const unickSel = $('select[id$="-unickkeys"]', row);
// // // //         clearOptions(variationSel, "Select variation");
// // // //         if (unickSel) unickSel.innerHTML = "";
// // // //       });
// // // //     });

// // // //     bindAllRows();

// // // //     // initial load (edit page / create page)
// // // //     await loadProductsForAllRows();
// // // //   }

// // // //   document.addEventListener("DOMContentLoaded", init);

// // // //   // when clicking "Add another StockTransferLine"
// // // //   document.addEventListener("click", function (e) {
// // // //     const btn = e.target;
// // // //     if (btn && btn.classList && btn.classList.contains("add-row")) {
// // // //       setTimeout(() => {
// // // //         bindAllRows();
// // // //         loadProductsForAllRows();
// // // //       }, 50);
// // // //     }
// // // //   });
// // // // })();
// // // (function () {
// // //   function $(sel, root) { return (root || document).querySelector(sel); }
// // //   function $all(sel, root) { return Array.from((root || document).querySelectorAll(sel)); }

// // //   function getFromBranchId() {
// // //     const el = $("#id_from_branch_name");
// // //     return el ? el.value : "";
// // //   }

// // //   async function fetchJSON(url) {
// // //     const res = await fetch(url, { credentials: "same-origin" });
// // //     return await res.json();
// // //   }

// // //   function clearOptions(selectEl, placeholder) {
// // //     if (!selectEl) return;
// // //     selectEl.innerHTML = "";
// // //     const opt = document.createElement("option");
// // //     opt.value = "";
// // //     opt.textContent = placeholder || "---------";
// // //     selectEl.appendChild(opt);
// // //   }

// // //   function addOptions(selectEl, items, valueKey, labelKey) {
// // //     if (!selectEl) return;
// // //     items.forEach((it) => {
// // //       const opt = document.createElement("option");
// // //       opt.value = it[valueKey];
// // //       opt.textContent = it[labelKey];
// // //       selectEl.appendChild(opt);
// // //     });
// // //   }

// // //   //  Variation payload format auto-detect:
// // //   // - new robust: {id, label}
// // //   // - old: {product_variation_id, product_variation__name}
// // //   function normalizeVariations(vars) {
// // //     return (vars || []).map((v) => {
// // //       if (v && v.id !== undefined && v.label !== undefined) {
// // //         return { id: v.id, label: v.label };
// // //       }
// // //       return {
// // //         id: v.product_variation_id,
// // //         label: v.product_variation__name
// // //       };
// // //     }).filter(x => x.id !== undefined && x.id !== null);
// // //   }

// // //   function getAdminBaseAjaxUrl() {
// // //     const parts = window.location.pathname.split("/");
// // //     const idx = parts.indexOf("stocktransfer");
// // //     if (idx === -1) return "";
// // //     const base = parts.slice(0, idx + 1).join("/");
// // //     return base + "/ajax";
// // //   }

// // //   async function loadProductsForAllRows() {
// // //     const fromBranchId = getFromBranchId();
// // //     const baseAjax = getAdminBaseAjaxUrl();
// // //     if (!fromBranchId || !baseAjax) return;

// // //     const data = await fetchJSON(`${baseAjax}/products/?from_branch_id=${fromBranchId}`);
// // //     const products = data.results || [];

// // //     const productSelects = $all('select[id$="-product"]');

// // //     productSelects.forEach((sel) => {
// // //       const current = sel.value;
// // //       clearOptions(sel, "Select product");
// // //       addOptions(sel, products, "product_name_id", "product_name__name");
// // //       if (current) sel.value = current;
// // //     });
// // //   }

// // //   async function loadVariationsForRow(rowRoot) {
// // //     const fromBranchId = getFromBranchId();
// // //     const baseAjax = getAdminBaseAjaxUrl();
// // //     if (!fromBranchId || !baseAjax) return;

// // //     const productSel = $('select[id$="-product"]', rowRoot);
// // //     const variationSel = $('select[id$="-variation"]', rowRoot);

// // //     //  Django admin M2M widget selectors
// // //     const unickFrom = $('select[id$="-unickkeys_from"]', rowRoot);
// // //     const unickTo = $('select[id$="-unickkeys_to"]', rowRoot);

// // //     clearOptions(variationSel, "Select variation");
// // //     if (unickFrom) unickFrom.innerHTML = "";
// // //     if (unickTo) unickTo.innerHTML = "";

// // //     if (!productSel || !productSel.value) return;

// // //     const data = await fetchJSON(`${baseAjax}/variations/?from_branch_id=${fromBranchId}&product_id=${productSel.value}`);
// // //     const vars = normalizeVariations(data.results || []);

// // //     //  always fill using id/label
// // //     addOptions(variationSel, vars, "id", "label");
// // //   }

// // //   async function loadUnickForRow(rowRoot) {
// // //     const fromBranchId = getFromBranchId();
// // //     const baseAjax = getAdminBaseAjaxUrl();
// // //     if (!fromBranchId || !baseAjax) return;

// // //     const variationSel = $('select[id$="-variation"]', rowRoot);

// // //     //  Must use _from list (available)
// // //     const unickFrom = $('select[id$="-unickkeys_from"]', rowRoot);
// // //     const unickTo = $('select[id$="-unickkeys_to"]', rowRoot);

// // //     if (!variationSel || !unickFrom) return;

// // //     // reset
// // //     unickFrom.innerHTML = "";
// // //     if (unickTo) unickTo.innerHTML = ""; // optional: clear selected too

// // //     if (!variationSel.value) return;

// // //     const data = await fetchJSON(`${baseAjax}/unickkeys/?from_branch_id=${fromBranchId}&variation_id=${variationSel.value}`);
// // //     const keys = data.results || [];

// // //     keys.forEach((k) => {
// // //       const opt = document.createElement("option");
// // //       opt.value = k.id;
// // //       opt.textContent = k.label;
// // //       unickFrom.appendChild(opt);
// // //     });
// // //   }

// // //   function bindRowEvents(rowRoot) {
// // //     const productSel = $('select[id$="-product"]', rowRoot);
// // //     const variationSel = $('select[id$="-variation"]', rowRoot);

// // //     if (productSel && !productSel.dataset.bound) {
// // //       productSel.dataset.bound = "1";
// // //       productSel.addEventListener("change", async () => {
// // //         await loadVariationsForRow(rowRoot);
// // //       });
// // //     }

// // //     if (variationSel && !variationSel.dataset.bound) {
// // //       variationSel.dataset.bound = "1";
// // //       variationSel.addEventListener("change", async () => {
// // //         await loadUnickForRow(rowRoot);
// // //       });
// // //     }
// // //   }

// // //   function getInlineRows() {
// // //     //  robust
// // //     return $all('tr[class*="dynamic-"]').filter(r => !r.classList.contains("empty-form"));
// // //   }

// // //   function bindAllRows() {
// // //     getInlineRows().forEach(bindRowEvents);
// // //   }

// // //   async function resetAllRows() {
// // //     getInlineRows().forEach((row) => {
// // //       const variationSel = $('select[id$="-variation"]', row);
// // //       const unickFrom = $('select[id$="-unickkeys_from"]', row);
// // //       const unickTo = $('select[id$="-unickkeys_to"]', row);

// // //       clearOptions(variationSel, "Select variation");
// // //       if (unickFrom) unickFrom.innerHTML = "";
// // //       if (unickTo) unickTo.innerHTML = "";
// // //     });
// // //   }

// // //   async function init() {
// // //     const fromBranch = $("#id_from_branch_name");
// // //     if (!fromBranch) return;

// // //     fromBranch.addEventListener("change", async () => {
// // //       await loadProductsForAllRows();
// // //       await resetAllRows();
// // //     });

// // //     // initial
// // //     bindAllRows();
// // //     await loadProductsForAllRows();
// // //   }

// // //   document.addEventListener("DOMContentLoaded", init);

// // //   //  when clicking "Add another" (plus icon)
// // //   document.addEventListener("click", function (e) {
// // //     const btn = e.target;
// // //     if (btn && btn.classList && btn.classList.contains("add-row")) {
// // //       setTimeout(async () => {
// // //         bindAllRows();
// // //         await loadProductsForAllRows();
// // //       }, 50);
// // //     }
// // //   });
// // // })();


// // (function () {
// //   console.log("[ST ADMIN] JS file loaded");

// //   function $(sel, root) { return (root || document).querySelector(sel); }
// //   function $all(sel, root) { return Array.from((root || document).querySelectorAll(sel)); }

// //   function getFromBranchId() {
// //     const el = $("#id_from_branch_name");
// //     const val = el ? el.value : "";
// //     console.log("[ST ADMIN] from_branch_id =", val);
// //     return val;
// //   }

// //   function getAdminBaseAjaxUrl() {
// //     const parts = window.location.pathname.split("/").filter(Boolean);
// //     const idx = parts.indexOf("stocktransfer");
// //     if (idx === -1) {
// //       console.warn("[ST ADMIN] stocktransfer not found in URL", parts);
// //       return "";
// //     }
// //     const base = "/" + parts.slice(0, idx + 1).join("/");
// //     const ajaxUrl = base + "/ajax";
// //     console.log("[ST ADMIN] ajax base url =", ajaxUrl);
// //     return ajaxUrl;
// //   }

// //   async function fetchJSON(url) {
// //     console.log("[ST ADMIN] FETCH →", url);
// //     const res = await fetch(url, { credentials: "same-origin" });
// //     console.log("[ST ADMIN] status =", res.status);
// //     const data = await res.json();
// //     console.log("[ST ADMIN] response =", data);
// //     return data;
// //   }

// //   function clearSelect(selectEl, placeholder) {
// //     if (!selectEl) {
// //       console.warn("[ST ADMIN] clearSelect: selectEl not found");
// //       return;
// //     }
// //     selectEl.innerHTML = "";
// //     const opt = document.createElement("option");
// //     opt.value = "";
// //     opt.textContent = placeholder || "---------";
// //     selectEl.appendChild(opt);
// //   }

// //   function fillSelect(selectEl, items, getVal, getLabel, placeholder) {
// //     if (!selectEl) {
// //       console.warn("[ST ADMIN] fillSelect: selectEl not found");
// //       return;
// //     }
// //     console.log("[ST ADMIN] fillSelect items =", items);
// //     clearSelect(selectEl, placeholder);
// //     (items || []).forEach((it) => {
// //       const opt = document.createElement("option");
// //       opt.value = getVal(it);
// //       opt.textContent = getLabel(it);
// //       selectEl.appendChild(opt);
// //     });
// //   }

// //   function getRowRootFromField(fieldEl) {
// //     const row = fieldEl.closest('tr[class*="dynamic-"]') || fieldEl.closest("tr");
// //     console.log("[ST ADMIN] row root =", row);
// //     return row;
// //   }

// //   function normalizeVariations(vars) {
// //     console.log("[ST ADMIN] raw variations =", vars);
// //     const out = (vars || []).map(v => ({
// //       id: (v.id !== undefined) ? v.id : v.product_variation_id,
// //       label: (v.label !== undefined) ? v.label : v.product_variation__name
// //     })).filter(x => x.id);
// //     console.log("[ST ADMIN] normalized variations =", out);
// //     return out;
// //   }

// //   async function loadProductsForAllRows() {
// //     console.log("[ST ADMIN] loadProductsForAllRows()");
// //     const fromBranchId = getFromBranchId();
// //     const baseAjax = getAdminBaseAjaxUrl();
// //     if (!fromBranchId || !baseAjax) {
// //       console.warn("[ST ADMIN] cannot load products (missing branch or ajax url)");
// //       return;
// //     }

// //     const data = await fetchJSON(`${baseAjax}/products/?from_branch_id=${fromBranchId}`);
// //     const products = data.results || [];

// //     console.log("[ST ADMIN] products =", products);

// //     $all('select[id$="-product"]').forEach((sel) => {
// //       console.log("[ST ADMIN] filling product select", sel.id);
// //       const current = sel.value;
// //       fillSelect(
// //         sel,
// //         products,
// //         (x) => x.product_name_id,
// //         (x) => x.product_name__name,
// //         "Select product"
// //       );
// //       if (current) sel.value = current;
// //     });
// //   }

// //   async function loadVariationsForRow(rowRoot) {
// //     console.log("[ST ADMIN] loadVariationsForRow()", rowRoot);

// //     const fromBranchId = getFromBranchId();
// //     const baseAjax = getAdminBaseAjaxUrl();
// //     if (!fromBranchId || !baseAjax) return;

// //     const productSel = $('select[id$="-product"]', rowRoot);
// //     const variationSel = $('select[id$="-variation"]', rowRoot);

// //     console.log("[ST ADMIN] productSel =", productSel);
// //     console.log("[ST ADMIN] variationSel =", variationSel);

// //     const unickFrom = $('select[id$="-unickkeys_from"]', rowRoot);
// //     const unickTo = $('select[id$="-unickkeys_to"]', rowRoot);

// //     clearSelect(variationSel, "Select variation");
// //     if (unickFrom) unickFrom.innerHTML = "";
// //     if (unickTo) unickTo.innerHTML = "";

// //     if (!productSel || !productSel.value) {
// //       console.warn("[ST ADMIN] no product selected");
// //       return;
// //     }

// //     const url = `${baseAjax}/variations/?from_branch_id=${fromBranchId}&product_id=${productSel.value}`;
// //     const data = await fetchJSON(url);

// //     const vars = normalizeVariations(data.results || []);
// //     fillSelect(variationSel, vars, (x) => x.id, (x) => x.label, "Select variation");
// //   }

// //   async function loadUnickForRow(rowRoot) {
// //     console.log("[ST ADMIN] loadUnickForRow()", rowRoot);

// //     const fromBranchId = getFromBranchId();
// //     const baseAjax = getAdminBaseAjaxUrl();
// //     if (!fromBranchId || !baseAjax) return;

// //     const variationSel = $('select[id$="-variation"]', rowRoot);
// //     const unickFrom = $('select[id$="-unickkeys_from"]', rowRoot);
// //     const unickTo = $('select[id$="-unickkeys_to"]', rowRoot);

// //     console.log("[ST ADMIN] variationSel =", variationSel);
// //     console.log("[ST ADMIN] unickFrom =", unickFrom);

// //     if (!variationSel || !unickFrom) return;

// //     unickFrom.innerHTML = "";
// //     if (unickTo) unickTo.innerHTML = "";

// //     if (!variationSel.value) {
// //       console.warn("[ST ADMIN] no variation selected");
// //       return;
// //     }

// //     const url = `${baseAjax}/unickkeys/?from_branch_id=${fromBranchId}&variation_id=${variationSel.value}`;
// //     const data = await fetchJSON(url);

// //     const keys = data.results || [];
// //     console.log("[ST ADMIN] unick keys =", keys);

// //     keys.forEach((k) => {
// //       const opt = document.createElement("option");
// //       opt.value = k.id;
// //       opt.textContent = k.label;
// //       unickFrom.appendChild(opt);
// //     });
// //   }

// //   async function init() {
// //     console.log("[ST ADMIN] init()");
// //     const fromBranch = $("#id_from_branch_name");
// //     if (!fromBranch) {
// //       console.warn("[ST ADMIN] from_branch field not found");
// //       return;
// //     }

// //     fromBranch.addEventListener("change", async () => {
// //       console.log("[ST ADMIN] from branch changed");
// //       await loadProductsForAllRows();
// //     });

// //     document.addEventListener("change", async (e) => {
// //       const t = e.target;

// //       if (t && t.matches('select[id$="-product"]')) {
// //         console.log("[ST ADMIN] product changed", t.id, t.value);
// //         const row = getRowRootFromField(t);
// //         await loadVariationsForRow(row);
// //       }

// //       if (t && t.matches('select[id$="-variation"]')) {
// //         console.log("[ST ADMIN] variation changed", t.id, t.value);
// //         const row = getRowRootFromField(t);
// //         await loadUnickForRow(row);
// //       }
// //     });

// //     await loadProductsForAllRows();
// //   }

// //   document.addEventListener("DOMContentLoaded", init);
// // })();

// (function () {
//   console.log("[ST ADMIN] JS file loaded");

//   function $(sel, root) { return (root || document).querySelector(sel); }
//   function $all(sel, root) { return Array.from((root || document).querySelectorAll(sel)); }

//   function getFromBranchId() {
//     const el = $("#id_from_branch_name");
//     const val = el ? el.value : "";
//     console.log("[ST ADMIN] from_branch_id =", val);
//     return val;
//   }

//   function getAdminBaseAjaxUrl() {
//     const parts = window.location.pathname.split("/").filter(Boolean);
//     const idx = parts.indexOf("stocktransfer");
//     if (idx === -1) {
//       console.warn("[ST ADMIN] stocktransfer not found in URL", parts);
//       return "";
//     }
//     const base = "/" + parts.slice(0, idx + 1).join("/");
//     const ajaxUrl = base + "/ajax";
//     console.log("[ST ADMIN] ajax base url =", ajaxUrl);
//     return ajaxUrl;
//   }

//   async function fetchJSON(url) {
//     console.log("[ST ADMIN] FETCH →", url);
//     const res = await fetch(url, { credentials: "same-origin" });
//     console.log("[ST ADMIN] status =", res.status);
//     const data = await res.json();
//     console.log("[ST ADMIN] response =", data);
//     return data;
//   }

//   function clearSelect(selectEl, placeholder) {
//     if (!selectEl) {
//       console.warn("[ST ADMIN] clearSelect: selectEl not found");
//       return;
//     }
//     selectEl.innerHTML = "";
//     const opt = document.createElement("option");
//     opt.value = "";
//     opt.textContent = placeholder || "---------";
//     selectEl.appendChild(opt);
//   }

//   function fillSelect(selectEl, items, getVal, getLabel, placeholder) {
//     if (!selectEl) {
//       console.warn("[ST ADMIN] fillSelect: selectEl not found");
//       return;
//     }
//     console.log("[ST ADMIN] fillSelect items =", items);
//     clearSelect(selectEl, placeholder);
//     (items || []).forEach((it) => {
//       const opt = document.createElement("option");
//       opt.value = getVal(it);
//       opt.textContent = getLabel(it);
//       selectEl.appendChild(opt);
//     });
//   }

//   function getRowRootFromField(fieldEl) {
//     const row = fieldEl.closest('tr[class*="dynamic-"]') || fieldEl.closest("tr");
//     console.log("[ST ADMIN] row root =", row);
//     return row;
//   }

//   function normalizeVariations(vars) {
//     console.log("[ST ADMIN] raw variations =", vars);
//     const out = (vars || []).map(v => ({
//       id: (v.id !== undefined) ? v.id : v.product_variation_id,
//       label: (v.label !== undefined) ? v.label : v.product_variation__name
//     })).filter(x => x.id);
//     console.log("[ST ADMIN] normalized variations =", out);
//     return out;
//   }

//   async function loadProductsForAllRows() {
//     console.log("[ST ADMIN] loadProductsForAllRows()");
//     const fromBranchId = getFromBranchId();
//     const baseAjax = getAdminBaseAjaxUrl();
//     if (!fromBranchId || !baseAjax) {
//       console.warn("[ST ADMIN] cannot load products (missing branch or ajax url)");
//       return;
//     }

//     const data = await fetchJSON(`${baseAjax}/products/?from_branch_id=${fromBranchId}`);
//     const products = data.results || [];

//     console.log("[ST ADMIN] products =", products);

//     $all('select[id$="-product"]').forEach((sel) => {
//       console.log("[ST ADMIN] filling product select", sel.id);
//       const current = sel.value;
//       fillSelect(sel, products, (x) => x.product_name_id, (x) => x.product_name__name, "Select product");
//       if (current) sel.value = current;
//     });
//   }

//   async function loadVariationsForRow(rowRoot) {
//     console.log("[ST ADMIN] loadVariationsForRow()", rowRoot);

//     const fromBranchId = getFromBranchId();
//     const baseAjax = getAdminBaseAjaxUrl();
//     if (!fromBranchId || !baseAjax) return;

//     const productSel = $('select[id$="-product"]', rowRoot);
//     const variationSel = $('select[id$="-variation"]', rowRoot);

//     console.log("[ST ADMIN] productSel =", productSel);
//     console.log("[ST ADMIN] variationSel =", variationSel);

//     // reset unick selects too
//     const unickFromFallback =
//       $('select[id$="-unickkeys_from"]', rowRoot) ||
//       $('select[id$="-unickkeys"]', rowRoot);
//     const unickTo = $('select[id$="-unickkeys_to"]', rowRoot);

//     clearSelect(variationSel, "Select variation");
//     if (unickFromFallback) unickFromFallback.innerHTML = "";
//     if (unickTo) unickTo.innerHTML = "";

//     if (!productSel || !productSel.value) {
//       console.warn("[ST ADMIN] no product selected");
//       return;
//     }

//     const url = `${baseAjax}/variations/?from_branch_id=${fromBranchId}&product_id=${productSel.value}`;
//     const data = await fetchJSON(url);

//     const vars = normalizeVariations(data.results || []);
//     fillSelect(variationSel, vars, (x) => x.id, (x) => x.label, "Select variation");
//   }

//   async function loadUnickForRow(rowRoot) {
//     console.log("[ST ADMIN] loadUnickForRow()", rowRoot);

//     const fromBranchId = getFromBranchId();
//     const baseAjax = getAdminBaseAjaxUrl();
//     if (!fromBranchId || !baseAjax) return;

//     const variationSel = $('select[id$="-variation"]', rowRoot);

//     //  critical fix: fallback selector
//     const unickFrom =
//       $('select[id$="-unickkeys_from"]', rowRoot) ||
//       $('select[id$="-unickkeys"]', rowRoot);

//     const unickTo = $('select[id$="-unickkeys_to"]', rowRoot);

//     console.log("[ST ADMIN] variationSel =", variationSel);
//     console.log("[ST ADMIN] unickFrom =", unickFrom);

//     if (!variationSel) {
//       console.warn("[ST ADMIN] variationSel not found");
//       return;
//     }
//     if (!unickFrom) {
//       console.warn("[ST ADMIN] unick select not found (unickkeys field not rendered in inline)");
//       return;
//     }

//     unickFrom.innerHTML = "";
//     if (unickTo) unickTo.innerHTML = "";

//     if (!variationSel.value) {
//       console.warn("[ST ADMIN] no variation selected");
//       return;
//     }

//     const url = `${baseAjax}/unickkeys/?from_branch_id=${fromBranchId}&variation_id=${variationSel.value}`;
//     const data = await fetchJSON(url);

//     const keys = data.results || [];
//     console.log("[ST ADMIN] unick keys =", keys);

//     keys.forEach((k) => {
//       const opt = document.createElement("option");
//       opt.value = k.id;
//       opt.textContent = k.label;
//       unickFrom.appendChild(opt);
//     });
//   }

//   async function init() {
//     console.log("[ST ADMIN] init()");
//     const fromBranch = $("#id_from_branch_name");
//     if (!fromBranch) {
//       console.warn("[ST ADMIN] from_branch field not found");
//       return;
//     }

//     fromBranch.addEventListener("change", async () => {
//       console.log("[ST ADMIN] from branch changed");
//       await loadProductsForAllRows();
//     });

//     document.addEventListener("change", async (e) => {
//       const t = e.target;

//       if (t && t.matches('select[id$="-product"]')) {
//         console.log("[ST ADMIN] product changed", t.id, t.value);
//         const row = getRowRootFromField(t);
//         await loadVariationsForRow(row);
//       }

//       if (t && t.matches('select[id$="-variation"]')) {
//         console.log("[ST ADMIN] variation changed", t.id, t.value);
//         const row = getRowRootFromField(t);
//         await loadUnickForRow(row);
//       }
//     });

//     await loadProductsForAllRows();
//   }

//   document.addEventListener("DOMContentLoaded", init);
// })();


(function () {
  console.log("[ST ADMIN] JS file loaded");

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $all(sel, root) { return Array.from((root || document).querySelectorAll(sel)); }

  function getFromBranchId() {
    const el = $("#id_from_branch_name");
    const val = el ? el.value : "";
    console.log("[ST ADMIN] from_branch_id =", val);
    return val;
  }

  function getToBranchId() {
    const el = $("#id_to_branch_name");
    const val = el ? el.value : "";
    console.log("[ST ADMIN] to_branch_id =", val);
    return val;
  }

  function getAdminBaseAjaxUrl() {
    const parts = window.location.pathname.split("/").filter(Boolean);
    const idx = parts.indexOf("stocktransfer");
    if (idx === -1) {
      console.warn("[ST ADMIN] stocktransfer not found in URL", parts);
      return "";
    }
    const base = "/" + parts.slice(0, idx + 1).join("/");
    const ajaxUrl = base + "/ajax";
    console.log("[ST ADMIN] ajax base url =", ajaxUrl);
    return ajaxUrl;
  }

  async function fetchJSON(url) {
    console.log("[ST ADMIN] FETCH →", url);
    try {
      const res = await fetch(url, { credentials: "same-origin" });
      console.log("[ST ADMIN] status =", res.status);
      const data = await res.json();
      console.log("[ST ADMIN] response =", data);
      return data;
    } catch (err) {
      console.error("[ST ADMIN] Fetch error:", err);
      return { results: [] };
    }
  }

  function clearSelect(selectEl, placeholder) {
    if (!selectEl) {
      console.warn("[ST ADMIN] clearSelect: selectEl not found");
      return;
    }
    selectEl.innerHTML = "";
    const opt = document.createElement("option");
    opt.value = "";
    opt.textContent = placeholder || "---------";
    selectEl.appendChild(opt);
  }

  function fillSelect(selectEl, items, getVal, getLabel, placeholder) {
    if (!selectEl) {
      console.warn("[ST ADMIN] fillSelect: selectEl not found");
      return;
    }
    console.log("[ST ADMIN] fillSelect items =", items);
    clearSelect(selectEl, placeholder);
    (items || []).forEach((it) => {
      const opt = document.createElement("option");
      opt.value = getVal(it);
      opt.textContent = getLabel(it);
      selectEl.appendChild(opt);
    });
  }

  function getRowRootFromField(fieldEl) {
    const row = fieldEl.closest('tr[class*="dynamic-"]') || fieldEl.closest("tr");
    console.log("[ST ADMIN] row root =", row);
    return row;
  }

  function normalizeVariations(vars) {
    console.log("[ST ADMIN] raw variations =", vars);
    const out = (vars || []).map(v => ({
      id: (v.id !== undefined) ? v.id : v.product_variation_id,
      label: (v.label !== undefined) ? v.label : v.product_variation__name
    })).filter(x => x.id);
    console.log("[ST ADMIN] normalized variations =", out);
    return out;
  }

  async function loadProductsForAllRows() {
    console.log("[ST ADMIN] loadProductsForAllRows()");

    const fromBranchId = getFromBranchId();
    const baseAjax = getAdminBaseAjaxUrl();
    if (!fromBranchId || !baseAjax) {
      console.warn("[ST ADMIN] cannot load products (missing branch or ajax url)");
      return;
    }

    const data = await fetchJSON(`${baseAjax}/products/?from_branch_id=${fromBranchId}`);
    const products = data.results || [];

    console.log("[ST ADMIN] products =", products);

    $all('select[id$="-product"]').forEach((sel) => {
      console.log("[ST ADMIN] filling product select", sel.id);
      const current = sel.value;
      fillSelect(sel, products, (x) => x.product_name_id, (x) => x.product_name__name, "Select product");
      if (current) sel.value = current;
    });
  }

  async function loadVariationsForRow(rowRoot) {
    console.log("[ST ADMIN] loadVariationsForRow()", rowRoot);

    const fromBranchId = getFromBranchId();
    const baseAjax = getAdminBaseAjaxUrl();
    if (!fromBranchId || !baseAjax) return;

    const productSel = $('select[id$="-product"]', rowRoot);
    const variationSel = $('select[id$="-variation"]', rowRoot);

    console.log("[ST ADMIN] productSel =", productSel);
    console.log("[ST ADMIN] variationSel =", variationSel);

    // Reset unickkeys selects
    const unickkeySel = $('select[id$="-unickkeys"]', rowRoot);

    clearSelect(variationSel, "Select variation");
    if (unickkeySel) clearSelect(unickkeySel, "Select unickkeys");

    if (!productSel || !productSel.value) {
      console.warn("[ST ADMIN] no product selected");
      return;
    }

    const url = `${baseAjax}/variations/?from_branch_id=${fromBranchId}&product_id=${productSel.value}`;
    const data = await fetchJSON(url);

    const vars = normalizeVariations(data.results || []);
    fillSelect(variationSel, vars, (x) => x.id, (x) => x.label, "Select variation");
  }

  async function loadUnickForRow(rowRoot) {
    console.log("[ST ADMIN] loadUnickForRow()", rowRoot);

    const fromBranchId = getFromBranchId();
    const baseAjax = getAdminBaseAjaxUrl();
    if (!fromBranchId || !baseAjax) return;

    const variationSel = $('select[id$="-variation"]', rowRoot);
    const unickkeySel = $('select[id$="-unickkeys"]', rowRoot);

    console.log("[ST ADMIN] variationSel =", variationSel);
    console.log("[ST ADMIN] unickkeySel =", unickkeySel);

    if (!variationSel) {
      console.warn("[ST ADMIN] variationSel not found");
      return;
    }

    if (!unickkeySel) {
      console.warn("[ST ADMIN] unickkeySel not found (unickkeys field not rendered in inline)");
      return;
    }

    clearSelect(unickkeySel, "Select unickkeys");

    if (!variationSel.value) {
      console.warn("[ST ADMIN] no variation selected");
      return;
    }

    const url = `${baseAjax}/unickkeys/?from_branch_id=${fromBranchId}&variation_id=${variationSel.value}`;
    const data = await fetchJSON(url);

    const keys = data.results || [];
    console.log("[ST ADMIN] unick keys =", keys);

    //  Fill unickkeys select with multiple attribute
    keys.forEach((k) => {
      const opt = document.createElement("option");
      opt.value = k.id;
      opt.textContent = k.label;
      unickkeySel.appendChild(opt);
    });

    console.log("[ST ADMIN] Unickkeys loaded successfully");
  }

  async function init() {
    console.log("[ST ADMIN] init()");

    const fromBranch = $("#id_from_branch_name");
    if (!fromBranch) {
      console.warn("[ST ADMIN] from_branch field not found");
      return;
    }

    // When from_branch changes, reload all products
    fromBranch.addEventListener("change", async () => {
      console.log("[ST ADMIN] from branch changed");
      await loadProductsForAllRows();
    });

    // Event delegation for product and variation changes
    document.addEventListener("change", async (e) => {
      const t = e.target;

      // When product changes, load variations
      if (t && t.matches('select[id$="-product"]')) {
        console.log("[ST ADMIN] product changed", t.id, t.value);
        const row = getRowRootFromField(t);
        await loadVariationsForRow(row);
      }

      // When variation changes, load unickkeys
      if (t && t.matches('select[id$="-variation"]')) {
        console.log("[ST ADMIN] variation changed", t.id, t.value);
        const row = getRowRootFromField(t);
        await loadUnickForRow(row);
      }
    });

    // Initial load of products
    await loadProductsForAllRows();
  }

  // Wait for DOM ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();