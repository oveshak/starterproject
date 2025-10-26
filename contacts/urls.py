from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'customergroups', views.CustomerGroupViewSet, basename='customer-groups')
router.register(r'contacts', views.ContactViewSet, basename='contacts')
router.register(r'customertypes', views.CustomerTypeViewSet, basename='customertypes')
router.register(r'customers', views.CustomerViewSet, basename='customers')

urlpatterns = [
    path('', include(router.urls)),
]