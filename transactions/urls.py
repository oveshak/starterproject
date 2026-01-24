from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'purchases', views.PurchaseViewSet, basename='purchases')
router.register(r'purchaseitems', views.PurchaseItemViewSet, basename='purchase-items')
router.register(r'purchasereturns', views.PurchaseReturnViewSet, basename='purchase-returns')
router.register(r'sales', views.SaleViewSet, basename='sales')
router.register(r'saleitems', views.SaleItemViewSet, basename='sale-items')
router.register(r'payments', views.PaymentViewSet, basename='payments')
router.register(r'cheques', views.ChequeViewSet, basename='cheques')
router.register(r'affiliatecommissions', views.AffiliateCommissionViewSet, basename='affiliate-commissions')
router.register(r'loantypes', views.LoanTypeViewSet, basename='loan-types')
router.register(r'installmenttypes', views.InstallmentTypeViewSet, basename='installment-types')
router.register(r'dailysavings', views.DailySavingViewSet, basename='dailysavings')
router.register(r'transections', views.TransectionViewSet, basename='transections')
router.register(r'branchaccounts', views.BranchAccountViewSet, basename='branchaccounts')
router.register(r'installments', views.InstallmentViewSet, basename='installments')
router.register(r'loans', views.LoanViewSet, basename='loans')
router.register(
    r'downpayments',
    views.DownPaymentViewSet,
    basename='downpayment'
)
urlpatterns = [

    path("_admin/variations/", views.AdminVariationByProductView.as_view()),
    path('', include(router.urls)),
]