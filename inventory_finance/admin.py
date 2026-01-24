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


@admin.register(StockTransfer)
class StockTransferAdmin(HistoryModelAdmin):
    list_display = ['from_branch_name', 'to_branch_name', 'transfer_date', 'stc_status']
    search_fields = ['from_branch_name__name', 'to_branch_name__name', 'stc_status']
    list_filter = ['from_branch_name', 'to_branch_name', 'stc_status', 'transfer_date']


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
