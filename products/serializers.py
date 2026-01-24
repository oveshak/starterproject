# from rest_framework import serializers

# from users.models import Branch
# from users.serializers import BranchSerializer
# from .models import Product, Unit, Category, Brand, Warranty, SellingPriceGroup, Variation, BranchProductStock
# from globalapp.serializers import GlobalSerializers

# class UnitSerializer(GlobalSerializers):
#     class Meta:
#         model = Unit
#         fields = '__all__'

# class CategorySerializer(GlobalSerializers):
#     class Meta:
#         model = Category
#         fields = '__all__'

# class BrandSerializer(GlobalSerializers):
#     class Meta:
#         model = Brand
#         fields = '__all__'

# class WarrantySerializer(GlobalSerializers):
#     class Meta:
#         model = Warranty
#         fields = '__all__'

# class SellingPriceGroupSerializer(GlobalSerializers):
#     class Meta:
#         model = SellingPriceGroup
#         fields = '__all__'


        
# class VariationSerializer(GlobalSerializers):
#     # Writeable field for POST/PUT
#     product_name = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

#     class Meta:
#         model = Variation
#         fields = '__all__'

#     def to_representation(self, instance):
#         """Return full nested product object instead of just ID"""
#         data = super().to_representation(instance)

#         if instance.product_name:
#             data['product_name'] = ProductSerializer(instance.product_name).data

#         return data
    

    
# # class ProductSerializer(GlobalSerializers):
# #     unit_name = serializers.CharField(source='unit.name', read_only=True)
# #     category_name = serializers.CharField(source='category.name', read_only=True)
# #     brand_name = serializers.CharField(source='brand.name', read_only=True)
# #     warranty_name = serializers.CharField(source='warranty.name', read_only=True)
# #     variations = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

# #     class Meta:
# #         model = Product
# #         fields = '__all__'
# class ProductSerializer(serializers.ModelSerializer):
#     unit_name_data = serializers.CharField(source='unit_name.name', read_only=True)
#     category_name_data = serializers.CharField(source='category_name.name', read_only=True)
#     brand_name_data = serializers.CharField(source='brand_name.name', read_only=True)
#     warranty_name_data = serializers.CharField(source='warranty_name.name', read_only=True)

#     unit_name = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all(), allow_null=True)
#     category_name = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True)
#     brand_name = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all(), allow_null=True)
#     warranty_name = serializers.PrimaryKeyRelatedField(queryset=Warranty.objects.all(), allow_null=True)

#     class Meta:
#         model = Product
#         fields = '__all__'


# # class VariationSerializer(GlobalSerializers):
# #     class Meta:
# #         model = Variation
# #         fields = '__all__'

from rest_framework import serializers

from users.models import Branch
from users.serializers import BranchSerializer
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
from globalapp.serializers import GlobalSerializers


# -------- BASIC --------

class UnitSerializer(GlobalSerializers):
    class Meta:
        model = Unit
        fields = "__all__"


class CategorySerializer(GlobalSerializers):
    class Meta:
        model = Category
        fields = "__all__"


class BrandSerializer(GlobalSerializers):
    class Meta:
        model = Brand
        fields = "__all__"


class WarrantySerializer(GlobalSerializers):
    class Meta:
        model = Warranty
        fields = "__all__"


# -------- ATTRIBUTE --------

class VariationAttributeSerializer(GlobalSerializers):
    class Meta:
        model = VariationAttribute
        fields = "__all__"


class VariationAttributeValueSerializer(GlobalSerializers):
    attribute_name = serializers.CharField(
        source="attribute.name",
        read_only=True
    )

    class Meta:
        model = VariationAttributeValue
        fields = ["id", "attribute", "attribute_name", "value"]


class UnickSerializer(GlobalSerializers):
    class Meta:
        model = unick
        fields = "__all__"


from rest_framework import serializers
from .models import Variation, unick

