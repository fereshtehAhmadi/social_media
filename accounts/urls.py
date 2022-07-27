from django.urls import path
from accounts import views

urlpatterns = [
    path('register/', views.UserRegisterationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('show_user_profile/', views.UserEditView.as_view(), name='show_user_profile'),
    path('user_edit/', views.UserEditView.as_view(), name='user_edit'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('delete_account/', views.UserDeleteAccountView.as_view(), name='delete_account'),
]
