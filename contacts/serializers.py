from rest_framework import serializers

from users.models import Area, Branch, Users
from users.serializers import AreaSerializer, BranchSerializer
from .models import Contact, Customer, CustomerGroup, CustomerType
from globalapp.serializers import GlobalSerializers

class CustomerSerializers(GlobalSerializers):
    # Serializer for Customer model
    class Meta:
        model = Customer
        fields = '__all__'

# class CustomerGroupSerializer(GlobalSerializers):
#     # # Nest related serializers for detailed fields
#     # group_leader_user = CustomerSerializers(read_only=True)  # Display customer details for the leader
#     # members = CustomerSerializers(many=True, read_only=True)  # Display list of customers in the group
#     # customer_group_branch_name = BranchSerializer(read_only=True)  # Display branch details
#     # customer_group_area_name = AreaSerializer(read_only=True)  # Display area details

#     class Meta:
#         model = CustomerGroup
#         fields = '__all__'  # Include all fields of CustomerGroup

#     # def update(self, instance, validated_data):
#     #     """
#     #     Update the CustomerGroup instance with validated data
#     #     """
#     #     # Update simple fields directly (e.g., 'name')
#     #     instance.name = validated_data.get('name', instance.name)

#     #     # Handle the ForeignKey fields properly (group_leader_user, customer_group_branch_name, customer_group_area_name)
#     #     group_leader_user_data = validated_data.get('group_leader_user', None)
#     #     if group_leader_user_data:
#     #         try:
#     #             # Assuming group_leader_user_data is the ID
#     #             group_leader_user = Customer.objects.get(id=group_leader_user_data)
#     #             instance.group_leader_user = group_leader_user
#     #         except Customer.DoesNotExist:
#     #             raise serializers.ValidationError("Customer with this ID does not exist.")
        
#     #     customer_group_branch_name_data = validated_data.get('customer_group_branch_name', None)
#     #     if customer_group_branch_name_data:
#     #         try:
#     #             # Assuming customer_group_branch_name_data is the ID
#     #             customer_group_branch_name = Branch.objects.get(id=customer_group_branch_name_data)
#     #             instance.customer_group_branch_name = customer_group_branch_name
#     #         except Branch.DoesNotExist:
#     #             raise serializers.ValidationError("Branch with this ID does not exist.")
        
#     #     customer_group_area_name_data = validated_data.get('customer_group_area_name', None)
#     #     if customer_group_area_name_data:
#     #         try:
#     #             # Assuming customer_group_area_name_data is the ID
#     #             customer_group_area_name = Area.objects.get(id=customer_group_area_name_data)
#     #             instance.customer_group_area_name = customer_group_area_name
#     #         except Area.DoesNotExist:
#     #             raise serializers.ValidationError("Area with this ID does not exist.")

#     #     # No need to update the 'members' field here as per your requirement

#     #     instance.save()  # Save the updated instance
#     #     return instance

class CustomerGroupSerializer(GlobalSerializers):
    # Nest related serializers for detailed fields
    group_leader_user  = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), required=False, allow_null=True)
      # Display customer details for the leader
   
 # Display list of customers in the group
    customer_group_branch_name =serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all(), required=False, allow_null=True)  # Display branch details
    customer_group_area_name = serializers.PrimaryKeyRelatedField(queryset=Area.objects.all(), required=False, allow_null=True)  # Display area details

    class Meta:
        model = CustomerGroup
        fields = '__all__'  # Include all fields of CustomerGroup

    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        # Serialize group_leader_user with the CustomerSerializers

            
        data['group_leader_user'] = (
    CustomerSerializers(instance.group_leader_user).data 
    if instance.group_leader_user and instance.group_leader_user.full_name 
    else None
)
        # Serialize customer_group_branch_name with BranchSerializer
        if instance.customer_group_branch_name:
            data['customer_group_branch_name'] = BranchSerializer(instance.customer_group_branch_name).data
        
        # Serialize customer_group_area_name with AreaSerializer
        if instance.customer_group_area_name:
            data['customer_group_area_name'] = AreaSerializer(instance.customer_group_area_name).data
        
        # Optionally, you can add any other related fields here, like members, etc.
        return data


class ContactSerializer(GlobalSerializers):
    # Writeable ForeignKey
    customer_group = serializers.PrimaryKeyRelatedField(queryset=CustomerGroup.objects.all(), required=False, allow_null=True)
    branch_name = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Contact
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Nested representation
        data['customer_group'] = CustomerGroupSerializer(instance.customer_group).data if instance.customer_group else None
        data['branch_name'] = BranchSerializer(instance.branch_name).data if instance.branch_name else None

        return data


class CustomerTypeSerializer(GlobalSerializers):
    # Show full branch info in GET response
    customer_branch = serializers.PrimaryKeyRelatedField(
        queryset=Branch.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = CustomerType
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Nested branch info
        data['customer_branch'] = BranchSerializer(instance.customer_type_branch).data if instance.customer_type_branch else None
        return data
    

from rest_framework import serializers

class CustomerSerializer(GlobalSerializers):
    branch_name = serializers.PrimaryKeyRelatedField(
        queryset=Branch.objects.all(), required=False, allow_null=True
    )
    guarantor = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(), required=False, allow_null=True
    )
    customer_group = serializers.PrimaryKeyRelatedField(
        queryset=CustomerGroup.objects.all(), required=False, allow_null=True
    )

    # ✅ dropdown friendly fields (read-only)
    label = serializers.CharField(source="full_name", read_only=True)  # label = full_name
    name = serializers.CharField(source="full_name", read_only=True)   # name = full_name
    value = serializers.IntegerField(source="id", read_only=True)      # value = id (safe standard)

    class Meta:
        model = Customer
        fields = "__all__"  # label/name/value automatically included because declared above

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # nested objects (as you had)
        data["branch_name"] = (
            BranchSerializer(instance.branch_name).data if instance.branch_name else None
        )
        data["customer_group"] = (
            CustomerGroupSerializer(instance.customer_group).data if instance.customer_group else None
        )
        data["guarantor"] = (
            ContactSerializer(instance.guarantor).data if instance.guarantor else None
        )

        # ✅ ensure label/name/value are always present
        data["label"] = instance.full_name
        data["name"] = instance.full_name
        data["value"] = instance.id

        return data

    def create(self, validated_data):
        group = validated_data.get("customer_group", None)
        customer = Customer.objects.create(**validated_data)
        if group:
            group.members.add(customer)
        return customer