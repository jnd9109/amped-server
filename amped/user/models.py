from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, password=None, email=None):
        user = self.model()
        user.is_superuser = False
        user.email = email
        user.admin = False

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, password, email=None):
        user = self.create_user(
            password=password
        )
        user.is_superuser = True
        user.email = email
        user.admin = True
        user.save()
        return user

    def get_queryset(self, *args, **kwargs):
        qs = super(UserManager, self).get_queryset(*args, **kwargs)
        return qs


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=128, unique=True, db_index=True, blank=True, null=True)
    first_name = models.CharField(max_length=128, blank=True, null=True)
    last_name = models.CharField(max_length=128, blank=True, null=True)
    introduction = models.TextField(blank=True, null=True)
    profession = models.CharField(max_length=128, blank=True, null=True)
    skills = models.ManyToManyField('skill.Skill', related_name='users', blank=True)
    profile_image = models.ImageField(blank=True, null=True)
    phone = models.CharField(max_length=48, blank=True, null=True)
    website = models.CharField(max_length=128, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True, null=True)
    active = models.BooleanField(default=True, help_text="Active account")
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return f'[{self.id}] {self.email}'

