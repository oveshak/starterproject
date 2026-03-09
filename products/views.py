from django.shortcuts import render

# Create your views here.
from rest_framework import permissions, authentication
from globalapp.views import BaseViews
from .models import Product, Unit, Category, Brand, Warranty, SellingPriceGroup, Variation, BranchProductStock, unick
from .serializers import (
    ProductSerializer, UnickSerializer, UnitSerializer, CategorySerializer, BrandSerializer,
    WarrantySerializer, SellingPriceGroupSerializer, VariationSerializer,
    BranchProductStockSerializer
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication
from .models import Variation
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication

from products.models import Variation
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication

from products.models import Variation
from .models import BranchProductStock


class UnitViewSet(BaseViews):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = Unit
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy", "soft_delete", "change_status", "restore_soft_deleted"]

class CategoryViewSet(BaseViews):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = Category
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy", "soft_delete", "change_status", "restore_soft_deleted"]

class BrandViewSet(BaseViews):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = Brand
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy", "soft_delete", "change_status", "restore_soft_deleted"]

class WarrantyViewSet(BaseViews):
    queryset = Warranty.objects.all()
    serializer_class = WarrantySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = Warranty
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy", "soft_delete", "change_status", "restore_soft_deleted"]

class SellingPriceGroupViewSet(BaseViews):
    queryset = SellingPriceGroup.objects.all()
    serializer_class = SellingPriceGroupSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = SellingPriceGroup
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy", "soft_delete", "change_status", "restore_soft_deleted"]

class ProductViewSet(BaseViews):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = Product
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy", "soft_delete", "change_status", "restore_soft_deleted"]

class UnickViewSet(BaseViews):
    queryset = unick.objects.all()
    serializer_class = UnickSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = unick
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy", "soft_delete", "change_status", "restore_soft_deleted"]

class VariationViewSet(BaseViews):
    queryset = Variation.objects.all()
    serializer_class = VariationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = Variation
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy", "soft_delete", "change_status", "restore_soft_deleted"]
    
class BranchProductStockViewSet(BaseViews):
    queryset = BranchProductStock.objects.all()
    serializer_class = BranchProductStockSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model_name = BranchProductStock
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy", "soft_delete", "change_status", "restore_soft_deleted"]
    def get_queryset(self):
        qs = super().get_queryset()
        product_id = self.request.query_params.get("product")

        if product_id:
            qs = qs.filter(product_name_id=product_id)

        return qs
    




class AdminVariationByProductView(APIView):
    """
    Admin JS only (NO JWT)
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        product_id = request.GET.get("product")

        qs = Variation.objects.none()
        if product_id:
            qs = Variation.objects.filter(product_name_id=product_id)

        data = [
            {
                "id": v.id,
                "name": v.name or f"Variation {v.id}",
                "isunck": v.isunck   #  MUST ADD THIS

            }
            for v in qs
        ]
        return Response(data)
    




# class AdminUnickByVariationView(APIView):
#     authentication_classes = [SessionAuthentication]
#     permission_classes = [AllowAny]

#     def get(self, request):
#         variation_id = request.GET.get("variation")
#         stock_id = request.GET.get("stock_id")  # edit support

#         if not variation_id:
#             return Response([])

#         variation = Variation.objects.filter(id=variation_id).first()
#         if not variation:
#             return Response([])

#         # 🔹 variation অনুযায়ী unick
#         qs = variation.unickkey.all()

#         # 🔹 অন্য branch-এ already used unick বাদ
#         used = BranchProductStock.objects.filter(
#             product_variation_id=variation_id
#         )

#         if stock_id:
#             used = used.exclude(id=stock_id)

#         used_ids = used.values_list("unickkey__id", flat=True)

#         available = qs.exclude(id__in=used_ids)

#         return Response([
#             {"id": u.id, "text": str(u)}
#             for u in available
#         ])



# class AdminUnickByVariationView(APIView):
#     authentication_classes = [SessionAuthentication]
#     permission_classes = [AllowAny]

#     def get(self, request):
#         variation_id = request.GET.get("variation")
#         stock_id = request.GET.get("stock_id")  # edit support

#         if not variation_id:
#             return Response([])

#         variation = Variation.objects.filter(id=variation_id).first()
#         if not variation:
#             return Response([])

#         # ✅ 1) only this variation's unicks
#         qs = variation.unickkey.all()

#         # ✅ 2) exclude unicks already assigned to OTHER branches (same variation)
#         used = BranchProductStock.objects.filter(product_variation_id=variation_id)

#         # edit page হলে current stock বাদ
#         if stock_id:
#             used = used.exclude(id=stock_id)

#         used_ids = used.values_list("unickkey__id", flat=True)

#         available = qs.exclude(id__in=used_ids)

#         return Response([{"id": u.id, "text": str(u)} for u in available])



# from products.models import Variation
# from .models import BranchProductStock

# class AdminUnickByVariationView(APIView):
#     authentication_classes = [SessionAuthentication]
#     permission_classes = [AllowAny]

#     def get(self, request):
#         variation_id = request.GET.get("variation")
#         stock_id = request.GET.get("stock_id")

#         if not variation_id:
#             return Response([])

#         variation = Variation.objects.filter(id=variation_id).first()
#         if not variation:
#             return Response([])

#         qs = variation.unickkey.all()

#         used = BranchProductStock.objects.filter(
#             product_variation_id=variation_id
#         )

#         if stock_id:
#             used = used.exclude(id=stock_id)

#         used_ids = used.values_list("unickkey__id", flat=True)

#         available = qs.exclude(id__in=used_ids)

#         return Response([
#             {"id": u.id, "text": str(u)}
#             for u in available
#         ])





# class AdminUnickByVariationView(APIView):
#     authentication_classes = [SessionAuthentication]
#     permission_classes = [AllowAny]

#     def get(self, request):
#         variation_id = request.GET.get("variation")
#         stock_id = request.GET.get("stock_id")

#         if not variation_id:
#             return Response([])

#         variation = Variation.objects.filter(id=variation_id).first()
#         if not variation:
#             return Response([])

#         # ✅ STEP 1: ONLY this variation's unickkeys
#         qs = variation.unickkey.all()

#         # ✅ STEP 2: find used unickkeys for this variation (other branches)
#         used = BranchProductStock.objects.filter(
#             product_variation_id=variation_id
#         )

#         # edit page support (current stock er gulo বাদ)
#         if stock_id:
#             used = used.exclude(id=stock_id)

#         used_ids = used.values_list("unickkey__id", flat=True)

#         # ✅ STEP 3: exclude already-used unickkeys
#         available = qs.exclude(id__in=used_ids)

#         return Response([
#             {"id": u.id, "text": str(u)}
#             for u in available
#         ])



class AdminUnickByVariationView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        variation_id = request.GET.get("variation")
        stock_id = request.GET.get("stock_id")

        print(" API HIT: AdminUnickByVariationView")
        print("variation_id =", variation_id)
        print("stock_id =", stock_id)

        if not variation_id:
            print(" No variation_id")
            return Response([])

        variation = Variation.objects.filter(id=variation_id).first()
        print("variation object =", variation)

        if not variation:
            print(" Variation not found")
            return Response([])

        qs = variation.unickkey.all()
        print("🔹 variation.unickkey.count() =", qs.count())

        used = BranchProductStock.objects.filter(
            product_variation_id=variation_id
        )

        if stock_id:
            used = used.exclude(id=stock_id)

        used_ids = list(used.values_list("unickkey__id", flat=True))
        print("🔹 used_ids =", used_ids)

        available = qs.exclude(id__in=used_ids)
        print(" available.count() =", available.count())

        return Response([
            {"id": u.id, "text": str(u)}
            for u in available
        ])


