from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.urls import reverse


def register(request):
    """
    Handle user registration.

    If the request method is POST, the function processes the submitted form data.
    If the form is valid, a new user is created, logged in, and redirected to the homepage.
    Otherwise, the registration form is displayed again with errors.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered registration page or a redirect to the homepage.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homepage')
    else:
        form = CustomUserCreationForm()
    rendered_form = form.render("custom_auth/form_custom.html")
    return render(request, 'custom_auth/register.html', {'form': rendered_form})


def login_view(request):
    """
    Handle user login.

    If the request method is POST, the function processes the submitted form data.
    If the form is valid and the user is authenticated, the user is logged in and redirected to the homepage.
    Otherwise, the login form is displayed again with errors.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered login page or a redirect to the homepage.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect based on user role
                return redirect('homepage')

    else:
        form = AuthenticationForm()
    rendered_form = form.render("custom_auth/form_custom.html")
    return render(request, 'custom_auth/login.html', {'form': rendered_form})


@login_required
def logout_view(request):
    """
    Handle user logout.

    This view requires the user to be logged in. Upon calling, the user is logged out and redirected to the login page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A redirect to the login page.
    """
    logout(request)
    return redirect('login')
