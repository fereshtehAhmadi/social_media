from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, phone, password=None, password2=None):
        if not first_name or not last_name or not phone:
            raise ValueError('please fill in all fields!!')

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, phone, password=None, password2=None):
    
        user = self.create_user(
            username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            phone=phone,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser):
    username = models.CharField(max_length=200, unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=11, unique=True, 
                            validators=[RegexValidator(regex=r'09(\d{9})$')])
    cover = models.ImageField(blank=True, default='profile.png', upload_to='profile/')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', ]

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    follower = models.ManyToManyField(User, related_name='follower', blank=True)
    following = models.ManyToManyField(User, related_name='following', blank=True)
    request = models.ManyToManyField(User, related_name='request', blank=True)
    
    def __str__(self):
        return self.user.username


class Validation(models.Model):
    phone = phone = models.CharField(max_length=11, unique=True, 
                            validators=[RegexValidator(regex=r'09(\d{9})$')])
    code = models.CharField(max_length=4)
    
    def __str__(self):
        return self.phone
