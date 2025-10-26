from django.shortcuts import render

# Create your views here.
from rest_framework import permissions, authentication
from globalapp.views import BaseViews
from .models import DailySaving, Installment, InstallmentType, Loan, LoanType, Purchase, PurchaseItem, PurchaseReturn, Sale, SaleItem, Payment, Cheque, AffiliateCommission, Transection
from .serializers import (
    DailySavingSerializer, InstallmentSerializer, InstallmentTypeSerializer, LoanSerializer, LoanTypeSerializer, PurchaseSerializer, PurchaseItemSerializer, PurchaseReturnSerializer, SaleSerializer,
    SaleItemSerializer, PaymentSerializer, ChequeSerializer, AffiliateCommissionSerializer, TransectionSerializer
)
from rest_framework_simplejwt.authentication import JWTAuthentication
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


from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
from .models import Installment, Loan
from .serializers import InstallmentSerializer, LoanSerializer

class InstallmentViewSet(BaseViews):
    queryset = Installment.objects.all()
    serializer_class = InstallmentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = Installment
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



class TransectionViewSet(BaseViews):
    queryset = Transection.objects.all()
    serializer_class = TransectionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = Transection
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy"]