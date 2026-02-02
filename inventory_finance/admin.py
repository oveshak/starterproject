from django.contrib import admin
from unfold.admin import ModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from .models import (
    StockTransfer, StockAdjustment, Daybook,
    Expense, VendorCheque, RepairRequest
)

# ✅ A base class that combines Unfold ModelAdmin with SimpleHistoryAdmin
class HistoryModelAdmin(SimpleHistoryAdmin, ModelAdmin):
    pass


from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F
from django.http import JsonResponse
from django.urls import path



from .models import StockTransfer, StockTransferLine
from products.models import BranchProductStock


# class StockTransferLineInline(admin.TabularInline):
#     model = StockTransferLine
#     extra = 1

#     # ✅ VERY IMPORTANT: render unickkeys field in inline
#     fields = ("product", "variation", "quantity", "unickkeys")

#     # JS দিয়ে options ভরবো, তাই শুরুতে queryset empty
#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name in ("product", "variation"):
#             kwargs["queryset"] = db_field.remote_field.model.objects.none()
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)

#     def formfield_for_manytomany(self, db_field, request, **kwargs):
#         if db_field.name == "unickkeys":
#             kwargs["queryset"] = db_field.remote_field.model.objects.none()
#         return super().formfield_for_manytomany(db_field, request, **kwargs)


class StockTransferLineInline(admin.TabularInline):
    model = StockTransferLine
    extra = 1
    fields = ("product", "variation", "quantity", "unickkeys")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ("product", "variation"):
            # ✅ POST এ validation লাগবে
            if request.method == "POST":
                kwargs["queryset"] = db_field.remote_field.model.objects.all()
            else:
                # ✅ GET এ empty, JS fill করবে
                kwargs["queryset"] = db_field.remote_field.model.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "unickkeys":
            if request.method == "POST":
                kwargs["queryset"] = db_field.remote_field.model.objects.all()
            else:
                kwargs["queryset"] = db_field.remote_field.model.objects.none()
        return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(StockTransfer)
