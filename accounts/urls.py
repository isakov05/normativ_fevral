from django.urls import path
from .views import register_view, login_view, logout_view
from .views import forgot_password, restore_password

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('restore-password/', restore_password, name='restore_password'),
]