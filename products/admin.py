# from django.contrib import admin
# from unfold.admin import ModelAdmin
# from .models import (
#     Product, Unit, Category, Brand, Warranty,
#     SellingPriceGroup, Variation, BranchProductStock
# )
# class VariationInline(admin.TabularInline):
#     model = Variation
#     fk_name = "product_name"
#     extra = 1
#     fields = ("name", "sku_suffix")
#     show_change_link = True

# class VariationInline(admin.TabularInline):
#     model = Variation
#     fk_name = "product_name"
#     extra = 1
#     fields = ("name", "sku_suffix")
#     show_change_link = True

# @admin.register(Unit)
# class UnitAdmin(ModelAdmin):
#     list_display = ['name']
#     search_fields = ['name']

# @admin.register(Category)
# class CategoryAdmin(ModelAdmin):
#     list_display = ['name']
#     search_fields = ['name']

# @admin.register(Brand)
# class BrandAdmin(ModelAdmin):
#     list_display = ['name']
#     search_fields = ['name']

# @admin.register(Warranty)
# class WarrantyAdmin(ModelAdmin):
#     list_display = ['name', 'duration', 'duration_type']
#     search_fields = ['name']
#     list_filter = ['duration_type']

# @admin.register(SellingPriceGroup)
# class SellingPriceGroupAdmin(ModelAdmin):
#     list_display = ['name', 'price_multiplier']
#     search_fields = ['name']

# @admin.register(Product)
# class ProductAdmin(ModelAdmin):
#     list_display = ['name', 'sku', 'unit_name', 'category_name', 'brand_name', 'warranty_name']
#     search_fields = ['name', 'sku']
#     list_filter = ['unit_name', 'category_name', 'brand_name']

#     inlines = [VariationInline]

# @admin.register(Variation)
# class VariationAdmin(ModelAdmin):
#     list_display = ['name', 'sku_suffix', 'product_name']
#     search_fields = ['name', 'sku_suffix']
#     list_filter = ['product_name']
from django.contrib import admin
from django.forms import ModelForm
from unfold.admin import ModelAdmin
from .models import (
    BranchProductStock,
    Product,
    SellingPriceGroup,
    Unit,
    Category,
    Brand,
    Warranty,
    Variation,
    VariationAttribute,
    VariationAttributeValue,
    unick,
)


# ---------- ATTRIBUTE VALUE INLINE ----------

class VariationAttributeValueInline(admin.TabularInline):
    model = VariationAttributeValue
    fk_name = "variation_ref"
    extra = 1


# ---------- VARIATION INLINE (INSIDE PRODUCT PAGE) ----------

class VariationInline(admin.TabularInline):
    model = Variation
    fk_name = "product_name"
    extra = 1
    show_change_link = True
    fields = ("sku_suffix", "price", "quantity")


# ---------- PRODUCT ADMIN ----------
from django.urls import reverse
from django.utils.html import format_html
@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ["name", "sku", "brand_name", "category_name"]
    search_fields = ["name", "sku"]
    inlines = [VariationInline]

    

# ---------- VARIATION ADMIN ----------
from django.core.exceptions import ValidationError
@admin.register(unick)
class UnickAdmin(ModelAdmin):
    list_display = ("key1", "key2")
    search_fields = ("key1", "key2")

class VariationAdminForm(ModelForm):
    class Meta:
        model = Variation
        fields = "__all__"

    def clean(self):
        cleaned = super().clean()

        isunck = cleaned.get("isunck")
        quantity = cleaned.get("quantity") or 0
        unickkey = cleaned.get("unickkey")

        if isunck:
            count = unickkey.count() if unickkey else 0
            if quantity != count:
                raise ValidationError({
                    "quantity": (
                        f"Quantity must exactly equal UnickKey count ({count}) "
                        f"when isunck is True."
                    )
                })

        return cleaned


@admin.register(Variation)
class VariationAdmin(ModelAdmin):
    form = VariationAdminForm
    list_display = ("product_name", "name", "quantity", "isunck")
    filter_horizontal = ("unickkey",)
    inlines = [VariationAttributeValueInline]



# ---------- ATTRIBUTE ADMIN ----------

