from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
    )

from django.conf import settings
# Create your models here.

class UserManager(BaseUserManager):


    def create_user(self, email, password=None, **extra_fields):
        """create and save a new user"""
        if not email:
            raise ValueError('The email field is not provided!')
        user = self.model(email= self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    
    def create_superuser(self, email, password):
        
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)

        return user
        


class User(AbstractBaseUser, PermissionsMixin):
    """custom user model that supports using email instead of username"""

    email = models.EmailField(max_length=250, unique=True)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default= False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Tag(models.Model):
    """tags to be used for a recipe"""
    name = models.CharField(max_length = 250)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name='tags')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length = 250)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = 'ingredients'
        )
    
    def __str__(self):
        return self.name


class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    time_minutes = models.IntegerField()
    title = models.CharField(max_length = 250)
    price = models.DecimalField(max_digits = 5, decimal_places = 2)
    link = models.CharField(max_length = 250, blank = True)
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title