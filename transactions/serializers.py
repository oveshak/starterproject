from rest_framework import serializers

from contacts.models import Contact, Customer
from contacts.serializers import ContactSerializer, CustomerSerializer
from products.models import Product, unick
from products.serializers import ProductSerializer
from users.models import Area, Branch, Users
from users.serializers import AreaSerializer, BranchSerializer, UsersSerializer
from .models import BranchAccount, DailySaving, DownPayment, Purchase, PurchaseItem, PurchaseReturn, Sale, SaleItem, Payment, Cheque, AffiliateCommission,LoanType, InstallmentType, Installment, Loan, Transection
from globalapp.serializers import GlobalSerializers



# from rest_framework import serializers

# class PurchaseSerializer(GlobalSerializers):
#     purchaseitem = serializers.PrimaryKeyRelatedField(
#         many=True,
#         queryset=PurchaseItem.objects.all(),
#         required=False
#     )

#     class Meta:
#         model = Purchase
#         fields = "__all__"

#     def to_internal_value(self, data):
#         mutable_data = data.copy()

#         if hasattr(data, "getlist"):
#             raw_items = data.getlist("purchaseitem")
#             raw_items_bracket = data.getlist("purchaseitem[]")

#             final_items = raw_items if raw_items else raw_items_bracket

#             if final_items:
#                 cleaned = [
#                     x for x in final_items
#                     if str(x).strip() not in ("", "null", "undefined")
#                 ]
#                 mutable_data.setlist("purchaseitem", cleaned)
#             elif "purchaseitem" in data or "purchaseitem[]" in data:
#                 mutable_data.setlist("purchaseitem", [])

#         return super().to_internal_value(mutable_data)

#     def create(self, validated_data):
#         purchase_items = validated_data.pop("purchaseitem", [])
#         instance = super().create(validated_data)
#         instance.purchaseitem.set(purchase_items)
#         return instance

#     def update(self, instance, validated_data):
#         purchase_items = validated_data.pop("purchaseitem", None)

#         instance = super().update(instance, validated_data)

#         if purchase_items is not None:
#             instance.purchaseitem.set(purchase_items)

#         return instance


# from rest_framework import serializers

# class PurchaseItemSerializer(GlobalSerializers):
#     unickkey = serializers.PrimaryKeyRelatedField(
#         many=True,
#         queryset=unick.objects.all(),
#         required=False
#     )

#     class Meta:
#         model = PurchaseItem
#         fields = "__all__"

#     def to_internal_value(self, data):
#         mutable_data = data.copy()

#         if hasattr(data, "getlist"):
#             raw_keys = data.getlist("unickkey")
#             raw_keys_bracket = data.getlist("unickkey[]")

#             final_keys = raw_keys if raw_keys else raw_keys_bracket

#             if final_keys:
#                 cleaned = [
#                     x for x in final_keys
#                     if str(x).strip() not in ("", "null", "undefined")
#                 ]
#                 mutable_data.setlist("unickkey", cleaned)
#             elif "unickkey" in data or "unickkey[]" in data:
#                 mutable_data.setlist("unickkey", [])

#         return super().to_internal_value(mutable_data)

#     def create(self, validated_data):
#         unick_ids = validated_data.pop("unickkey", [])
#         instance = super().create(validated_data)
#         instance.unickkey.set(unick_ids)
#         return instance

#     def update(self, instance, validated_data):
#         unick_ids = validated_data.pop("unickkey", None)

#         instance = super().update(instance, validated_data)

#         if unick_ids is not None:
#             instance.unickkey.set(unick_ids)

#         return instance



from rest_framework import serializers
from .models import Purchase, PurchaseItem, Variation, unick


