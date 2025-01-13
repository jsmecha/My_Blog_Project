from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, TemplateView
from .models import Blog, Comment, Likes
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required #for def function
from django.contrib.auth.mixins import LoginRequiredMixin #for class view
import uuid


class BlogList(ListView):
    context_object_name = 'blogs'
    model = Blog
    template_name = 'App_Blog/blog_list.html'
    #queryset = Blog.objects.order_by('-publish_date') #-publish_date : descending order


class CreateBlog(CreateView, LoginRequiredMixin):
    
    model = Blog
    fields = ('blog_title','blog_content', 'blog_image')
    template_name = 'App_Blog/create_blog.html'


    def form_valid(self, form):
        blog_obj = form.save(commit=False) #commit = False means "hold data"
        blog_obj.author = self.request.user
        title = blog_obj.blog_title
        blog_obj.slug = f"{title.replace(' ', '-')}-{uuid.uuid4()}" #가상의 id를 임의로 만들어내서 붙여줌. 동일한 user의 블로그들을 구분하기 위함.
        blog_obj.save()
        return redirect('index')
        
        


class UpdateBLog(UpdateView, LoginRequiredMixin):
    model = Blog
    fields = '__all__'
    template_name = 'App_Blog/edit_blog.html'
    