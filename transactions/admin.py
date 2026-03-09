from django.contrib import admin
from unfold.admin import ModelAdmin

from products.models import Variation, unick
from .models import (
    DailySaving, DownPayment, Installment, InstallmentType, Loan, LoanType, Purchase, PurchaseItem, PurchaseReturn,
    Sale, SaleItem, Payment, Cheque, AffiliateCommission, Transection
)

from django import forms
from django.core.exceptions import ValidationError


class PurchaseAdminForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = "__all__"

    def clean(self):
        cleaned = super().clean()

        variation = cleaned.get("purchase_product_variation")
        unickkeys = cleaned.get("unickkey")
        qty = cleaned.get("qty")

        if variation and variation.isunck:
            count = unickkeys.count() if unickkeys else 0

            if count == 0:
                raise ValidationError("UnickKey is required for this variation.")

            if qty != count:
                raise ValidationError(
                    f"Quantity must equal UnickKey count ({count}) for isunck variation."
                )

        return cleaned


@admin.register(Purchase)
class PurchaseAdmin(ModelAdmin):
    
    list_display = ['supplier_name', 'purchase_date', 'total_amount', 'purchase_status']
    list_filter = ['purchase_status', 'purchase_date']
    filter_horizontal = ("purchaseitem",)


@admin.register(PurchaseItem)
class PurchaseItemAdmin(ModelAdmin):
    form = PurchaseAdminForm
    filter_horizontal = ("unickkey",)

    class Media:
        js = ("admin/js/purchase_variation_v2.js",)

@admin.register(PurchaseReturn)
class PurchaseReturnAdmin(ModelAdmin):
    list_display = ['purchase_name', 'return_date']
    search_fields = ['purchase_name__id']
    list_filter = ['return_date']

@admin.register(Sale)
class SaleAdmin(ModelAdmin):
    list_display = [
        'customer_name', 'branch_name', 'sale_date', 'total_amount', 'sale_status',
        'supervisor_user_name', 'manager_user_name'
    ]
    search_fields = ['customer_name__name', 'sale_status', 'supervisor_user_name__email', 'manager_user_name__email']
    list_filter = ['branch_name', 'sale_status', 'sale_date']

@admin.register(SaleItem)
class SaleItemAdmin(ModelAdmin):
    list_display = ['sale_name', 'product_name', 'imei_number', 'quantity', 'unit_price']
    search_fields = ['imei_number', 'product_name__name', 'sale_name__id']
    list_filter = ['product_name', 'sale_name']

@admin.register(Payment)
class PaymentAdmin(ModelAdmin):
    list_display = ['sale_name', 'customer_name', 'payment_date', 'amount', 'type', 'payment_method']
    search_fields = ['customer_name__name', 'type', 'payment_method']
    list_filter = ['type', 'payment_method', 'payment_date']

@admin.register(Cheque)
class ChequeAdmin(ModelAdmin):
    list_display = ['cheque_number', 'customer_name', 'loan_name', 'cheque_status']
    search_fields = ['cheque_number', 'customer_name__name', 'cheque_status']
    list_filter = ['cheque_status']

@admin.register(AffiliateCommission)
class AffiliateCommissionAdmin(ModelAdmin):
    list_display = ['affiliate_user_name', 'sale_name', 'commission_amount', 'affiliate_status']
    search_fields = ['affiliate_user_name__email', 'affiliate_status']
    list_filter = ['affiliate_status']
@admin.register(LoanType)
class LoanTypeAdmin(ModelAdmin):
    list_display = ['name', 'behaviour_type']
    search_fields = ['name', 'behaviour_type']
    list_filter = ['behaviour_type']


@admin.register(InstallmentType)
class InstallmentTypeAdmin(ModelAdmin):
    list_display = ['type', 'instalment_cullect']
    search_fields = ['type']
    list_filter = ['type']

@admin.register(DailySaving)
class DailySavingAdmin(ModelAdmin):
    list_display = ('customer_name', 'amount', 'received_by', 'branch_name', 'area_name')  # Fields to display
    search_fields = ('customer_name__name', 'branch_name__name', 'area_name__name')  # Searchable fields
    list_filter = ('branch_name', 'area_name')  # Fields to filter by
    ordering = ('amount',)


@admin.register(DownPayment)
class DownPaymentAdmin(ModelAdmin):
    list_display = (
        'title',
        'ispercentage',
        'amount_or_percentage',
        'branch_name',
        'area_name',
    )

    list_filter = (
        'ispercentage',
        'branch_name',
        'area_name',
    )

    search_fields = (
        'title',
    )

    ordering = ('amount_or_percentage',)

@admin.register(Installment)
class InstallmentAdmin(ModelAdmin):
    list_display = ['customer_name', 'installment_date', 'amount', 'received_by', 'installment_status']
    search_fields = ['customer_name__full_name', 'customer_name__mobile_number']
    list_filter = ['installment_status', 'installment_date']

@admin.register(Loan)
class LoanAdmin(ModelAdmin):
    list_display = ['customer_name', 'receive_type', 'amount', 'loan_type', 'pay_from_account', 'installment_type']
    search_fields = ['customer_name__full_name', 'customer_name__mobile_number', 'loan_type__name']
    list_filter = ['receive_type', 'pay_from_account', 'loan_type', 'installment_type']
    filter_horizontal = ['installment']  # for ManyToMany field

@admin.register(Transection)
class TransectionAdmin(ModelAdmin):
    # List display will show these fields in the admin panel
    list_display = ('id', 'transection_type', 'amount', 'customer_name', 'received_by', 'modelname', 'created_at')
    
    # Filter options in the sidebar
    list_filter = ('transection_type', 'customer_name', 'received_by')
    
    # Search bar functionality
    search_fields = ('customer_name', 'transection_type', 'amount')
    
    # Ordering of the records (optional)
    ordering = ['-created_at']
    
    # Add/edit form fields customization
    fields = ('transection_type', 'amount', 'customer_name', 'received_by', 'modelname', 'created_at')
    
    # You can also define readonly_fields to make fields read-only if needed
    readonly_fields = ('created_at',)



