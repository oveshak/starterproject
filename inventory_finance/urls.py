from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'stocktransfers', views.StockTransferViewSet, basename='stock-transfers')
router.register(r'stockadjustments', views.StockAdjustmentViewSet, basename='stock-adjustments')
router.register(r'daybooks', views.DaybookViewSet, basename='daybooks')
router.register(r'expenses', views.ExpenseViewSet, basename='expenses')
router.register(r'vendorcheques', views.VendorChequeViewSet, basename='vendor-cheques')
router.register(r'repairrequests', views.RepairRequestViewSet, basename='repair-requests')

urlpatterns = [
    path('', include(router.urls)),
]