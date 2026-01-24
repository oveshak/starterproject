from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Area, MultiBranch, Users, Roles, Branch


@admin.register(Roles)
class RolesAdmin(ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    filter_horizontal = ['menu']  # For many-to-many Group relation


@admin.register(Users)
class UsersAdmin(ModelAdmin):
    list_display = [
        'name', 'email', 'username', 'phone_number', 'branch', 'area',
        'roles', 'customer_group', 'get_mult_branch',
        'is_admin', 'is_staff', 'is_verified', 'status',
    ]
    search_fields = ['name', 'email', 'username', 'phone_number']
    list_filter = ['is_admin', 'is_staff', 'is_verified', 'status', 'branch', 'roles', 'area', 'mult_branch']

    # ✅ এখানে method টাকে read-only হিসেবে যোগ করলাম
    readonly_fields = ['last_login', 'created_at', 'get_mult_branch']

    filter_horizontal = ('mult_branch', 'groups', 'user_permissions')

    fieldsets = (
        (None, {
            'fields': (
                'email', 'username', 'name', 'phone_number', 'password', 'profile_picture',
                'roles', 'branch', 'area',
                'mult_branch',          # editable M2M
                'get_mult_branch',      # read-only summary (now allowed)
                'customer_group',
                'address', 'descriptions',
                'nid_number', 'nid_front', 'nid_back',
            )
        }),
        ('Permissions', {
            'fields': ('is_admin', 'is_staff', 'is_verified', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Status', {
            'fields': ('status', 'created_at', 'is_deleted', 'last_login')
        }),
    )

    def save_model(self, request, obj, form, change):
        raw_password = form.cleaned_data.get("password")
        if raw_password and not raw_password.startswith('pbkdf2_'):
            obj.set_password(raw_password)
        super().save_model(request, obj, form, change)

    def get_mult_branch(self, obj):
        return ", ".join(str(b) for b in obj.mult_branch.all())
    get_mult_branch.short_description = "Multi Branches"

@admin.register(Area)

class AreaAdmin(ModelAdmin):
    list_display = ['name', 'address']   # area_staf M2M, তাই list_display তে ডাইরেক্ট দেখানো যাবে না
    search_fields = ['name', 'address', 'area_staf__email']
    # list_filter = ['manager']  # Area model এ manager নাই, তাই বাদ দিলাম

    # M2M ফিল্ড admin এ দেখাতে চাইলে কাস্টম মেথড বানাতে হবে
    def get_area_stafs(self, obj):
        return ", ".join([user.email for user in obj.area_staf.all()])
    get_area_stafs.short_description = "Area Staff"



@admin.register(MultiBranch)
class MultiBranchAdmin(ModelAdmin):
    # address ফিল্ড নেই বলে সরিয়ে দিলাম, বদলে কাস্টম কলাম যোগ করেছি
    list_display = ('title', 'branch_count', 'branch_list', 'address_list')
    search_fields = ('title',)
    filter_horizontal = ('multi_branch',)   # M2M UI টা সহজ হবে

    def get_queryset(self, request):
        # N+1 এড়াতে prefetch
        qs = super().get_queryset(request)
        return qs.prefetch_related('multi_branch')

    def branch_count(self, obj):
        return obj.multi_branch.count()
    branch_count.short_description = "Branches"

    def branch_list(self, obj):
        # Branch মডেলে যে নাম/কোড ফিল্ড আছে সেটি ব্যবহার করো (নিচে 'name' ধরে দেখানো)
        return ", ".join(b.name for b in obj.multi_branch.all())
    branch_list.short_description = "Branch Names"

    def address_list(self, obj):
        """
        Branch মডেলে address-টাইপ ফিল্ডের নামটা ঠিক করে দাও:
        - যদি 'address' থাকে: b.address
        - যদি 'full_address' থাকে: b.full_address
        - যদি 'location' থাকে: b.location
        নিচে কয়েকটা অপশন থেকে প্রথম পাওয়া ভ্যালু নিলাম।
        """
        parts = []
        for b in obj.multi_branch.all():
            addr = getattr(b, 'address', None) or getattr(b, 'full_address', None) or getattr(b, 'location', None)
            if addr:
                parts.append(str(addr))
        return ", ".join(parts)
    address_list.short_description = "Addresses"

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'phone', 'manager']  # total_area M2M, তাই ডাইরেক্ট রাখা যাবে না
    search_fields = ['name', 'address', 'phone', 'manager__email', 'total_area__name']
    list_filter = ['manager']

    # total_area দেখানোর জন্য কাস্টম মেথড
    def get_total_areas(self, obj):
        return ", ".join([area.name for area in obj.total_area.all()])
    get_total_areas.short_description = "Total Areas"

