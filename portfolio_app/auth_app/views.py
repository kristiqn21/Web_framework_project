from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views, login, authenticate
from portfolio_app.auth_app.forms import RegisterUserForm, LoginUserForm
from django.views import generic as views


# def is_admin(user):
#     return user.is_authenticated and user.is_staff
#
#
# @user_passes_test(is_admin)
# def admin_view(request):
#     return render(request, 'base.html')


class OnlyAnonymousMixin:
    login_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse(self.get_success_url())

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return redirect_to_login(self.request.get_full_path(), self.login_url)


class RegisterUserView(OnlyAnonymousMixin, views.CreateView):
    template_name = 'register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            next_page = request.POST.get('next', '')
            if next_page:
                return redirect(next_page)
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})


# class LoginUserView(auth_views.LoginView):
#     template_name = 'login.html'
#     form_class = LoginUserForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')

    form = LoginUserForm()  # Create an instance of the form
    return render(request, 'login.html', {'form': form})  # Pass the form as part of the context

# class LoginUserView(View):
#     template_name = 'login.html'
#     form_class = LoginForm
#
#     def get(self, request, *args, **kwargs):
#         form = self.form_class()
#         return render(request, self.template_name, {'form': form})
#
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('index')  # Redirect to the home page after successful login
#         return render(request, self.template_name, {'form': form})


class LogoutUserView(auth_views.LogoutView):
    pass

