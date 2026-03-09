# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Area, Branch, Users

@receiver(post_save, sender=Area)
def update_area_staff(sender, instance, created, **kwargs):
    if created:  # Only add staff if the area is newly created
        if instance.parent_branch:
            # Add the users associated with the branch to the area staff
            branch_users = instance.parent_branch.users.all()
            instance.area_staf.add(*branch_users)  # Add all branch users to the area staff
            instance.save()
        else:
            print(f"Area {instance.name} has no parent branch, no staff added.")
    else:
        print(f"Area {instance.name} already exists, no new staff added.")
