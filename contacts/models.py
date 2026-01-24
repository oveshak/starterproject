from django.db import models
from globalapp.models import Common
from users.models import Area, Branch, Users
from simple_history.models import HistoricalRecords


class CustomerGroup(Common):
    name = models.CharField(max_length=100, verbose_name="Group Name")

    # যদি Customer একই অ্যাপে থাকে, model string "Customer" দিন (case-sensitive)
    group_leader_user = models.ForeignKey(
        "Customer",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Group Leader User",
        related_name="lead_groups",
    )

    members = models.ManyToManyField(
        "Customer",
        blank=True,
        related_name="groups",
        verbose_name="Group Members",
    )

    customer_group_branch_name = models.ForeignKey(
        Branch, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Branch Name"
    )
    customer_group_area_name = models.ForeignKey(
        Area, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Area Name"
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Customer Group"
        verbose_name_plural = "Customer Groups"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Contact(Common):
    CONTACT_TYPES = (
        ('Supplier', 'Supplier'),
        
        ('Guarantor', 'Guarantor'),
    )

    type = models.CharField(
        max_length=20,
        choices=CONTACT_TYPES,
        verbose_name="Contact Type"
    )



    name = models.CharField(
        max_length=100,
        verbose_name="Full Name"
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Email Address"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Phone Number"
    )
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name="Address"
    )
    customer_group = models.ForeignKey(
        CustomerGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Customer Group"
    )
    branch_name = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Branch Name"
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        ordering = ["name"]

    def __str__(self):
        return self.name

class CustomerType(Common):
    name = models.CharField(max_length=150, verbose_name="Name")
    behaviour_type = models.JSONField(default=list, blank=True, null=True)

    customer_type_branch = models.ForeignKey(
        Branch, 
        on_delete=models.CASCADE, 
        related_name="customer_type", 
        null=True, 
        blank=True, 
        verbose_name="Branch"
    )

    class Meta:
        verbose_name = "Customer Type"
        verbose_name_plural = "Customer Type"
        ordering = ["name"]

    def __str__(self):
        return self.name

class Customer(Common):
    full_name = models.CharField(
        max_length=150,
        verbose_name="Full Name"
    )
    father_husband_name = models.CharField(
        max_length=150,
        verbose_name="Father/Husband Name"
    )
    mobile_number = models.CharField(
        max_length=20,
        verbose_name="Mobile Number"
    )
    
    secondary_mobile_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Secondary Mobile Number"
    )
    guarantor = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'type': 'Guarantor'},
        verbose_name="Guarantor"
    )
    nid_front = models.ImageField(
        upload_to='customer/nid/front/',
        blank=True,
        null=True,
        verbose_name="NID Front"
    )
    nid_back = models.ImageField(
        upload_to='customer/nid/back/',
        blank=True,
        null=True,
        verbose_name="NID Back"
    )
    nid_number = models.CharField(
        max_length=30,
        verbose_name="NID Number"
    )
    photo = models.ImageField(
        upload_to='customer/photos/',
        blank=True,
        null=True,
        verbose_name="Photo"
    )
    house_photo = models.ImageField(
        upload_to='customer/house_photos/',
        blank=True,
        null=True,
        verbose_name="House Photo"
    )
    utility_bill = models.ImageField(
        upload_to='customer/bills/',
        blank=True,
        null=True,
        verbose_name="Electric/Water Bill"
    )
    house_remark_bn = models.TextField(
        verbose_name="House Remark (Bangla)",
        blank=True,
        null=True
    )
    branch_name = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Branch Name"
    )
    area_name = models.ForeignKey(
        Area,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Area Name"
    )
    account_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    location_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Location URL"
    )
    customer_group = models.ForeignKey(
        CustomerGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Customers Group"
    )
    coustomer_type=models.ForeignKey(
        CustomerType,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Customer Type"
    )
    
    received_by = models.ForeignKey(
        Users,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Received By"
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name


