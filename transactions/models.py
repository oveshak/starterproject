from django.db import models
from globalapp.models import Common
from users.models import Area, Branch, Users
from products.models import Product
from contacts.models import Contact, Customer, CustomerGroup
from simple_history.models import HistoricalRecords

class Purchase(Common):
    supplier_name = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        null=True,
        related_name='purchases',
        verbose_name="Supplier"
    )
    branch_name = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        related_name='purchases',
        verbose_name="Branch"
    )
    purchase_date = models.DateField(verbose_name="Purchase Date")
    total_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Total Amount"
    )
    purchase_status = models.CharField(
        max_length=20,
        verbose_name="Purchase Status"
    )
    vendor_cheque_details = models.TextField(
        blank=True,
        null=True,
        verbose_name="Vendor Cheque Details"
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Purchase"
        verbose_name_plural = "Purchases"
        ordering = ['-purchase_date']

    def __str__(self):
        supplier = getattr(self, "supplier_name", None)
        if supplier is None:
            supplier = "Unknown Supplier"
        return f"{supplier} - {self.total_amount}"


class PurchaseItem(Common):
    purchase_name = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Purchase"
    )
    product_name = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='purchase_items',
        verbose_name="Product"
    )
    quantity = models.IntegerField(verbose_name="Quantity")
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Unit Price"
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Purchase Item"
        verbose_name_plural = "Purchase Items"
        ordering = ['-id']

    def __str__(self):
        return f"{self.product_name} ({self.quantity} x {self.unit_price})"


class PurchaseReturn(Common):
    purchase_name = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name='returns',
        verbose_name="Purchase"
    )
    return_date = models.DateField(verbose_name="Return Date")
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Purchase Return"
        verbose_name_plural = "Purchase Returns"
        ordering = ['-return_date']

    def __str__(self):
        return f"Return - {self.purchase_name}"


class Sale(Common):
    customer_name = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        null=True,
        related_name='sales',
        verbose_name="Customer"
    )
    branch_name = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        related_name='sales',
        verbose_name="Branch"
    )
    sale_date = models.DateField(verbose_name="Sale Date")
    total_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Total Amount"
    )
    sale_status = models.CharField(
        max_length=20,
        verbose_name="Sale Status"
    )
    loan_period = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Loan Period (Months)"
    )
    first_time_down_payment = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="First Time Down Payment"
    )
    emi_start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="EMI Start Date"
    )
    emi_end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="EMI End Date"
    )
    supervisor_user_name = models.ForeignKey(
        Users,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='supervised_sales',
        verbose_name="Supervisor"
    )
    manager_user_name = models.ForeignKey(
        Users,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_sales',
        verbose_name="Manager"
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Sale"
        verbose_name_plural = "Sales"
        ordering = ['-sale_date']

    def __str__(self):
        return f"{self.customer_name} - {self.total_amount}"


class SaleItem(Common):
    sale_name = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Sale"
    )
    product_name = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='sale_items',
        verbose_name="Product"
    )
    imei_number = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        verbose_name="IMEI Number"
    )
    quantity = models.IntegerField(verbose_name="Quantity")
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Unit Price"
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Sale Item"
        verbose_name_plural = "Sale Items"
        ordering = ['-id']

    def __str__(self):
        return f"{self.product_name} ({self.quantity} x {self.unit_price})"


class Payment(Common):
    sale_name = models.ForeignKey(
        Sale,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments',
        verbose_name="Sale"
    )
    customer_name = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        null=True,
        related_name='payments',
        verbose_name="Customer"
    )
    payment_date = models.DateField(verbose_name="Payment Date")
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Amount"
    )
    type = models.CharField(
        max_length=20,
        verbose_name="Payment Type"
    )
    payment_method = models.CharField(
        max_length=20,
        verbose_name="Payment Method"
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ['-payment_date']

    def __str__(self):
        return f"{self.customer_name} - {self.amount}"


class Cheque(Common):
    cheque_number = models.CharField(
        max_length=100,
        verbose_name="Cheque Number"
    )
    customer_name = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        null=True,
        related_name='cheques',
        verbose_name="Customer"
    )
    loan_name = models.ForeignKey(
        Sale,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cheques',
        verbose_name="Loan Sale"
    )
    cheque_status = models.CharField(
        max_length=20,
        verbose_name="Cheque Status"
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Cheque"
        verbose_name_plural = "Cheques"
        ordering = ['-id']

    def __str__(self):
        return f"{self.cheque_number} - {self.customer_name}"


class AffiliateCommission(Common):
    affiliate_user_name = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='affiliate_commissions',
        verbose_name="Affiliate User"
    )
    sale_name = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name='affiliate_commissions',
        verbose_name="Sale"
    )
    commission_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Commission Amount"
    )
    affiliate_status = models.CharField(
        max_length=20,
        verbose_name="Affiliate Status"
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Affiliate Commission"
        verbose_name_plural = "Affiliate Commissions"
        ordering = ['-id']

    def __str__(self):
        return f"{self.affiliate_user_name} - {self.commission_amount}"


class LoanType(Common):
    name = models.CharField(max_length=150, verbose_name="Name")
    behaviour_type = models.JSONField(default=list, blank=True, null=True)

    loan_branch = models.ForeignKey(
        Branch, 
        on_delete=models.CASCADE, 
        related_name="loan_types", 
        null=True, 
        blank=True, 
        verbose_name="Branch"
    )

    class Meta:
        verbose_name = "Loan Type"
        verbose_name_plural = "Loan Types"
        ordering = ["name"]

    def __str__(self):
        return self.name
 

class InstallmentType(Common):
    TYPE_CHOICES = [
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
        ("yearly", "Yearly"),
    ]

    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name="Type"
    )
    instalment_cullect = models.IntegerField(verbose_name="Amount")
    total_duration = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Total Duration"
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Installment Type"
        verbose_name_plural = "Installment Types"
        ordering = ["type"]

    def __str__(self):
        return f"{self.get_type_display()} - {self.instalment_cullect}"


