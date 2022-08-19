from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, User
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
    bio = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
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


class Validation(models.Model):
    phone = phone = models.CharField(max_length=11, unique=True,
                            validators=[RegexValidator(regex=r'09(\d{9})$')])
    code = models.CharField(max_length=4)
    
    def __str__(self):
        return self.phone


class Request(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_request')
    request = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request')
    
    def get_user_info(self):
        user_dict = vars(self.user)
        return {"id": user_dict["id"], "username": user_dict["username"]}

    def get_requester_info(self):
        user_dict = vars(self.request)
        return {"id": user_dict["id"], "username": user_dict["username"]}

    def get_requests(self, user):
        return Request.objects.filter(user=user).exclude(request=user)

    def get_request_count(self, user):
        return Request.objects.filter(user=user).count()
        
    def __str__(self):
        return str(self.user.username)


class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')

    def get_user_info(self):
        user_dict = vars(self.user)
        return {"id": user_dict["id"], "username": user_dict["username"]}

    def get_follower_info(self):
        user_dict = vars(self.follower)
        return {"id": user_dict["id"], "username": user_dict["username"]}
        
    def get_following(self, user):
        return Follower.objects.filter(follower=user)

    def get_followers(self, user):
        return Follower.objects.filter(user=user).exclude(follower=user)

    def get_following_count(self, user):
        return Follower.objects.filter(follower=user).count()

    def get_followers_count(self, user):
        return Follower.objects.filter(user=user).count()
        
    def __str__(self):
        return str(self.user.username)
