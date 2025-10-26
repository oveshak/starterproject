from django.db import models
from globalapp.models import Common
from users.models import Branch


class Unit(Common):
    name = models.CharField(
        max_length=50,
        verbose_name="Unit Name"
    )

    class Meta:
        verbose_name = "Unit"
        verbose_name_plural = "Units"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Category(Common):
    name = models.CharField(
        max_length=100,
        verbose_name="Category Name"
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Brand(Common):
    name = models.CharField(
        max_length=100,
        verbose_name="Brand Name"
    )

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Warranty(Common):
    DURATION_TYPES = (
        ('Days', 'Days'),
        ('Months', 'Months'),
        ('Years', 'Years'),
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Warranty Name"
    )
    duration = models.IntegerField(
        verbose_name="Duration"
    )
    duration_type = models.CharField(
        max_length=10,
        choices=DURATION_TYPES,
        verbose_name="Duration Type"
    )

    class Meta:
        verbose_name = "Warranty"
        verbose_name_plural = "Warranties"
        ordering = ["name"]

    def __str__(self):
        return self.name


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


class Product(Common):
    name = models.CharField(
        max_length=200,
        verbose_name="Product Name"
    )
    sku = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="SKU"
    )
    unit_name = models.ForeignKey(
        Unit,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Unit"
    )
    category_name = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Category"
    )
    brand_name = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Brand"
    )
    warranty_name = models.ForeignKey(
        Warranty,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Warranty"
    )
    thumbnail_image = models.ImageField(
        upload_to='products/thumbnails/',
        null=True,
        blank=True,
        verbose_name="Thumbnail Image"
    )
    price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Price"
    )

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["name"]

    def __str__(self):
        return self.name

class Variation(Common):
    product_name = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variations',
        verbose_name="Product"
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Variation Name"
    )
    sku_suffix = models.CharField(
        max_length=50,
        verbose_name="SKU Suffix"
    )

    class Meta:
        verbose_name = "Variation"
        verbose_name_plural = "Variations"
        ordering = ["name"]

    def __str__(self):
        return f"{self.product_name} - {self.name}"


class BranchProductStock(Common):
    product_name = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Product"
    )
    branch_name = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        verbose_name="Branch"
    )
    quantity = models.IntegerField(
        verbose_name="Quantity"
    )
    opening_stock = models.IntegerField(
        verbose_name="Opening Stock"
    )

    class Meta:
        verbose_name = "Branch Product Stock"
        verbose_name_plural = "Branch Product Stocks"
        ordering = ["product_name"]

    def __str__(self):
        return f"{self.product_name} - {self.branch_name}"