class PurchaseItemSerializer(GlobalSerializers):
    unickkey = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=unick.objects.all(),
        required=False
    )

    class Meta:
        model = PurchaseItem
        fields = "__all__"

    def _extract_id_list(self, *field_names):
        request = self.context.get("request")
        if not request:
            return [], False

        data = request.data
        provided = False
        raw_values = []

        if hasattr(data, "getlist"):
            for field_name in field_names:
                values = data.getlist(field_name)
                if field_name in data or values:
                    provided = True
                raw_values.extend(values)
        else:
            for field_name in field_names:
                if field_name in data:
                    provided = True
                    value = data.get(field_name)
                    if isinstance(value, list):
                        raw_values.extend(value)
                    elif value is not None:
                        raw_values.append(value)

        cleaned = []
        for value in raw_values:
            if value in ("", None, "null", "undefined"):
                continue
            try:
                cleaned.append(int(value))
            except (TypeError, ValueError):
                pass

        return cleaned, provided

    def create(self, validated_data):
        key_ids, key_field_present = self._extract_id_list("unickkey", "unickkey[]")
        validated_data.pop("unickkey", None)

        instance = super().create(validated_data)

        if key_field_present:
            instance.unickkey.set(unick.objects.filter(pk__in=key_ids))

        return instance

    def update(self, instance, validated_data):
        key_ids, key_field_present = self._extract_id_list("unickkey", "unickkey[]")
        validated_data.pop("unickkey", None)

        instance = super().update(instance, validated_data)

        if key_field_present:
            instance.unickkey.set(unick.objects.filter(pk__in=key_ids))

        return instance


class PurchaseSerializer(GlobalSerializers):
    purchaseitem = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=PurchaseItem.objects.all(),
        required=False
    )

    class Meta:
        model = Purchase
        fields = "__all__"

    def _extract_id_list(self, *field_names):
        request = self.context.get("request")
        if not request:
            return [], False

        data = request.data
        provided = False
        raw_values = []

        if hasattr(data, "getlist"):
            for field_name in field_names:
                values = data.getlist(field_name)
                if field_name in data or values:
                    provided = True
                raw_values.extend(values)
        else:
            for field_name in field_names:
                if field_name in data:
                    provided = True
                    value = data.get(field_name)
                    if isinstance(value, list):
                        raw_values.extend(value)
                    elif value is not None:
                        raw_values.append(value)

        cleaned = []
        for value in raw_values:
            if value in ("", None, "null", "undefined"):
                continue
            try:
                cleaned.append(int(value))
            except (TypeError, ValueError):
                pass

        return cleaned, provided

    def create(self, validated_data):
        purchase_item_ids, purchaseitem_field_present = self._extract_id_list(
            "purchaseitem", "purchaseitem[]"
        )
        validated_data.pop("purchaseitem", None)

        instance = super().create(validated_data)

        if purchaseitem_field_present:
            instance.purchaseitem.set(
                PurchaseItem.objects.filter(pk__in=purchase_item_ids, is_deleted=False)
            )

        return instance

    def update(self, instance, validated_data):
        purchase_item_ids, purchaseitem_field_present = self._extract_id_list(
            "purchaseitem", "purchaseitem[]"
        )
        validated_data.pop("purchaseitem", None)

        instance = super().update(instance, validated_data)

        # VERY IMPORTANT:
        # field provided হলে exact list set করবে
        # তাই new item add হবে, removed item remove হবে
        if purchaseitem_field_present:
            instance.purchaseitem.set(
                PurchaseItem.objects.filter(pk__in=purchase_item_ids, is_deleted=False)
            )

        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["purchaseitem"] = [
            {
                "id": item.id,
                "purchase_product": item.purchase_product.id if item.purchase_product else None,
                "purchase_product_variation": item.purchase_product_variation.id if item.purchase_product_variation else None,
                "qty": item.qty,
                "unit_price": str(item.unit_price),
                "unickkey": list(item.unickkey.values_list("id", flat=True)),
                "is_deleted": getattr(item, "is_deleted", False),
            }
            for item in instance.purchaseitem.filter(is_deleted=False)
        ]

        return data



class PurchaseReturnSerializer(GlobalSerializers):
    class Meta:
        model = PurchaseReturn
        fields = '__all__'

# class SaleItemSerializer(GlobalSerializers):
#     product_name = serializers.CharField(source='product.name', read_only=True)
#     class Meta:
#         model = SaleItem
#         fields = '__all__'
class SaleItemSerializer(GlobalSerializers):
    # Writeable field for POST/PUT
    product_name = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )

    class Meta:
        model = SaleItem
        fields = '__all__'

    def to_representation(self, instance):
        """Return full nested product object instead of just ID"""
        data = super().to_representation(instance)

        if instance.product_name:
            data['product_name'] = ProductSerializer(instance.product_name).data

        return data


