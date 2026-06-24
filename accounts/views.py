from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm

def home_view(request):
    """
    If authenticated: redirects to the dashboard.
    If not authenticated: redirects to the login page.
    """
    if request.user.is_authenticated:
        return redirect("dashboard")
    return redirect("login")

def register_view(request):
    """
    Handles user registration.
    Registers a new user, hashes the password, auto-logs them in, 
    and redirects to the dashboard.
    """
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = RegisterForm()

    return render(
        request,
        "register.html",
        {"form": form}
    )

def logout_view(request):
    """
    Logs out the current user and redirects to the login page.
    """
    logout(request)
    return redirect('login')

@login_required 
def dashboard_view(request):
    """
    Renders the dashboard. Accessible only to authenticated users.
    """
    return render(
        request,
        "dashboard.html"
    )