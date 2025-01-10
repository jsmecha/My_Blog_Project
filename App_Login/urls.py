from django.urls import path
from . import views

app_name = 'app_login'

urlpatterns = [    
    path('login/', views.log_in, name='login'),
    path('signup/', views.sign_up, name='signup'),
    path('logout/', views.log_out, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('change_profile/', views.user_change, name='change_profile'),
    path('change_password/', views.password_change, name='change_password'),
]
