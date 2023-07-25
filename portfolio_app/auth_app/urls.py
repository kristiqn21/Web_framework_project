from portfolio_app.auth_app.views import RegisterUserView, LogoutUserView, login_view
from django.urls import path


urlpatterns = [
    path('register/', RegisterUserView.as_view(), name="register"),
    # path('login/', LoginUserView.as_view(), name="login"),
    path('login/', login_view, name="login"),
    path('logout/', LogoutUserView.as_view(), name="logout"),
]