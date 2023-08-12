from django import forms
from .models import Contact, Blog, Testimonial
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content']


class CommentForm(forms.Form):
    name = forms.CharField(max_length=30, label='Your Name')
    email = forms.EmailField(label='Your Email')
    comment = forms.CharField(widget=forms.Textarea, label='Your Comment')


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['author', 'content', 'photo']