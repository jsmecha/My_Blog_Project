from django.urls import path
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
from . import views

app_name = 'app_login'

urlpatterns = [    
    path('login/', views.log_in, name='login'),
    path('signup/', views.sign_up, name='signup'),
    path('logout/', views.log_out, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('change_profile/', views.user_change, name='change_profile'),
    path('change_password/', views.password_change, name='change_password'),
    path('add_profile_pic', views.add_profile_pic, name='add_pro_pic'),
    path('change_profile_pic', views.change_profile_pic, name='change_pro_pic'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('reset_password_confirm/<uidb64>/<token>/', views.CustomPasswordResetComfirmView.as_view(), name = 'reset_password_confirm'),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(template_name='App_Login/password_reset_complete.html'), name='password_reset_complete'),
]
