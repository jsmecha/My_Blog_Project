from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse

def index(request):
    return HttpResponseRedirect(reverse('app_blog:blog_list')) #directly go to blog_list.html