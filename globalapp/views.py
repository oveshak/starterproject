# from django.shortcuts import render
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework import viewsets,parsers
# from des.models import DynamicEmailConfiguration
# from globalapp.ed import encode_jwt
# from rest_framework import status
# from rest_framework.exceptions import ValidationError
# from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination
# from django_filters.rest_framework import DjangoFilterBackend
# from django.db.models import FileField, ImageField
# from django_filters import rest_framework as filters
# from django.db.models import CharField, TextField
# from django.utils import timezone
# from datetime import datetime
# from django.db.models import Q
# from django.db import models
# from users.permissions import IsStaff
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework import permissions
# from globalapp.models import SoftwareAsset
# from globalapp.serializers import EmailConfigureSerializer, SoftwareAssetSerializer
# from rest_framework import serializers
# from django.utils.text import capfirst

# class CustomPagination(LimitOffsetPagination):

#     def get_paginated_response(self, data):
#         return Response({
#             'success': True,
#             'status': 200,
#             'message': 'Data retrieved successfully',
#             'error': None,
#             'data': {
#                 'meta': {
#                     'count': self.count,
#                     'next': self.get_next_link(),
#                     'previous': self.get_previous_link()
#                 },
#                 'results': data
#             }
#         })
    
# class CaseInsensitiveCharFilter(filters.CharFilter):
#     def filter(self, qs, value):
#         if value:
#             # Perform a case-insensitive search using 'icontains'
#             return qs.filter(**{f"{self.field_name}__icontains": value})
#         return qs


# class BaseViews(viewsets.ModelViewSet):
#     filter_backends = [DjangoFilterBackend]
#     # filterset_fields = '__all__'
#     # Define message templates
#     pagination_class = CustomPagination  # Replace with your custom pagination class if defined
#     message_templates = {
#         "list_success": "Data retrieved successfully",
#         "list_not_allowed": "List method is not allowed",
#         "retrieve_success": "Object retrieved successfully",
#         "retrieve_not_allowed": "Retrieve method is not allowed",
#         "create_success": "Object created successfully",
#         "create_validation_error": "Validation error",
#         "create_not_allowed": "Create method is not allowed",
#         "update_success": "Object updated successfully",
#         "update_not_allowed": "Update method is not allowed",
#         "partial_update_not_allowed": "Partial Update method is not allowed",
#         "destroy_success": "Object deleted successfully",
#         "destroy_not_allowed": "Delete method is not allowed",
#         "soft_delete_success": "Data deleted. But you can recover your data",
#         "soft_delete_not_allowed": "Soft Delete method is not allowed",
#         "change_status_success": "Status changed",
#         "change_status_not_allowed": "Change Status method is not allowed",
#         "restore_soft_deleted_success": "Soft deleted data restored successfully",
#         "restore_soft_deleted_not_allowed": "Restore Soft Deleted method is not allowed",
#         "leave_count_message": "Count Data get successfully",
#         "leave_approve": "Approved Successfully",
#         "leave_reject":"Rejected Successfully"
#     }


#     # Define the custom filter class dynamically
#     # def get_queryset(self):
#     #     queryset = self.model_name.objects.filter(is_deleted=False)

#     #     # Get parameters from the request
#     #     params = self.request.query_params

#     #     # Iterate through parameters and filter queryset dynamically
#     #     for param, value in params.items():
#     #         if param in [field.name for field in self.model_name._meta.get_fields()]:
#     #             kwargs = {f"{param}__icontains": value}  # Perform case-insensitive partial match
#     #             queryset = queryset.filter(Q(**kwargs))
#     #         else:
#     #             # Check if the parameter corresponds to a field in a related model
#     #             related_fields = [field.name for field in self.model_name._meta.get_fields(include_hidden=True) if field.is_relation]
#     #             for field_name in related_fields:
#     #                 field_object = getattr(self.model_name, field_name)
#     #                 if hasattr(field_object, 'related'):
#     #                     related_model = field_object.related.related_model
#     #                     if param in [related_field.name for related_field in related_model._meta.get_fields()]:
#     #                         kwargs = {f"{field_name}__{param}__icontains": value}  # Traverse the relationship
#     #                         queryset = queryset.filter(Q(**kwargs))

#     #     return queryset.order_by('-id')
#     # def get_queryset(self):
#     #     try:
#     #         queryset = self.model_name.objects.filter(is_deleted=False)
#     #     except:
#     #         queryset = self.model_name.objects.all()

#     #     # Get parameters from the request
#     #     params = self.request.query_params
        

#     #     start_date = params.get('start_date')
#     #     end_date = params.get('end_date')

#     #     # If both start_date and end_date are provided, filter the queryset by the date range
#     #     if start_date and end_date:
#     #         try:
#     #             start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
#     #             end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
#     #             # Assuming your model has a 'created_date' field
#     #             try:
#     #                 queryset = queryset.filter(date__range=[start_date, end_date])
#     #             except:
#     #                 queryset = queryset.filter(created_at__range=[start_date, end_date])
#     #         except ValueError:
#     #             # Handle invalid date format
#     #             pass
#     #     keyword = params.get('keyword')

#     #     if keyword:
#     #         # Filter all character and text fields for similar data
#     #         char_fields = [f.name for f in self.model_name._meta.fields if isinstance(f, models.CharField)]
#     #         text_fields = [f.name for f in self.model_name._meta.fields if isinstance(f, models.TextField)]

#     #         char_queries = [Q(**{f"{field}__icontains": keyword}) for field in char_fields]
#     #         text_queries = [Q(**{f"{field}__icontains": keyword}) for field in text_fields]

#     #         # Combine all queries with OR operator
#     #         combined_queries = char_queries + text_queries
#     #         final_query = combined_queries.pop()
#     #         for query in combined_queries:
#     #             final_query |= query

#     #         queryset = queryset.filter(final_query)

#     #     params = {param: value for param, value in params.items() if param not in ['limit', 'offset','start_date','end_date','keyword','depth','leave_ids','em_id']}
#     #     # Iterate through parameters and filter queryset dynamically
#     #     for param, value in params.items():
#     #         # Check if the parameter corresponds to a field in a related model
#     #         if "__" in param:
#     #             try:
#     #                 queryset = queryset.filter(**{param + "__icontains": value})
#     #             except:
#     #                 queryset = queryset.filter(**{param: value})
#     #         else:
#     #             try:
#     #                 queryset = queryset.filter(**{param + "__icontains": value})
#     #             except:
#     #                 queryset = queryset.filter(**{param: value})

#     #     return queryset.order_by('-id')

