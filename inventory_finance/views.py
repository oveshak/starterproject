from django.shortcuts import render
# Create your views here.
from rest_framework import permissions, authentication
from globalapp.views import BaseViews
from .models import StockTransfer, StockAdjustment, Daybook, Expense, VendorCheque, RepairRequest
from .serializers import (
    StockTransferSerializer, StockAdjustmentSerializer, DaybookSerializer,
    ExpenseSerializer, VendorChequeSerializer, RepairRequestSerializer
)
from rest_framework_simplejwt.authentication import JWTAuthentication
class StockTransferViewSet(BaseViews):
    queryset = StockTransfer.objects.all()
    serializer_class = StockTransferSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = StockTransfer
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy", "soft_delete", "change_status", "restore_soft_deleted"]

    # def create(self, request, *args, **kwargs):
    #     print("📌 Incoming data:", request.data)  # debug
    #     return super().create(request, *args, **kwargs)

class StockAdjustmentViewSet(BaseViews):
    queryset = StockAdjustment.objects.all()
    serializer_class = StockAdjustmentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = StockAdjustment
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy", "soft_delete", "change_status", "restore_soft_deleted"]


class DaybookViewSet(BaseViews):
    queryset = Daybook.objects.all()
    serializer_class = DaybookSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = Daybook
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy", "soft_delete", "change_status", "restore_soft_deleted"]

class ExpenseViewSet(BaseViews):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = Expense
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy", "soft_delete", "change_status", "restore_soft_deleted"]

class VendorChequeViewSet(BaseViews):
    queryset = VendorCheque.objects.all()
    serializer_class = VendorChequeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = VendorCheque
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy", "soft_delete", "change_status", "restore_soft_deleted"]

class RepairRequestViewSet(BaseViews):
    queryset = RepairRequest.objects.all()
    serializer_class = RepairRequestSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = RepairRequest
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy", "soft_delete", "change_status", "restore_soft_deleted"]
