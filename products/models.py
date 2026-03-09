# from django.db import models
# from globalapp.models import Common
# from users.models import Branch




# class Unit(Common):
#     name = models.CharField(
#         max_length=50,
#         verbose_name="Unit Name"
#     )

#     class Meta:
#         verbose_name = "Unit"
#         verbose_name_plural = "Units"
#         ordering = ["name"]

#     def __str__(self):
#         return self.name


# class Category(Common):
#     name = models.CharField(
#         max_length=100,
#         verbose_name="Category Name"
#     )

#     class Meta:
#         verbose_name = "Category"
#         verbose_name_plural = "Categories"
#         ordering = ["name"]

#     def __str__(self):
#         return self.name


# class Brand(Common):
#     name = models.CharField(
#         max_length=100,
#         verbose_name="Brand Name"
#     )

#     class Meta:
#         verbose_name = "Brand"
#         verbose_name_plural = "Brands"
#         ordering = ["name"]

#     def __str__(self):
#         return self.name


# class Warranty(Common):
#     DURATION_TYPES = (
#         ('Days', 'Days'),
#         ('Months', 'Months'),
#         ('Years', 'Years'),
#     )
#     name = models.CharField(
#         max_length=100,
#         verbose_name="Warranty Name"
#     )
#     duration = models.IntegerField(
#         verbose_name="Duration"
#     )
#     duration_type = models.CharField(
#         max_length=10,
#         choices=DURATION_TYPES,
#         verbose_name="Duration Type"
#     )

#     class Meta:
#         verbose_name = "Warranty"
#         verbose_name_plural = "Warranties"
#         ordering = ["name"]

#     def __str__(self):
#         return self.name


# class SellingPriceGroup(Common):
#     name = models.CharField(
#         max_length=100,
#         verbose_name="Price Group Name"
#     )
#     price_multiplier = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         verbose_name="Price Multiplier"
#     )

#     class Meta:
#         verbose_name = "Selling Price Group"
#         verbose_name_plural = "Selling Price Groups"
#         ordering = ["name"]

#     def __str__(self):
#         return self.name


# class Product(Common):
#     name = models.CharField(
#         max_length=200,
#         verbose_name="Product Name"
#     )
#     sku = models.CharField(
#         max_length=50,
#         unique=True,
#         verbose_name="SKU"
#     )
#     unit_name = models.ForeignKey(
#         Unit,
#         on_delete=models.SET_NULL,
#         null=True,
#         verbose_name="Unit"
#     )
#     category_name = models.ForeignKey(
#         Category,
#         on_delete=models.SET_NULL,
#         null=True,
#         verbose_name="Category"
#     )
#     brand_name = models.ForeignKey(
#         Brand,
#         on_delete=models.SET_NULL,
#         null=True,
#         verbose_name="Brand"
#     )
#     warranty_name = models.ForeignKey(
#         Warranty,
#         on_delete=models.SET_NULL,
#         null=True,
#         verbose_name="Warranty"
#     )
#     thumbnail_image = models.ImageField(
#         upload_to='products/thumbnails/',
#         null=True,
#         blank=True,
#         verbose_name="Thumbnail Image"
#     )
#     price = models.DecimalField(
#         max_digits=15,
#         decimal_places=2,
#         null=True,
#         blank=True,
#         verbose_name="Price"
#     )

#     class Meta:
#         verbose_name = "Product"
#         verbose_name_plural = "Products"
#         ordering = ["name"]

#     def __str__(self):
#         return self.name

# class Variation(Common):
#     product_name = models.ForeignKey(
#         Product,
#         on_delete=models.CASCADE,
#         related_name='variations',
#         verbose_name="Product"
#     )
#     name = models.CharField(
#         max_length=100,
#         verbose_name="Variation Name"
#     )
#     sku_suffix = models.CharField(
#         max_length=50,
#         verbose_name="SKU Suffix"
#     )

#     class Meta:
#         verbose_name = "Variation"
#         verbose_name_plural = "Variations"
#         ordering = ["name"]

#     def __str__(self):
#         return f"{self.product_name} - {self.name}"


from users.models import Branch


# ------------------ BASIC ------------------
from django.db import models
from globalapp.models import Common
from django.core.exceptions import ValidationError

from django.core.exceptions import ValidationError
from django.db.models import Sum
# ------------------ Unit ------------------

class Unit(Common):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# ------------------ Category ------------------

class Category(Common):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
# ------------------ Brand ------------------

class Brand(Common):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# ------------------ Warranty ------------------

class Warranty(Common):
    DURATION_TYPES = (
        ('Days', 'Days'),
        ('Months', 'Months'),
        ('Years', 'Years'),
    )
    name = models.CharField(max_length=100)
    duration = models.IntegerField()
    duration_type = models.CharField(max_length=10, choices=DURATION_TYPES)

    def __str__(self):
        return self.name


# ------------------ PRODUCT ------------------