#     def get_queryset(self):
#         # ---------------- Base Queryset ----------------
#         try:
#             queryset = self.model_name.objects.filter(is_deleted=False)
#         except:
#             queryset = self.model_name.objects.all()

#         params = self.request.query_params

#         # ---------------- Search Section ----------------
#         search = params.get("search")
#         if search:
#             char_fields = [f.name for f in self.model_name._meta.fields if isinstance(f, models.CharField)]
#             text_fields = [f.name for f in self.model_name._meta.fields if isinstance(f, models.TextField)]
#             int_fields = [f.name for f in self.model_name._meta.fields if isinstance(f, models.IntegerField)]

#             # Text/Char Search
#             char_queries = [Q(**{f"{field}__icontains": search}) for field in char_fields]
#             text_queries = [Q(**{f"{field}__icontains": search}) for field in text_fields]

#             # Integer Search (id বা অন্য integer ফিল্ড)
#             int_queries = []
#             if search.isdigit():
#                 for field in int_fields:
#                     int_queries.append(Q(**{f"{field}": int(search)}))

#             # Auto ForeignKey & M2M Search
#             related_queries = []
#             for field in self.model_name._meta.get_fields():
#                 if (field.is_relation and field.many_to_one) or field.many_to_many:
#                     rel_model = field.related_model
#                     for lookup in ["name", "username", "title", "code"]:
#                         if lookup in [f.name for f in rel_model._meta.fields]:
#                             related_queries.append(Q(**{f"{field.name}__{lookup}__icontains": search}))
#                             break

#             # Combine all queries
#             combined_queries = char_queries + text_queries + int_queries + related_queries
#             if combined_queries:
#                 final_query = combined_queries.pop()
#                 for query in combined_queries:
#                     final_query |= query
#                 queryset = queryset.filter(final_query)

#         # ---------------- Date / Date Range Section ----------------
#         single_date = params.get("date")
#         start_date = params.get("start_date")
#         end_date = params.get("end_date")

#         if single_date:
#             try:
#                 single_date = datetime.strptime(single_date, "%Y-%m-%d").date()
#                 try:
#                     queryset = queryset.filter(date=single_date)
#                 except:
#                     queryset = queryset.filter(created_at__date=single_date)
#             except ValueError:
#                 pass

#         elif start_date and end_date:
#             try:
#                 start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
#                 end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
#                 try:
#                     queryset = queryset.filter(date__range=[start_date, end_date])
#                 except:
#                     queryset = queryset.filter(created_at__range=[start_date, end_date])
#             except ValueError:
#                 pass

#         # ---------------- Keyword Section ----------------
#         keyword = params.get("keyword")
#         if keyword:
#             char_fields = [f.name for f in self.model_name._meta.fields if isinstance(f, models.CharField)]
#             text_fields = [f.name for f in self.model_name._meta.fields if isinstance(f, models.TextField)]
#             int_fields = [f.name for f in self.model_name._meta.fields if isinstance(f, models.IntegerField)]

#             char_queries = [Q(**{f"{field}__icontains": keyword}) for field in char_fields]
#             text_queries = [Q(**{f"{field}__icontains": keyword}) for field in text_fields]

#             int_queries = []
#             if keyword.isdigit():
#                 for field in int_fields:
#                     int_queries.append(Q(**{f"{field}": int(keyword)}))

#             combined_queries = char_queries + text_queries + int_queries
#             if combined_queries:
#                 final_query = combined_queries.pop()
#                 for query in combined_queries:
#                     final_query |= query
#                 queryset = queryset.filter(final_query)

#         # ---------------- Dynamic Filters Section ----------------
#         filter_params = {
#             param: value
#             for param, value in params.items()
#             if param not in [
#                 "limit", "offset", "date", "start_date", "end_date",
#                 "keyword", "depth", "leave_ids", "em_id", "search"
#             ]
#         }

#         for param, value in filter_params.items():
#             if "__" in param:
#                 try:
#                     queryset = queryset.filter(**{param + "__icontains": value})
#                 except:
#                     queryset = queryset.filter(**{param: value})
#             else:
#                 try:
#                     queryset = queryset.filter(**{param + "__icontains": value})
#                 except:
#                     queryset = queryset.filter(**{param: value})

#         return queryset.order_by("-id")
    
#     def generate_response(self, success, status_code, message_key, error=None, data=None, page=None):
#         model_name = self.model_name.__name__
#         message = self.message_templates.get(message_key, "")
#         if page is not None:
#             data = self.get_paginated_response(data)
#         # Convert ErrorDetail objects to strings
#         # Ensure error is a dictionary
#         # formatted_error = {}
#         # if error and isinstance(error, dict):
#         #     for key, value in error.items():
#         #         formatted_error[key] = [str(error_item) for error_item in value]
#         # elif error:
#         #     # If error is not None but not a dictionary, handle it as a single error message
#         #     formatted_error['_global'] = [str(error)]
#         return Response({
#             "success": success,
#             "status": status_code,
#             "message": f"{model_name} {message}",
#             "error": error,
#             "data": {"results":data}
#         })

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
#                 token = encode_jwt({"data": serializer.data})  # Encode serialized data into JWT token
#                 return self.generate_response(True, status.HTTP_200_OK, "list_success", data={"token": token})
#             else:
#                 # Pagination requested, apply pagination
#                 queryset = self.filter_queryset(self.get_queryset())
#                 page = self.paginate_queryset(queryset)
#                 if page is not None:
#                     serializer = self.get_serializer(page, many=True)
#                     token = encode_jwt({"data": serializer.data})  # Encode serialized data into JWT token
#                     return self.get_paginated_response({"token": token})
#         else:
#             return self.generate_response(False, status.HTTP_405_METHOD_NOT_ALLOWED, "list_not_allowed")

#     def retrieve(self, request, *args, **kwargs):
#         if "retrieve" in self.methods:
#             instance = self.get_object()
#             serializer = self.get_serializer(instance)
#             token = encode_jwt({"data": serializer.data})  # Encode serialized data into JWT token
#             return self.generate_response(True, status.HTTP_200_OK, "retrieve_success", data={"token": token})
#         else:
#             return self.generate_response(False, status.HTTP_405_METHOD_NOT_ALLOWED, "retrieve_not_allowed")

