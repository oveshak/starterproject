from collections import defaultdict
from decimal import Decimal
from django.forms import DecimalField
from django.shortcuts import render
from django.db.models import Sum, Count, DecimalField

# Create your views here.
from rest_framework import permissions, authentication
from globalapp.views import BaseViews, decode_jwt
from users.models import Users
from django.db import models
from .models import BranchAccount, DailySaving, DownPayment, Installment, InstallmentType, Loan, LoanType, Purchase, PurchaseItem, PurchaseReturn, Sale, SaleItem, Payment, Cheque, AffiliateCommission, Transection
from .serializers import (
    BranchAccountSerializer, DailySavingSerializer, DownPaymentSerializer, InstallmentSerializer, InstallmentTypeSerializer, LoanSerializer, LoanTypeSerializer, PurchaseSerializer, PurchaseItemSerializer, PurchaseReturnSerializer, SaleSerializer,
    SaleItemSerializer, PaymentSerializer, ChequeSerializer, AffiliateCommissionSerializer, TransectionSerializer
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
from .models import Installment, Loan
from .serializers import InstallmentSerializer, LoanSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication
from .models import Variation



class PurchaseViewSet(BaseViews):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = Purchase
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy", "soft_delete", "change_status", "restore_soft_deleted"]



class PurchaseItemViewSet(BaseViews):
    queryset = PurchaseItem.objects.all()
    serializer_class = PurchaseItemSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = PurchaseItem
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy", "soft_delete", "change_status", "restore_soft_deleted"]

class PurchaseReturnViewSet(BaseViews):
    queryset = PurchaseReturn.objects.all()
    serializer_class = PurchaseReturnSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = PurchaseReturn
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy", "soft_delete", "change_status", "restore_soft_deleted"]

class SaleViewSet(BaseViews):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = Sale
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy", "soft_delete", "change_status", "restore_soft_deleted"]

class SaleItemViewSet(BaseViews):
    queryset = SaleItem.objects.all()
    serializer_class = SaleItemSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = SaleItem
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy", "soft_delete", "change_status", "restore_soft_deleted"]

class PaymentViewSet(BaseViews):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = Payment
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy", "soft_delete", "change_status", "restore_soft_deleted"]

class ChequeViewSet(BaseViews):
    queryset = Cheque.objects.all()
    serializer_class = ChequeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = Cheque
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy", "soft_delete", "change_status", "restore_soft_deleted"]

class AffiliateCommissionViewSet(BaseViews):
    queryset = AffiliateCommission.objects.all()
    serializer_class = AffiliateCommissionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = AffiliateCommission
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy", "soft_delete", "change_status", "restore_soft_deleted"]

class LoanTypeViewSet(BaseViews):
    queryset = LoanType.objects.all()
    serializer_class = LoanTypeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = LoanType
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy"]


class InstallmentTypeViewSet(BaseViews):
    queryset = InstallmentType.objects.all()
    serializer_class = InstallmentTypeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = InstallmentType
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy"]


class DailySavingViewSet(BaseViews):
    queryset = DailySaving.objects.all()
    serializer_class = DailySavingSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = DailySaving
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy"]







class AdminVariationByProductView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        product_id = request.GET.get("product")
        qs = Variation.objects.filter(product_name_id=product_id) if product_id else Variation.objects.none()

        return Response([
            {"id": v.id, "name": v.name}
            for v in qs
        ])





class InstallmentViewSet(BaseViews):
    queryset = Installment.objects.all()
    serializer_class = InstallmentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = Installment
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy"]




class DownPaymentViewSet(BaseViews):
    queryset = DownPayment.objects.all()
    serializer_class = DownPaymentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = DownPayment
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy"]
    
    # def update(self, request, *args, **kwargs):
    #     """
    #     Override update to handle insufficient balance errors
    #     """
    #     try:
    #         with transaction.atomic():
    #             # Call parent update method
    #             response = super().update(request, *args, **kwargs)
    #             return response
                
    #     except ValidationError as e:
    #         # Catch insufficient balance error from signal
    #         error_message = str(e)
            
    #         # Check if it's an insufficient balance error
    #         if "Insufficient balance" in error_message or "insufficient" in error_message.lower():
    #             return Response({
    #                 'success': False,
    #                 'error': error_message,
    #                 'message': 'Payment failed: Customer does not have sufficient account balance',
    #                 'error': 'insufficient_balance'
    #             }, status=status.HTTP_400_BAD_REQUEST)
            
    #         # Other validation errors
    #         return Response({
    #             'success': False,
    #             'error': error_message,
    #             'message': 'Validation error occurred'
    #         }, status=status.HTTP_400_BAD_REQUEST)
            
    #     except Exception as e:
    #         return Response({
    #             'success': False,
    #             'error': str(e),
    #             'message': 'An unexpected error occurred'
    #         }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # def partial_update(self, request, *args, **kwargs):
    #     """
    #     Override partial_update to handle insufficient balance errors
    #     """
    #     try:
    #         with transaction.atomic():
    #             # Call parent partial_update method
    #             response = super().partial_update(request, *args, **kwargs)
    #             return response
                
    #     except ValidationError as e:
    #         error_message = str(e)
            
    #         if "Insufficient balance" in error_message or "insufficient" in error_message.lower():
    #             return Response({
    #                 'success': False,
    #                 'error': error_message,
    #                 'message': 'Payment failed: Customer does not have sufficient account balance',
    #                 'error': 'insufficient_balance'
    #             }, status=status.HTTP_400_BAD_REQUEST)
            
    #         return Response({
    #             'success': False,
    #             'error': error_message,
    #             'message': 'Validation error occurred'
    #         }, status=status.HTTP_400_BAD_REQUEST)
            
    #     except Exception as e:
    #         return Response({
    #             'success': False,
    #             'error': str(e),
    #             'message': 'An unexpected error occurred'
    #         }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class BranchAccountViewSet(BaseViews):
    queryset =  BranchAccount.objects.all()
    serializer_class =  BranchAccountSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name =  BranchAccount
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy"]

class LoanViewSet(BaseViews):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = Loan
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy"]
    
    # def create(self, request, *args, **kwargs):
    #     """
    #     Override create to handle insufficient balance errors during loan creation
    #     """
    #     try:
    #         with transaction.atomic():
    #             # Call parent create method
    #             response = super().create(request, *args, **kwargs)
    #             return response
                
    #     except ValidationError as e:
    #         error_message = str(e)
            
    #         # Check if it's an insufficient balance error for down payment
    #         if "Insufficient balance" in error_message or "insufficient" in error_message.lower():
    #             return Response({
    #                 'success': False,
    #                 'error': error_message,
    #                 'message': 'Loan creation failed: Customer does not have sufficient balance for down payment',
    #                 'error_type': 'insufficient_balance_down_payment'
    #             }, status=status.HTTP_400_BAD_REQUEST)
            
    #         return Response({
    #             'success': False,
    #             'error': error_message,
    #             'message': 'Validation error occurred during loan creation'
    #         }, status=status.HTTP_400_BAD_REQUEST)
            
    #     except Exception as e:
    #         return Response({
    #             'success': False,
    #             'error': str(e),
    #             'message': 'An unexpected error occurred'
    #         }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============================================================
# ALTERNATIVE APPROACH: Modify BaseViews (if you have access)
# ============================================================

# class BaseViewsWithErrorHandling(BaseViews):
#     """
#     Enhanced BaseViews with automatic ValidationError handling
#     Use this as parent class instead of BaseViews
#     """
    
#     def handle_exception(self, exc):
#         """
#         Override DRF's handle_exception to catch ValidationError from signals
#         """
#         if isinstance(exc, ValidationError):
#             error_message = str(exc)
            
#             # Determine error type
#             if "Insufficient balance" in error_message or "insufficient" in error_message.lower():
#                 return Response({
#                     'success': False,
#                     'error': error_message,
#                     'message': 'Operation failed: Insufficient account balance',
#                     'error_type': 'insufficient_balance'
#                 }, status=status.HTTP_400_BAD_REQUEST)
            
#             return Response({
#                 'success': False,
#                 'error': error_message,
#                 'message': 'Validation error occurred'
#             }, status=status.HTTP_400_BAD_REQUEST)
        
#         # Let parent class handle other exceptions
#         return super().handle_exception(exc)
    
#     def perform_create(self, serializer):
#         """Wrap create in transaction"""
#         with transaction.atomic():
#             super().perform_create(serializer)
    
#     def perform_update(self, serializer):
#         """Wrap update in transaction"""
#         with transaction.atomic():
#             super().perform_update(serializer)


# # Using the enhanced base view (RECOMMENDED)
# class InstallmentViewSetEnhanced(BaseViewsWithErrorHandling):
#     queryset = Installment.objects.all()
#     serializer_class = InstallmentSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     model_name = Installment
#     methods = ["list", "retrieve", "create", "update", "partial_update", "destroy"]


# class LoanViewSetEnhanced(BaseViewsWithErrorHandling):
#     queryset = Loan.objects.all()
#     serializer_class = LoanSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     model_name = Loan
#     methods = ["list", "retrieve", "create", "update", "partial_update", "destroy"]



# class TransectionViewSet(BaseViews):
#     queryset = Transection.objects.all()
#     serializer_class = TransectionSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     model_name = Transection
#     methods = ["list", "retrieve", "create", "update", "partial_update", "destroy"]
    
# from django.db.models import Sum, DecimalField
# from django.db.models.functions import Coalesce
# from django.utils.dateparse import parse_date
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework import status

# from .models import Transection
# from .serializers import TransectionSerializer
# def normalize_modelname(name):
#     if not name:
#         return "Unknown"

#     if ":" in name:
#         return name.split(":")[0].strip()

#     if "(" in name:
#         return name.split("(")[0].strip()

#     return name.strip()

# class TransectionViewSet(BaseViews):
#     queryset = Transection.objects.all()
#     serializer_class = TransectionSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     model_name = Transection
#     methods = ["list", "retrieve", "create", "update", "partial_update", "destroy"]

#     @action(detail=False, methods=["get"], url_path="summary")
#     def summary(self, request):
#         queryset = self.get_queryset()

#         # =========================
#         # FILTERS
#         # =========================
#         branch = request.GET.get("branch")
#         area = request.GET.get("area")
#         customer_group = request.GET.get("customer_group")
#         from_date = request.GET.get("from_date")
#         to_date = request.GET.get("to_date")

#         if branch:
#             queryset = queryset.filter(branch_name_id=branch)

#         if area:
#             queryset = queryset.filter(area_name_id=area)

#         if customer_group:
#             queryset = queryset.filter(customer_group_id=customer_group)

#         if from_date:
#             queryset = queryset.filter(created_at__date__gte=from_date)

#         if to_date:
#             queryset = queryset.filter(created_at__date__lte=to_date)

#         # =========================
#         # OVERALL SUMMARY
#         # =========================
#         overall = queryset.aggregate(
#             total_amount=Coalesce(Sum("amount"), Decimal("0.00"), output_field=DecimalField()),
#             total_paid_amount=Coalesce(Sum("paid_amount"), Decimal("0.00"), output_field=DecimalField()),
#             total_due_amount=Coalesce(Sum("due_amount"), Decimal("0.00"), output_field=DecimalField()),
#         )

#         # =========================
#         # MODELNAME WISE SUMMARY
#         # =========================
#         model_bucket = defaultdict(lambda: {
#             "total_amount": Decimal("0.00"),
#             "total_paid_amount": Decimal("0.00"),
#             "total_due_amount": Decimal("0.00"),
#         })

#         for row in queryset.values("modelname", "amount", "paid_amount", "due_amount"):
#             base_name = normalize_modelname(row["modelname"])

#             model_bucket[base_name]["total_amount"] += row["amount"] or Decimal("0.00")
#             model_bucket[base_name]["total_paid_amount"] += row["paid_amount"] or Decimal("0.00")
#             model_bucket[base_name]["total_due_amount"] += row["due_amount"] or Decimal("0.00")

#         modelname_wise = [
#             {
#                 "modelname": key,
#                 "total_amount": value["total_amount"],
#                 "total_paid_amount": value["total_paid_amount"],
#                 "total_due_amount": value["total_due_amount"],
#             }
#             for key, value in model_bucket.items()
#         ]

#         # =========================
#         # RECEIVED BY WISE SUMMARY
#         # =========================
#         received_by_wise = list(
#             queryset.values("received_by_id", "received_by__name")
#             .annotate(
#                 total_amount=Coalesce(Sum("amount"), Decimal("0.00"), output_field=DecimalField()),
#                 total_paid_amount=Coalesce(Sum("paid_amount"), Decimal("0.00"), output_field=DecimalField()),
#                 total_due_amount=Coalesce(Sum("due_amount"), Decimal("0.00"), output_field=DecimalField()),
#             )
#         )

#         # =========================
#         # FINAL RESPONSE
#         # =========================
#         return Response({
#             "success": True,
#             "status": 200,
#             "message": "Transection summary retrieved successfully",
#             "error": None,
#             "data": {
#                 "overall": overall,
#                 "modelname_wise": modelname_wise,
#                 "received_by_wise": received_by_wise,
#             }
#         })

import re
from decimal import Decimal
from collections import defaultdict

from django.db.models import Sum, DecimalField
from django.db.models.functions import Coalesce
from django.utils import timezone

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Transection
from .serializers import TransectionSerializer
from globalapp.views import BaseViews


# =========================
# Helper: Clean model name
# =========================
def normalize_modelname(name):
    if not name:
        return "Unknown"

    # 1️ Take only before colon (:)
    name = name.split(":")[0]

    # 2️ Remove anything inside brackets ()
    name = re.sub(r"\s*\(.*?\)", "", name)

    return name.strip()
class TransectionViewSet(BaseViews):
    queryset = Transection.objects.all()
    serializer_class = TransectionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = Transection
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy"]

    @action(detail=False, methods=["get"], url_path="summary")
    def summary(self, request):
        queryset = self.get_queryset()

        # =========================
        # FILTERS
        # =========================
        branch = request.GET.get("branch")
        area = request.GET.get("area")
        customer_group = request.GET.get("customer_group")
        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date")
        today = request.GET.get("today")

        if branch:
            queryset = queryset.filter(branch_name_id=branch)

        if area:
            queryset = queryset.filter(area_name_id=area)

        if customer_group:
            queryset = queryset.filter(customer_group_id=customer_group)

        if today == "1":
            queryset = queryset.filter(created_at__date=timezone.now().date())

        if from_date:
            queryset = queryset.filter(created_at__date__gte=from_date)

        if to_date:
            queryset = queryset.filter(created_at__date__lte=to_date)

        # =========================
        # 1️⃣ OVERALL SUMMARY
        # =========================
        overall = queryset.aggregate(
            total_amount_sum=Coalesce(Sum("amount"), Decimal("0.00"), output_field=DecimalField()),
            total_paid_amount_sum=Coalesce(Sum("paid_amount"), Decimal("0.00"), output_field=DecimalField()),
            total_due_amount_sum=Coalesce(Sum("due_amount"), Decimal("0.00"), output_field=DecimalField()),
        )

        # =========================
        # 2️⃣ MODEL NAME WISE (NORMALIZED)
        # =========================
        model_bucket = defaultdict(lambda: {
            "total_amount_sum": Decimal("0.00"),
            "total_paid_amount_sum": Decimal("0.00"),
            "total_due_amount_sum": Decimal("0.00"),
        })

        for row in queryset.values("modelname", "amount", "paid_amount", "due_amount"):
            base_name = normalize_modelname(row["modelname"])

            model_bucket[base_name]["total_amount_sum"] += row["amount"] or Decimal("0.00")
            model_bucket[base_name]["total_paid_amount_sum"] += row["paid_amount"] or Decimal("0.00")
            model_bucket[base_name]["total_due_amount_sum"] += row["due_amount"] or Decimal("0.00")

        modelname_wise = [
            {
                "modelname": name,
                "total_amount_sum": data["total_amount_sum"],
                "total_paid_amount_sum": data["total_paid_amount_sum"],
                "total_due_amount_sum": data["total_due_amount_sum"],
            }
            for name, data in model_bucket.items()
        ]

        # =========================
        # 3️⃣ RECEIVED BY WISE
        # =========================
        received_by_wise = list(
            queryset
            .values("received_by_id", "received_by__name")
            .annotate(
                total_amount_sum=Coalesce(Sum("amount"), Decimal("0.00"), output_field=DecimalField()),
                total_paid_amount_sum=Coalesce(Sum("paid_amount"), Decimal("0.00"), output_field=DecimalField()),
                total_due_amount_sum=Coalesce(Sum("due_amount"), Decimal("0.00"), output_field=DecimalField()),
            )
            .order_by("received_by__name")
        )

        # =========================
        # FINAL RESPONSE
        # =========================
        return Response({
            "success": True,
            "status": 200,
            "message": "Transection summary retrieved successfully",
            "error": None,
            "data": {
                "overall": overall,
                "modelname_wise": modelname_wise,
                "received_by_wise": received_by_wise,
            }
        })

# from django.db.models import Sum, Value, DecimalField
# from django.db.models.functions import Coalesce
# from rest_framework.views import APIView
# from rest_framework.response import Response

# from .models import Transection


# class TransectionSummaryView(APIView):
#     """
#     Model-name wise & received_by wise total amount, paid amount, due amount summary
#     """

#     def get(self, request):

#         MODEL_PREFIXES = [
#             "Customer Type Behavior",
#             "Installment Payment",
#             "Loan Down Payment",
#             "Daily Saving",
#             "Loan Behavior",
#             "Loan Disbursement",
#         ]

#         base_qs = Transection.objects.filter(
#             is_deleted=False,
#             status=True
#         )

#         response_data = {}

#         for prefix in MODEL_PREFIXES:

#             # -----------------------------
#             # Model name wise TOTAL summary
#             # -----------------------------
#             model_qs = base_qs.filter(modelname__startswith=prefix)

#             model_summary = model_qs.aggregate(
#                 total_amount=Coalesce(
#                     Sum("amount"),
#                     Value(0),
#                     output_field=DecimalField()
#                 ),
#                 total_paid_amount=Coalesce(
#                     Sum("paid_amount"),
#                     Value(0),
#                     output_field=DecimalField()
#                 ),
#                 total_due_amount=Coalesce(
#                     Sum("due_amount"),
#                     Value(0),
#                     output_field=DecimalField()
#                 ),
#             )

#             # --------------------------------
#             # received_by wise breakdown
#             # --------------------------------
#             received_by_summary = (
#                 model_qs
#                 .values("received_by")
#                 .annotate(
#                     total_amount=Coalesce(
#                         Sum("amount"),
#                         Value(0),
#                         output_field=DecimalField()
#                     ),
#                     total_paid_amount=Coalesce(
#                         Sum("paid_amount"),
#                         Value(0),
#                         output_field=DecimalField()
#                     ),
#                     total_due_amount=Coalesce(
#                         Sum("due_amount"),
#                         Value(0),
#                         output_field=DecimalField()
#                     ),
#                 )
#                 .order_by("received_by")
#             )

#             response_data[prefix] = {
#                 "summary": model_summary,
#                 "received_by_breakdown": list(received_by_summary),
#             }

#         return Response({
#             "success": True,
#             "data": response_data
#         })


# from django.db import models
# from django.db.models import Q, Sum
# from django.utils import timezone
# from decimal import Decimal

# from rest_framework import status, permissions
# from rest_framework_simplejwt.authentication import JWTAuthentication

# from .models import Transection
# from users.models import Users
# from .serializers import TransectionSerializer


# from django.db import models
# from django.db.models import Q, Sum
# from django.utils import timezone
# from decimal import Decimal

# from rest_framework import status, permissions
# from rest_framework_simplejwt.authentication import JWTAuthentication

# from .models import Transection
# from users.models import Users
# from .serializers import TransectionSerializer


# class TransectionViewSet(BaseViews):
#     queryset = Transection.objects.all()
#     serializer_class = TransectionSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     model_name = Transection
#     methods = ["list", "retrieve", "create", "update", "partial_update", "destroy"]

#     def list(self, request, *args, **kwargs):

#         # ===============================
#         # AUTH CHECK
#         # ===============================
#         auth_header = request.headers.get("Authorization")
#         if not auth_header or not auth_header.startswith("Bearer "):
#             return self.generate_response(
#                 False, status.HTTP_401_UNAUTHORIZED, "authorization_header_missing"
#             )

#         access_token = auth_header.split(" ")[1]

#         try:
#             payload = decode_jwt(access_token)
#             user_id = payload.get("user_id") or payload.get("id")
#             if not user_id:
#                 raise Exception("Invalid token payload")
#         except Exception as e:
#             return self.generate_response(
#                 False, status.HTTP_401_UNAUTHORIZED, "invalid_token", error=str(e)
#             )

#         # ===============================
#         # USER CONTEXT
#         # ===============================
#         try:
#             user = Users.objects.get(id=user_id)
#         except Users.DoesNotExist:
#             return self.generate_response(
#                 False, status.HTTP_401_UNAUTHORIZED, "user_not_found"
#             )

#         branch = getattr(user, "branch", None)
#         area = getattr(user, "area", None)
#         customer_group = getattr(user, "customer_group", None)

#         # ===============================
#         # MULTI BRANCH IDS
#         # ===============================
#         multibranch_ids = []
#         if hasattr(user, "mult_branch") and user.mult_branch.exists():
#             for mb in user.mult_branch.all():
#                 multibranch_ids.extend(
#                     mb.multi_branch.values_list("id", flat=True)
#                 )
#         multibranch_ids = multibranch_ids or None

#         # ===============================
#         # BASE QUERYSET
#         # ===============================
#         queryset = self.filter_queryset(self.get_queryset())

#         # ===============================
#         # INSTALLMENT SPECIAL LOGIC
#         # ===============================
#         if self.model_name.__name__ == "Installment" and area:
#             queryset = queryset.filter(
#                 area_name=area,
#                 installment_date=timezone.localdate()
#             )

#         # ===============================
#         # BRANCH / MULTI-BRANCH FILTER
#         # ===============================
#         if branch:
#             allowed_branch_ids = [branch.id]
#         elif multibranch_ids:
#             allowed_branch_ids = multibranch_ids
#         else:
#             allowed_branch_ids = []

#         branch_fields = [
#             f for f in self.model_name._meta.get_fields()
#             if "branch" in f.name
#         ]

#         if allowed_branch_ids:
#             if self.model_name.__name__ == "Branch":
#                 queryset = queryset.filter(id__in=allowed_branch_ids)
#             elif branch_fields:
#                 q = Q()
#                 for f in branch_fields:
#                     if isinstance(f, (models.ForeignKey, models.OneToOneField)):
#                         q |= Q(**{f"{f.name}_id__in": allowed_branch_ids})
#                     elif isinstance(f, models.ManyToManyField):
#                         q |= Q(**{f"{f.name}__id__in": allowed_branch_ids})
#                 if q:
#                     queryset = queryset.filter(q)

#         # ===============================
#         # AREA FILTER (ALL MODELS)
#         # ===============================
#         if area:
#             area_fields = [
#                 f for f in self.model_name._meta.get_fields()
#                 if "area" in f.name.lower()
#             ]
#             if self.model_name.__name__ == "Area":
#                 queryset = queryset.filter(id=area.id)
#             elif area_fields:
#                 q = Q()
#                 for f in area_fields:
#                     if isinstance(f, (models.ForeignKey, models.OneToOneField)):
#                         q |= Q(**{f"{f.name}_id": area.id})
#                     elif isinstance(f, models.ManyToManyField):
#                         q |= Q(**{f"{f.name}__id": area.id})
#                 if q:
#                     queryset = queryset.filter(q)

#         # ===============================
#         # CUSTOMER GROUP (UNCHANGED)
#         # ===============================
#         if customer_group is not None:
#             try:
#                 queryset = queryset.filter(customer_group=customer_group)
#             except Exception:
#                 pass

#         # ==========================================================
#         # TRANSECTION SUMMARY (FIXED & OPTIMIZED)
#         # ==========================================================
#         # NOTE:
#         # Using iregex so that:
#         # - case insensitive
#         # - space / typo safe
#         # - future-proof
#         # ==========================================================

#         summary_qs = queryset.filter(
#             modelname__iregex=r"(loan|installment|saving)"
#         )

#         overall = summary_qs.aggregate(
#             total_amount=Sum("amount"),
#             total_paid_amount=Sum("paid_amount"),
#             total_due_amount=Sum("due_amount"),
#         )

#         overall_summary = {
#             "total_amount": overall["total_amount"] or Decimal("0.00"),
#             "total_paid_amount": overall["total_paid_amount"] or Decimal("0.00"),
#             "total_due_amount": overall["total_due_amount"] or Decimal("0.00"),
#         }

#         received_by_rows = (
#             summary_qs
#             .values("received_by__id", "received_by__username")
#             .annotate(
#                 paid_amount=Sum("paid_amount"),
#                 due_amount=Sum("due_amount"),
#             )
#             .order_by("received_by__username")
#         )

#         received_by_summary = [
#             {
#                 "received_by_id": row["received_by__id"],
#                 "received_by": row["received_by__username"] or "Unknown",
#                 "paid_amount": row["paid_amount"] or Decimal("0.00"),
#                 "due_amount": row["due_amount"] or Decimal("0.00"),
#             }
#             for row in received_by_rows
#         ]

#         # ===============================
#         # RESPONSE
#         # ===============================
#         limit = request.GET.get("limit")

#         if limit is None:
#             serializer = self.get_serializer(queryset, many=True)
#             return self.generate_response(
#                 True,
#                 status.HTTP_200_OK,
#                 "Transection Data retrieved successfully",
#                 data={
#                     "results": serializer.data,
#                     "summary": {
#                         "overall": overall_summary,
#                         "received_by": received_by_summary,
#                     }
#                 }
#             )

#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response({
#                 "results": serializer.data,
#                 "summary": {
#                     "overall": overall_summary,
#                     "received_by": received_by_summary,
#                 }
#             })


# from django.db import models
# from django.db.models import Q, Sum
# from django.utils import timezone
# from decimal import Decimal

# from rest_framework import status, permissions
# from rest_framework_simplejwt.authentication import JWTAuthentication

# from .models import Transection
# from users.models import Users
# from .serializers import TransectionSerializer


# class TransectionViewSet(BaseViews):
#     queryset = Transection.objects.all()
#     serializer_class = TransectionSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     model_name = Transection
#     methods = ["list", "retrieve", "create", "update", "partial_update", "destroy"]

#     def list(self, request, *args, **kwargs):

#         # ===============================
#         # AUTH CHECK
#         # ===============================
#         auth_header = request.headers.get("Authorization")
#         if not auth_header or not auth_header.startswith("Bearer "):
#             return self.generate_response(
#                 False, status.HTTP_401_UNAUTHORIZED, "authorization_header_missing"
#             )

#         access_token = auth_header.split(" ")[1]

#         try:
#             payload = decode_jwt(access_token)
#             user_id = payload.get("user_id") or payload.get("id")
#             if not user_id:
#                 raise Exception("Invalid token payload")
#         except Exception as e:
#             return self.generate_response(
#                 False, status.HTTP_401_UNAUTHORIZED, "invalid_token", error=str(e)
#             )

#         # ===============================
#         # USER CONTEXT
#         # ===============================
#         try:
#             user = Users.objects.get(id=user_id)
#         except Users.DoesNotExist:
#             return self.generate_response(
#                 False, status.HTTP_401_UNAUTHORIZED, "user_not_found"
#             )

#         branch = getattr(user, "branch", None)
#         area = getattr(user, "area", None)
#         customer_group = getattr(user, "customer_group", None)

#         # ===============================
#         # MULTI BRANCH IDS
#         # ===============================
#         multibranch_ids = []
#         if hasattr(user, "mult_branch") and user.mult_branch.exists():
#             for mb in user.mult_branch.all():
#                 multibranch_ids.extend(
#                     mb.multi_branch.values_list("id", flat=True)
#                 )
#         multibranch_ids = multibranch_ids or None

#         # ===============================
#         # BASE QUERYSET
#         # ===============================
#         queryset = self.filter_queryset(self.get_queryset())

#         # ===============================
#         # INSTALLMENT SPECIAL LOGIC
#         # ===============================
#         if self.model_name.__name__ == "Installment" and area:
#             queryset = queryset.filter(
#                 area_name=area,
#                 installment_date=timezone.localdate()
#             )

#         # ===============================
#         # BRANCH / MULTI-BRANCH FILTER
#         # ===============================
#         if branch:
#             allowed_branch_ids = [branch.id]
#         elif multibranch_ids:
#             allowed_branch_ids = multibranch_ids
#         else:
#             allowed_branch_ids = []

#         branch_fields = [
#             f for f in self.model_name._meta.get_fields()
#             if "branch" in f.name
#         ]

#         if allowed_branch_ids:
#             if self.model_name.__name__ == "Branch":
#                 queryset = queryset.filter(id__in=allowed_branch_ids)
#             elif branch_fields:
#                 q = Q()
#                 for f in branch_fields:
#                     if isinstance(f, (models.ForeignKey, models.OneToOneField)):
#                         q |= Q(**{f"{f.name}_id__in": allowed_branch_ids})
#                     elif isinstance(f, models.ManyToManyField):
#                         q |= Q(**{f"{f.name}__id__in": allowed_branch_ids})
#                 if q:
#                     queryset = queryset.filter(q)

#         # ===============================
#         # AREA FILTER (ALL MODELS)
#         # ===============================
#         if area:
#             area_fields = [
#                 f for f in self.model_name._meta.get_fields()
#                 if "area" in f.name.lower()
#             ]
#             if self.model_name.__name__ == "Area":
#                 queryset = queryset.filter(id=area.id)
#             elif area_fields:
#                 q = Q()
#                 for f in area_fields:
#                     if isinstance(f, (models.ForeignKey, models.OneToOneField)):
#                         q |= Q(**{f"{f.name}_id": area.id})
#                     elif isinstance(f, models.ManyToManyField):
#                         q |= Q(**{f"{f.name}__id": area.id})
#                 if q:
#                     queryset = queryset.filter(q)

#         # ===============================
#         # CUSTOMER GROUP (UNCHANGED)
#         # ===============================
#         if customer_group is not None:
#             try:
#                 queryset = queryset.filter(customer_group=customer_group)
#             except Exception:
#                 pass

#         # ==========================================================
#         #  SUMMARY QUERYSET (MODELNAME SAFE)
#         # ==========================================================
#         summary_qs = queryset.filter(
#             modelname__iregex=r"(loan|installment|saving)"
#         )

#         # ===============================
#         # OVERALL SUMMARY
#         # ===============================
#         overall = summary_qs.aggregate(
#             total_amount=Sum("amount"),
#             total_paid_amount=Sum("paid_amount"),
#             total_due_amount=Sum("due_amount"),
#         )

#         overall_summary = {
#             "total_amount": overall["total_amount"] or Decimal("0.00"),
#             "total_paid_amount": overall["total_paid_amount"] or Decimal("0.00"),
#             "total_due_amount": overall["total_due_amount"] or Decimal("0.00"),
#         }

#         # ===============================
#         # MODELNAME-WISE SUMMARY 
#         # ===============================
#         model_wise_rows = (
#             summary_qs
#             .values("modelname")
#             .annotate(
#                 total_amount=Sum("amount"),
#                 total_paid_amount=Sum("paid_amount"),
#                 total_due_amount=Sum("due_amount"),
#             )
#             .order_by("modelname")
#         )

#         model_wise_summary = [
#             {
#                 "modelname": row["modelname"],
#                 "total_amount": row["total_amount"] or Decimal("0.00"),
#                 "total_paid_amount": row["total_paid_amount"] or Decimal("0.00"),
#                 "total_due_amount": row["total_due_amount"] or Decimal("0.00"),
#             }
#             for row in model_wise_rows
#         ]

#         # ===============================
#         # RECEIVED-BY SUMMARY
#         # ===============================
#         received_by_rows = (
#             summary_qs
#             .values("received_by__id", "received_by__username")
#             .annotate(
#                 paid_amount=Sum("paid_amount"),
#                 due_amount=Sum("due_amount"),
#             )
#             .order_by("received_by__username")
#         )

#         received_by_summary = [
#             {
#                 "received_by_id": row["received_by__id"],
#                 "received_by": row["received_by__username"] or "Unknown",
#                 "paid_amount": row["paid_amount"] or Decimal("0.00"),
#                 "due_amount": row["due_amount"] or Decimal("0.00"),
#             }
#             for row in received_by_rows
#         ]

#         # ===============================
#         # RESPONSE
#         # ===============================
#         limit = request.GET.get("limit")

#         if limit is None:
#             serializer = self.get_serializer(queryset, many=True)
#             return self.generate_response(
#                 True,
#                 status.HTTP_200_OK,
#                 "Transection Data retrieved successfully",
#                 data={
#                     "results": serializer.data,
#                     "summary": {
#                         "overall": overall_summary,
#                         "model_wise": model_wise_summary,
#                         "received_by": received_by_summary,
#                     }
#                 }
#             )

#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response({
#                 "results": serializer.data,
#                 "summary": {
#                     "overall": overall_summary,
#                     "model_wise": model_wise_summary,
#                     "received_by": received_by_summary,
#                 }
#             })



# from django.db import models
# from django.db.models import Q, Sum
# from django.utils import timezone
# from decimal import Decimal

# from rest_framework import status, permissions
# from rest_framework_simplejwt.authentication import JWTAuthentication

# from .models import Transection
# from users.models import Users
# from .serializers import TransectionSerializer


# class TransectionViewSet(BaseViews):
#     queryset = Transection.objects.all()
#     serializer_class = TransectionSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     model_name = Transection
#     methods = ["list", "retrieve", "create", "update", "partial_update", "destroy"]

#     def list(self, request, *args, **kwargs):

#         # ===============================
#         # AUTH
#         # ===============================
#         auth_header = request.headers.get("Authorization")
#         if not auth_header or not auth_header.startswith("Bearer "):
#             return self.generate_response(
#                 False,
#                 status.HTTP_401_UNAUTHORIZED,
#                 "authorization_header_missing"
#             )

#         access_token = auth_header.split(" ")[1]

#         try:
#             payload = decode_jwt(access_token)
#             user_id = payload.get("user_id") or payload.get("id")
#             if not user_id:
#                 raise Exception("Invalid token payload")
#         except Exception as e:
#             return self.generate_response(
#                 False,
#                 status.HTTP_401_UNAUTHORIZED,
#                 "invalid_token",
#                 error=str(e)
#             )

#         # ===============================
#         # USER CONTEXT
#         # ===============================
#         try:
#             user = Users.objects.get(id=user_id)
#         except Users.DoesNotExist:
#             return self.generate_response(
#                 False,
#                 status.HTTP_401_UNAUTHORIZED,
#                 "user_not_found"
#             )

#         branch = getattr(user, "branch", None)
#         area = getattr(user, "area", None)
#         customer_group = getattr(user, "customer_group", None)

#         # ===============================
#         # MULTI BRANCH
#         # ===============================
#         multibranch_ids = []
#         if hasattr(user, "mult_branch") and user.mult_branch.exists():
#             for mb in user.mult_branch.all():
#                 multibranch_ids.extend(
#                     mb.multi_branch.values_list("id", flat=True)
#                 )
#         multibranch_ids = multibranch_ids or None

#         # ===============================
#         # BASE QUERYSET
#         # ===============================
#         queryset = self.filter_queryset(self.get_queryset())

#         # ===============================
#         # INSTALLMENT SPECIAL LOGIC (UNCHANGED)
#         # ===============================
#         if self.model_name.__name__ == "Installment" and area:
#             queryset = queryset.filter(
#                 area_name=area,
#                 installment_date=timezone.localdate()
#             )

#         # ===============================
#         # BRANCH / MULTI-BRANCH FILTER
#         # ===============================
#         if branch:
#             allowed_branch_ids = [branch.id]
#         elif multibranch_ids:
#             allowed_branch_ids = multibranch_ids
#         else:
#             allowed_branch_ids = []

#         branch_fields = [
#             f for f in self.model_name._meta.get_fields()
#             if "branch" in f.name
#         ]

#         if allowed_branch_ids:
#             if self.model_name.__name__ == "Branch":
#                 queryset = queryset.filter(id__in=allowed_branch_ids)
#             elif branch_fields:
#                 q = Q()
#                 for f in branch_fields:
#                     if isinstance(f, (models.ForeignKey, models.OneToOneField)):
#                         q |= Q(**{f"{f.name}_id__in": allowed_branch_ids})
#                     elif isinstance(f, models.ManyToManyField):
#                         q |= Q(**{f"{f.name}__id__in": allowed_branch_ids})
#                 if q:
#                     queryset = queryset.filter(q)

#         # ===============================
#         # AREA FILTER (UNCHANGED)
#         # ===============================
#         if area:
#             area_fields = [
#                 f for f in self.model_name._meta.get_fields()
#                 if "area" in f.name.lower()
#             ]
#             if self.model_name.__name__ == "Area":
#                 queryset = queryset.filter(id=area.id)
#             elif area_fields:
#                 q = Q()
#                 for f in area_fields:
#                     if isinstance(f, (models.ForeignKey, models.OneToOneField)):
#                         q |= Q(**{f"{f.name}_id": area.id})
#                     elif isinstance(f, models.ManyToManyField):
#                         q |= Q(**{f"{f.name}__id": area.id})
#                 if q:
#                     queryset = queryset.filter(q)

#         # ===============================
#         # CUSTOMER GROUP (UNCHANGED)
#         # ===============================
#         if customer_group is not None:
#             try:
#                 queryset = queryset.filter(customer_group=customer_group)
#             except Exception:
#                 pass

#         # ==================================================
#         #  MODELNAME + RECEIVED_BY SUMMARY (NEW LOGIC)
#         # ==================================================

#         TARGET_MODELS = [
#             "Customer Type Behavior",
#             "Installment Payment",
#             "Loan Down Payment",
#             "Daily Saving",
#             "Loan Behavior",
#             "Loan Disbursement",
#         ]

#         target_qs = queryset.filter(modelname__in=TARGET_MODELS)

#         # ---------- MODELNAME WISE ----------
#         modelname_summary_rows = (
#             target_qs
#             .values("modelname")
#             .annotate(
#                 total_amount=Sum("amount"),
#                 total_paid_amount=Sum("paid_amount"),
#                 total_due_amount=Sum("due_amount"),
#             )
#             .order_by("modelname")
#         )

#         modelname_summary = [
#             {
#                 "modelname": row["modelname"],
#                 "total_amount": row["total_amount"] or Decimal("0.00"),
#                 "total_paid_amount": row["total_paid_amount"] or Decimal("0.00"),
#                 "total_due_amount": row["total_due_amount"] or Decimal("0.00"),
#             }
#             for row in modelname_summary_rows
#         ]

#         # ---------- MODELNAME + RECEIVED_BY ----------
#         model_received_by_rows = (
#             target_qs
#             .values("modelname", "received_by__id", "received_by__username")
#             .annotate(
#                 total_amount=Sum("amount"),
#                 total_paid_amount=Sum("paid_amount"),
#                 total_due_amount=Sum("due_amount"),
#             )
#             .order_by("modelname", "received_by__username")
#         )

#         model_received_by_summary = [
#             {
#                 "modelname": row["modelname"],
#                 "received_by": row["received_by__username"] or "Unknown",
#                 "total_amount": row["total_amount"] or Decimal("0.00"),
#                 "total_paid_amount": row["total_paid_amount"] or Decimal("0.00"),
#                 "total_due_amount": row["total_due_amount"] or Decimal("0.00"),
#             }
#             for row in model_received_by_rows
#         ]

#         # ===============================
#         # RESPONSE
#         # ===============================
#         limit = request.GET.get("limit")

#         if limit is None:
#             serializer = self.get_serializer(queryset, many=True)
#             return self.generate_response(
#                 True,
#                 status.HTTP_200_OK,
#                 "Transection Data retrieved successfully",
#                 data={
#                     "results": serializer.data,
#                     "summary": {
#                         "modelname_wise": modelname_summary,
#                         "modelname_received_by_wise": model_received_by_summary,
#                     }
#                 }
#             )

#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response({
#                 "results": serializer.data,
#                 "summary": {
#                     "modelname_wise": modelname_summary,
#                     "modelname_received_by_wise": model_received_by_summary,
#                 }
#             })


