from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.core.validators import RegexValidator
import uuid
from users.managers import CustomUserManager


class Users(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, validators=[RegexValidator(regex=r'^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$')])
    created_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name']
    
    objects = CustomUserManager()
    
    def __str__(self):
        return f"Name: {self.name}, Email: {self.email}"
    