class VariationSerializer(GlobalSerializers):
    unickkey = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=unick.objects.all(),
        required=False
    )

    class Meta:
        model = Variation
        fields = '__all__'

    def validate(self, attrs):
        isunck = attrs.get("isunck", getattr(self.instance, "isunck", False))
        quantity = attrs.get("quantity", getattr(self.instance, "quantity", 0))

        if "unickkey" in attrs:
            unick_count = len(attrs["unickkey"])
        elif self.instance:
            unick_count = self.instance.unickkey.count()
        else:
            unick_count = 0

        if isunck and quantity != unick_count:
            raise serializers.ValidationError({
                "quantity": (
                    f"Quantity must exactly equal UnickKey count "
                    f"({unick_count}) when isunck is True."
                )
            })

        return attrs

# -------- PRODUCT --------

class ProductSerializer(GlobalSerializers):
    variations = VariationSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields ="__all__"



class SellingPriceGroupSerializer(GlobalSerializers):
    class Meta:
        model = SellingPriceGroup
        fields = '__all__'
# class BranchProductStockSerializer(GlobalSerializers):
#     # Writeable fields for POST/PUT
#     product_name = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
#     branch_name = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all())

#     class Meta:
#         model = BranchProductStock
#         fields = '__all__'

#     def to_representation(self, instance):
#         """Return full nested product and branch objects"""
#         data = super().to_representation(instance)

#         if instance.product_name:
#             data['product_name'] = ProductSerializer(instance.product_name).data
#         if instance.branch_name:
#             data['branch_name'] = BranchSerializer(instance.branch_name).data

#         return data


# class BranchProductStockSerializer(GlobalSerializers):
#     product_variation = serializers.PrimaryKeyRelatedField(
#         queryset=Variation.objects.all()
#     )
#     stock_branch = serializers.PrimaryKeyRelatedField(
#         queryset=Branch.objects.all()
#     )

#     class Meta:
#         model = BranchProductStock
#         fields = "__all__"

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         data["product_variation"] = VariationSerializer(instance.product_variation).data
#         data["stock_branch"] = BranchSerializer(instance.stock_branch).data
#         return data



# admin.py
from django import forms
from django.core.exceptions import ValidationError
from .models import BranchProductStock, unick

class BranchProductStockAdminForm(forms.ModelForm):
    class Meta:
        model = BranchProductStock
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # default empty
        self.fields["unickkey"].queryset = unick.objects.none()

        variation = None
        # add page: user selected variation -> POST will contain it
        if self.data.get("product_variation"):
            variation = self.data.get("product_variation")
        # edit page
        elif self.instance.pk and self.instance.product_variation_id:
            variation = self.instance.product_variation_id

        if variation:
            # already used in other branches for same variation
            used = (BranchProductStock.objects
                    .filter(product_variation_id=variation)
                    .exclude(pk=self.instance.pk)
                    .values_list("unickkey__id", flat=True))

            # allowed list = variation’s own unicks minus used
            self.fields["unickkey"].queryset = (
                unick.objects.filter(variation__id=variation)  # ❌ যদি reverse relation না থাকে
            )


class BranchProductStockSerializer(GlobalSerializers):
    product_variation = serializers.PrimaryKeyRelatedField(queryset=Variation.objects.all())
    stock_branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all())
    unickkey = serializers.PrimaryKeyRelatedField(queryset=unick.objects.all(), many=True, required=False)

    class Meta:
        model = BranchProductStock
        fields = "__all__"

    def validate(self, attrs):
        variation = attrs.get("product_variation", getattr(self.instance, "product_variation", None))
        qty = attrs.get("quantity", getattr(self.instance, "quantity", 0))
        unicks = attrs.get("unickkey", None)

        if variation and variation.isunck:
            cnt = len(unicks or [])
            if qty != cnt:
                raise serializers.ValidationError({"quantity": f"Quantity must equal UnickKey count ({cnt}) for unique variation."})

        return attrs