class Product(Common):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True)

    unit_name = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True)
    category_name = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    brand_name = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    warranty_name = models.ForeignKey(Warranty, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


# ------------------ VARIATION ATTRIBUTE ------------------

class VariationAttribute(Common):
    """
    Universal attributes:
    Color, RAM, Storage, Size, IMEI, Batch, Expiry, Fabric etc.
    """
    name = models.CharField(max_length=50, unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name

# ------------------ Unick Key ------------------
class unick(Common):
    key1 = models.CharField(max_length=100,unique=True)
    key2 = models.CharField(max_length=100,unique=True,null=True)
    def __str__(self):
        return f'{self.key1}- {self.key2}'

# ------------------ VARIATION ------------------



class Variation(Common):
    product_name = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variations"
    )

    name = models.CharField(max_length=300, blank=True)
    sku_suffix = models.CharField(max_length=50, blank=True)

    price = models.DecimalField(max_digits=15, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    dealer_price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    isunck = models.BooleanField(default=False)
    unickkey = models.ManyToManyField(unick, blank=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.product_name.name} - {self.name}"

# ------------------ VARIATION ATTRIBUTE VALUE ------------------

class VariationAttributeValue(Common):
    variation_ref = models.ForeignKey(
        Variation,
        on_delete=models.CASCADE,
        related_name="attribute_values"
    )
    attribute = models.ForeignKey(
        VariationAttribute,
        on_delete=models.CASCADE
    )
    value = models.CharField(max_length=150)

    class Meta:
        # same attribute twice in same variation not allowed
        unique_together = ("variation_ref", "attribute")

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


# ------------------ SellingPriceGroup VALUE ------------------

class SellingPriceGroup(Common):
    name = models.CharField(
        max_length=100,
        verbose_name="Price Group Name"
    )
    price_multiplier = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Price Multiplier"
    )

    class Meta:
        verbose_name = "Selling Price Group"
        verbose_name_plural = "Selling Price Groups"
        ordering = ["name"]

    def __str__(self):
        return self.name




# class BranchProductStock(Common):
#     product_name = models.ForeignKey(
#         Product,
#         on_delete=models.CASCADE,
#         verbose_name="Product"
#     )
#     branch_name = models.ForeignKey(
#         Branch,
#         on_delete=models.CASCADE,
#         verbose_name="Branch"
#     )
#     quantity = models.IntegerField(
#         verbose_name="Quantity"
#     )
#     opening_stock = models.IntegerField(
#         verbose_name="Opening Stock"
#     )

#     class Meta:
#         verbose_name = "Branch Product Stock"
#         verbose_name_plural = "Branch Product Stocks"
#         ordering = ["product_name"]

#     def __str__(self):
#         return f"{self.product_name} - {self.branch_name}"


# class BranchProductStock(Common):
#     # product_name = models.ForeignKey(
#     #      Product,
#     #      on_delete=models.CASCADE,
#     #      verbose_name="Product"
#     # )
#     product_variation = models.ForeignKey(
#         "products.Variation",
#         on_delete=models.CASCADE,
#         related_name="branch_stocks",
#         verbose_name="Variation"
#     )

#     stock_branch = models.ForeignKey(
#         Branch,
#         on_delete=models.CASCADE,
#         verbose_name="Branch"
#     )

#     quantity = models.PositiveIntegerField(default=0)

#     class Meta:
#         unique_together = ("product_variation", "stock_branch")
#         ordering = ["product_variation"]

#     def __str__(self):
#         return f"{self.product_variation.name} - {self.stock_branch.name}"


# from django.core.exceptions import ValidationError
# from django.db.models import Sum

# class BranchProductStock(Common):
#     product_name = models.ForeignKey(
#         Product,
#         on_delete=models.CASCADE,
#         verbose_name="Product"
#     )
#     product_variation = models.ForeignKey(
#         "products.Variation",
#         on_delete=models.CASCADE,
#         related_name="branch_stocks",
#         verbose_name="Variation"
#     )
#     stock_branch = models.ForeignKey(
#         Branch,
#         on_delete=models.CASCADE,
#         verbose_name="Branch"
#     )
#     quantity = models.PositiveIntegerField(default=0)

#     class Meta:
#         unique_together = ("product_variation", "stock_branch")

#     def clean(self):
#         """
#         Prevent branch stock exceeding variation quantity
#         """
#         existing_total = BranchProductStock.objects.filter(
#             product_variation=self.product_variation
#         ).exclude(pk=self.pk).aggregate(
#             total=Sum("quantity")
#         )["total"] or 0

#         if existing_total + self.quantity > self.product_variation.quantity:
#             raise ValidationError({
#                 "quantity": (
#                     f"Total branch quantity ({existing_total + self.quantity}) "
#                     f"cannot exceed variation quantity "
#                     f"({self.product_variation.quantity})."
#                 )
#             })

#     def save(self, *args, **kwargs):
#         self.full_clean()   #  force validation
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.product_variation.name} - {self.stock_branch.name}"
# from django.core.exceptions import ValidationError
# from django.db.models import Sum