# class SaleSerializer(GlobalSerializers):
#     items = SaleItemSerializer(many=True, read_only=True)
#     customer_name = serializers.CharField(source='customer.name', read_only=True)
#     branch_name = serializers.CharField(source='branch.name', read_only=True)
#     supervisor_name = serializers.CharField(source='supervisor_user.name', read_only=True)
#     manager_name = serializers.CharField(source='manager_user.name', read_only=True)
#     class Meta:
#         model = Sale
#         fields = '__all__'

class SaleSerializer(GlobalSerializers):
    # Nested items
    items = SaleItemSerializer(many=True, read_only=True)

    # Writeable fields
    customer_name = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all()
    )
    branch_name = serializers.PrimaryKeyRelatedField(
        queryset=Branch.objects.all()
    )
    supervisor_user_name = serializers.PrimaryKeyRelatedField(
        queryset=Users.objects.all(),
        allow_null=True,
        required=False
    )
    manager_user_name = serializers.PrimaryKeyRelatedField(
        queryset=Users.objects.all(),
        allow_null=True,
        required=False
    )

    class Meta:
        model = Sale
        fields = '__all__'

    def to_representation(self, instance):
        """
        Replace ForeignKey IDs with full nested objects in response
        """
        data = super().to_representation(instance)

        # Expand nested objects
        if instance.customer_name:
            data['customer_name'] = ContactSerializer(instance.customer_name).data
        if instance.branch_name:
            data['branch_name'] = BranchSerializer(instance.branch_name).data
        if instance.supervisor_user_name:
            data['supervisor_user_name'] = UsersSerializer(instance.supervisor_user_name).data
        if instance.manager_user_name:
            data['manager_user_name'] = UsersSerializer(instance.manager_user_name).data

        return data


# class PaymentSerializer(GlobalSerializers):
#     customer_name = serializers.CharField(source='customer.name', read_only=True)
#     class Meta:
#         model = Payment
#         fields = '__all__'

# class ChequeSerializer(GlobalSerializers):
#     customer_name = serializers.CharField(source='customer.name', read_only=True)
#     class Meta:
#         model = Cheque
#         fields = '__all__'

# class AffiliateCommissionSerializer(GlobalSerializers):
#     affiliate_user_name = serializers.CharField(source='affiliate_user.name', read_only=True)
#     class Meta:
#         model = AffiliateCommission
#         fields = '__all__'


# ---------------- Payment ----------------
class PaymentSerializer(GlobalSerializers):
    customer_name = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all()
    )
    sale_name = serializers.PrimaryKeyRelatedField(
        queryset=Sale.objects.all(),
        allow_null=True,
        required=False
    )

    class Meta:
        model = Payment
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.customer_name:
            data['customer_name'] = ContactSerializer(instance.customer_name).data
        if instance.sale_name:
            data['sale_name'] = SaleSerializer(instance.sale_name).data
        return data


# ---------------- Cheque ----------------
class ChequeSerializer(GlobalSerializers):
    customer_name = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all()
    )
    loan_name = serializers.PrimaryKeyRelatedField(
        queryset=Sale.objects.all(),
        allow_null=True,
        required=False
    )

    class Meta:
        model = Cheque
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.customer_name:
            data['customer_name'] = ContactSerializer(instance.customer_name).data
        if instance.loan_name:
            data['loan_name'] = SaleSerializer(instance.loan_name).data
        return data


# ---------------- Affiliate Commission ----------------
class AffiliateCommissionSerializer(GlobalSerializers):
    affiliate_user_name = serializers.PrimaryKeyRelatedField(
        queryset=Users.objects.all()
    )
    sale_name = serializers.PrimaryKeyRelatedField(
        queryset=Sale.objects.all()
    )

    class Meta:
        model = AffiliateCommission
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.affiliate_user_name:
            data['affiliate_user_name'] = UsersSerializer(instance.affiliate_user_name).data
        if instance.sale_name:
            data['sale_name'] = SaleSerializer(instance.sale_name).data
        return data



