from django.urls import path
from . import views

app_name = 'app_blog'

urlpatterns = [    
    path('', views.BlogList.as_view(), name='blog_list'),
   
    path('create/', views.CreateBlog.as_view(), name = 'create_blog'),
    path('edit/<int:blog_id>/', views.UpdateBLog.as_view(), name='edit_blog'),
    
]
