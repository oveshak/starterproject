from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from globalapp.serializers import GlobalSerializers
from .models import Area, MultiBranch, Roles, Users, Branch
from rest_framework_simplejwt.tokens import RefreshToken
class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()
    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']
    
    def get_permissions(self, obj):
        permissions = obj.permissions.all().values('codename')
        for permission in permissions:
            codename = permission.get('codename', '')
            if '_' in codename:
                permission['access'] = codename.split('_')[0]
                permission['submenu'] = codename.split('_')[1]
        return permissions

class RolesSerializer(GlobalSerializers):
    menu = GroupSerializer(many=True, read_only=True)
    class Meta:
        model = Roles
        fields = '__all__'
class AreaSerializer(GlobalSerializers):
    #manager_name = serializers.CharField(source='manager.name', read_only=True)
    class Meta:
        model = Area
        fields = '__all__'
        
class BranchSerializer(GlobalSerializers):
    manager_name = serializers.CharField(source='manager.name', read_only=True)
    class Meta:
        model = Branch
        fields = '__all__'
        
class MultiBranchSerializer(GlobalSerializers):
    
    class Meta:
        model = MultiBranch
        fields = '__all__'

class UsersSerializer(GlobalSerializers):
    roles_name = serializers.CharField(source='roles.name', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)

    class Meta:
        model = Users
        fields = [
            'id', 'name', 'email', 'username', 'phone_number', 'profile_picture',
            'address', 'nid_number', 'nid_front', 'nid_back', 'roles', 'roles_name',
            'branch', 'branch_name', 'is_admin', 'is_staff', 'is_verified', 'password'
        ]
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def create(self, validated_data):
        user = Users.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)

class CustomTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        try:
            user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            raise serializers.ValidationError('Invalid credentials')

        if not user.check_password(password):
            raise serializers.ValidationError('Invalid credentials')
        
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class AllUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = '__all__'
        depth =3

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'