class StockTransferAdmin(HistoryModelAdmin):
    list_display = ["from_branch_name", "to_branch_name", "transfer_date", "stc_status", "is_applied"]
    list_filter = ["from_branch_name", "to_branch_name", "stc_status", "transfer_date", "is_applied"]
    search_fields = ["from_branch_name__name", "to_branch_name__name", "stc_status"]
    inlines = [StockTransferLineInline]

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.is_applied:
            return ["from_branch_name", "to_branch_name", "transfer_date", "stc_status", "is_applied"]
        return ["is_applied"]

    # ---------------------------
    # ✅ Admin endpoints (JSON)
    # ---------------------------
    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path("ajax/products/", self.admin_site.admin_view(self.ajax_products), name="st_ajax_products"),
            path("ajax/variations/", self.admin_site.admin_view(self.ajax_variations), name="st_ajax_variations"),
            path("ajax/unickkeys/", self.admin_site.admin_view(self.ajax_unickkeys), name="st_ajax_unickkeys"),
        ]
        return custom + urls

    def ajax_products(self, request):
        """
        from_branch_id -> products that have variation stock available in that branch
        NOTE: আপনি যদি BranchProductStock.quantity ব্যবহার করেন, quantity__gt=0 রাখুন।
              আপনি যদি Variation.quantity ব্যবহার করেন, product_variation__quantity__gt=0 রাখুন।
        """
        branch_id = request.GET.get("from_branch_id")
        if not branch_id:
            return JsonResponse({"results": []})

        # ✅ Choose ONE of these filters (আমি এখানে Variation.quantity based রেখেছি কারণ আপনি বলেছেন product qty নাই)
        qs = (BranchProductStock.objects
              .filter(stock_branch_id=branch_id, product_variation__quantity__gt=0)
              .select_related("product_name")
              .values("product_name_id", "product_name__name")
              .distinct()
              .order_by("product_name__name"))

        return JsonResponse({"results": list(qs)})

    def ajax_variations(self, request):
        branch_id = request.GET.get("from_branch_id")
        product_id = request.GET.get("product_id")
        if not (branch_id and product_id):
            return JsonResponse({"results": []})

        # ✅ Variation.quantity based
        bps_qs = (BranchProductStock.objects
                  .filter(stock_branch_id=branch_id, product_name_id=product_id, product_variation__quantity__gt=0)
                  .select_related("product_variation")
                  .order_by("product_variation__id"))

        results, seen = [], set()
        for b in bps_qs:
            vid = b.product_variation_id
            if vid in seen:
                continue
            seen.add(vid)
            v = b.product_variation
            results.append({"id": vid, "label": str(v)})

        return JsonResponse({"results": results})

    def ajax_unickkeys(self, request):
        branch_id = request.GET.get("from_branch_id")
        variation_id = request.GET.get("variation_id")
        if not (branch_id and variation_id):
            return JsonResponse({"results": []})

        bps = (BranchProductStock.objects
               .filter(stock_branch_id=branch_id, product_variation_id=variation_id)
               .prefetch_related("unickkey")
               .first())
        if not bps:
            return JsonResponse({"results": []})

        return JsonResponse({
            "results": [{"id": u.id, "label": str(u)} for u in bps.unickkey.all()]
        })

    # ---------------------------
    # ✅ Stock Apply (posted হলে)
    # ---------------------------
    @transaction.atomic
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        transfer: StockTransfer = form.instance
        transfer.full_clean()

        # only apply when posted
        if transfer.is_applied:
            return
        if (transfer.stc_status or "").lower() != "posted":
            return

        if transfer.from_branch_name_id == transfer.to_branch_name_id:
            raise ValidationError("From branch এবং To branch একই হতে পারবে না।")

        lines = transfer.lines.select_related("variation", "product").prefetch_related("unickkeys")
        if not lines.exists():
            raise ValidationError("কমপক্ষে ১টা line add করতে হবে।")

        for line in lines:
            line.full_clean()

            product = line.product
            variation = line.variation
            qty = line.quantity
            is_unick = bool(getattr(variation, "is_unick", False))

            from_bps = (BranchProductStock.objects.select_for_update()
                        .filter(
                            stock_branch=transfer.from_branch_name,
                            product_name=product,
                            product_variation=variation
                        )
                        .prefetch_related("unickkey")
                        .first())
            if not from_bps:
                raise ValidationError(f"From branch এ stock নেই: {product} / {variation}")

            to_bps, _ = (BranchProductStock.objects.select_for_update()
                        .get_or_create(
                            stock_branch=transfer.to_branch_name,
                            product_name=product,
                            product_variation=variation,
                            defaults={"quantity": 0}
                        ))

            # qty check
            if from_bps.quantity < qty:
                raise ValidationError(
                    f"Stock কম: {product}/{variation} (have {from_bps.quantity}, need {qty})"
                )

            if is_unick:
                selected = list(line.unickkeys.all())

                # ✅ qty must equal number of selected keys
                if qty != len(selected):
                    raise ValidationError(
                        f"Unique variation হলে quantity({qty}) == selected unickkeys({len(selected)}) হতে হবে "
                        f"[{product}/{variation}]"
                    )

                # ✅ selected keys must exist in from branch stock keys
                from_ids = set(from_bps.unickkey.values_list("id", flat=True))
                need_ids = {u.id for u in selected}
                missing = need_ids - from_ids
                if missing:
                    raise ValidationError(
                        f"From branch এ এই unick keys নেই ({product}/{variation}): {sorted(list(missing))}"
                    )

                # ✅ qty move
                BranchProductStock.objects.filter(pk=from_bps.pk).update(quantity=F("quantity") - qty)
                BranchProductStock.objects.filter(pk=to_bps.pk).update(quantity=F("quantity") + qty)

                # ✅ KEY MOVE (this is what you want)
                from_bps.unickkey.remove(*selected)
                to_bps.unickkey.add(*selected)

            else:
                # normal (non-unique)
                BranchProductStock.objects.filter(pk=from_bps.pk).update(quantity=F("quantity") - qty)
                BranchProductStock.objects.filter(pk=to_bps.pk).update(quantity=F("quantity") + qty)

        transfer.is_applied = True
        transfer.save(update_fields=["is_applied"])
        messages.success(request, "✅ Stock transfer applied: qty updated + unick keys moved.")

    class Media:
        js = ("admin/js/stock_transfer_admin.js",)


@admin.register(StockAdjustment)
class StockAdjustmentAdmin(HistoryModelAdmin):
    list_display = ['branch_name', 'product_name', 'quantity_adjusted', 'reason']
    search_fields = ['branch_name__name', 'product_name__name', 'reason']
    list_filter = ['branch_name', 'product_name']


@admin.register(Daybook)
class DaybookAdmin(HistoryModelAdmin):
    list_display = [
        'branch_name', 'date', 'hand_cash', 'total_collection',
        'total_expenses', 'bank_transfer_to_ho', 'report_submitted_by_user_name'
    ]
    search_fields = ['branch_name__name', 'report_submitted_by_user_name__email']
    list_filter = ['branch_name', 'date']


@admin.register(Expense)
class ExpenseAdmin(HistoryModelAdmin):
    list_display = ['branch_name', 'expense_date', 'amount', 'expense_category']
    search_fields = ['branch_name__name', 'expense_category', 'description']
    list_filter = ['branch_name', 'expense_date', 'expense_category']


@admin.register(VendorCheque)
class VendorChequeAdmin(HistoryModelAdmin):
    list_display = ['cheque_number', 'vendor_name', 'issue_date', 'amount', 'vndcq_status']
    search_fields = ['cheque_number', 'vendor_name__name', 'vndcq_status']
    list_filter = ['vndcq_status', 'issue_date']


@admin.register(RepairRequest)
class RepairRequestAdmin(HistoryModelAdmin):
    list_display = [
        'product_name', 'customer_name', 'branch_name',
        'requested_by_user_name', 'request_date', 'repair_status'
    ]
    search_fields = ['product_name__name', 'customer_name__name', 'repair_status']
    list_filter = ['branch_name', 'repair_status', 'request_date']