#     def create(self, request, *args, **kwargs):
#         if "create" in self.methods:
#             serializer = self.get_serializer(data=request.data)
#             try:
#                 # serializer = self.get_serializer(data=request.data)
#                 serializer.is_valid(raise_exception=True)
#                 self.perform_create(serializer)
#                 token = encode_jwt({"data": serializer.data})  # Encode serialized data into JWT token
#                 return self.generate_response(True, status.HTTP_201_CREATED, "create_success", data={"token": token})
#             except:
#                 # print(e)
#                 return self.generate_response(False, status.HTTP_400_BAD_REQUEST, "create_validation_error", error=serializer.errors)
#         else:
#             return self.generate_response(False, status.HTTP_405_METHOD_NOT_ALLOWED, "create_not_allowed")

#     def update(self, request, *args, **kwargs):
#         if "update" in self.methods:
#             partial = kwargs.pop('partial', False)
#             instance = self.get_object()
#             serializer = self.get_serializer(instance, data=request.data, partial=partial)
#             serializer.is_valid(raise_exception=True)
#             self.perform_update(serializer)
#             token = encode_jwt({"data": serializer.data})  # Encode serialized data into JWT token
#             return self.generate_response(True, status.HTTP_200_OK, "update_success", data={"token": token})
#         else:
#             return self.generate_response(False, status.HTTP_405_METHOD_NOT_ALLOWED, "update_not_allowed")

#     def partial_update(self, request, *args, **kwargs):
#         if "partial_update" in self.methods:
#             kwargs['partial'] = True
#             return self.update(request, *args, **kwargs)
#         else:
#             return self.generate_response(False, status.HTTP_405_METHOD_NOT_ALLOWED, "partial_update_not_allowed")

#     def destroy(self, request, *args, **kwargs):
#         if "destroy" in self.methods:
#             instance = self.get_object()
#             self.perform_destroy(instance)
#             return self.generate_response(True, status.HTTP_204_NO_CONTENT, "destroy_success")
#         else:
#             return self.generate_response(False, status.HTTP_405_METHOD_NOT_ALLOWED, "destroy_not_allowed")

#     @action(detail=True, methods=['post'])
#     def soft_delete(self, request, pk=None):
#         if "soft_delete" in self.methods:
#             item = self.get_object()
#             item.is_deleted = True
#             item.save()
#             return self.generate_response(True, status.HTTP_200_OK, "soft_delete_success")
#         else:
#             return self.generate_response(False, status.HTTP_405_METHOD_NOT_ALLOWED, "soft_delete_not_allowed")

#     @action(detail=True, methods=['post'])
#     def change_status(self, request, pk=None):
#         if "change_status" in self.methods:
#             item = self.get_object()
#             item.status = not item.status
#             item.save()
#             return self.generate_response(True, status.HTTP_200_OK, "change_status_success")
#         else:
#             return self.generate_response(False, status.HTTP_405_METHOD_NOT_ALLOWED, "change_status_not_allowed")

#     @action(detail=False, methods=['post'])
#     def restore_soft_deleted(self, request):
#         if "restore_soft_deleted" in self.methods:
#             queryset = self.model_name.objects.filter(is_deleted=True)
#             queryset.update(is_deleted=False)
#             return self.generate_response(True, status.HTTP_200_OK, "restore_soft_deleted_success")
#         else:
#             return self.generate_response(False, status.HTTP_405_METHOD_NOT_ALLOWED, "restore_soft_deleted_not_allowed")
#     def get_serializer_context(self):
#         # Get the query parameters from the request
#         serializer_context = super().get_serializer_context()
        
#         # Check if 'depth' parameter is provided in query parameters
#         depth_param = self.request.query_params.get('depth')
#         if depth_param is not None:
#             # Set the depth parameter in the serializer context
#             serializer_context['depth'] = int(depth_param)
#         else:
#             serializer_context['depth'] = None

#         return serializer_context
#     @action(detail=False, methods=['get'])
#     def fields(self, request):
#         model = self.queryset.model
#         fields_data = []

#         for field in model._meta.get_fields():
#             if not hasattr(field, "verbose_name"):
#                 continue

#             # Skip reverse relations
#             if field.auto_created and not field.concrete:
#                 continue

#             # Skip if verbose name starts with lowercase
#             if str(field.verbose_name)[0].islower():
#                 continue

#             # Detect relation type
#             if field.is_relation and field.related_model:
#                 if field.many_to_many:
#                     related_type = "ManyToMany"
#                 else:
#                     related_type = "ForeignKey"
#             else:
#                 related_type = None

#             # Get choices if available
#             choices_list = None
#             if hasattr(field, "choices") and field.choices:
#                 choices_list = [{"value": c[0], "label": c[1]} for c in field.choices]

#             # 🟢 Add data type
#             field_type = field.get_internal_type()  # e.g. CharField, IntegerField, DateTimeField

#             fields_data.append({
#                 "name": field.name,
#                 "verbose_name": field.verbose_name,
#                 "data_type": field_type,   # 👈 এখানে ফিল্ড টাইপ আসবে
#                 "related_model": field.related_model.__name__ if field.is_relation and field.related_model else None,
#                 "related_type": related_type,
#                 "choices": choices_list
#             })

#         return Response(fields_data, status=status.HTTP_200_OK)



#     # @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
#     # def logout(self, request):
#     #     """
#     #     Logout user by blacklisting refresh token.
#     #     Frontend should send {"refresh": "<refresh_token>"} in body.
#     #     """
#     #     refresh_token = request.data.get("refresh")
#     #     if not refresh_token:
#     #         return Response(
#     #             {"success": False, "message": "Refresh token required"},
#     #             status=status.HTTP_400_BAD_REQUEST
#     #         )
#     #     try:
#     #         token = RefreshToken(refresh_token)
#     #         token.blacklist()  # blacklist the token
#     #         return Response(
#     #             {"success": True, "message": "Logout successful"},
#     #             status=status.HTTP_205_RESET_CONTENT
#     #         )
#     #     except Exception as e:
#     #         return Response(
#     #             {"success": False, "message": "Logout failed", "error": str(e)},
#     #             status=status.HTTP_400_BAD_REQUEST
#     #         )

    
#     # @property
#     # def filterset_fields(self):
#     #     model = self.model_name
#     #     model_fields = model._meta.get_fields()
        
#     #     # Generate a list of filter fields excluding fields related to inheritance models
#     #     filter_fields = [field.name for field in model_fields if not field.auto_created and not isinstance(field, (ImageField, FileField))]
        
#     #     return filter_fields
#     # @property
#     # def filterset_fields(self):
#     #     model = self.model_name
#     #     model_fields = model._meta.get_fields()

#     #     # Generate a list of filter fields excluding fields related to inheritance models
#     #     filter_fields = [field.name for field in model_fields if not field.auto_created and not isinstance(field, (ImageField, FileField))]