# class BranchProductStock(Common):
#     product_name = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product")
#     product_variation = models.ForeignKey(
#         "products.Variation",
#         on_delete=models.CASCADE,
#         related_name="branch_stocks",
#         verbose_name="Variation"
#     )
#     stock_branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name="Branch")
#     quantity = models.PositiveIntegerField(default=0)

#     # 🔥 NEW: branch-wise unique allocation
#     unickkey = models.ManyToManyField("products.unick", blank=True)

#     class Meta:
#         unique_together = ("product_variation", "stock_branch")

#     def clean(self):
#         # basic guard
#         if self.product_variation and self.product_name_id and self.product_variation.product_name_id != self.product_name_id:
#             raise ValidationError({"product_variation": "Selected variation does not belong to selected product."})

#         # 1) branch total cannot exceed variation total
#         existing_total = BranchProductStock.objects.filter(
#             product_variation=self.product_variation
#         ).exclude(pk=self.pk).aggregate(total=Sum("quantity"))["total"] or 0

#         if self.product_variation and existing_total + self.quantity > self.product_variation.quantity:
#             raise ValidationError({
#                 "quantity": (
#                     f"Total branch quantity ({existing_total + self.quantity}) "
#                     f"cannot exceed variation quantity ({self.product_variation.quantity})."
#                 )
#             })

#         # 2) if variation is unique → qty must equal selected unickkey count
#         if self.product_variation and self.product_variation.isunck and self.pk:
#             cnt = self.unickkey.count()
#             if self.quantity != cnt:
#                 raise ValidationError({"quantity": f"For unique variation, quantity must equal selected UnickKey count ({cnt})."})

#             # 3) selected unick must be from this variation’s pool (optional but strong)
#             bad = self.unickkey.exclude(id__in=self.product_variation.unickkey.values_list("id", flat=True))
#             if bad.exists():
#                 raise ValidationError({"unickkey": "Some selected UnickKeys do not belong to this variation."})

#             # 4) unick cannot be assigned to other branches already
#             clash = BranchProductStock.objects.filter(
#                 product_variation=self.product_variation,
#                 unickkey__in=self.unickkey.all()
#             ).exclude(pk=self.pk).exists()

#             if clash:
#                 raise ValidationError({"unickkey": "One or more UnickKeys are already assigned to another branch."})

#     def save(self, *args, **kwargs):
#         self.full_clean()
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.product_variation.name} - {self.stock_branch.name}"




# class BranchProductStock(Common):
#     product_name = models.ForeignKey(Product, on_delete=models.CASCADE)
#     product_variation = models.ForeignKey(
#         "products.Variation",
#         on_delete=models.CASCADE,
#         related_name="branch_stocks"
#     )
#     stock_branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=0)

#     unickkey = models.ManyToManyField("products.unick", blank=True)

#     class Meta:
#         unique_together = ("product_variation", "stock_branch")

#     def clean(self):
#         # variation must belong to product
#         if self.product_variation.product_name_id != self.product_name_id:
#             raise ValidationError({"product_variation": "Variation does not belong to product"})

#         # total branch qty <= variation qty
#         total = BranchProductStock.objects.filter(
#             product_variation=self.product_variation
#         ).exclude(pk=self.pk).aggregate(t=Sum("quantity"))["t"] or 0

#         if total + self.quantity > self.product_variation.quantity:
#             raise ValidationError({"quantity": "Branch stock exceeds variation stock"})

#         # unique logic
#         if self.product_variation.isunck and self.pk:
#             cnt = self.unickkey.count()
#             if self.quantity != cnt:
#                 raise ValidationError({"quantity": f"Quantity must equal UnickKey count ({cnt})"})

#             # unick cannot be reused in another branch
#             clash = BranchProductStock.objects.filter(
#                 product_variation=self.product_variation,
#                 unickkey__in=self.unickkey.all()
#             ).exclude(pk=self.pk).exists()

#             if clash:
#                 raise ValidationError({"unickkey": "UnickKey already assigned to another branch"})

#     def save(self, *args, **kwargs):
#         self.full_clean()
#         super().save(*args, **kwargs)

# ------------------ BranchProductStock VALUE ------------------

class BranchProductStock(Common):
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_variation = models.ForeignKey(
        Variation, on_delete=models.CASCADE, related_name="branch_stocks"
    )
    stock_branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    unickkey = models.ManyToManyField("products.unick", blank=True)

    class Meta:
        unique_together = ("product_variation", "stock_branch")

    def clean(self):
    # variation must belong to product
        if self.product_variation_id and self.product_name_id:
            if self.product_variation.product_name_id != self.product_name_id:
                raise ValidationError({"product_variation": "Variation does not belong to product"})

    # total qty cannot exceed variation qty
        if self.product_variation_id:
            total = BranchProductStock.objects.filter(
                product_variation=self.product_variation
            ).exclude(pk=self.pk).aggregate(t=Sum("quantity"))["t"] or 0

            if total + (self.quantity or 0) > self.product_variation.quantity:
                raise ValidationError({"quantity": "Branch stock exceeds variation stock"})

        #  DO NOT touch M2M here (unickkey) because object may be unsaved
        # Move unique-unick validation to AdminForm.clean() or save_related

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
