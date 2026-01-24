# from django.shortcuts import render
# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.tokens import AccessToken
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework import permissions
# from django.contrib.auth.models import Group, Permission
# from rest_framework import status
# from users.permissions import IsStaff
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework import filters
# try:
#     from globalapp.ed import encode_jwt
# except:
#     pass
# from globalapp.views import BaseViews
# from users.models import Roles, Users
# from users.serializers import AllUserSerializer, CustomTokenObtainPairSerializer, GropuSerializer, PermissionSerializer, RolesSerializer, UserSerializer
# # Create your views here.
# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class =CustomTokenObtainPairSerializer
#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, **kwargs)
#         token=response.data['access']
#         payload = AccessToken(token).payload
#         user_id = payload.get('user_id')
#         user = Users.objects.filter(id=user_id)
#         serializer = AllUserSerializer(user, many=True)
#         for user_data in serializer.data:
#             if 'roles' in user_data:
#                 for role in user_data['roles']['menu']:
#                     if 'permissions' in role:
#                         for permission in role['permissions']:
#                             permission['submenu'] = permission['codename'].split('_')[1]
#                             permission['access'] = permission['codename'].split('_')[0]
        
#         serializer.instance = user
#         try:
#             response.data["user"] = encode_jwt({"data": serializer.data})

#         except:
#             response.data["user"] = {"data": serializer.data}
#         return response

# class RoleViewSet(BaseViews):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated,IsStaff]
#     model_name = Roles
#     methods=["list", "retrieve", "create", "update", "partial_update", "destroy", "soft_delete", "change_status", "restore_soft_deleted"]
#     queryset = Roles.objects.all()
#     serializer_class = RolesSerializer

# class GroupViewSet(BaseViews):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated,IsStaff]
#     model_name = Group
    
#     methods=["list", "retrieve", "create", "update", "partial_update", "destroy", "soft_delete", "change_status", "restore_soft_deleted"]
#     serializer_class = GropuSerializer

# class PermissionViewSet(BaseViews):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated,IsStaff]
#     model_name = Permission
    
#     methods=["list", "retrieve", "create", "update", "partial_update", "destroy", "soft_delete", "change_status", "restore_soft_deleted"]
#     serializer_class = PermissionSerializer
#     def list(self, request, *args, **kwargs):
#         if "list" in self.methods:
#             try:
#                 limit = request.GET.get('limit')
#             except:
#                 limit = None
#             if limit is None:
#                 # No limit parameter provided, return all data
                
#                 queryset = self.filter_queryset(self.get_queryset())
#                 # print(self.get_queryset())
#                 serializer = self.get_serializer(queryset, many=True)
#                 for data in serializer.data:
#                     data['access'] = data['codename'].split('_')[0]
#                     # print(data)

#                 token = encode_jwt({"data": serializer.data})  # Encode serialized data into JWT token
#                 return self.generate_response(True, status.HTTP_200_OK, "list_success", data={"token": token})
#             else:
#                 # Pagination requested, apply pagination
#                 queryset = self.filter_queryset(self.get_queryset())
#                 page = self.paginate_queryset(queryset)
#                 if page is not None:
#                     serializer = self.get_serializer(page, many=True)
#                     for data in serializer.data:
#                         data['access'] = data['codename'].split('_')[0]
#                     # print(data)
#                     token = encode_jwt({"data": serializer.data})  # Encode serialized data into JWT token
#                     return self.get_paginated_response({"token": token})
#         else:
#             return self.generate_response(False, status.HTTP_405_METHOD_NOT_ALLOWED, "list_not_allowed")
        
# class UserViewSet(BaseViews):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated,IsStaff]
#     model_name = Users
#     methods=["list", "retrieve", "create", "update", "partial_update", "destroy", "soft_delete", "change_status", "restore_soft_deleted"]
#     serializer_class = UserSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['roles__name']  # Enable filtering by role name
#     def get_permissions(self):
#         # Allow list and create actions without authentication
#         if self.action in ['list', 'create']:
#             return [permissions.AllowAny()]
#         if self.action in ['update_profile', 'get_own_data']:
#             return [permissions.IsAuthenticated()]
#         # For other actions, staff permission is required
#         return super().get_permissions()
        
#     @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
#     def update_profile(self, request, pk=None):
#         # If user is a staff member, they can update anyone's profile
#         if request.user.is_staff:
#             user = Users.objects.get(pk=pk)
#         else:
#             # Non-staff users can only update their own profile
#             user = request.user
#         print(request.data)
#         serializer = UserSerializer(user, data=request.data, partial=True, context={'request': request})
        
        
#         if serializer.is_valid():
#             serializer.save()
            
#             token = encode_jwt({"data": serializer.data})
#             return self.generate_response(True, status.HTTP_201_CREATED, "create_success", data={"token": token})
#         else:
#             print(f"Validation failed for phone number: {request.data.get('phone_number')}")
#             print(serializer.errors)  # Log detailed errors
#         return self.generate_response(False, status.HTTP_405_METHOD_NOT_ALLOWED, "list_not_allowed")
#     @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
#     def get_own_data(self, request):
#         user = request.user
#         serializer = UserSerializer(user, partial=True, context={'request': request})
#         token = encode_jwt({"data": serializer.data})
#         return self.generate_response(
#             True,
#             status.HTTP_200_OK,
#             "user_data_retrieved",
#             data={"token": token}
#         )
    
from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions, status
from django.contrib.auth.models import Group, Permission
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.parsers import MultiPartParser, FormParser
from globalapp.ed import encode_jwt
import json
try:
    from globalapp.ed import encode_jwt