#     #     # Include CharField and TextField for case-insensitive searching
#     #     text_fields = [field.name for field in model_fields if isinstance(field, (CharField, TextField))]

#     #     return filter_fields + text_fields
    
        




#     ################################# System Settings #########################################
# class SystemAssetsViewSet(BaseViews):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated,IsStaff]
#     model_name = SoftwareAsset
#     methods = ["list", "retrieve", "create", "update", "partial_update", "destroy", "soft_delete", "change_status", "restore_soft_deleted"]
#     serializer_class = SoftwareAssetSerializer
# class EmailConfigureViewSet(viewsets.ModelViewSet):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated,IsStaff]
#     queryset = DynamicEmailConfiguration.objects.all()
#     serializer_class = EmailConfigureSerializer
#     def partial_update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=True)
#         try:
#             serializer.is_valid(raise_exception=True)
#             self.perform_update(serializer)
#             model_name = self.serializer_class.Meta.model.__name__  # Get the model name
#             message = "updated successfully"
#             success = True
#             status_code = status.HTTP_200_OK
#             error = None
#             data = serializer.data
#         except Exception as e:
#             model_name = self.serializer_class.Meta.model.__name__  # Get the model name
#             message = "update failed"
#             success = False
#             status_code = status.HTTP_400_BAD_REQUEST
#             error = str(e)
#             data = None

#         return Response({
#             "success": success,
#             "status": status_code,
#             "message": f"{model_name} {message}",
#             "error": error,
#             "data": {"results": data}
#         })
    

from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets,parsers
from des.models import DynamicEmailConfiguration
from globalapp.ed import encode_jwt
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import FileField, ImageField
from django_filters import rest_framework as filters
from django.db.models import CharField, TextField
from django.utils import timezone
from datetime import datetime
from django.db.models import Q
from django.db import models
# from users.permissions import IsStaff
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
from globalapp.models import SoftwareAsset
from globalapp.serializers import EmailConfigureSerializer, SoftwareAssetSerializer
from rest_framework import serializers
from django.utils.text import capfirst
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from django.conf import settings

from users.models import Users
from users.permissions import IsStaff

