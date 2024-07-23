from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),

]
"""
URL patterns for the custom_auth app.

The `urlpatterns` list routes URLs to views. For more information please see:
https://docs.djangoproject.com/en/stable/topics/http/urls/

Routes:
    - /login/: Routes to the login view.
    - /logout/: Routes to the logout view.
    - /register/: Routes to the register view.

"""
