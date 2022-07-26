from django.urls import path
from accounts import views

urlpatterns = [
    path('register/', views.UserRegisterationView.as_view(), name='register'),
]