@admin.register(VariationAttribute)
class VariationAttributeAdmin(ModelAdmin):
    list_display = ["name", "order"]


@admin.register(Unit)
class UnitAdmin(ModelAdmin):
    list_display = ["name"]


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ["name"]


@admin.register(Brand)
class BrandAdmin(ModelAdmin):
    list_display = ["name"]


@admin.register(Warranty)
class WarrantyAdmin(ModelAdmin):
    list_display = ["name", "duration", "duration_type"]

@admin.register(SellingPriceGroup)
class SellingPriceGroupAdmin(ModelAdmin):
    list_display = ['name', 'price_multiplier']
    search_fields = ['name']

# @admin.register(BranchProductStock)
# class BranchProductStockAdmin(ModelAdmin):
#     list_display = ['product_name', 'branch_name', 'quantity', 'opening_stock']
#     search_fields = ['product_name__name', 'branch_name__name']
#     list_filter = ['branch_name']

# @admin.register(BranchProductStock)
# class BranchProductStockAdmin(ModelAdmin):
#     list_display = ["product_name", "product_variation", "stock_branch", "quantity"]

#     class Media:
#         js = ("admin/js/product_variation.js",)


from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from .models import BranchProductStock

# class BranchProductStockAdminForm(forms.ModelForm):
#     class Meta:
#         model = BranchProductStock
#         fields = "__all__"

#     def clean(self):
#         cleaned = super().clean()
#         variation = cleaned.get("product_variation")
#         qty = cleaned.get("quantity") or 0
#         unickkeys = cleaned.get("unickkey")

#         if variation and variation.isunck:
#             count = unickkeys.count() if unickkeys else 0
#             if qty != count:
#                 raise ValidationError({"quantity": f"Quantity must equal UnickKey count ({count}) for unique variation."})

#         return cleaned


from django import forms
from django.core.exceptions import ValidationError
from products.models import Variation  # ✅ your model name

class BranchProductStockAdminForm(forms.ModelForm):
    class Meta:
        model = BranchProductStock
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # edit page: instance থেকে product
        product_id = None
        if self.instance and self.instance.pk:
            product_id = self.instance.product_name_id

        # add/post: form data থেকে product
        if not product_id:
            product_id = self.data.get("product_name") or None

        # ✅ queryset filter (এতে saved variation list-এর ভিতর থাকবে)
        if product_id:
            self.fields["product_variation"].queryset = Variation.objects.filter(
                product_name_id=product_id
            )
        else:
            self.fields["product_variation"].queryset = Variation.objects.none()

        # ✅ edit page এ initial set
        if self.instance and self.instance.pk and self.instance.product_variation_id:
            self.fields["product_variation"].initial = self.instance.product_variation_id

    def clean(self):
        cleaned = super().clean()
        variation = cleaned.get("product_variation")
        qty = cleaned.get("quantity") or 0
        unicks = cleaned.get("unickkey")

        if variation and variation.isunck:
            cnt = unicks.count() if unicks else 0
            if qty != cnt:
                raise ValidationError({"quantity": f"Quantity must equal UnickKey count ({cnt}) for unique variation."})

            if unicks and BranchProductStock.objects.filter(
                product_variation=variation,
                unickkey__in=unicks
            ).exclude(pk=self.instance.pk).exists():
                raise ValidationError({"unickkey": "One or more UnickKey already assigned to another branch."})
        else:
            if unicks and unicks.exists():
                raise ValidationError({"unickkey": "This variation is not unique; do not assign UnickKey."})

        return cleaned


@admin.register(BranchProductStock)
class BranchProductStockAdmin(ModelAdmin):
    form = BranchProductStockAdminForm
    list_display = ["product_name", "product_variation", "stock_branch", "quantity"]
    filter_horizontal = ("unickkey",)

    class Media:
        js = ("admin/js/product_variation.js",)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication
from products.models import Variation

class AdminVariationByProductView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        product_id = request.GET.get("product")
        qs = Variation.objects.filter(product_name_id=product_id) if product_id else []

        return Response([
            {
                "id": v.id,
                "name": v.name,
                "isunck": v.isunck   # 🔥 REQUIRED
            }
            for v in qs
        ])
        
