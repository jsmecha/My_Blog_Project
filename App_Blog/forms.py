from django import forms
from .models import Blog, Comment, Likes


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment', )