except:
    pass

from globalapp.views import BaseViews
from .models import Area, MultiBranch, Roles, Users, Branch
from .serializers import (
    AllUserSerializer, AreaSerializer, CustomTokenObtainPairSerializer, GroupSerializer, MultiBranchSerializer,
    PermissionSerializer, RolesSerializer, UsersSerializer, BranchSerializer
)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class =CustomTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token=response.data['access']
        payload = AccessToken(token).payload
        user_id = payload.get('user_id')
        user = Users.objects.filter(id=user_id)
        serializer = AllUserSerializer(user, many=True)
        for user_data in serializer.data:
            if 'roles' in user_data:
                for role in user_data['roles']['menu']:
                    if 'permissions' in role:
                        for permission in role['permissions']:
                            permission['submenu'] = permission['codename'].split('_')[1]
                            permission['access'] = permission['codename'].split('_')[0]
        
        serializer.instance = user
        try:
            response.data["user"] = encode_jwt({"data": serializer.data})

        except:
            response.data["user"] = {"data": serializer.data}
        return response

class AreaViewSet(BaseViews):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = Area
    methods = [
        "list", "retrieve", "create", "update", "partial_update",
        "destroy", "soft_delete", "change_status", "restore_soft_deleted"
    ]

    def perform_create(self, serializer):
        instance = serializer.save()
        area_staf_data = self.request.data.getlist('area_staf[]') or self.request.data.get('area_staf[]', [])
        if area_staf_data:
            instance.area_staf.set([int(pk) for pk in area_staf_data])
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        area_staf_data = self.request.data.getlist('area_staf[]') or self.request.data.get('area_staf[]', [])
        if area_staf_data is not None:
            instance.area_staf.set([int(pk) for pk in area_staf_data])
        return instance

class MultiBranchViewSet(BaseViews):
    queryset = MultiBranch.objects.all()
    serializer_class = MultiBranchSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = MultiBranch
    methods = [
        "list", "retrieve", "create", "update", "partial_update",
        "destroy", "soft_delete", "change_status", "restore_soft_deleted"
    ]


class BranchViewSet(BaseViews):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = Branch
    methods = [
        "list", "retrieve", "create", "update", "partial_update",
        "destroy", "soft_delete", "change_status", "restore_soft_deleted"
    ]

    def perform_create(self, serializer):
        # প্রথমে instance save করি
        instance = serializer.save()

        # ManyToMany field handle
        total_area_data = self.request.data.getlist('total_area[]') or self.request.data.get('total_area[]', [])
        if total_area_data:
            # str থেকে int এ convert
            instance.total_area.set([int(pk) for pk in total_area_data])
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        total_area_data = self.request.data.getlist('total_area[]') or self.request.data.get('total_area[]', [])
        if total_area_data is not None:
            instance.total_area.set([int(pk) for pk in total_area_data])
        return instance

class RoleViewSet(BaseViews):
    queryset = Roles.objects.all()
    serializer_class = RolesSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = Roles
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy", "soft_delete", "change_status", "restore_soft_deleted"]


class GroupViewSet(BaseViews):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = Group
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy"]


class PermissionViewSet(BaseViews):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = Permission
    methods = ["list", "retrieve"]
    filter_backends = [filters.SearchFilter]
    search_fields = ['codename']

    def list(self, request, *args, **kwargs):
        limit = request.GET.get('limit')
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        for data in serializer.data:
            codename = data.get('codename', '')
            if '_' in codename:
                data['access'] = codename.split('_')[0]
                data['submenu'] = codename.split('_')[1]

        try:
            token = encode_jwt({"data": serializer.data})
            if not limit:
                return self.generate_response(True, status.HTTP_200_OK, "list_success", data={"token": token})
            else:
                return self.get_paginated_response({"token": token})
        except NameError:
            if not limit:
                return self.generate_response(True, status.HTTP_200_OK, "list_success", data=serializer.data)
            else:
                return self.get_paginated_response(serializer.data)

        return self.generate_response(False, status.HTTP_405_METHOD_NOT_ALLOWED, "list_not_allowed")


class UserViewSet(BaseViews):
    queryset = Users.objects.all()
    
    authentication_classes = [JWTAuthentication]
    # parser_classes = (MultiPartParser, FormParser)
    model_name = Users
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy", "update_profile", "get_own_data"]
    filter_backends = [filters.SearchFilter]
    search_fields = ['roles__name']
    serializer_class = UsersSerializer

    def get_permissions(self):
        if self.action in ['list', 'create']:
            return [permissions.AllowAny()]
        if self.action in ['update_profile', 'get_own_data']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated, permissions.IsAdminUser()]

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def update_profile(self, request, pk=None):
        if request.user.is_staff:
            user = self.get_object()
        else:
            user = request.user

        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            try:
                token = encode_jwt({"data": serializer.data})
                return Response({"status": True, "message": "update_success", "data": {"token": token}}, status=status.HTTP_200_OK)
            except NameError:
                return Response({"status": True, "message": "update_success", "data": serializer.data}, status=status.HTTP_200_OK)

        return Response({"status": False, "message": "update_failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def get_own_data(self, request):
        user = request.user
        serializer = self.get_serializer(user, context={'request': request})
        try:
            token = encode_jwt({"data": serializer.data})
            return Response({"status": True, "message": "user_data_retrieved", "data": {"token": token}}, status=status.HTTP_200_OK)
        except NameError:
            return Response({"status": True, "message": "user_data_retrieved", "data": serializer.data}, status=status.HTTP_200_OK)
