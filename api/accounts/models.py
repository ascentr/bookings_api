from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, name, username, email, password=None):
        if not email:
            raise ValueError('user must have a valid email')

        if not username:
            raise ValueError('user must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, name, username, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            name=name,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    VENDOR = 1
    CUSTOMER = 2

    ROLE_CHOICE = (
        (VENDOR, 'Vendor'),
        (CUSTOMER, 'Customer'),
    )

    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=12, blank=True)
    role = models.PositiveIntegerField(choices=ROLE_CHOICE, blank=True,
                                       null=True)  # change to required when migrating for deployment
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_supderadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def get_role(self):
        if self.role == 1:
            user_role = 'Vendor'
        elif self.role == 2:
            user_role = 'Customer'
        return user_role

    # def has_module_perms(self, app_label):
    #     return True


    #
    # def get_profile(self):
    #     try:
    #         return self.userprofile  # Access the related UserProfile instance
    #     except userprofile.DoesNotExist:
    #         return None  # Return None if the profile doesn't exist
