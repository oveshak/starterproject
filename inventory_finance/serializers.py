from rest_framework import serializers

from contacts.models import Contact
from products.models import Product
from products.serializers import ProductSerializer
from users.models import Branch, Users
from users.serializers import BranchSerializer, UsersSerializer
from .models import StockTransfer, StockAdjustment, Daybook, Expense, VendorCheque, RepairRequest
from globalapp.serializers import GlobalSerializers


class StockTransferSerializer(GlobalSerializers):
    # Writeable ID fields
    from_branch_name = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all())
    to_branch_name = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all())

    class Meta:
        model = StockTransfer
        fields = '__all__'

    def to_representation(self, instance):
        """Return full nested objects for branch fields."""
        data = super().to_representation(instance)

        if instance.from_branch_name:
            data['from_branch_name'] = BranchSerializer(instance.from_branch_name).data
        if instance.to_branch_name:
            data['to_branch_name'] = BranchSerializer(instance.to_branch_name).data

        return data
# class StockAdjustmentSerializer(GlobalSerializers):
#     # # POST করার জন্য ID
#     branch_name = serializers.PrimaryKeyRelatedField(
#         queryset=Branch.objects.all()
#     )
#     product_name = serializers.PrimaryKeyRelatedField(
#         queryset=Product.objects.all()
#     )

#     # GET করার সময় নাম দেখানোর জন্য
#     branch_names = serializers.CharField(source='branch_name.name', read_only=True)
#     product_names = serializers.CharField(source='product_name.name', read_only=True)

#     class Meta:
#         model = StockAdjustment
#         fields = '__all__'


class StockAdjustmentSerializer(GlobalSerializers):
    # Keep original fields for write/update
    branch_name = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all())
    product_name = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = StockAdjustment
        fields = '__all__'

    def to_representation(self, instance):
        """Return full nested objects for ForeignKey fields."""
        data = super().to_representation(instance)

        # Replace ForeignKey IDs with full objects
        if instance.branch_name:
            data['branch_name'] = BranchSerializer(instance.branch_name).data
        if instance.product_name:
            data['product_name'] = ProductSerializer(instance.product_name).data

        return data



# class DaybookSerializer(GlobalSerializers):
#     branch_name = serializers.PrimaryKeyRelatedField(
#         queryset=Branch.objects.all()
#     )
#     branch_name_display = serializers.CharField(
#         source='branch_name.name', read_only=True
#     )

#     report_submitted_by_user_name = serializers.PrimaryKeyRelatedField(
#         queryset=Users.objects.all()
#     )
#     report_submitted_by_user_display = serializers.CharField(
#         source='report_submitted_by_user_name.name', read_only=True
#     )

#     class Meta:
#         model = Daybook
#         fields = '__all__'


class DaybookSerializer(GlobalSerializers):
    # Writeable fields for input
    branch_name = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all())
    report_submitted_by_user_name = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())

    class Meta:
        model = Daybook
        fields = '__all__'

    def to_representation(self, instance):
        """Return full nested objects for related fields."""
        data = super().to_representation(instance)

        if instance.branch_name:
            data['branch_name'] = BranchSerializer(instance.branch_name).data
        if instance.report_submitted_by_user_name:
            data['report_submitted_by_user_name'] =UsersSerializer(instance.report_submitted_by_user_name).data

        return data




# class ExpenseSerializer(GlobalSerializers):
#     #Writable field: accept branch ID (frontend sends branch_name as number)
#     branch_name = serializers.PrimaryKeyRelatedField(
#         queryset=Branch.objects.all()
#     )

#     # Readable field: return branch name
#     branch_names = serializers.CharField(
#         source='branch_name.name',
#         read_only=True
#     )

#     class Meta:
#         model = Expense
#         fields = '__all__'

class ExpenseSerializer(GlobalSerializers):
    # Writeable field for POST/PUT
    branch_name = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all())

    class Meta:
        model = Expense
        fields = '__all__'

    def to_representation(self, instance):
        """Return full nested branch object instead of just ID"""
        data = super().to_representation(instance)
        
        if instance.branch_name:
            data['branch_name'] = BranchSerializer(instance.branch_name).data
        
        return data

# class VendorChequeSerializer(GlobalSerializers):
#     vendor_name = serializers.CharField(source='vendor.name', read_only=True)
#     class Meta:
#         model = VendorCheque
#         fields = '__all__'

class VendorChequeSerializer(GlobalSerializers):
    # Writeable field for POST/PUT
    vendor_name = serializers.PrimaryKeyRelatedField(queryset=Contact.objects.all(), allow_null=True)

    class Meta:
        model = VendorCheque
        fields = '__all__'

    def to_representation(self, instance):
        """Return full nested vendor object instead of just ID"""
        data = super().to_representation(instance)

        if instance.vendor_name:
            data['vendor_name'] = UsersSerializer(instance.vendor_name).data

        return data
# class VendorChequeSerializer(GlobalSerializers):
#     # Writeable field for POST/PUT
#     vendor = serializers.PrimaryKeyRelatedField(queryset=Vendor.objects.all())

#     class Meta:
#         model = VendorCheque
#         fields = '__all__'

#     def to_representation(self, instance):
#         """Return full nested vendor object instead of just ID"""
#         data = super().to_representation(instance)

#         if instance.vendor:
#             data['vendor'] = VendorSerializer(instance.vendor).data

#         return data

# class RepairRequestSerializer(GlobalSerializers):
#     product_name = serializers.CharField(source='product.name', read_only=True)
#     customer_name = serializers.CharField(source='customer.name', read_only=True)
#     branch_name = serializers.CharField(source='branch.name', read_only=True)
#     requested_by_name = serializers.CharField(source='requested_by_user.name', read_only=True)
#     class Meta:
#         model = RepairRequest
#         fields = '__all__'



class RepairRequestSerializer(GlobalSerializers):
    # Writeable fields for POST/PUT (use model field names)
    product_name = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    customer_name = serializers.PrimaryKeyRelatedField(queryset=Contact.objects.all(), allow_null=True)
    branch_name = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all())
    requested_by_user_name = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all(), allow_null=True)

    class Meta:
        model = RepairRequest
        fields = '__all__'

    def to_representation(self, instance):
        """Return full nested objects for ForeignKey fields"""
        data = super().to_representation(instance)

        if instance.product_name:
            data['product_name'] = ProductSerializer(instance.product_name).data
        if instance.customer_name:
            data['customer_name'] = UsersSerializer(instance.customer_name).data
        if instance.branch_name:
            data['branch_name'] = BranchSerializer(instance.branch_name).data
        if instance.requested_by_user_name:
            data['requested_by_user_name'] = UsersSerializer(instance.requested_by_user_name).data

        return data