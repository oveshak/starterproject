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







# class AdminVariationByProductView(APIView):
#     authentication_classes = [SessionAuthentication]
#     permission_classes = [AllowAny]

#     def get(self, request):
#         product_id = request.GET.get("product")
#         qs = Variation.objects.filter(product_name_id=product_id) if product_id else Variation.objects.none()

#         return Response([
#             {"id": v.id, "name": v.name}
#             for v in qs
#         ])

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
class AdminVariationByProductView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        product_id = request.GET.get("product")

        qs = Variation.objects.filter(product_name_id=product_id) if product_id else Variation.objects.none()

        return Response([
            {
                "id": v.id,
                "name": v.name,
                "isunck": v.isunck,
            }
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
#         today = request.GET.get("today")

#         if branch:
#             queryset = queryset.filter(branch_name_id=branch)

#         if area:
#             queryset = queryset.filter(area_name_id=area)

#         if customer_group:
#             queryset = queryset.filter(customer_group_id=customer_group)

#         if today == "1":
#             queryset = queryset.filter(created_at__date=timezone.now().date())

#         if from_date:
#             queryset = queryset.filter(created_at__date__gte=from_date)

#         if to_date:
#             queryset = queryset.filter(created_at__date__lte=to_date)

#         # =========================
#         # 1️⃣ OVERALL SUMMARY
#         # =========================
#         overall = queryset.aggregate(
#             total_amount_sum=Coalesce(Sum("amount"), Decimal("0.00"), output_field=DecimalField()),
#             total_paid_amount_sum=Coalesce(Sum("paid_amount"), Decimal("0.00"), output_field=DecimalField()),
#             total_due_amount_sum=Coalesce(Sum("due_amount"), Decimal("0.00"), output_field=DecimalField()),
#         )

#         # =========================
#         # 2️⃣ MODEL NAME WISE (NORMALIZED)
#         # =========================
#         model_bucket = defaultdict(lambda: {
#             "total_amount_sum": Decimal("0.00"),
#             "total_paid_amount_sum": Decimal("0.00"),
#             "total_due_amount_sum": Decimal("0.00"),
#         })

#         for row in queryset.values("modelname", "amount", "paid_amount", "due_amount"):
#             base_name = normalize_modelname(row["modelname"])

#             model_bucket[base_name]["total_amount_sum"] += row["amount"] or Decimal("0.00")
#             model_bucket[base_name]["total_paid_amount_sum"] += row["paid_amount"] or Decimal("0.00")
#             model_bucket[base_name]["total_due_amount_sum"] += row["due_amount"] or Decimal("0.00")

#         modelname_wise = [
#             {
#                 "modelname": name,
#                 "total_amount_sum": data["total_amount_sum"],
#                 "total_paid_amount_sum": data["total_paid_amount_sum"],
#                 "total_due_amount_sum": data["total_due_amount_sum"],
#             }
#             for name, data in model_bucket.items()
#         ]

#         # =========================
#         # 3️⃣ RECEIVED BY WISE
#         # =========================
#         received_by_wise = list(
#             queryset
#             .values("received_by_id", "received_by__name")
#             .annotate(
#                 total_amount_sum=Coalesce(Sum("amount"), Decimal("0.00"), output_field=DecimalField()),
#                 total_paid_amount_sum=Coalesce(Sum("paid_amount"), Decimal("0.00"), output_field=DecimalField()),
#                 total_due_amount_sum=Coalesce(Sum("due_amount"), Decimal("0.00"), output_field=DecimalField()),
#             )
#             .order_by("received_by__name")
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



from decimal import Decimal
from collections import defaultdict

from django.db.models import Sum, DecimalField
from django.db.models.functions import Coalesce
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response

# make sure Installment is imported
# from .models import Transection, Installment


from decimal import Decimal
from collections import defaultdict
from datetime import datetime

from django.db.models import Sum, DecimalField
from django.db.models.functions import Coalesce
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions

# make sure these imports exist in your file
# from .models import Transection, Installment
# from .serializers import TransectionSerializer
# from rest_framework_simplejwt.authentication import JWTAuthentication


from decimal import Decimal
from collections import defaultdict
from datetime import datetime

from django.db.models import Sum, DecimalField
from django.db.models.functions import Coalesce
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions

# make sure these imports exist in your file
# from .models import Transection, Installment
# from .serializers import TransectionSerializer
# from rest_framework_simplejwt.authentication import JWTAuthentication


def safe_decimal(val):
    return val or Decimal("0.00")


def normalize_bucket_name(modelname):
    if not modelname:
        return "Others"

    name = str(modelname).strip()

    if "Customer Type Behavior" in name:
        return "Customer Type Behavior"
    elif "Daily Saving" in name:
        return "Daily Saving"
    elif "Loan Behavior" in name:
        return "Loan Behavior"
    elif "Loan Disbursement" in name:
        return "Loan Disbursement"
    elif "Loan Down Payment" in name:
        return "Loan Down Payment | Loan"

    return "Others"


def build_pdf_summary_rows(
    tran_qs,
    installment_qs,
    tran_group_id_field,
    tran_group_name_field,
    ins_group_id_field,
    ins_group_name_field,
    label_key,
):
    rows = defaultdict(
        lambda: {
            f"{label_key}_id": None,
            label_key: None,
            "Customer Type Behavior": Decimal("0.00"),
            "Daily Saving": Decimal("0.00"),
            "Loan Behavior": Decimal("0.00"),
            "Loan Disbursement": Decimal("0.00"),
            "Loan Down Payment | Loan": Decimal("0.00"),
            "instalment pay": Decimal("0.00"),
            "total_amount_sum": Decimal("0.00"),
        }
    )

    # Transection side
    for row in tran_qs.values(
        tran_group_id_field,
        tran_group_name_field,
        "modelname",
        "amount",
    ):
        gid = row.get(tran_group_id_field)
        gname = row.get(tran_group_name_field)
        bucket_name = normalize_bucket_name(row.get("modelname"))
        amount = safe_decimal(row.get("amount"))

        rows[gid][f"{label_key}_id"] = gid
        rows[gid][label_key] = gname
        rows[gid]["total_amount_sum"] += amount

        if bucket_name in rows[gid]:
            rows[gid][bucket_name] += amount

    # Installment side
    for row in installment_qs.values(
        ins_group_id_field,
        ins_group_name_field,
    ).annotate(
        total_installment_pay_sum=Coalesce(
            Sum("installment_pay"),
            Decimal("0.00"),
            output_field=DecimalField(max_digits=18, decimal_places=2),
        )
    ):
        gid = row.get(ins_group_id_field)
        gname = row.get(ins_group_name_field)
        ins_pay = safe_decimal(row.get("total_installment_pay_sum"))

        rows[gid][f"{label_key}_id"] = gid
        rows[gid][label_key] = gname
        rows[gid]["instalment pay"] = ins_pay

    return list(rows.values())


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
        installment_queryset = Installment.objects.all()

        # =========================
        # GET PARAMS
        # =========================
        branch = request.GET.get("branch")
        area = request.GET.get("area")
        customer_group = request.GET.get("customer_group")
        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date")
        today = request.GET.get("today")

        # =========================
        # PARSE DATE
        # =========================
        parsed_from_date = None
        parsed_to_date = None

        try:
            if from_date:
                parsed_from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
            if to_date:
                parsed_to_date = datetime.strptime(to_date, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {
                    "success": False,
                    "status": 400,
                    "message": "Invalid date format. Use YYYY-MM-DD",
                    "error": "Invalid date format",
                    "data": None,
                },
                status=400,
            )

        today_date = timezone.localdate()

        # =========================
        # TRANSECTION FILTERS
        # =========================
        if branch:
            queryset = queryset.filter(branch_name_id=branch)

        if area:
            queryset = queryset.filter(area_name_id=area)

        if customer_group:
            queryset = queryset.filter(customer_group_id=customer_group)

        if today == "1":
            queryset = queryset.filter(created_at__date=today_date)
        else:
            if parsed_from_date:
                queryset = queryset.filter(created_at__date__gte=parsed_from_date)
            if parsed_to_date:
                queryset = queryset.filter(created_at__date__lte=parsed_to_date)

        # =========================
        # INSTALLMENT FILTERS
        # =========================
        if branch:
            installment_queryset = installment_queryset.filter(branch_name_id=branch)

        if area:
            installment_queryset = installment_queryset.filter(area_name_id=area)

        if customer_group:
            installment_queryset = installment_queryset.filter(customergroup_name_id=customer_group)

        if today == "1":
            installment_queryset = installment_queryset.filter(installment_date=today_date)
        else:
            if parsed_from_date:
                installment_queryset = installment_queryset.filter(installment_date__gte=parsed_from_date)
            if parsed_to_date:
                installment_queryset = installment_queryset.filter(installment_date__lte=parsed_to_date)

        # =========================
        # 1. OVERALL TRANSECTION
        # =========================
        overall = queryset.aggregate(
            total_amount_sum=Coalesce(
                Sum("amount"),
                Decimal("0.00"),
                output_field=DecimalField(max_digits=18, decimal_places=2),
            ),
            total_paid_amount_sum=Coalesce(
                Sum("paid_amount"),
                Decimal("0.00"),
                output_field=DecimalField(max_digits=18, decimal_places=2),
            ),
            total_due_amount_sum=Coalesce(
                Sum("due_amount"),
                Decimal("0.00"),
                output_field=DecimalField(max_digits=18, decimal_places=2),
            ),
        )

        # =========================
        # 2. MODEL NAME WISE
        # =========================
        model_bucket = defaultdict(
            lambda: {
                "total_amount_sum": Decimal("0.00"),
                "total_paid_amount_sum": Decimal("0.00"),
                "total_due_amount_sum": Decimal("0.00"),
            }
        )

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
        # 3. RECEIVED BY WISE
        # =========================
        received_by_wise = list(
            queryset.values("received_by_id", "received_by__name")
            .annotate(
                total_amount_sum=Coalesce(
                    Sum("amount"),
                    Decimal("0.00"),
                    output_field=DecimalField(max_digits=18, decimal_places=2),
                ),
                total_paid_amount_sum=Coalesce(
                    Sum("paid_amount"),
                    Decimal("0.00"),
                    output_field=DecimalField(max_digits=18, decimal_places=2),
                ),
                total_due_amount_sum=Coalesce(
                    Sum("due_amount"),
                    Decimal("0.00"),
                    output_field=DecimalField(max_digits=18, decimal_places=2),
                ),
            )
            .order_by("received_by__name")
        )

        # =========================
        # 4. INSTALLMENT OVERALL
        # =========================
        installment_overall = installment_queryset.aggregate(
            total_amount_sum=Coalesce(
                Sum("amount"),
                Decimal("0.00"),
                output_field=DecimalField(max_digits=18, decimal_places=2),
            ),
            total_installment_pay_sum=Coalesce(
                Sum("installment_pay"),
                Decimal("0.00"),
                output_field=DecimalField(max_digits=18, decimal_places=2),
            ),
            total_due_amount_sum=Coalesce(
                Sum("due_amount"),
                Decimal("0.00"),
                output_field=DecimalField(max_digits=18, decimal_places=2),
            ),
        )

        # =========================
        # 5. INSTALLMENT AREA WISE
        # =========================
        installment_area_wise = list(
            installment_queryset.values("area_name_id", "area_name__name")
            .annotate(
                total_amount_sum=Coalesce(
                    Sum("amount"),
                    Decimal("0.00"),
                    output_field=DecimalField(max_digits=18, decimal_places=2),
                ),
                total_installment_pay_sum=Coalesce(
                    Sum("installment_pay"),
                    Decimal("0.00"),
                    output_field=DecimalField(max_digits=18, decimal_places=2),
                ),
                total_due_amount_sum=Coalesce(
                    Sum("due_amount"),
                    Decimal("0.00"),
                    output_field=DecimalField(max_digits=18, decimal_places=2),
                ),
            )
            .order_by("area_name__name")
        )

        # =========================
        # 6. INSTALLMENT CUSTOMER GROUP WISE
        # =========================
        installment_customer_group_wise = list(
            installment_queryset.values("customergroup_name_id", "customergroup_name__name")
            .annotate(
                total_amount_sum=Coalesce(
                    Sum("amount"),
                    Decimal("0.00"),
                    output_field=DecimalField(max_digits=18, decimal_places=2),
                ),
                total_installment_pay_sum=Coalesce(
                    Sum("installment_pay"),
                    Decimal("0.00"),
                    output_field=DecimalField(max_digits=18, decimal_places=2),
                ),
                total_due_amount_sum=Coalesce(
                    Sum("due_amount"),
                    Decimal("0.00"),
                    output_field=DecimalField(max_digits=18, decimal_places=2),
                ),
            )
            .order_by("customergroup_name__name")
        )

        # =========================
        # 7. INSTALLMENT RECEIVED BY WISE
        # =========================
        installment_received_by_wise = list(
            installment_queryset.values("received_by_id", "received_by__name")
            .annotate(
                total_amount_sum=Coalesce(
                    Sum("amount"),
                    Decimal("0.00"),
                    output_field=DecimalField(max_digits=18, decimal_places=2),
                ),
                total_installment_pay_sum=Coalesce(
                    Sum("installment_pay"),
                    Decimal("0.00"),
                    output_field=DecimalField(max_digits=18, decimal_places=2),
                ),
                total_due_amount_sum=Coalesce(
                    Sum("due_amount"),
                    Decimal("0.00"),
                    output_field=DecimalField(max_digits=18, decimal_places=2),
                ),
            )
            .order_by("received_by__name")
        )

        # =========================
        # 8. TODAY INSTALLMENT SUMMARY
        # =========================
        today_installment_summary = Installment.objects.all()

        if branch:
            today_installment_summary = today_installment_summary.filter(branch_name_id=branch)

        if area:
            today_installment_summary = today_installment_summary.filter(area_name_id=area)

        if customer_group:
            today_installment_summary = today_installment_summary.filter(customergroup_name_id=customer_group)

        today_installment_summary = today_installment_summary.filter(installment_date=today_date).aggregate(
            total_amount_sum=Coalesce(
                Sum("amount"),
                Decimal("0.00"),
                output_field=DecimalField(max_digits=18, decimal_places=2),
            ),
            total_installment_pay_sum=Coalesce(
                Sum("installment_pay"),
                Decimal("0.00"),
                output_field=DecimalField(max_digits=18, decimal_places=2),
            ),
            total_due_amount_sum=Coalesce(
                Sum("due_amount"),
                Decimal("0.00"),
                output_field=DecimalField(max_digits=18, decimal_places=2),
            ),
        )

        # =========================
        # 9. PDF SUMMARY AREA WISE
        # =========================
        area_wise_pdf_summary = build_pdf_summary_rows(
            tran_qs=queryset,
            installment_qs=installment_queryset,
            tran_group_id_field="area_name_id",
            tran_group_name_field="area_name__name",
            ins_group_id_field="area_name_id",
            ins_group_name_field="area_name__name",
            label_key="area_name",
        )

        # =========================
        # 10. PDF SUMMARY CUSTOMER GROUP WISE
        # =========================
        customer_group_wise_pdf_summary = build_pdf_summary_rows(
            tran_qs=queryset,
            installment_qs=installment_queryset,
            tran_group_id_field="customer_group_id",
            tran_group_name_field="customer_group__name",
            ins_group_id_field="customergroup_name_id",
            ins_group_name_field="customergroup_name__name",
            label_key="customer_group",
        )

        # =========================
        # 11. PDF SUMMARY BRANCH WISE
        # =========================
        branch_wise_pdf_summary = build_pdf_summary_rows(
            tran_qs=queryset,
            installment_qs=installment_queryset,
            tran_group_id_field="branch_name_id",
            tran_group_name_field="branch_name__name",
            ins_group_id_field="branch_name_id",
            ins_group_name_field="branch_name__name",
            label_key="branch_name",
        )

        return Response(
            {
                "success": True,
                "status": 200,
                "message": "Transection and installment summary retrieved successfully",
                "error": None,
                "data": {
                    "overall": overall,
                    "modelname_wise": modelname_wise,
                    "received_by_wise": received_by_wise,
                    "installment_summary": {
                        "overall": installment_overall,
                        "area_wise": installment_area_wise,
                        "customer_group_wise": installment_customer_group_wise,
                        "received_by_wise": installment_received_by_wise,
                        "today_summary": today_installment_summary,
                    },
                    "pdf_summary": {
                        "area_wise": area_wise_pdf_summary,
                        "customer_group_wise": customer_group_wise_pdf_summary,
                        "branch_wise": branch_wise_pdf_summary,
                    },
                },
            }
        )




# from decimal import Decimal
# from collections import defaultdict
# from io import BytesIO

# from django.db.models import Sum, DecimalField
# from django.db.models.functions import Coalesce
# from django.utils import timezone
# from django.http import HttpResponse
# from rest_framework import permissions
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework_simplejwt.authentication import JWTAuthentication

# from reportlab.lib import colors
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.enums import TA_CENTER, TA_LEFT
# from reportlab.lib.units import mm
# from reportlab.platypus import (
#     SimpleDocTemplate,
#     Table,
#     TableStyle,
#     Paragraph,
#     Spacer,
# )

# # from .models import Transection, Installment
# # from .serializers import TransectionSerializer


# class TransectionViewSet(BaseViews):
#     queryset = Transection.objects.all()
#     serializer_class = TransectionSerializer
#     # authentication_classes = [JWTAuthentication]
#     # permission_classes = [permissions.IsAuthenticated]
#     model_name = Transection
#     methods = ["list", "retrieve", "create", "update", "partial_update", "destroy"]

#     def _get_summary_data(self, request):
#         queryset = self.get_queryset()

#         # =========================
#         # FILTERS
#         # =========================
#         branch = request.GET.get("branch")
#         area = request.GET.get("area")
#         customer_group = request.GET.get("customer_group")
#         from_date = request.GET.get("from_date")
#         to_date = request.GET.get("to_date")
#         today = request.GET.get("today")
#         date = request.GET.get("date")

#         # =========================
#         # TRANSECTION FILTERS
#         # =========================
#         if branch:
#             queryset = queryset.filter(branch_name_id=branch)

#         if area:
#             queryset = queryset.filter(area_name_id=area)

#         if customer_group:
#             queryset = queryset.filter(customer_group_id=customer_group)

#         if date:
#             queryset = queryset.filter(created_at__date=date)
#         elif today in ["1", "true", "True"]:
#             queryset = queryset.filter(created_at__date=timezone.localdate())
#         else:
#             if from_date:
#                 queryset = queryset.filter(created_at__date__gte=from_date)

#             if to_date:
#                 queryset = queryset.filter(created_at__date__lte=to_date)

#         # =========================
#         # INSTALLMENT FILTERS
#         # =========================
#         installment_queryset = Installment.objects.all()

#         if branch:
#             installment_queryset = installment_queryset.filter(branch_name_id=branch)

#         if area:
#             installment_queryset = installment_queryset.filter(area_name_id=area)

#         if customer_group:
#             try:
#                 installment_queryset = installment_queryset.filter(
#                     customer_name__customer_group_id=customer_group
#                 )
#             except Exception:
#                 pass

#         if date:
#             installment_queryset = installment_queryset.filter(installment_date=date)
#         elif today in ["1", "true", "True"]:
#             installment_queryset = installment_queryset.filter(
#                 installment_date=timezone.localdate()
#             )
#         else:
#             if from_date:
#                 installment_queryset = installment_queryset.filter(
#                     installment_date__gte=from_date
#                 )

#             if to_date:
#                 installment_queryset = installment_queryset.filter(
#                     installment_date__lte=to_date
#                 )

#         # =========================
#         # TRANSECTION OVERALL SUMMARY
#         # =========================
#         transection_overall = queryset.aggregate(
#             total_amount_sum=Coalesce(
#                 Sum("amount"),
#                 Decimal("0.00"),
#                 output_field=DecimalField(max_digits=12, decimal_places=2),
#             ),
#             total_paid_amount_sum=Coalesce(
#                 Sum("paid_amount"),
#                 Decimal("0.00"),
#                 output_field=DecimalField(max_digits=12, decimal_places=2),
#             ),
#             total_due_amount_sum=Coalesce(
#                 Sum("due_amount"),
#                 Decimal("0.00"),
#                 output_field=DecimalField(max_digits=12, decimal_places=2),
#             ),
#         )

#         # =========================
#         # TRANSECTION MODEL NAME WISE
#         # =========================
#         model_bucket = defaultdict(lambda: {
#             "total_amount_sum": Decimal("0.00"),
#             "total_paid_amount_sum": Decimal("0.00"),
#             "total_due_amount_sum": Decimal("0.00"),
#         })

#         for row in queryset.values("modelname", "amount", "paid_amount", "due_amount"):
#             base_name = normalize_modelname(row["modelname"])

#             model_bucket[base_name]["total_amount_sum"] += row["amount"] or Decimal("0.00")
#             model_bucket[base_name]["total_paid_amount_sum"] += row["paid_amount"] or Decimal("0.00")
#             model_bucket[base_name]["total_due_amount_sum"] += row["due_amount"] or Decimal("0.00")

#         transection_modelname_wise = [
#             {
#                 "modelname": name,
#                 "total_amount_sum": data["total_amount_sum"],
#                 "total_paid_amount_sum": data["total_paid_amount_sum"],
#                 "total_due_amount_sum": data["total_due_amount_sum"],
#             }
#             for name, data in model_bucket.items()
#         ]

#         # =========================
#         # TRANSECTION RECEIVED BY WISE
#         # =========================
#         transection_received_by_wise = list(
#             queryset
#             .values("received_by_id", "received_by__name")
#             .annotate(
#                 total_amount_sum=Coalesce(
#                     Sum("amount"),
#                     Decimal("0.00"),
#                     output_field=DecimalField(max_digits=12, decimal_places=2),
#                 ),
#                 total_paid_amount_sum=Coalesce(
#                     Sum("paid_amount"),
#                     Decimal("0.00"),
#                     output_field=DecimalField(max_digits=12, decimal_places=2),
#                 ),
#                 total_due_amount_sum=Coalesce(
#                     Sum("due_amount"),
#                     Decimal("0.00"),
#                     output_field=DecimalField(max_digits=12, decimal_places=2),
#                 ),
#             )
#             .order_by("received_by__name")
#         )

#         # =========================
#         # INSTALLMENT OVERALL SUMMARY
#         # =========================
#         installment_overall = installment_queryset.aggregate(
#             total_installment_amount_sum=Coalesce(
#                 Sum("amount"),
#                 Decimal("0.00"),
#                 output_field=DecimalField(max_digits=12, decimal_places=2),
#             ),
#             total_installment_pay_sum=Coalesce(
#                 Sum("installment_pay"),
#                 Decimal("0.00"),
#                 output_field=DecimalField(max_digits=12, decimal_places=2),
#             ),
#             total_installment_due_sum=Coalesce(
#                 Sum("due_amount"),
#                 Decimal("0.00"),
#                 output_field=DecimalField(max_digits=12, decimal_places=2),
#             ),
#         )

#         # =========================
#         # INSTALLMENT RECEIVED BY WISE
#         # =========================
#         installment_received_by_wise = list(
#             installment_queryset
#             .values("received_by_id", "received_by__name")
#             .annotate(
#                 total_installment_amount_sum=Coalesce(
#                     Sum("amount"),
#                     Decimal("0.00"),
#                     output_field=DecimalField(max_digits=12, decimal_places=2),
#                 ),
#                 total_installment_pay_sum=Coalesce(
#                     Sum("installment_pay"),
#                     Decimal("0.00"),
#                     output_field=DecimalField(max_digits=12, decimal_places=2),
#                 ),
#                 total_installment_due_sum=Coalesce(
#                     Sum("due_amount"),
#                     Decimal("0.00"),
#                     output_field=DecimalField(max_digits=12, decimal_places=2),
#                 ),
#             )
#             .order_by("received_by__name")
#         )

#         return {
#             "filters": {
#                 "branch": branch or "All",
#                 "area": area or "All",
#                 "customer_group": customer_group or "All",
#                 "date": date or "N/A",
#                 "from_date": from_date or "N/A",
#                 "to_date": to_date or "N/A",
#                 "today": today or "No",
#             },
#             "transection_summary": {
#                 "overall": transection_overall,
#                 "modelname_wise": transection_modelname_wise,
#                 "received_by_wise": transection_received_by_wise,
#             },
#             "installment_summary": {
#                 "overall": installment_overall,
#                 "received_by_wise": installment_received_by_wise,
#             }
#         }

#     @action(detail=False, methods=["get"], url_path="report-summary")
#     def summary(self, request):
#         data = self._get_summary_data(request)

#         return Response({
#             "success": True,
#             "status": 200,
#             "message": "Transection and Installment summary retrieved successfully",
#             "error": None,
#             "data": data
#         })

#     @action(detail=False, methods=["get"], url_path="report-summary-pdf")
#     def summary_pdf(self, request):
#         data = self._get_summary_data(request)

#         buffer = BytesIO()
#         doc = SimpleDocTemplate(
#             buffer,
#             pagesize=A4,
#             rightMargin=20,
#             leftMargin=20,
#             topMargin=20,
#             bottomMargin=20,
#         )

#         styles = getSampleStyleSheet()

#         title_style = ParagraphStyle(
#             name="TitleStyle",
#             parent=styles["Title"],
#             alignment=TA_CENTER,
#             fontSize=18,
#             textColor=colors.HexColor("#0F172A"),
#             spaceAfter=12,
#         )

#         sub_title_style = ParagraphStyle(
#             name="SubTitleStyle",
#             parent=styles["Normal"],
#             alignment=TA_CENTER,
#             fontSize=10,
#             textColor=colors.HexColor("#475569"),
#             spaceAfter=16,
#         )

#         section_style = ParagraphStyle(
#             name="SectionStyle",
#             parent=styles["Heading2"],
#             alignment=TA_LEFT,
#             fontSize=12,
#             textColor=colors.white,
#             backColor=colors.HexColor("#1E3A8A"),
#             spaceBefore=10,
#             spaceAfter=8,
#             leftIndent=6,
#         )

#         normal_style = styles["Normal"]

#         elements = []

#         def money(v):
#             return f"{v}"

#         def add_section_title(text):
#             elements.append(Paragraph(text, section_style))
#             elements.append(Spacer(1, 6))

#         def make_table(data_rows, col_widths=None, header_bg="#1D4ED8"):
#             table = Table(data_rows, colWidths=col_widths, repeatRows=1)
#             table.setStyle(TableStyle([
#                 ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(header_bg)),
#                 ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
#                 ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
#                 ("FONTSIZE", (0, 0), (-1, -1), 9),
#                 ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
#                 ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.HexColor("#EFF6FF")]),
#                 ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
#                 ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#94A3B8")),
#                 ("ALIGN", (1, 1), (-1, -1), "CENTER"),
#                 ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
#                 ("LEFTPADDING", (0, 0), (-1, -1), 8),
#                 ("RIGHTPADDING", (0, 0), (-1, -1), 8),
#                 ("TOPPADDING", (0, 0), (-1, -1), 6),
#                 ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
#             ]))
#             return table

#         elements.append(Paragraph("Transection and Installment Summary Report", title_style))
#         elements.append(
#             Paragraph(
#                 f"Generated on {timezone.localdate()}",
#                 sub_title_style
#             )
#         )

#         # Filters Table
#         add_section_title("Applied Filters")
#         filter_data = [
#             ["Branch", data["filters"]["branch"], "Area", data["filters"]["area"]],
#             ["Customer Group", data["filters"]["customer_group"], "Date", data["filters"]["date"]],
#             ["From Date", data["filters"]["from_date"], "To Date", data["filters"]["to_date"]],
#             ["Today", data["filters"]["today"], "", ""],
#         ]
#         elements.append(make_table(filter_data, col_widths=[90, 140, 90, 140], header_bg="#334155"))
#         elements.append(Spacer(1, 12))

#         # Transection Overall
#         add_section_title("Transection Overall Summary")
#         tran_overall = data["transection_summary"]["overall"]
#         tran_overall_table = [
#             ["Total Amount", "Total Paid", "Total Due"],
#             [
#                 money(tran_overall["total_amount_sum"]),
#                 money(tran_overall["total_paid_amount_sum"]),
#                 money(tran_overall["total_due_amount_sum"]),
#             ]
#         ]
#         elements.append(make_table(tran_overall_table, col_widths=[170, 170, 170]))
#         elements.append(Spacer(1, 12))

#         # Installment Overall
#         add_section_title("Installment Overall Summary")
#         ins_overall = data["installment_summary"]["overall"]
#         ins_overall_table = [
#             ["Installment Amount", "Installment Pay", "Installment Due"],
#             [
#                 money(ins_overall["total_installment_amount_sum"]),
#                 money(ins_overall["total_installment_pay_sum"]),
#                 money(ins_overall["total_installment_due_sum"]),
#             ]
#         ]
#         elements.append(make_table(ins_overall_table, col_widths=[170, 170, 170], header_bg="#0F766E"))
#         elements.append(Spacer(1, 12))

#         # Transection Modelname Wise
#         add_section_title("Transection Modelname Wise")
#         model_rows = [["Model Name", "Total Amount", "Total Paid", "Total Due"]]
#         model_data = data["transection_summary"]["modelname_wise"]

#         if model_data:
#             for item in model_data:
#                 model_rows.append([
#                     str(item["modelname"]),
#                     money(item["total_amount_sum"]),
#                     money(item["total_paid_amount_sum"]),
#                     money(item["total_due_amount_sum"]),
#                 ])
#         else:
#             model_rows.append(["No data found", "-", "-", "-"])

#         elements.append(make_table(model_rows, col_widths=[180, 110, 110, 110]))
#         elements.append(Spacer(1, 12))

#         # Transection Received By Wise
#         add_section_title("Transection Received By Wise")
#         tran_received_rows = [["Received By", "Total Amount", "Total Paid", "Total Due"]]
#         tran_received = data["transection_summary"]["received_by_wise"]

#         if tran_received:
#             for item in tran_received:
#                 tran_received_rows.append([
#                     str(item["received_by__name"] or "N/A"),
#                     money(item["total_amount_sum"]),
#                     money(item["total_paid_amount_sum"]),
#                     money(item["total_due_amount_sum"]),
#                 ])
#         else:
#             tran_received_rows.append(["No data found", "-", "-", "-"])

#         elements.append(make_table(tran_received_rows, col_widths=[180, 110, 110, 110], header_bg="#7C3AED"))
#         elements.append(Spacer(1, 12))

#         # Installment Received By Wise
#         add_section_title("Installment Received By Wise")
#         ins_received_rows = [["Received By", "Installment Amount", "Installment Pay", "Installment Due"]]
#         ins_received = data["installment_summary"]["received_by_wise"]

#         if ins_received:
#             for item in ins_received:
#                 ins_received_rows.append([
#                     str(item["received_by__name"] or "N/A"),
#                     money(item["total_installment_amount_sum"]),
#                     money(item["total_installment_pay_sum"]),
#                     money(item["total_installment_due_sum"]),
#                 ])
#         else:
#             ins_received_rows.append(["No data found", "-", "-", "-"])

#         elements.append(make_table(ins_received_rows, col_widths=[180, 110, 110, 110], header_bg="#BE185D"))
#         elements.append(Spacer(1, 10))

#         elements.append(
#             Paragraph(
#                 "This report is system generated.",
#                 ParagraphStyle(
#                     name="FooterStyle",
#                     parent=normal_style,
#                     alignment=TA_CENTER,
#                     fontSize=9,
#                     textColor=colors.HexColor("#64748B"),
#                     spaceBefore=10,
#                 )
#             )
#         )

#         doc.build(elements)

#         buffer.seek(0)
#         response = HttpResponse(buffer, content_type="application/pdf")
#         response["Content-Disposition"] = 'attachment; filename="transection_summary_report.pdf"'
#         return response


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


