from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Customer, CustomerGroup, Contact, CustomerType

@admin.register(CustomerGroup)
class CustomerGroupAdmin(ModelAdmin):
    list_display = ("id", "name", "group_leader_user", "created_at")
    search_fields = ("id","name", "group_leader_user__email", "group_leader_user__name")
    list_filter = ("created_at",)
    raw_id_fields = ("group_leader_user",)
    filter_horizontal = ("members",)  # M2M সিলেক্ট করা সহজ হবে

@admin.register(Contact)
class ContactAdmin(ModelAdmin):
    list_display = ("id", "type", "name", "email", "phone", "customer_group", "branch_name", "created_at")  # removed updated_at, is_active
    search_fields = ("id","name", "email", "phone", "customer_group__name", "branch_name__name")
    list_filter = ("type", "customer_group", "branch_name", "created_at")  # removed is_active, updated_at
    raw_id_fields = ("customer_group", "branch_name")

@admin.register(CustomerType)
class CustomerTypeAdmin(ModelAdmin):
    list_display = ['name', 'behaviour_type']
    search_fields = ["id",'name', 'behaviour_type']
    list_filter = ['behaviour_type']

@admin.register(Customer)
class CustomerAdmin(ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "father_husband_name",
        "mobile_number",
        "secondary_mobile_number",
        "guarantor",
        "nid_number",
        "branch_name",
        "account_balance",
        "created_at"
    )
    search_fields = (
        "id",
        "full_name",
        "father_husband_name",
        "mobile_number",
        "secondary_mobile_number",
        "nid_number",
        "guarantor__name",
        "branch_name__name"
    )
    list_filter = (
        "branch_name",
        "created_at"
    )
    raw_id_fields = (
        "guarantor",
        "branch_name"
    )
    readonly_fields = ("account_balance",)