from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse, reverse_lazy
from django.contrib import messages

from .forms import SignUpForm, UserProfileChangeForm, ProfilePic, ResetPasswordForm
 



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


@login_required
def add_profile_pic(request):    
    form = ProfilePic()
    if request.method == 'POST':
        form = ProfilePic(request.POST, request.FILES)
        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.user = request.user
            user_obj.save()
            messages.success(request, "Profile Picture Added Successfully.")
            return redirect('app_login:profile')


    return render(request, 'App_Login/pro_pic_add.html', context={'form':form})


@login_required
def change_profile_pic(request):
    form = ProfilePic(instance=request.user.user_profile)
    if request.method == 'POST':
        form = ProfilePic(request.POST, request.FILES, instance=request.user.user_profile)
        if form.is_valid():
            form.save()
            return redirect('app_login:profile')


    return render(request, 'App_Login/pro_pic_add.html', context={'form':form})


def reset_password(request):
    form = ResetPasswordForm()
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            
            try:
                user = User.objects.get(first_name=first_name, last_name=last_name,
                                        username=username, email=email)
                if user:
                    if user.is_active:
                        token = default_token_generator.make_token(user)
                        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
                        return redirect('app_login:reset_password_confirm', uidb64=uidb64, token=token)
                    else:
                        messages.error(request, "This user is not active.")
                else:
                    messages.error(request, "No user found with the provided informations.")
                    
            except:        
                messages.error(request, "No user found with the provided informations.")

    return render(request, 'App_Login/password_reset_form.html', context = {'form':form})
        

class CustomPasswordResetComfirmView(PasswordResetConfirmView):
    template_name = 'App_Login/password_reset_complete.html'
    success_url = reverse_lazy('app_login:password_reset_comoplete')

