from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model
from django.contrib.auth.forms import AuthenticationForm

UserModel = get_user_model()


class LoginUserForm(AuthenticationForm):
    class Meta:
        model = UserModel
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'ala-bala',
                'placeholder': 'Enter your username',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'ala-bala',
                'placeholder': 'Enter your password',
            }
        )
    )


class RegisterUserForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control'
            })
        }
