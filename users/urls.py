from django.urls import path
from users import views
from rest_framework.routers import DefaultRouter,SimpleRouter
router = SimpleRouter()
router.register(r'areas', views.AreaViewSet, basename='areas')
router.register(r'branchs', views.BranchViewSet, basename='branches')
router.register(r'multibranchs', views.MultiBranchViewSet, basename='multibranchs')
router.register(r'roles', views.RoleViewSet, basename='roles')
router.register(r'groups', views.GroupViewSet, basename='groups')
router.register(r'permissions', views.PermissionViewSet, basename='permissions')
router.register(r'users', views.UserViewSet, basename='users')
urlpatterns = [
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/update-profile/', views.UserViewSet.as_view({'patch': 'update_profile'}), name='update_profile'),
]
urlpatterns+= router.urls