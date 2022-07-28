from django.urls import path
from accounts import views

urlpatterns = [
    path('register/', views.UserRegisterationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('changepassword/', views.UserChangePasswordView.as_view(), name='changepassword'),
    path('profile/', views.UserEditView.as_view(), name='profile'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('delete_account/', views.UserDeleteAccountView.as_view(), name='delete_account'),
    
    path('send_request/<int:pk>', views.SendRequest.as_view(), name='send_request'),
    path('accept_request/<int:pk>/<str:status>', views.AcceptRequest.as_view(), name='accept_request'),
    path('request_list/', views.RequestList.as_view(), name='request_list'),
    path('follower_list/<int:pk>', views.FollowerList.as_view(), name='follower_list'),
    path('follower_list/', views.FollowerList.as_view(), name='follower_list'),
    path('following_list/<int:pk>', views.FollowingList.as_view(), name='following_list'),
    path('following_list/', views.FollowingList.as_view(), name='following_list'),
    path('user_info/<int:pk>', views.UserInfo.as_view(), name='user_info'),
]
