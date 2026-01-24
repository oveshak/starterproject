# from django.contrib import admin
# from django.urls import path
# from django.shortcuts import render
# from django.apps import apps
# import re

# from globalapp.models import SoftwareAsset
# from solo.admin import SingletonModelAdmin

# # Register models
# admin.site.register(SoftwareAsset, SingletonModelAdmin)
# def activity_log_view(request):
#     historical_models = [
#         model for model in apps.get_models()
#         if model._meta.model_name.startswith("historical")
#     ]

#     all_history = []

#     for hist_model in historical_models:
#         entries = hist_model.objects.all().select_related("history_user")[:200]

#         for e in entries:
#             real_model = None
#             try:
#                 real_model_name = hist_model.__name__.replace("Historical", "")
#                 for m in apps.get_models():
#                     if m.__name__ == real_model_name:
#                         real_model = m
#                         break
#             except Exception:
#                 pass

#             # Default object_repr
#             obj_name = f"{real_model_name if real_model else hist_model.__name__} [ID={e.history_id}]"

#             # Current object safe fetch
#             if real_model:
#                 try:
#                     current_obj = real_model.objects.filter(pk=e.id).first()
#                     if current_obj:
#                         obj_name = str(current_obj)
#                 except Exception:
#                     pass

#             # Model name
#             model_name = (real_model._meta.verbose_name if real_model else hist_model._meta.verbose_name).title()
#             model_name = model_name.replace("Historical ", "")

#             # Branch & User safe fetch
#             try:
#                 user_obj = e.history_user
#                 user_name = getattr(user_obj, "username", "System") or "System"
#                 branch_name = getattr(getattr(user_obj, "branch", None), "name", "Admin Change")
#             except Exception:
#                 user_name = "System"
#                 branch_name = "Admin Change"

#             # Object display logic
#             object_repr = obj_name
#             change_type = e.get_history_type_display()

#             # Update logic
#             if e.history_type == "~":  # Update
#                 prev_entry = hist_model.objects.filter(id=e.id, history_date__lt=e.history_date).order_by('-history_date').first()
#                 if prev_entry:
#                     try:
#                         prev_data = str(prev_entry)
#                         # Only show Before → After if value changed
#                         if prev_data != obj_name:
#                             object_repr = f"Before: {prev_data} → After: {obj_name}"
#                         else:
#                             object_repr = obj_name
#                     except Exception:
#                         object_repr = obj_name



#             # Append entry
#             all_history.append({
#                 "model": model_name,
#                 "date": e.history_date,
#                 "user": user_name,
#                 "branch": branch_name,
#                 "change": change_type,
#                 "object_repr": object_repr,
#             })

#     # Sort by date descending
#     all_history.sort(key=lambda x: x["date"], reverse=True)

#     context = dict(
#         admin.site.each_context(request),
#         title="Activity Log",
#         history_list=all_history,
#     )
#     return render(request, "admin/activity_log.html", context)


# # Append custom URL to admin
# original_get_urls = admin.site.get_urls

# def get_urls():
#     urls = original_get_urls()
#     custom_urls = [
#         path("activity-log/", admin.site.admin_view(activity_log_view), name="activity-log"),
#     ]
#     return custom_urls + urls

# admin.site.get_urls = get_urls


from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.apps import apps
import re

from globalapp.models import SoftwareAsset
from solo.admin import SingletonModelAdmin

# Register models
admin.site.register(SoftwareAsset, SingletonModelAdmin)

def activity_log_view(request):
    historical_models = [
        model for model in apps.get_models()
        if model._meta.model_name.startswith("historical")
    ]

    all_history = []

    for hist_model in historical_models:
        entries = hist_model.objects.all().select_related("history_user")[:200]

        for e in entries:
            real_model = None
            try:
                real_model_name = hist_model.__name__.replace("Historical", "")
                for m in apps.get_models():
                    if m.__name__ == real_model_name:
                        real_model = m
                        break
            except Exception:
                pass

            # ✅ instead of str(e), use history_id safely
            obj_name = f"{real_model_name if real_model else hist_model.__name__} [ID={e.history_id}]"

            # Try original object, but safe
            if real_model:
                try:
                    original_obj = real_model.objects.filter(pk=e.id).first()
                    if original_obj:
                        obj_name = str(original_obj)
                except Exception:
                    pass  # keep fallback

            # Pretty model name
            if real_model:
                model_name = real_model._meta.verbose_name.title()
            else:
                model_name = hist_model._meta.verbose_name.title()
            model_name = model_name.replace("Historical ", "")

            all_history.append({
                "model": model_name,
                "date": e.history_date,
                "user": getattr(e.history_user, "username", "System") or "System",
                "branch": getattr(getattr(e.history_user, "branch", None), "name", "Admin Change"),
                "change": e.get_history_type_display(),
                "object_repr": obj_name,
            })

    all_history.sort(key=lambda x: x["date"], reverse=True)

    context = dict(
        admin.site.each_context(request),
        title="Activity Log",
        history_list=all_history,
    )
    return render(request, "admin/activity_log.html", context)




# ✅ Append custom URL to admin
original_get_urls = admin.site.get_urls


def get_urls():
    urls = original_get_urls()
    custom_urls = [
        path("activity-log/", admin.site.admin_view(activity_log_view), name="activity-log"),
    ]
    return custom_urls + urls


admin.site.get_urls = get_urls
