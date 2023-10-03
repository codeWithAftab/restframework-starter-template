from django.db import models
from django.contrib.auth.models import AbstractUser
from account.managers import CustomUserManager


# Create your models here.
class CustomUser(AbstractUser):
    uid = models.CharField(max_length=255, null=True, blank=True) # add unique=True
    username = models.CharField(verbose_name="username",max_length=122, unique=True,null=True,blank=True)
    email = models.EmailField(verbose_name='email', unique=True)
    is_email_verified = models.BooleanField(default=False)
    first_name  = models.CharField(max_length=20, null=True, blank=True)
    last_name  = models.CharField(max_length=20, null=True, blank=True)
    address_line_1 = models.CharField(max_length=200, null=True, blank=True)
    address_line_2 = models.CharField(max_length=200, null=True, blank=True)
    zip_code = models.CharField(max_length=6, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    categories = models.ManyToManyField("master.category")
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.uid or ''