class LoanTypeSerializer(GlobalSerializers):
    # Show full branch info in GET response
    loan_branch = serializers.PrimaryKeyRelatedField(
        queryset=Branch.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = LoanType
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Nested branch info
        data['loan_branch'] = BranchSerializer(instance.loan_branch).data if instance.loan_branch else None
        return data



class InstallmentTypeSerializer(GlobalSerializers):
    label = serializers.CharField(source="get_type_display", read_only=True)

    class Meta:
        model = InstallmentType
        fields = '__all__'
        

class DailySavingSerializer(GlobalSerializers):
    class Meta:
        model = DailySaving
        fields = '__all__'  # or specify the fields you want to include




class DownPaymentSerializer(GlobalSerializers):
    class Meta:
        model =  DownPayment
        fields = '__all__'  # or specify the fields you want to include



class InstallmentSerializer(serializers.ModelSerializer):
    # Accept IDs for input
    customer_name = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all()
    )
    received_by = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all(), allow_null=True, required=False)
    branch_name = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all(), allow_null=True, required=False)
    area_name = serializers.PrimaryKeyRelatedField(queryset=Area.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Installment
        fields = '__all__'

    def to_representation(self, instance):
        """Return nested objects for related fields instead of just IDs."""
        data = super().to_representation(instance)

        

        # Nested received_by
        data['received_by'] = UsersSerializer(instance.received_by).data if instance.received_by else None

        # Nested branch
        data['branch_name'] = BranchSerializer(instance.branch_name).data if instance.branch_name else None

        # Nested area
        data['area_name'] = AreaSerializer(instance.area_name).data if instance.area_name else None

        return data


class LoanSerializer(GlobalSerializers):
    # customer_name_display = serializers.CharField(source='customer_name.full_name', read_only=True)
    # loan_type_name = serializers.CharField(source='loan_type.name', read_only=True)
    # installment_type_name = serializers.CharField(source='installment_type.type', read_only=True)
    #installments = InstallmentSerializer(many=True, read_only=True)

    class Meta:
        model = Loan
        fields = '__all__'


class BranchAccountSerializer(GlobalSerializers):
    class Meta:
        model = BranchAccount
        fields = '__all__'

class TransectionSerializer(serializers.ModelSerializer):
    # Nested serializers to show detailed information for customer and received_by fields
    customer_name = serializers.StringRelatedField()
    received_by = serializers.StringRelatedField(allow_null=True)
    
    class Meta:
        model = Transection
        fields =  '__all__'

# ---------------- Installment ----------------
# class InstallmentSerializer(GlobalSerializers):
#     customer_name = serializers.PrimaryKeyRelatedField(
#         queryset=Customer.objects.all()
#     )
#     received_by = serializers.PrimaryKeyRelatedField(
#         queryset=Users.objects.all(),
#         allow_null=True,
#         required=False
#     )

#     class Meta:
#         model = Installment
#         fields = '__all__'

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         if instance.customer_name:
#             data['customer_name'] = CustomerSerializer(instance.customer_name).data
#         if instance.received_by:
#             data['received_by'] = UsersSerializer(instance.received_by).data
#         return data


# # ---------------- Loan ----------------
# class LoanSerializer(GlobalSerializers):
#     customer_name = serializers.PrimaryKeyRelatedField(
#         queryset=Customer.objects.all()
#     )
#     loan_type = serializers.PrimaryKeyRelatedField(
#         queryset=LoanType.objects.all(),
#         allow_null=True,
#         required=False
#     )
#     installment_type = serializers.PrimaryKeyRelatedField(
#         queryset=InstallmentType.objects.all(),
#         allow_null=True,
#         required=False
#     )
#     installment = InstallmentSerializer(many=True, read_only=True)

#     class Meta:
#         model = Loan
#         fields = '__all__'

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         if instance.customer_name:
#             data['customer_name'] = CustomerSerializer(instance.customer_name).data
#         if instance.loan_type:
#             data['loan_type'] = LoanTypeSerializer(instance.loan_type).data
#         if instance.installment_type:
#             data['installment_type'] = InstallmentTypeSerializer(instance.installment_type).data
#         # Already handled installments via nested serializer
#         return data






from rest_framework import serializers
from .models import CollectionReport

class CollectionReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionReport
        fields = "__all__"