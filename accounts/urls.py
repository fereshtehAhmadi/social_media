from django.urls import path
from accounts import views

urlpatterns = [
    path('send_phone/', views.SendPhoneNumber.as_view(), name='send_phone'),
    path('valid_phone/<int:pk>', views.Validate.as_view(), name='valid_phone'),
    path('register/<str:status>/<int:pk>', views.UserRegisterationView.as_view(), name='register'),
    
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
    path('unfollow/<int:pk>', views.Unfollow.as_view(), name='unfollow'),
    path('block/<int:pk>', views.Block.as_view(), name='block'),
    path('user_info/<int:pk>', views.UserInfo.as_view(), name='user_info'),
]
