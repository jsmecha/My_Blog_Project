from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from .forms import SignUpForm, UserProfileChangeForm
 



def sign_up(request):
    form = SignUpForm()
    
    registered = False

    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            registered = True

    dict = {'form':form, 'registered':registered}
    return render(request, 'App_Login/signup.html', context = dict)



def log_in(request):
    form = AuthenticationForm()
    
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect(reverse('index'))

    dict = {'form':form}
    return render(request, 'App_Login/login.html', context=dict)



@login_required
def log_out(request):
    logout(request)
    return redirect(reverse('index'))


@login_required
def profile(request):
    return render(request,'App_Login/profile.html', context={})


@login_required
def user_change(request):
    current_user = request.user
    form = UserProfileChangeForm(instance=current_user)
    if request.method == 'POST':
        form = UserProfileChangeForm(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            messages.success(request,'Profile Changed Successfully')
            return redirect('app_login:profile')#form = UserProfileChangeForm(instance = current_user)

    return render(request, 'App_Login/change_profile.html', context={'form':form})



@login_required
def password_change(request):    
    current_user = request.user
    form = PasswordChangeForm(user=current_user)
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=current_user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password Changed Successfully')
            return redirect('app_login:login')
        
    return render(request, 'App_Login/pass_change.html', context={'form':form})