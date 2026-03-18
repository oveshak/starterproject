from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'units', views.UnitViewSet, basename='units')
router.register(r'categorys', views.CategoryViewSet, basename='categories')
router.register(r'brands', views.BrandViewSet, basename='brands')
router.register(r'warrantys', views.WarrantyViewSet, basename='warranties')
router.register(r'sellingpricegroups', views.SellingPriceGroupViewSet, basename='selling-price-groups')
router.register(r'products', views.ProductViewSet, basename='products')
router.register(r'variations', views.VariationViewSet, basename='variations')
router.register(r'branchproductstocks', views.BranchProductStockViewSet, basename='branch-product-stocks')
router.register(r'unicks', views.UnickViewSet, basename='unicks')
router.register(r'variationattributes', views.VariationAttributeViewSet, basename='variationattributes')
router.register(r'variationattributevalues', views.VariationAttributeValueViewSet, basename='variationattributevalues')
urlpatterns = [
    # path("admin/variations/", views.AdminVariationByProductView.as_view(), name="admin-variations"),
    path("admin/variations/", views.AdminVariationByProductView.as_view()),
    path("admin/unickkeys/", views.AdminUnickByVariationView.as_view()),


    path('', include(router.urls)),
]