def decode_jwt(token: str) -> dict:
    """
    Decode a JWT token and return its payload.
    Raises an exception if the token is invalid or expired.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,     # Use the same secret key used to encode the token
            algorithms=["HS256"],    # Use the same algorithm as used during encoding
        )
        return payload
    except ExpiredSignatureError:
        raise Exception("Token has expired")
    except InvalidTokenError:
        raise Exception("Invalid token")


class CustomPagination(LimitOffsetPagination):

    def get_paginated_response(self, data):
        return Response({
            'success': True,
            'status': 200,
            'message': 'Data retrieved successfully',
            'error': None,
            'data': {
                'meta': {
                    'count': self.count,
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link()
                },
                'results': data
            }
        })
    
class CaseInsensitiveCharFilter(filters.CharFilter):
    def filter(self, qs, value):
        if value:
            # Perform a case-insensitive search using 'icontains'
            return qs.filter(**{f"{self.field_name}__icontains": value})
        return qs

# class BaseViews(viewsets.ModelViewSet):
#     filter_backends = [DjangoFilterBackend]
#     # filterset_fields = '__all__'
#     # Define message templates
#     pagination_class = CustomPagination  # Replace with your custom pagination class if defined
#     message_templates = {
#         "list_success": "Data retrieved successfully",
#         "list_not_allowed": "List method is not allowed",
#         "retrieve_success": "Object retrieved successfully",
#         "retrieve_not_allowed": "Retrieve method is not allowed",
#         "create_success": "Object created successfully",
#         "create_validation_error": "Validation error",
#         "create_not_allowed": "Create method is not allowed",
#         "update_success": "Object updated successfully",
#         "update_not_allowed": "Update method is not allowed",
#         "partial_update_not_allowed": "Partial Update method is not allowed",
#         "destroy_success": "Object deleted successfully",
#         "destroy_not_allowed": "Delete method is not allowed",
#         "soft_delete_success": "Data deleted. But you can recover your data",
#         "soft_delete_not_allowed": "Soft Delete method is not allowed",
#         "change_status_success": "Status changed",
#         "change_status_not_allowed": "Change Status method is not allowed",
#         "restore_soft_deleted_success": "Soft deleted data restored successfully",
#         "restore_soft_deleted_not_allowed": "Restore Soft Deleted method is not allowed",
#         "leave_count_message": "Count Data get successfully",
#         "leave_approve": "Approved Successfully",
#         "leave_reject":"Rejected Successfully"
#     }


   

#     def get_queryset(self):
#         # ---------------- Base Queryset ----------------
#         try:
#             queryset = self.model_name.objects.filter(is_deleted=False)
#         except:
#             queryset = self.model_name.objects.all()

#         params = self.request.query_params

#         # ---------------- Search Section ----------------
#         search = params.get("search")
#         if search:
#             char_fields = [f.name for f in self.model_name._meta.fields if isinstance(f, models.CharField)]
#             text_fields = [f.name for f in self.model_name._meta.fields if isinstance(f, models.TextField)]
#             int_fields = [f.name for f in self.model_name._meta.fields if isinstance(f, models.IntegerField)]

#             # Text/Char Search
#             char_queries = [Q(**{f"{field}__icontains": search}) for field in char_fields]
#             text_queries = [Q(**{f"{field}__icontains": search}) for field in text_fields]

#             # Integer Search (id বা অন্য integer ফিল্ড)
#             int_queries = []
#             if search.isdigit():
#                 for field in int_fields:
#                     int_queries.append(Q(**{f"{field}": int(search)}))

#             # Auto ForeignKey & M2M Search
#             related_queries = []
#             for field in self.model_name._meta.get_fields():
#                 if (field.is_relation and field.many_to_one) or field.many_to_many:
#                     rel_model = field.related_model
#                     for lookup in ["name", "username", "title", "code"]:
#                         if lookup in [f.name for f in rel_model._meta.fields]:
#                             related_queries.append(Q(**{f"{field.name}__{lookup}__icontains": search}))
#                             break

#             # Combine all queries
#             combined_queries = char_queries + text_queries + int_queries + related_queries
#             if combined_queries:
#                 final_query = combined_queries.pop()
#                 for query in combined_queries:
#                     final_query |= query
#                 queryset = queryset.filter(final_query)

#         # ---------------- Date / Date Range Section ----------------
#         single_date = params.get("date")
#         start_date = params.get("start_date")
#         end_date = params.get("end_date")

#         if single_date:
#             try:
#                 single_date = datetime.strptime(single_date, "%Y-%m-%d").date()
#                 try:
#                     queryset = queryset.filter(date=single_date)
#                 except:
#                     queryset = queryset.filter(created_at__date=single_date)
#             except ValueError:
#                 pass

#         elif start_date and end_date:
#             try:
#                 start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
#                 end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
#                 try:
#                     queryset = queryset.filter(date__range=[start_date, end_date])
#                 except:
#                     queryset = queryset.filter(created_at__range=[start_date, end_date])
#             except ValueError:
#                 pass

#         # ---------------- Keyword Section ----------------
#         keyword = params.get("keyword")
#         if keyword:
#             char_fields = [f.name for f in self.model_name._meta.fields if isinstance(f, models.CharField)]
#             text_fields = [f.name for f in self.model_name._meta.fields if isinstance(f, models.TextField)]
#             int_fields = [f.name for f in self.model_name._meta.fields if isinstance(f, models.IntegerField)]

#             char_queries = [Q(**{f"{field}__icontains": keyword}) for field in char_fields]
#             text_queries = [Q(**{f"{field}__icontains": keyword}) for field in text_fields]

#             int_queries = []
#             if keyword.isdigit():
#                 for field in int_fields:
#                     int_queries.append(Q(**{f"{field}": int(keyword)}))

#             combined_queries = char_queries + text_queries + int_queries
#             if combined_queries:
#                 final_query = combined_queries.pop()
#                 for query in combined_queries:
#                     final_query |= query
#                 queryset = queryset.filter(final_query)

#         # ---------------- Dynamic Filters Section ----------------
#         filter_params = {
#             param: value
#             for param, value in params.items()
#             if param not in [
#                 "limit", "offset", "date", "start_date", "end_date",
#                 "keyword", "depth", "leave_ids", "em_id", "search"
#             ]
#         }

#         for param, value in filter_params.items():
#             if "__" in param:
#                 try:
#                     queryset = queryset.filter(**{param + "__icontains": value})
#                 except:
#                     queryset = queryset.filter(**{param: value})
#             else:
#                 try:
#                     queryset = queryset.filter(**{param + "__icontains": value})
#                 except:
#                     queryset = queryset.filter(**{param: value})

#         return queryset.order_by("-id")
    
#     def generate_response(self, success, status_code, message_key, error=None, data=None, page=None):
#         model_name = self.model_name.__name__
#         message = self.message_templates.get(message_key, "")
#         if page is not None:
#             data = self.get_paginated_response(data)
#         # Convert ErrorDetail objects to strings
#         # Ensure error is a dictionary
#         # formatted_error = {}
#         # if error and isinstance(error, dict):
#         #     for key, value in error.items():
#         #         formatted_error[key] = [str(error_item) for error_item in value]
#         # elif error:
#         #     # If error is not None but not a dictionary, handle it as a single error message
#         #     formatted_error['_global'] = [str(error)]
#         return Response({
#             "success": success,
#             "status": status_code,
#             "message": f"{model_name} {message}",
#             "error": error,
#             "data": {"results":data}
#         })

    


  

#     def list(self, request, *args, **kwargs):
#         if "list" not in self.methods:
#             return self.generate_response(False, status.HTTP_405_METHOD_NOT_ALLOWED, "list_not_allowed")

#         # 1. Get Authorization header
#         auth_header = request.headers.get("Authorization")
#         if not auth_header or not auth_header.startswith("Bearer "):
#             return self.generate_response(False, status.HTTP_401_UNAUTHORIZED, "authorization_header_missing")

#         access_token = auth_header.split(" ")[1]

#         # 2. Decode JWT and get user_id
#         try:
#             payload = decode_jwt(access_token)
#             user_id = payload.get("user_id")
#             if not user_id:
#                 return self.generate_response(False, status.HTTP_401_UNAUTHORIZED, "invalid_token")
#         except Exception:
#             return self.generate_response(False, status.HTTP_401_UNAUTHORIZED, "invalid_token")

#         # 3. Get user, branch, area
#         try:
#             user = Users.objects.get(id=user_id)
#             branch = getattr(user, "branch", None)
#             area = getattr(user, "area", None)
#         except Users.DoesNotExist:
#             return self.generate_response(False, status.HTTP_401_UNAUTHORIZED, "user_not_found")

#         # 4. Get base queryset
#         queryset = self.filter_queryset(self.get_queryset())

#         # 5. Area filter for Installment only
#         if self.model_name.__name__ == "Installment" and area:
#             today = timezone.localdate()  # বর্তমান তারিখ
#             queryset = queryset.filter(
#                 area_name=area,
#                 installment_date=today
#             )

#         # 6. Branch filter (existing logic)
#         branch_fields = [f for f in self.model_name._meta.get_fields() if "branch" in f.name]
#         if branch and branch_fields:
#             q_objects = Q()
#             for f in branch_fields:
#                 field_name = f.name
#                 if isinstance(f, (models.ForeignKey, models.OneToOneField)):
#                     q_objects |= Q(**{f"{field_name}_id": branch.id})
#                 elif isinstance(f, models.ManyToManyField):
#                     q_objects |= Q(**{f"{field_name}__id": branch.id})
#                 elif isinstance(f, (models.CharField, models.TextField)):
#                     q_objects |= Q(**{field_name: str(branch)})
#             queryset = queryset.filter(q_objects)

#         # 7. Pagination
#         limit = request.GET.get("limit")
#         if limit is None:
#             serializer = self.get_serializer(queryset, many=True)
#             token = encode_jwt({"data": serializer.data})
#             return self.generate_response(True, status.HTTP_200_OK, "list_success", data={"token": token})
#         else:
#             page = self.paginate_queryset(queryset)
#             if page is not None:
#                 serializer = self.get_serializer(page, many=True)
#                 token = encode_jwt({"data": serializer.data})
#                 return self.get_paginated_response({"token": token})





#     def retrieve(self, request, *args, **kwargs):
#         if "retrieve" in self.methods:
#             instance = self.get_object()
#             serializer = self.get_serializer(instance)
#             token = encode_jwt({"data": serializer.data})  # Encode serialized data into JWT token
#             return self.generate_response(True, status.HTTP_200_OK, "retrieve_success", data={"token": token})
#         else:
#             return self.generate_response(False, status.HTTP_405_METHOD_NOT_ALLOWED, "retrieve_not_allowed")

#     def create(self, request, *args, **kwargs):
#         if "create" in self.methods:
#             serializer = self.get_serializer(data=request.data)
#             try:
#                 # serializer = self.get_serializer(data=request.data)
#                 serializer.is_valid(raise_exception=True)
#                 self.perform_create(serializer)
#                 token = encode_jwt({"data": serializer.data})  # Encode serialized data into JWT token
#                 return self.generate_response(True, status.HTTP_201_CREATED, "create_success", data={"token": token})
#             except:
#                 # print(e)
#                 return self.generate_response(False, status.HTTP_400_BAD_REQUEST, "create_validation_error", error=serializer.errors)
#         else:
#             return self.generate_response(False, status.HTTP_405_METHOD_NOT_ALLOWED, "create_not_allowed")

#     def update(self, request, *args, **kwargs):
#         if "update" in self.methods:
#             partial = kwargs.pop('partial', False)
#             instance = self.get_object()
#             serializer = self.get_serializer(instance, data=request.data, partial=partial)
#             serializer.is_valid(raise_exception=True)
#             self.perform_update(serializer)
#             token = encode_jwt({"data": serializer.data})  # Encode serialized data into JWT token
#             return self.generate_response(True, status.HTTP_200_OK, "update_success", data={"token": token})
#         else:
#             return self.generate_response(False, status.HTTP_405_METHOD_NOT_ALLOWED, "update_not_allowed")

#     def partial_update(self, request, *args, **kwargs):
#         if "partial_update" in self.methods:
#             kwargs['partial'] = True
#             return self.update(request, *args, **kwargs)
#         else:
#             return self.generate_response(False, status.HTTP_405_METHOD_NOT_ALLOWED, "partial_update_not_allowed")

#     def destroy(self, request, *args, **kwargs):
#         if "destroy" in self.methods:
#             instance = self.get_object()
#             self.perform_destroy(instance)
#             return self.generate_response(True, status.HTTP_204_NO_CONTENT, "destroy_success")
#         else:
#             return self.generate_response(False, status.HTTP_405_METHOD_NOT_ALLOWED, "destroy_not_allowed")

#     @action(detail=True, methods=['post'])
#     def soft_delete(self, request, pk=None):
#         if "soft_delete" in self.methods:
#             item = self.get_object()
#             item.is_deleted = True
#             item.save()
#             return self.generate_response(True, status.HTTP_200_OK, "soft_delete_success")
#         else:
#             return self.generate_response(False, status.HTTP_405_METHOD_NOT_ALLOWED, "soft_delete_not_allowed")

#     @action(detail=True, methods=['post'])
#     def change_status(self, request, pk=None):
#         if "change_status" in self.methods:
#             item = self.get_object()
#             item.status = not item.status
#             item.save()
#             return self.generate_response(True, status.HTTP_200_OK, "change_status_success")
#         else:
#             return self.generate_response(False, status.HTTP_405_METHOD_NOT_ALLOWED, "change_status_not_allowed")

#     @action(detail=False, methods=['post'])
#     def restore_soft_deleted(self, request):
#         if "restore_soft_deleted" in self.methods:
#             queryset = self.model_name.objects.filter(is_deleted=True)
#             queryset.update(is_deleted=False)
#             return self.generate_response(True, status.HTTP_200_OK, "restore_soft_deleted_success")
#         else:
#             return self.generate_response(False, status.HTTP_405_METHOD_NOT_ALLOWED, "restore_soft_deleted_not_allowed")
#     def get_serializer_context(self):
#         # Get the query parameters from the request
#         serializer_context = super().get_serializer_context()
        
#         # Check if 'depth' parameter is provided in query parameters
#         depth_param = self.request.query_params.get('depth')
#         if depth_param is not None:
#             # Set the depth parameter in the serializer context
#             serializer_context['depth'] = int(depth_param)
#         else:
#             serializer_context['depth'] = None

#         return serializer_context
#     @action(detail=False, methods=['get'])
#     def fields(self, request):
#         model = self.queryset.model
#         fields_data = []

#         for field in model._meta.get_fields():
#             if not hasattr(field, "verbose_name"):
#                 continue

#             # Skip reverse relations
#             if field.auto_created and not field.concrete:
#                 continue

#             # Skip if verbose name starts with lowercase
#             if str(field.verbose_name)[0].islower():
#                 continue

#             # Detect relation type
#             if field.is_relation and field.related_model:
#                 if field.many_to_many:
#                     related_type = "ManyToMany"
#                 else:
#                     related_type = "ForeignKey"
#             else:
#                 related_type = None

#             # Get choices if available
#             choices_list = None
#             if hasattr(field, "choices") and field.choices:
#                 choices_list = [{"value": c[0], "label": c[1]} for c in field.choices]

#             # 🟢 Add data type
#             field_type = field.get_internal_type()  # e.g. CharField, IntegerField, DateTimeField

#             fields_data.append({
#                 "name": field.name,
#                 "verbose_name": field.verbose_name,
#                 "data_type": field_type,   # 👈 এখানে ফিল্ড টাইপ আসবে
#                 "related_model": field.related_model.__name__ if field.is_relation and field.related_model else None,
#                 "related_type": related_type,
#                 "choices": choices_list
#             })

#         return Response(fields_data, status=status.HTTP_200_OK)

#     ################################# System Settings #########################################

# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from django.core.exceptions import ValidationError
# from django.db import transaction
# from django_filters.rest_framework import DjangoFilterBackend
# from django.db.models import Q, models
# from datetime import datetime
# from django.utils import timezone
# from rest_framework.decorators import action
from django.db import transaction

class BaseViews(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    pagination_class = CustomPagination
    
    message_templates = {
        "list_success": "Data retrieved successfully",
        "list_not_allowed": "List method is not allowed",
        "retrieve_success": "Object retrieved successfully",
        "retrieve_not_allowed": "Retrieve method is not allowed",
        "create_success": "Object created successfully",
        "create_validation_error": "Validation error",
        "create_not_allowed": "Create method is not allowed",
        "update_success": "Object updated successfully",
        "update_not_allowed": "Update method is not allowed",
        "partial_update_not_allowed": "Partial Update method is not allowed",
        "destroy_success": "Object deleted successfully",
        "destroy_not_allowed": "Delete method is not allowed",
        "soft_delete_success": "Data deleted. But you can recover your data",
        "soft_delete_not_allowed": "Soft Delete method is not allowed",
        "change_status_success": "Status changed",
        "change_status_not_allowed": "Change Status method is not allowed",
        "restore_soft_deleted_success": "Soft deleted data restored successfully",
        "restore_soft_deleted_not_allowed": "Restore Soft Deleted method is not allowed",
        "leave_count_message": "Count Data get successfully",
        "leave_approve": "Approved Successfully",
        "leave_reject": "Rejected Successfully",
        "insufficient_balance": "Insufficient account balance",
        "payment_failed": "Payment processing failed"
    }

    def get_queryset(self):
        # ---------------- Base Queryset ----------------
        try:
            queryset = self.model_name.objects.filter(is_deleted=False)
        except:
            queryset = self.model_name.objects.all()

        params = self.request.query_params

        # ---------------- Search Section ----------------
        search = params.get("search")
        if search:
            char_fields = [f.name for f in self.model_name._meta.fields if isinstance(f, models.CharField)]
            text_fields = [f.name for f in self.model_name._meta.fields if isinstance(f, models.TextField)]
            int_fields = [f.name for f in self.model_name._meta.fields if isinstance(f, models.IntegerField)]

            char_queries = [Q(**{f"{field}__icontains": search}) for field in char_fields]
            text_queries = [Q(**{f"{field}__icontains": search}) for field in text_fields]

            int_queries = []
            if search.isdigit():
                for field in int_fields:
                    int_queries.append(Q(**{f"{field}": int(search)}))

            related_queries = []
            for field in self.model_name._meta.get_fields():
                if (field.is_relation and field.many_to_one) or field.many_to_many:
                    rel_model = field.related_model
                    for lookup in ["name", "username", "title", "code"]:
                        if lookup in [f.name for f in rel_model._meta.fields]:
                            related_queries.append(Q(**{f"{field.name}__{lookup}__icontains": search}))
                            break

            combined_queries = char_queries + text_queries + int_queries + related_queries
            if combined_queries:
                final_query = combined_queries.pop()
                for query in combined_queries:
                    final_query |= query
                queryset = queryset.filter(final_query)

        # ---------------- Date / Date Range Section ----------------
        single_date = params.get("date")
        start_date = params.get("start_date")
        end_date = params.get("end_date")

        if single_date:
            try:
                single_date = datetime.strptime(single_date, "%Y-%m-%d").date()
                try:
                    queryset = queryset.filter(date=single_date)
                except:
                    queryset = queryset.filter(created_at__date=single_date)
            except ValueError:
                pass

        elif start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                try:
                    queryset = queryset.filter(date__range=[start_date, end_date])
                except:
                    queryset = queryset.filter(created_at__range=[start_date, end_date])
            except ValueError:
                pass

        # ---------------- Keyword Section ----------------
        keyword = params.get("keyword")
        if keyword:
            char_fields = [f.name for f in self.model_name._meta.fields if isinstance(f, models.CharField)]
            text_fields = [f.name for f in self.model_name._meta.fields if isinstance(f, models.TextField)]
            int_fields = [f.name for f in self.model_name._meta.fields if isinstance(f, models.IntegerField)]

            char_queries = [Q(**{f"{field}__icontains": keyword}) for field in char_fields]
            text_queries = [Q(**{f"{field}__icontains": keyword}) for field in text_fields]

            int_queries = []
            if keyword.isdigit():
                for field in int_fields:
                    int_queries.append(Q(**{f"{field}": int(keyword)}))

            combined_queries = char_queries + text_queries + int_queries
            if combined_queries:
                final_query = combined_queries.pop()
                for query in combined_queries:
                    final_query |= query
                queryset = queryset.filter(final_query)

        # ---------------- Dynamic Filters Section ----------------
        filter_params = {
            param: value
            for param, value in params.items()
            if param not in [
                "limit", "offset", "date", "start_date", "end_date",
                "keyword", "depth", "leave_ids", "em_id", "search"
            ]
        }

        for param, value in filter_params.items():
            if "__" in param:
                try:
                    queryset = queryset.filter(**{param + "__icontains": value})
                except:
                    queryset = queryset.filter(**{param: value})
            else:
                try:
                    queryset = queryset.filter(**{param + "__icontains": value})
                except:
                    queryset = queryset.filter(**{param: value})

        return queryset.order_by("-id")
    
    def generate_response(self, success, status_code, message_key, error=None, data=None, page=None):
        model_name = self.model_name.__name__
        message = self.message_templates.get(message_key, "")
        if page is not None:
            data = self.get_paginated_response(data)
        
        return Response({
            "success": success,
            "status": status_code,
            "message": f"{model_name} {message}",
            "error": error,
            "data": {"results": data}
        })

    def list(self, request, *args, **kwargs):
        if "list" not in self.methods:
            return self.generate_response(False, status.HTTP_405_METHOD_NOT_ALLOWED, "list_not_allowed")

        # 1. Get Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return self.generate_response(False, status.HTTP_401_UNAUTHORIZED, "authorization_header_missing")

        access_token = auth_header.split(" ")[1]

        # 2. Decode JWT and get user_id
        try:
            payload = decode_jwt(access_token)
            user_id = payload.get("user_id")
            if not user_id:
                return self.generate_response(False, status.HTTP_401_UNAUTHORIZED, "invalid_token")
        except Exception:
            return self.generate_response(False, status.HTTP_401_UNAUTHORIZED, "invalid_token")

        # 3. Get user, branch, area
        try:
            user = Users.objects.get(id=user_id)
            branch = getattr(user, "branch", None)
            area = getattr(user, "area", None)
        except Users.DoesNotExist:
            return self.generate_response(False, status.HTTP_401_UNAUTHORIZED, "user_not_found")

        # 4. Get base queryset
        queryset = self.filter_queryset(self.get_queryset())

        # 5. Area filter for Installment only
        if self.model_name.__name__ == "Installment" and area:
            today = timezone.localdate()
            queryset = queryset.filter(
                area_name=area,
                installment_date=today
            )

        # 6. Branch filter
        branch_fields = [f for f in self.model_name._meta.get_fields() if "branch" in f.name]
        if branch and branch_fields:
            q_objects = Q()
            for f in branch_fields:
                field_name = f.name
                if isinstance(f, (models.ForeignKey, models.OneToOneField)):
                    q_objects |= Q(**{f"{field_name}_id": branch.id})
                elif isinstance(f, models.ManyToManyField):
                    q_objects |= Q(**{f"{field_name}__id": branch.id})
                elif isinstance(f, (models.CharField, models.TextField)):
                    q_objects |= Q(**{field_name: str(branch)})
            queryset = queryset.filter(q_objects)

        # 7. Pagination
        limit = request.GET.get("limit")
        if limit is None:
            serializer = self.get_serializer(queryset, many=True)
            token = encode_jwt({"data": serializer.data})
            return self.generate_response(True, status.HTTP_200_OK, "list_success", data={"token": token})
        else:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                token = encode_jwt({"data": serializer.data})
                return self.get_paginated_response({"token": token})

    def retrieve(self, request, *args, **kwargs):
        if "retrieve" in self.methods:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            token = encode_jwt({"data": serializer.data})
            return self.generate_response(True, status.HTTP_200_OK, "retrieve_success", data={"token": token})
        else:
            return self.generate_response(False, status.HTTP_405_METHOD_NOT_ALLOWED, "retrieve_not_allowed")

    def create(self, request, *args, **kwargs):
        if "create" not in self.methods:
            return self.generate_response(False, status.HTTP_405_METHOD_NOT_ALLOWED, "create_not_allowed")
        
        try:
            with transaction.atomic():
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                token = encode_jwt({"data": serializer.data})
                return self.generate_response(True, status.HTTP_201_CREATED, "create_success", data={"token": token})
                
        except ValidationError as e:
            # Handle insufficient balance error from signals
            error_message = str(e)
            if "Insufficient balance" in error_message or "insufficient" in error_message.lower():
                return Response({
                    "success": False,
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": self.message_templates.get("insufficient_balance"),
                    "error": error_message,
                    "error_type": "insufficient_balance"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Other validation errors
            return self.generate_response(False, status.HTTP_400_BAD_REQUEST, "create_validation_error", error=error_message)
            
        except Exception as e:
            return self.generate_response(False, status.HTTP_400_BAD_REQUEST, "create_validation_error", error=str(e))

    def update(self, request, *args, **kwargs):
        if "update" not in self.methods:
            return self.generate_response(False, status.HTTP_405_METHOD_NOT_ALLOWED, "update_not_allowed")
        
        try:
            with transaction.atomic():
                partial = kwargs.pop('partial', False)
                instance = self.get_object()
                serializer = self.get_serializer(instance, data=request.data, partial=partial)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                token = encode_jwt({"data": serializer.data})
                return self.generate_response(True, status.HTTP_200_OK, "update_success", data={"token": token})
                
        except ValidationError as e:
            # Handle insufficient balance error from signals
            error_message = str(e)
            if "Insufficient balance" in error_message or "insufficient" in error_message.lower():
                return Response({
                    "success": False,
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": self.message_templates.get("payment_failed"),
                    "error": error_message,
                    "error_type": "insufficient_balance"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Other validation errors
            return Response({
                "success": False,
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Validation error",
                "error": error_message
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                "success": False,
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Update failed",
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        if "partial_update" in self.methods:
            kwargs['partial'] = True
            return self.update(request, *args, **kwargs)
        else:
            return self.generate_response(False, status.HTTP_405_METHOD_NOT_ALLOWED, "partial_update_not_allowed")

    def destroy(self, request, *args, **kwargs):
        if "destroy" in self.methods:
            instance = self.get_object()
            self.perform_destroy(instance)
            return self.generate_response(True, status.HTTP_204_NO_CONTENT, "destroy_success")
        else:
            return self.generate_response(False, status.HTTP_405_METHOD_NOT_ALLOWED, "destroy_not_allowed")

    @action(detail=True, methods=['post'])
    def soft_delete(self, request, pk=None):
        if "soft_delete" in self.methods:
            item = self.get_object()
            item.is_deleted = True
            item.save()
            return self.generate_response(True, status.HTTP_200_OK, "soft_delete_success")
        else:
            return self.generate_response(False, status.HTTP_405_METHOD_NOT_ALLOWED, "soft_delete_not_allowed")

    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        if "change_status" in self.methods:
            item = self.get_object()
            item.status = not item.status
            item.save()
            return self.generate_response(True, status.HTTP_200_OK, "change_status_success")
        else:
            return self.generate_response(False, status.HTTP_405_METHOD_NOT_ALLOWED, "change_status_not_allowed")

    @action(detail=False, methods=['post'])
    def restore_soft_deleted(self, request):
        if "restore_soft_deleted" in self.methods:
            queryset = self.model_name.objects.filter(is_deleted=True)
            queryset.update(is_deleted=False)
            return self.generate_response(True, status.HTTP_200_OK, "restore_soft_deleted_success")
        else:
            return self.generate_response(False, status.HTTP_405_METHOD_NOT_ALLOWED, "restore_soft_deleted_not_allowed")

    def get_serializer_context(self):
        serializer_context = super().get_serializer_context()
        depth_param = self.request.query_params.get('depth')
        if depth_param is not None:
            serializer_context['depth'] = int(depth_param)
        else:
            serializer_context['depth'] = None
        return serializer_context

    @action(detail=False, methods=['get'])
    def fields(self, request):
        model = self.queryset.model
        fields_data = []

        for field in model._meta.get_fields():
            if not hasattr(field, "verbose_name"):
                continue

            if field.auto_created and not field.concrete:
                continue

            if str(field.verbose_name)[0].islower():
                continue

            if field.is_relation and field.related_model:
                if field.many_to_many:
                    related_type = "ManyToMany"
                else:
                    related_type = "ForeignKey"
            else:
                related_type = None

            choices_list = None
            if hasattr(field, "choices") and field.choices:
                choices_list = [{"value": c[0], "label": c[1]} for c in field.choices]

            field_type = field.get_internal_type()

            fields_data.append({
                "name": field.name,
                "verbose_name": field.verbose_name,
                "data_type": field_type,
                "related_model": field.related_model.__name__ if field.is_relation and field.related_model else None,
                "related_type": related_type,
                "choices": choices_list
            })

        return Response(fields_data, status=status.HTTP_200_OK)


class SystemAssetsViewSet(BaseViews):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated,IsStaff]
    model_name = SoftwareAsset
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy", "soft_delete", "change_status", "restore_soft_deleted"]
    serializer_class = SoftwareAssetSerializer
class EmailConfigureViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated,IsStaff]
    queryset = DynamicEmailConfiguration.objects.all()
    serializer_class = EmailConfigureSerializer
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            model_name = self.serializer_class.Meta.model.__name__  # Get the model name
            message = "updated successfully"
            success = True
            status_code = status.HTTP_200_OK
            error = None
            data = serializer.data
        except Exception as e:
            model_name = self.serializer_class.Meta.model.__name__  # Get the model name
            message = "update failed"
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
            error = str(e)
            data = None

        return Response({
            "success": success,
            "status": status_code,
            "message": f"{model_name} {message}",
            "error": error,
            "data": {"results": data}
        })
    