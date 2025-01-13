from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import UserProfile


class SignUpForm(UserCreationForm):    
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(label= 'Email Address', required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')



class UserProfileChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password' in self.fields:
            self.fields.pop('password') #password 필드 숨기기.



class ProfilePic(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_pic',) #쉼표 안들어가면 오류 발생. 이유는???


class ResetPasswordForm(forms.Form):
    first_name = forms.CharField(max_length=150, label='First Name')
    last_name = forms.CharField(max_length=150, label='Last Name')
    username = forms.CharField(max_length=150, label = 'Username')
    email = forms.EmailField(label='Email')