from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group, PermissionsMixin, Permission
from django.utils import timezone

# from contacts.models import CustomerGroup
from globalapp.models import Common
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator
from ckeditor.fields import RichTextField
from simple_history.models import HistoricalRecords


class Roles(Common):
    name = models.CharField(
        max_length=15,
        unique=True,
        verbose_name="Role Name"
    )
    menu = models.ManyToManyField(
        Group,
        verbose_name="Menu",
        blank=True,
        related_name="user_groups"
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"

    def __str__(self):
        return f"{self.name}"


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )

        user.set_password(password)
        user.joined_at = timezone.now()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# class Area(Common):
#     name = models.CharField(
#         max_length=100,
#         verbose_name="Area Name"
#     )
  
#     address = models.TextField(verbose_name="Address")
  
#     area_staf = models.ManyToManyField(
#         'Users',
#         blank=True,
#         verbose_name="AreaStaf"
#     )
   
#     history = HistoricalRecords()

#     class Meta:
#         verbose_name = "Area"
#         verbose_name_plural = "Areas"

#     def __str__(self):
#         return self.name


# class Branch(Common):
#     name = models.CharField(
#         max_length=100,
#         verbose_name="Branch Name"
#     )
#     address = models.TextField(verbose_name="Address")
#     phone = models.CharField(
#         max_length=20,
#         verbose_name="Phone"
#     )
#     manager = models.ForeignKey(
#         'Users',
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name='managed_branch',
#         verbose_name="Manager"
#     )
#     total_area = models.ManyToManyField(
#         'Area',
#         blank=True,
#         verbose_name="TotalArea"
#     )
#     history = HistoricalRecords()

#     class Meta:
#         verbose_name = "Branch"
#         verbose_name_plural = "Branches"

#     def __str__(self):
#         return self.name

class Area(Common):
    name = models.CharField(max_length=100, verbose_name="Area Name")
    address = models.TextField(verbose_name="Address")
    area_staf = models.ManyToManyField('Users', blank=True, related_name='staffed_areas',verbose_name="AreaStaf")

    # Branch এর সাথে একদিকের FK
    parent_branch = models.ForeignKey(
        "Branch",
        on_delete=models.CASCADE,
        related_name="areas",
        null=True,
        blank=True,
        verbose_name="Branch"
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Area"
        verbose_name_plural = "Areas"

    def __str__(self):
        return self.name


class Branch(Common):
    name = models.CharField(max_length=100, verbose_name="Branch Name")
    address = models.TextField(verbose_name="Address")
    phone = models.CharField(max_length=20, verbose_name="Phone")
    manager = models.ForeignKey(
        'Users',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_branches',
        verbose_name="Manager"
    )

    # Branch ↔ Area many-to-many
    total_area = models.ManyToManyField(
        'Area',
        blank=True,
        related_name="branches",
        verbose_name="TotalArea"
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Branch"
        verbose_name_plural = "Branches"

    def __str__(self):
        return self.name


class MultiBranch(Common):
    title = models.CharField(max_length=300)
    multi_branch = models.ManyToManyField(Branch)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "MultiBranch"
        verbose_name_plural = "MultiBranch"

    def __str__(self):
        return self.title

class Users(AbstractBaseUser, PermissionsMixin):
    status = models.BooleanField(
        default=True,
        null=True,
        blank=True,
        verbose_name="Active Status"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        blank=True,
        null=True,
        verbose_name="Created At"
    )
    descriptions = RichTextField(
        null=True,
        blank=True,
        verbose_name="Descriptions"
    )
    is_deleted = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name="Deleted"
    )
    name = models.CharField(
        max_length=100,
        default=None,
        null=True,
        blank=True,
        verbose_name="Full Name"
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Email Address"
    )
    username = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        blank=True,
        verbose_name="Username"
    )
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        null=True,
        blank=True,
        unique=True,
        verbose_name="Phone Number"
    )
    profile_picture = models.ImageField(
        upload_to='products/thumbnails/',
        null=True,
        blank=True,
        verbose_name="Profile Picture"
    )
    is_admin = models.BooleanField(
        default=False,
        verbose_name="Admin Status"
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name="Staff Status"
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name="Verified"
    )
    address = models.TextField(
        max_length=400,
        default=None,
        null=True,
        blank=True,
        verbose_name="Address"
    )
    roles = models.ForeignKey(
        Roles,
        on_delete=models.CASCADE,
        related_name="user_roles",
        null=True,
        blank=True,
        verbose_name="Role"
    )
    nid_number = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        verbose_name="NID Number"
    )
    nid_front = models.ImageField(
        upload_to='nid/front/',
        null=True,
        blank=True,
        verbose_name="NID Front Image"
    )
    nid_back = models.ImageField(
        upload_to='nid/back/',
        null=True,
        blank=True,
        verbose_name="NID Back Image"
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        verbose_name="Branch"
    )
    area = models.ForeignKey(
        Area,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='userss_area',  # <-- unique reverse name
        verbose_name="Area"
    )
    mult_branch=models.ManyToManyField(MultiBranch ,
        blank=True,
        related_name='userss_mult_branch',  # <-- unique reverse name
        verbose_name="MultiBranch")
    
    customer_group = models.IntegerField(
    null=True,
    blank=True
)
    history = HistoricalRecords()

    USERNAME_FIELD = 'email'
    objects = MyUserManager() 

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def get_all_permissions(self, obj=None):
        if self.is_admin:
            permissions = Permission.objects.values_list('content_type__app_label', 'codename')
        else:
            permissions = set()
            if self.roles:
                for menu in self.roles.menu.all():
                    permissions.update(menu.permissions.values_list('content_type__app_label', 'codename'))
        return {"{}.{}".format(ct, name) for ct, name in permissions}

    def has_perm(self, perm, obj=None):
        if self.is_admin:
            return True
        if perm in self.get_all_permissions():
            return True
        return False

    def has_module_perms(self, app_label):
        if self.is_admin:
            return True
        return any(perm.split('.')[0] == app_label for perm in self.get_all_permissions())

    def __str__(self):
        return self.name if self.name else self.email


