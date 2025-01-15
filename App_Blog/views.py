from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, TemplateView
from .models import Blog, Comment, Likes
from .forms import CommentForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required #for def function
from django.contrib.auth.mixins import LoginRequiredMixin #for class view
import uuid



class MyBlogs(TemplateView, LoginRequiredMixin):
    template_name = 'App_Blog/my_blogs.html'



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
    fields = ('blog_title','blog_content', 'blog_image')
    template_name = 'App_Blog/edit_blog.html'
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('app_blog:blog_detail', kwargs={'slug':self.object.slug})

   




    


def blog_detail(request, slug):
    blog = Blog.objects.get(slug=slug)    
    comment_form = CommentForm()
    liked = False
    
    if request.user.is_authenticated:       
        already_liked = Likes.objects.filter(blog=blog, user=request.user)
        if already_liked:
            liked = True
        

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_obj = comment_form.save(commit=False)
            comment_obj.user = request.user
            comment_obj.blog = blog
            comment_obj.save()
            return redirect('app_blog:blog_detail', slug=slug)


    return render(request, 'App_Blog/blog_details.html', context={'blog':blog, 'comment_form':comment_form, 'liked':liked})



@login_required
def liked(request, pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    already_liked = Likes.objects.filter(blog=blog, user=user)

    if not already_liked:
        liked_post = Likes(blog=blog, user=user)
        liked_post.save()
    
    return redirect('app_blog:blog_detail', slug=blog.slug)
    

@login_required
def unliked(request, pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    already_liked = Likes.objects.filter(blog=blog, user=user)
    if already_liked:
        already_liked.delete()

    return redirect('app_blog:blog_detail', slug=blog.slug)
