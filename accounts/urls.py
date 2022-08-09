from django.urls import path
from accounts import views

urlpatterns = [
    path('send_phone/', views.SendPhoneNumber.as_view(), name='send_phone'),
    path('register/<int:pk>', views.RegisterationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('reset_password/<int:pk>', views.UserResetPasswordView.as_view(), name='reset_password'),
    path('change_password/', views.UserChangePasswordView.as_view(), name='change_password'),
    path('change_password/', views.UserChangePasswordView.as_view(), name='change_password'),
    path('user_profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('user_profile/<int:pk>', views.UserProfile.as_view(), name='user_profile'),
    path('user_logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('delete_account/', views.UserDeleteAccountView.as_view(), name='delete_account'),
    
    path('search/<str:search>', views.SearchUser.as_view(), name='search'),
    
    path('send_request/', views.SendRequest.as_view(), name='send_request'),
    path('request_list/', views.RequestListView.as_view(), name='request_list'),
    path('request_status/<int:pk>/<int:status>', views.AcceptRequest.as_view(), name='request_status'),
    
    path('unfollow/<int:pk>', views.UnFollowUserView.as_view(), name='unfollow'),
    path('delete_follower/<int:pk>', views.DeleteFollowerView.as_view(), name='delete_follower'),
    path('block/<int:pk>', views.BlockView.as_view(), name='block'),
 
    path('follower_list/', views.MyFollowerList.as_view(), name='follower_list'),
    path('follower_list/<int:pk>', views.FollowerList.as_view(), name='follower_list'),
    path('following_list/', views.MyFollowingList.as_view(), name='following_list'),
    path('following_list/<int:pk>', views.FollowingList.as_view(), name='following_list'),
]
