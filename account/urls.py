from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_request, name="register"),
    path("home/", views.home_view, name="home"),
    path("", views.home_view, name="homebase"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
    path("update/", views.update_request, name="update"),
]