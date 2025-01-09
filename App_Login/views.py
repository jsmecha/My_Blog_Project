from django.shortcuts import render
from django.http import HttpResponse

def login(request):
    return HttpResponse("I am App_Login index page.")