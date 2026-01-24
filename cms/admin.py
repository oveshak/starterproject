# from django.contrib import admin
# from unfold.admin import ModelAdmin
# from .models import (
#     Button, BannerItem, Banner, BannerLMS,
#     CounterItem, FacilitiesItem, SpecialCta,
#     Page, FAQ, Testimonial, Blog
# )

# @admin.register(Button)
# class ButtonAdmin(ModelAdmin):
#     list_display = ("id", "title", "link", "created_at")
#     search_fields = ("title",)
#     list_filter = ("created_at",)

# @admin.register(BannerItem)
# class BannerItemAdmin(ModelAdmin):
#     list_display = ("id", "title", "order", "created_at")
#     search_fields = ("title",)
#     list_filter = ("created_at",)

# @admin.register(Banner)
# class BannerAdmin(ModelAdmin):
#     list_display = ("id", "title", "created_at")
#     search_fields = ("title",)
#     list_filter = ("created_at",)

# @admin.register(BannerLMS)
# class BannerLMSAdmin(ModelAdmin):
#     list_display = ("id", "title", "created_at")
#     search_fields = ("title",)
#     list_filter = ("created_at",)

# @admin.register(CounterItem)
# class CounterItemAdmin(ModelAdmin):
#     list_display = ("id", "title", "number", "created_at")
#     search_fields = ("title",)
#     list_filter = ("created_at",)

# @admin.register(FacilitiesItem)
# class FacilitiesItemAdmin(ModelAdmin):
#     list_display = ("id", "title", "created_at")
#     search_fields = ("title",)
#     list_filter = ("created_at",)

# @admin.register(SpecialCta)
# class SpecialCtaAdmin(ModelAdmin):
#     list_display = ("id", "title", "button_text")
#     search_fields = ("title", "button_text")
#     list_filter = ()

# @admin.register(Page)
# class PageAdmin(ModelAdmin):
#     list_display = ("id", "name", "slug", "pub_status", "created_at")
#     search_fields = ("name", "slug")
#     list_filter = ("pub_status", "created_at")

# @admin.register(FAQ)
# class FAQAdmin(ModelAdmin):
#     list_display = ("id", "question", "slug", "created_at")
#     search_fields = ("question", "slug")
#     list_filter = ("created_at",)

# @admin.register(Testimonial)
# class TestimonialAdmin(ModelAdmin):
#     list_display = ("id", "author", "slug", "rating", "created_at")
#     search_fields = ("author", "slug")
#     list_filter = ("created_at",)

# @admin.register(Blog)
# class BlogAdmin(ModelAdmin):
#     list_display = ("id", "title", "slug", "pub_status", "created_at")
#     search_fields = ("title", "slug")
#     list_filter = ("pub_status", "created_at")