class DailySaving(Common):
    customer_name = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name="Customer"
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Amount"
    )
    received_by = models.ForeignKey(
        Users,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Received By"
    )
    branch_name = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="dailysavings_branches",
        null=True,
        blank=True,
        verbose_name="Branch"
    )
    area_name = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        related_name="dailysavings_areas",
        null=True,
        blank=True,
        verbose_name="Area"
    )
    
    class Meta:
        verbose_name = "DailySaving"
        verbose_name_plural = "DailySavings"
        ordering = ["amount"]

    def __str__(self):
        return f" {self.amount} "


class Installment(Common):
    STATUS_CHOICES = [
        ("paid", "Paid"),
        ("due", "Due"),
    ]
    
    customer_name = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name="Customer"
    )
    due_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Due Amount"
    )
    installment_date = models.DateField(verbose_name="Installment Date")
    installment_pay = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Installment Pay",
        null=True,
        blank=True,
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Amount")
    received_by = models.ForeignKey(
        Users,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Received By"
    )
    installment_status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        verbose_name="Status"
    )
    branch_name = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="installments_branches",
        null=True,
        blank=True,
        verbose_name="Branch"
    )
    area_name = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        related_name="installments_areas",
        null=True,
        blank=True,
        verbose_name="Area"
    )
    loan_id = models.CharField(max_length=20, default="N/A")
    pay_from_account = models.BooleanField(
        default=False,
        verbose_name="Pay From Account"
    )

    class Meta:
        verbose_name = "Installment"
        verbose_name_plural = "Installments"
        ordering = ["-installment_date"]

    def __str__(self):
        return f"{self.installment_date} - {self.amount}"

    def is_extra_payment(self):
        """Check if installment pay is greater than amount."""
        if self.installment_pay:
            return self.installment_pay > self.amount
        return False

    def update_due_and_status(self):
        """Update due_amount, paid_amount, and installment status"""
        if self.installment_pay is not None:
            paid = self.installment_pay
            due = self.due_amount

            if paid >= due:
                # Fully paid
                self.installment_status = "paid"
                self.due_amount = 0
            else:
                # Partially paid
                self.installment_status = "due"
                self.due_amount = due - paid
            self.save(update_fields=["installment_status", "due_amount"])


class Loan(Common):
    RECEIVE_TYPE_CHOICES = [
        ("cash", "Cash"),
        ("product", "Product"),
    ]
    
    branch_name = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="loan_branch_set",
        null=True,
        blank=True,
        verbose_name="Branch"
    ) 
    area_name = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        related_name="loan_area_set",
        null=True,
        blank=True,
        verbose_name="Area"
    )
    customer_name = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name="Customer Name"
    )
    receive_type = models.CharField(
        max_length=20,
        choices=RECEIVE_TYPE_CHOICES,
        verbose_name="Receive Type"
    )
    product_details = models.JSONField(
        verbose_name="Product Details",
        blank=True,
        null=True
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Amount"
    )
    loan_type = models.ForeignKey(
        LoanType,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Loan Type"
    )
    installment = models.ManyToManyField(
        Installment,
        blank=True,
        verbose_name="Installments"
    )
    pay_from_account = models.BooleanField(
        default=False,
        verbose_name="Pay From Account"
    )
    installment_type = models.ForeignKey(
        InstallmentType,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Installment Type"
    )
    first_down_payment = models.DecimalField(
        null=True,
        blank=True,
        max_digits=12,
        decimal_places=2,
        verbose_name="First Down Payment"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Loan"
        verbose_name_plural = "Loans"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.customer_name} - {self.amount} ({self.receive_type})"


class Transection(Common):
    TYPE_CHOICES = [
        ("cashin", "Cash In"),
        ("cashout", "Cash Out"),
    ]
    
    transection_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        verbose_name="Status"
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Amount"
    )
    paid_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Paid Amount",
        null=True,
        blank=True
    )
    due_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Due Amount",
        null=True,
        blank=True
    )
    customer_name = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name="Customer Name"
    )

    received_by = models.ForeignKey(
        Users,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Received By"
    )
    modelname = models.CharField(max_length=200, verbose_name="Model Name", null=True, blank=True)
    branch_name = models.ForeignKey(
        Branch,  # Replace with your actual Branch model
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Branch Name"
    )
    area_name = models.ForeignKey(
        Area,  # Replace with your actual Area model
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Area Name"
    )
    customer_group = models.ForeignKey(
        CustomerGroup,  # Replace with your actual CustomerGroup model
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Customer Group"
    )

    def save(self, *args, **kwargs):
        # Auto-populate from customer if not provided
        if self.customer_name:
            if not self.branch_name and hasattr(self.customer_name, 'branch_name'):
                self.branch_name = self.customer_name.branch_name
            if not self.area_name and hasattr(self.customer_name, 'area_name'):
                self.area_name = self.customer_name.area_name
            if not self.customer_group and hasattr(self.customer_name, 'customer_group'):
                self.customer_group = self.customer_name.customer_group

        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transection_type} - {self.amount} for {self.modelname}"


