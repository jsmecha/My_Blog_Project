from django.urls import path
from . import views

app_name = 'app_blog'

urlpatterns = [    
    path('', views.BlogList.as_view(), name='blog_list'),
    path('detail/<str:slug>/', views.blog_detail, name = 'blog_detail'),
    path('create/', views.CreateBlog.as_view(), name = 'create_blog'),
    path('edit/<int:blog_id>/', views.UpdateBLog.as_view(), name='edit_blog'),
    path('liked/<int:pk>', views.liked, name='liked'),
    path('unliked/<int:pk>', views.unliked, name='unliked'),
    
]
