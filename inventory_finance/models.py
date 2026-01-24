from django.db import models
from globalapp.models import Common
from users.models import Branch, Users
from products.models import Product
from contacts.models import Contact
from simple_history.models import HistoricalRecords


class StockTransfer(Common):
    from_branch_name = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name='sent_transfers',
        verbose_name="From Branch"
    )
    to_branch_name = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name='received_transfers',
        verbose_name="To Branch"
    )
    transfer_date = models.DateField(
        verbose_name="Transfer Date"
    )
    stc_status = models.CharField(
        max_length=20,
        verbose_name="Status"
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Stock Transfer"
        verbose_name_plural = "Stock Transfers"
        ordering = ["-transfer_date"]

    def __str__(self):
        return f"{self.from_branch_name} → {self.to_branch_name} ({self.transfer_date})"


class StockAdjustment(Common):
    branch_name = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        verbose_name="Branch"
    )
    product_name = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Product"
    )
    quantity_adjusted = models.IntegerField(
        verbose_name="Quantity Adjusted"
    )
    reason = models.TextField(
        verbose_name="Reason"
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Stock Adjustment"
        verbose_name_plural = "Stock Adjustments"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.product_name} ({self.quantity_adjusted})"


class Daybook(Common):
    branch_name = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        verbose_name="Branch"
    )
    date = models.DateField(
        unique=True,
        verbose_name="Date"
    )
    hand_cash = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Hand Cash"
    )
    total_collection = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Total Collection"
    )
    total_expenses = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Total Expenses"
    )
    bank_transfer_to_ho = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Bank Transfer to HO"
    )
    report_submitted_by_user_name = models.ForeignKey(
        Users,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Report Submitted By"
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Daybook"
        verbose_name_plural = "Daybooks"
        ordering = ["-date"]

    def __str__(self):
        return f"{self.branch_name} - {self.date}"


class Expense(Common):
    branch_name = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        verbose_name="Branch"
    )
    expense_date = models.DateField(
        verbose_name="Expense Date"
    )
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Amount"
    )
    description = models.TextField(
        verbose_name="Description"
    )
    expense_category = models.CharField(
        max_length=50,
        verbose_name="Expense Category"
    )
    voucher_image_url = models.ImageField(
    upload_to="voucher_images/",   # এখানে কোথায় সেভ হবে সেটাও define করা ভালো
    blank=True,
    null=True,
    verbose_name="Voucher Image URL"
)

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"
        ordering = ["-expense_date"]

    def __str__(self):
        return f"{self.expense_category} - {self.amount}"


class VendorCheque(Common):
    cheque_number = models.CharField(
        max_length=100,
        verbose_name="Cheque Number"
    )
    vendor_name = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Vendor Name"
    )
    issue_date = models.DateField(
        verbose_name="Issue Date"
    )
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Amount"
    )
    vndcq_status = models.CharField(
        max_length=20,
        verbose_name="Status"
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Vendor Cheque"
        verbose_name_plural = "Vendor Cheques"
        ordering = ["-issue_date"]

    def __str__(self):
        return f"{self.cheque_number} - {self.vendor_name}"


class RepairRequest(Common):
    product_name = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Product"
    )
    customer_name = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Customer Name"
    )
    branch_name = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        verbose_name="Branch"
    )
    requested_by_user_name = models.ForeignKey(
        Users,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Requested By"
    )
    request_date = models.DateField(
        verbose_name="Request Date"
    )
    repair_status = models.CharField(
        max_length=20,
        verbose_name="Repair Status"
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Notes"
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Repair Request"
        verbose_name_plural = "Repair Requests"
        ordering = ["-request_date"]

    def __str__(self):
        return f"{self.product_name} - {self.repair_status}"
